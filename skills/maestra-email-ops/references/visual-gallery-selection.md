# Visual selection of images from the gallery

**When to read this:** the user wants to visually look at images, choose among
several similar options, or when a text list of candidates isn't enough.
**Return to:** after a number is chosen — the "Images: confirmation procedure"
section of `SKILL.md`, pass the Generator `{url, fileName}` (formula at the bottom
of this file).

A text list remains the fast default response; build a visual contact sheet on
user request or when similar options are ambiguous.

1. First get candidates via MCP `gallery_images_list`:

   ```json
   {
     "nameSubstring": "<user query>",
     "fileExtensions": [".gif", ".png", ".jpeg", ".jpg"],
     "includeSystemImages": true,
     "limit": 12
   }
   ```

   Don't include `.webp`. If the user explicitly asks for project assets only,
   pass `includeSystemImages: false`. If there are too many results, ask for a
   narrower query or use cursor pagination; don't build a contact sheet out of
   hundreds of images. For a visual sheet, 8–20 cards is usually enough.

2. Selection invariants:

   - the email always gets the original `url` from `gallery_images_list`, exactly
     as MCP printed it;
   - `fileName` is assembled as `name + fileExtension`, if `name` doesn't already
     end with that extension;
   - the user picks a card number; never silently pick a similar option for them;
   - base64/data URLs are allowed only for thumbnails in the contact sheet; a
     `data:` URL is forbidden in email JSX.

## Codex / local agent

Codex always uses a plain local HTML contact sheet with remote links to the
images.

1. Create `<projectRoot>/gallery-preview.html`.
2. Insert cards with `<img src="<url from MCP>" loading="lazy">`.
3. Don't download the images or convert them to base64.
4. Give the user the path to the HTML and ask them to open the file in an
   external browser.
5. After they've looked, ask: "Which image number should I use?"

The user's browser loads the images from the gallery links. The agent doesn't
read the image bytes or pass them into the model.

## Cowork

In Cowork, first try a side-panel-safe self-contained preview.

1. Save the rows from `gallery_images_list` as `outputs/gallery-images.json`.
2. Make sure Pillow is available in the sandbox:

   ```bash
   python3 - <<'PY'
   import PIL
   print("Pillow ok")
   PY
   ```

3. If Pillow isn't installed, try installing it into the sandbox:

   ```bash
   python3 -m pip install Pillow
   ```

   If the install fails, don't block the task — move on to the fallback below.

4. Run the helper:

   ```bash
   python3 "<skill>/scripts/gallery_contact_sheet.py" \
     outputs/gallery-images.json \
     outputs/gallery-preview.html \
     --max-px 96 \
     --quality 80
   ```

5. Show `outputs/gallery-preview.html` via `mcp__cowork__present_files`.
6. Ask the user to pick an image number.

Why this approach: `create_artifact`, `show_widget`, markdown images, and remote
`<img src="https://...">` don't work in the Cowork side panel — the
sandbox/CSP blocks external image domains. The helper downloads the images,
shrinks the thumbnails, and embeds them as `data:` URLs, so the HTML works in
the side panel with no external requests. This is preview only: after selection,
still use the original `url` from `gallery_images_list`.

### Cowork fallback if Pillow/the helper doesn't work

1. Create `outputs/gallery-preview.html` with remote `<img src="<url from MCP>">`.
2. Show the file via `mcp__cowork__present_files`.
3. Say: "Open the file in an external browser — the images will load from the
   gallery."
4. Don't expect the images to render in the Cowork side panel.

## Remote contact sheet card template

```html
<article class="card">
  <a class="thumb" href="<url>" target="_blank" rel="noreferrer">
    <img src="<url>" alt="<fileName>" loading="lazy" decoding="async" referrerpolicy="no-referrer">
  </a>
  <div class="name"><span class="num">#N</span> <fileName></div>
  <div class="source">system icon / project asset</div>
  <a class="open" href="<url>" target="_blank" rel="noreferrer">open original</a>
</article>
```

## After selection

Once the user has picked a number, return to the Generator:

```json
{
  "url": "<original url from gallery_images_list>",
  "fileName": "<name + fileExtension>"
}
```

If `name` already ends with `fileExtension`, don't duplicate the extension. If
the contact sheet used base64 thumbnails, still take `url` from the original
JSON/MCP row, not from the thumbnail's `data:` URL.
