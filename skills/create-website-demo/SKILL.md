---
name: create-website-demo
description: Create a complete multi-page website demo or substantial demo content on a connected pixfort WordPress site, using Elementor schemas, reusable demo sections, site media, and coordinated content planning.
---

# Create a pixfort website demo

Follow explicit user instructions over workflow defaults; remain within the available tools and the user's authorized scope.

Build a coherent website on the user's selected pixfort site. This workflow creates WordPress content through pixfort tools. A standalone coded website is a different task.

## Establish the brief and target

Discover the installed pixfort namespace, list connected sites, resolve the intended site, and verify compatibility with `pixfort_get_site_status`. For connection problems use the sibling [connect-sites skill](../connect-sites/SKILL.md). Keep the returned `site_id` explicit on site-scoped calls.

Use the supplied business, audience, language, visual direction, and requested pages. Ask only for missing details that materially affect the result, especially an ambiguous target site. Infer an appropriate sitemap when none was supplied and state it before building. A useful small business starting point is Home, About, Services, and Contact; adapt the pages and amount of content to the brief.

Inspect existing pages and site styles before creating anything. Reuse work already created for this request. Preserve unrelated pages and existing site settings. Treat a generic request for demo content as permission to create drafts; publication, changing the live homepage, and activating global templates need to be within the user's stated scope. Existing explicit authorization is sufficient; do not add another approval checkpoint.

When browser access is available, get each target page's actual `link` from `pixfort_get_page` or `pixfort_list_pages` and inspect the page before editing it to understand its current layout and the request. For a new page, inspect it after creation and before adding content if its authenticated preview is accessible. Do not infer a URL from its slug.

Maintain a compact local or conversational build ledger: selected site, intended pages, created IDs/slugs/statuses, media IDs, sections completed, latest readback, and remaining work. Record results immediately so an interrupted run resumes without duplicate creation. This ledger is task data, not plugin memory.

## Design and content

Create a shared voice, palette, typography, spacing, and imagery direction using `pixfort_get_theme_styles`. Prefer current color `utility_slug` values. Site-wide branding uses discovered Theme Options, not repeated page-local overrides; change it only when in scope.

Write page-specific copy with clear headings and relevant calls to action. Do not invent real testimonials, customer logos, certifications, prices, addresses, or business claims. Use clearly identified sample material where a demo needs it. Do not present a decorative contact form as a working email integration.

Before each section addition, call `pixfort_search_demo_sections` with a natural-language `query` to find the closest relevant section, even if it is not an exact match. Fetch its exact returned ID with `pixfort_get_demo_section`. Treat the supplied business brief as a request to adapt relevant copy, while preserving the section's layout, unrelated settings, widget types, and public demo image URLs unless the user explicitly requests different media. Build from scratch only when no relevant section exists or the user asks for it. Favor coherent sections over an unrelated mix. Read [builder-and-media.md](references/builder-and-media.md) before assembling or saving sections.

## Build in resumable units

Create each new page with `pixfort_create_content`, `type: page`, and explicit `status: draft` to keep it unpublished. Do not use scheduled or custom public statuses for draft work. Record the returned ID. Inspect its builder state before adding content. If the site rejects the item as non-Elementor, use a supported setup path exposed by the site or explain the necessary Elementor setup; do not write raw metadata or overwrite classic content to force compatibility.

Complete a representative page first to establish the style, then finish the rest of the requested sitemap using the same conventions. Inspect the target with `pixfort_get_builder_content` immediately before every section addition. Add bounded, complete sections and read back between batches. A server error or lost response after an append/create is not proof that nothing was saved: inspect/search before any retry. Resume only missing work.

Before adding or editing the first section of a page, check its effective Intro and header with `pixfort_get_applied_templates_for_content`; inspect a selected header with `pixfort_get_header` when available. If no Intro is displayed, check for a `boxed` or `transparent` (overlap) desktop header and an `overlap` mobile header. Where either can cover the first section, check its existing top spacing and add only the padding needed inside that section on the affected screen sizes.

For navigation/header/footer work in the brief, use the sibling [site-layout skill](../site-layout/SKILL.md). Discover support for missing operations; never invent a footer-creation or homepage-setting tool. If an operation is unavailable, finish supported pages and give the exact remaining WordPress action.

## Verify and deliver

Re-fetch every created/edited page and its builder tree. Verify requested page and section counts, saved copy, media references, CTA destinations, and statuses. Resolve internal links against returned page URLs/IDs instead of invented slugs; draft destinations become publicly usable only after publication.

If an authenticated browser preview is available, reopen the page using its MCP-returned `link` after each change. Check desktop and mobile views for header overlap, overflow, heading hierarchy, image crops, contrast, and navigation; make needed fixes and check again. Structural readback does not prove visual quality, delivery of form submissions, or public availability. State which checks ran and which remain unavailable.

Deliver links/IDs with draft or published status, what was created, and concrete unfinished items. If publishing is requested, finish content verification first, use the supported status-change operation, then verify public URLs and any authorized homepage/global-template changes. Do not label a partial build or draft-only site as fully live.
