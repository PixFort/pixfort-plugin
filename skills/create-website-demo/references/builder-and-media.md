# Builder and media contracts

Use live tool input schemas and returned element schemas as authority. This reference describes workflow boundaries, not a replacement JSON schema.

## Adding versus editing

- List with `pixfort_list_builder_elements`, then fetch `pixfort_get_builder_element_schema` for every type created or changed, including containers. The latter may return its complete schema as minified text rather than structuredContent.
- Use actual schema IDs such as `container` and `pix-heading`. Do not fabricate Elementor widget settings or send raw Elementor storage metadata.
- `pixfort_get_demo_section` returns cleaned public `content` suitable for `pixfort_add_builder_content`. There is no `premade_section_id` shortcut. Preserve supplied public demo image URLs unless replacing them with actual site media; do not copy attachment IDs from another site.
- `pixfort_add_builder_content` takes `content_id` and a non-empty native JSON `content` array of top-level containers. It appends; it does not replace. An inspection tree is not add input. Do not stringify the JSON array.
- To edit, fetch `pixfort_get_builder_content`. Choose the smallest existing editable subtree covering the change. Send its current `content_schema_version`, map returned `content_version` to `expected_content_version`, and supply `element` with stable existing IDs. Omit IDs only for new supported descendants.
- Preserve unsupported descendants and all unrelated settings. Do not remove protected nodes just to make validation pass. Never replace a page with an empty tree after a parse failure.
- Versions apply to the whole page. Serialize edits to a page and refresh after each mutation. For a conflict, re-read and reconcile the requested change; do not blindly replay the stale tree.
- On invalid colors, refresh site styling and choose a current returned slug. Preserve unchanged legacy colors during unrelated edits.

## Media

Prefer suitable existing attachments through `pixfort_list_media` / `pixfort_get_media`. Otherwise search `pixfort_search_media_assets` using a short visual query and supported filters. Default search is stills (`format` image). For short silent background or auto-video loops, pass `format: "video"`. If the user names a color or you already have theme styles, pass `colors` (named hues, or primary then secondary hex from `pixfort_get_theme_styles`). After the first pick, pass `match_asset_id` so later photos stay related by palette and, when they still fit, the same collection. Color and collection only rerank; they do not hide other matches. Use a consistent collection hard-filter for illustrations, graphics, icons, and mockups where appropriate. Choose images for their role and crop, not merely matching keywords.

Import an exact returned asset ID with `pixfort_import_media`, `source: pixfort_asset`, and a supported `ratio` when needed. A video hit includes `aspect` for the prepared frame and `ratios` of `16x9`, `1x1`, and `9x16`. Pass one of those ratios to match a wide, square, or tall area; omit `ratio` for the prepared frame. Video import also returns `poster: { id, url }`. Use `mp4_video.id` plus `poster.id` on `pix-auto-video`, or `background_video_link` as the video attachment URL and `background_video_fallback` as the poster. Catalog videos are not YouTube. Use returned attachment IDs/URLs in the element schema's expected format. Reuse imports across pages where appropriate; verify before retrying an uncertain import. Never invent a stock-photo URL, asset ID, or attachment ID. Search icons with `pixfort_search_icons` and use an exact returned canonical ID.

Use descriptive alt text for informative images and the widget's supported decorative behavior for decorative images. If external image generation is available and requested, verify that the live import schema supports its source before promising to upload it.
