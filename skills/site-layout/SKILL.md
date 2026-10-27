---
name: site-layout
description: Coordinate pixfort website navigation, headers, footers, global styling, and template display conditions using live schemas and version-safe updates.
---

# Coordinate a pixfort site layout

Follow explicit user instructions over workflow defaults; remain within the available tools and the user's authorized scope.

Resolve the selected connected site and use its `site_id` throughout. Inspect the current layout before changes. Apply only the requested global or page-specific scope. Preparing a draft template, publishing it, and activating it are distinct operations; use existing user authorization for each intended outcome.

## Navigation

Read `pixfort_get_menu_schema`, list menus, and resolve named destinations with content discovery. For an existing menu read both `pixfort_get_menu` and `pixfort_get_menu_items`. Use the returned schema/version tokens for every mutation. Read fresh state or use a returned fresh version before the next item change.

Create with `pixfort_create_menu`; use semantic add/update/move fields supported by the live item tools. Do not write native `_menu_item_*` metadata. Preserve unrelated items, unknown settings, and hierarchy. Menu creation does not assign theme locations. A header menu element can reference the discovered menu according to its live schema; do not claim it assigns a WordPress menu location.

## Headers and footers

Resolve names with `pixfort_search_builder_items`, using `item_type: header` or `footer`. Continue automatically for a unique exact match; disambiguate multiple matches instead of guessing IDs.

For headers, read `pixfort_get_header_schema`, `pixfort_list_header_elements`, and the schemas of changed elements. Create an empty draft with `pixfort_create_header_draft`, supplying its title and optional slug/general settings. Use `pixfort_update_header_settings` to change an existing header's title, slug, or general settings.

Use the dedicated tools for each structural change: `pixfort_add_header_column` adds only `topbar_3`; `pixfort_update_header_area` and `pixfort_update_header_column` patch settings on existing targets; `pixfort_add_header_element`, `pixfort_update_header_element`, `pixfort_move_header_element`, and `pixfort_remove_header_element` change one element. Each tool has its own input schema. Do not send an `operation` selector or `operations` array. The former `pixfort_create_header` and `pixfort_update_header` tools are unavailable.

Fetch `pixfort_get_header` immediately before each edit; map its version to `expected_header_version` and include `header_schema_version`. Preserve unrelated and unsupported legacy data. Add a missing third topbar column before adding an element to it, and use the saved element ID for later edits. Serialize changes and inspect between calls: each call saves independently, and edits to an active header can appear immediately. If a response is lost, inspect before retrying an addition. New headers remain drafts while being assembled. Publish through `pixfort_set_header_status` when requested, using the current version.

Check `pixfort_get_site_status` for `pixfooter` in the supported content types. When supported, create a draft footer with `pixfort_create_content` using `type: pixfooter`. Use `pixfort_get_builder_content` and `pixfort_add_builder_content` to populate its Elementor layout, and `pixfort_update_builder_content` for existing elements, using current schema/content versions. Use `pixfort_edit_content` for metadata or publishing when requested; do not send Elementor layout as its HTML content field. On older sites that do not expose `pixfooter` creation, ask the customer to create the empty footer in WordPress and then finish its supported builder content. Do not silently create a regular page as a footer substitute.

The dedicated `pixfort_set_default_website_header` and `pixfort_set_default_website_footer` select global fallbacks. They do not publish templates, change conditions, or guarantee which template wins on a page. Use them for requested global selection only.

## Conditional layout and global styles

For selected pages/contexts, read `pixfort_get_template_display_conditions`, choose a returned condition key, and resolve targets through `pixfort_search_display_condition_targets`. Add/remove individual rules with the dedicated tools, preserving all others. Do not use a global setter to implement a page-specific footer. Draft conditions can be prepared, but only published templates participate in frontend matching.

Inspect Theme Options schemas/current values before changing global styling. Use `validate_only` when useful and `expected_current_value` when supported to protect a prior read. Never infer raw storage keys. Read back normalized values after saving.

Verify menus and headers by readback. Use `pixfort_get_applied_templates_for_content` on representative pages to check effective selection and precedence. Its popup results indicate eligibility, not proof of a visible popup. Verify desktop/mobile header behavior and footer rendering in a browser when available; state any preview gap.
