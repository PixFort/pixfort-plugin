---
name: connect-sites
description: Connect a pixfort account and WordPress sites to the pixfort MCP server, select the intended site, or troubleshoot account authorization and site connectivity.
---

# Connect pixfort sites

Follow explicit user instructions over workflow defaults; remain within the available tools and the user's authorized scope.

The plugin registers the remote HTTP endpoint `https://mcp.pixfort.com/mcp`. Account OAuth and WordPress site enrollment are separate. No local server or manually supplied API key is required.

Discover available pixfort tools by their base names; installed namespace prefixes vary. Preserve any explicitly selected connection. Use `pixfort_list_connected_sites` to inspect account enrollment, then `pixfort_get_site_status` to verify actual WordPress reachability. A successful list alone is not a site health check.

The WordPress site should use at least **pixfort Theme version 1.20.2** and **pixfort Core version 4.3.4**. When version information is available, check both versions and advise updating either component if it is below the minimum.

If tools are unavailable or account authentication is required, guide the customer through the client's pixfort plugin connection/authentication UI and pixfort account consent. Never ask them to paste passwords, Application Passwords, OAuth tokens, or authorization callback URLs into chat. Authentication approval remains with the customer.

If no sites are connected:
1. Open or link to [pixfort connected sites](https://pixfort.com/mcp-sites).
2. Have the customer sign in and enter their public HTTPS WordPress site URL under Connect your website.
3. Follow the redirect to WordPress, sign in as an administrator, and approve the `pixfort MCP` application. The dashboard handles the Application Password exchange.
4. Return to the dashboard and verify the connection result. Re-list sites in MCP; refresh/reconnect the client's pixfort authorization if the authenticated site list remains stale.

Public service enrollment does not support localhost or private-network sites. Do not recommend disabling URL protections. If dashboard access is unavailable, report its actual account eligibility message rather than promising access or guessing a subscription requirement.

Select the site matching the user's domain/name. If several candidates remain ambiguous, ask which site to use before site-dependent writes. Pass its returned `site_id` on subsequent site-scoped tools, even when only one exists. Read `pixfort_get_site_status` for site compatibility and available version information. Report the selected URL and verified readiness for the requested operation.

## Diagnose at the failing layer

- MCP OAuth/HTTP 401 or `invalid_grant`: reconnect the pixfort account in the client. Do not revoke the WordPress site merely to repair account OAuth.
- Listed site but WordPress 401/403: inspect the message; use the dashboard's site Reconnect flow for invalid/revoked site credentials or authorization. Do not loop account login for a site permission problem.
- No tools after authentication: refresh client tool discovery or start a new task after plugin installation. Do not claim the plugin is connected until a tool succeeds.
- Missing route/unsupported builder: relay the tool's required pixfort Core/theme/Elementor compatibility guidance. A local element catalog can be available even when the site runtime is incompatible.
- Network failure: report the target and safe error, check site availability through permitted read tools, and stop repeated identical attempts. Never substitute a different customer's site.

Use only safe error text in the handoff. Do not expose credentials from logs or configuration.
