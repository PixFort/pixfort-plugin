#!/usr/bin/env python3
"""Validate this Codex-format package and build an allowlisted submission ZIP."""

import hashlib
import json
from pathlib import Path
import re
import struct
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = 'pixfort'


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def local(path):
    require(path.startswith('./'), f'Path must start with ./: {path}')
    target = ROOT / path
    require(not target.is_symlink(), f'Symlink is not a package file: {path}')
    require(target.resolve().is_relative_to(ROOT), f'Path escapes package: {path}')
    require(target.exists(), f'Missing file or directory: {path}')
    return target


def https(url):
    parsed = urlsplit(url)
    require(parsed.scheme == 'https' and parsed.hostname and not parsed.username
            and not parsed.password, f'Expected HTTPS URL without credentials: {url}')


manifest = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())
require(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', manifest['name']), 'Invalid name')
require(re.fullmatch(r'\d+\.\d+\.\d+', manifest['version']), 'Invalid release version')
require(manifest['description'] and len(manifest['description']) <= 4000, 'Invalid description')
require(manifest['author']['name'], 'Missing author')
require(manifest.get('license'), 'Missing package license')
https(manifest['repository'])
require(manifest['skills'] == './skills/' and manifest['mcpServers'] == './.mcp.json',
        'Unexpected component paths')
license_file = local('./LICENSE')
require(license_file.is_file() and license_file.read_text().strip(), 'Missing license text')
mcp = json.loads(local(manifest['mcpServers']).read_text())
require(set(mcp['mcpServers']) == {'pixfort'}, 'Expected one pixfort MCP server')
https(mcp['mcpServers']['pixfort']['url'])
for client in ('.claude-plugin', '.cursor-plugin'):
    client_manifest = json.loads(local(f'./{client}/plugin.json').read_text())
    require(client_manifest['name'] == PACKAGE_NAME, f'Unexpected {client} name')
    for field in ('version', 'repository', 'license', 'skills'):
        require(client_manifest.get(field) == manifest[field], f'Mismatched {client} {field}')
    expected_mcp = mcp
    expected_mcp_path = manifest['mcpServers']
    if client == '.claude-plugin':
        expected_mcp_path = './.mcp.claude.json'
        expected_mcp = {'mcpServers': {'pixfort': {
            **mcp['mcpServers']['pixfort'],
            'url': mcp['mcpServers']['pixfort']['url'] + '?tool_metadata=claude',
        }}}
        require(local(client_manifest['icon']).is_file(), 'Missing Claude listing icon')
        for field in ('documentationUrl', 'supportUrl', 'privacyPolicyUrl', 'termsOfServiceUrl'):
            https(client_manifest[field])
    require(client_manifest['mcpServers'] == expected_mcp_path,
            f'Unexpected {client} MCP configuration path')
    require(json.loads(local(client_manifest['mcpServers']).read_text()) == expected_mcp,
            f'Unexpected {client} MCP configuration')
    marketplace = json.loads(local(f'./{client}/marketplace.json').read_text())
    require(marketplace['name'] == PACKAGE_NAME and marketplace['owner']['name'],
            f'Invalid {client} marketplace identity')
    require(len(marketplace['plugins']) == 1
            and marketplace['plugins'][0]['name'] == PACKAGE_NAME
            and marketplace['plugins'][0]['source'] == './',
            f'Expected {client} marketplace to list the root plugin')
extension = manifest['extensions']['com.openai']
for settings in (manifest, extension):
    require(not any(key in settings for key in ('apps', 'hooks')), 'Public ZIP cannot use apps/hooks')
require(not (ROOT / '.app.json').exists() and not (ROOT / 'hooks').exists(), 'Remove apps/hooks')
listing = manifest['interface']
for field, limit in [('displayName', 30), ('shortDescription', 30), ('longDescription', 4000),
                     ('developerName', 80)]:
    require(isinstance(listing[field], str) and 0 < len(listing[field]) <= limit,
            f'Invalid {field}')
require(listing['category'] and len(listing['capabilities']) <= 20, 'Invalid listing')
require(all(isinstance(c, str) and 0 < len(c) <= 120 for c in listing['capabilities']),
        'Invalid capability labels')
for field in ('websiteURL', 'supportURL', 'privacyPolicyURL', 'termsOfServiceURL'):
    https(listing[field])
require(len(listing['defaultPrompt']) <= 3 and
        all(0 < len(p) <= 128 for p in listing['defaultPrompt']), 'Invalid starter prompts')
review = extension['review']
require(not any(key in review for key in ('test_credentials', 'reviewer_instructions')),
        'Reviewer access belongs in the secure dashboard')
for group, count in [('positive', 5), ('negative', 3)]:
    cases = review['test_cases'][group]
    require(len(cases) == count, f'Expected {count} {group} cases')
    for case in cases:
        fields = ['description', 'prompt', 'expected_behavior']
        if group == 'positive':
            fields.append('tools_triggered')
        require(all(isinstance(case.get(f), str) and case[f].strip() for f in fields),
                f'Incomplete {group} case')
if review.get('demo_recording_url'):
    https(review['demo_recording_url'])
else:
    print('Reminder: a reviewer-accessible recording must be supplied in the dashboard.')

files = {ROOT / '.codex-plugin/plugin.json', local(manifest['mcpServers']), license_file}
require(listing.get('logo') and listing.get('composerIcon'), 'Missing required icons')
for field in ('logo', 'composerIcon', 'logoDark', 'composerIconDark'):
    if field not in listing:
        continue
    asset = local(listing[field])
    require(asset.is_file() and asset.stat().st_size <= 5 * 1024 * 1024, 'Invalid asset size')
    if asset.suffix == '.png':
        data = asset.read_bytes()
        require(data[:8] == b'\x89PNG\r\n\x1a\n', 'Invalid PNG')
        width, height = struct.unpack('>II', data[16:24])
        require(width == height and 48 <= width <= 4096, f'Invalid PNG dimensions: {asset.name}')
    elif asset.suffix == '.svg':
        viewbox = list(map(float, ET.parse(asset).getroot().attrib['viewBox'].split()))
        require(viewbox[2] == viewbox[3] and viewbox[2] >= 48, 'Invalid SVG viewBox')
    else:
        raise SystemExit(f'Add validation for asset format: {asset.suffix}')
    files.add(asset)
skills = local(manifest['skills'])
entries = sorted(skills.glob('*/SKILL.md'))
require(len(entries) == 3, 'Expected three skills')
require(local(extension['onboardingSkill']) in entries, 'Onboarding must reference a skill')
for skill in entries:
    content = skill.read_text()
    header = content.split('---', 2)
    require(content.startswith('---\n') and len(header) == 3, f'Missing frontmatter: {skill}')
    require(f'\nname: {skill.parent.name}\n' in header[1]
            and re.search(r'^description: .+', header[1], re.M), f'Invalid skill metadata: {skill}')
    require((skill.parent / 'agents/openai.yaml').is_file(), f'Missing MCP dependency: {skill}')
    for path in skill.parent.rglob('*'):
        require(not path.is_symlink(), f'Symlink under skills: {path}')
        if path.is_file():
            require(path.suffix in ('.md', '.yaml'), f'Unexpected skill file: {path}')
            files.add(path)
for path in files:
    if path.suffix == '.md':
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' not in link and not link.startswith('#'):
                target = (path.parent / link.split('#')[0]).resolve()
                require(target in files, f'Unpackaged skill reference: {path}: {link}')

# The dashboard's immutable plugin name is separate from the distribution folder.
output = ROOT.parent / f"{PACKAGE_NAME}-{manifest['version']}.zip"
with ZipFile(output, 'w', ZIP_DEFLATED) as archive:
    for path in sorted(files):
        archive.write(path, Path(PACKAGE_NAME) / path.relative_to(ROOT))
with ZipFile(output) as archive:
    require(archive.testzip() is None, 'ZIP integrity check failed')
print(f'Validated and packaged {len(files)} files: {output}')
print(f'SHA256: {hashlib.sha256(output.read_bytes()).hexdigest()}')
