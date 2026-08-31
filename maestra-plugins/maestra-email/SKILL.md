---
name: maestra-email
description: Creates and modifies emails for the Maestra editor (visual builder) from a text description. Use when the user asks to create or modify an email, or describes an email template. The technical layout is passed for preview and saving to the linked skill maestra-email-ops.
---

# maestra-email — email generation

Generates a technical email layout from a text description. The internal output for Ops is valid JSX, which is then converted into the Maestra editor's JSON.

## Skill boundaries

This is a portable JSX generator. It does **not work directly** with gallery/upload tools,
mailing ID and rowVersion, VNet, or saving to Maestra. All operational
actions — uploading and searching images via Ops, JSX → JSON conversion, HTML rendering, PNG preview,
reading campaign metadata/visual template, and saving — are performed by the linked skill **maestra-email-ops**.
The Generator uses JSON/HTML/PNG feedback from Ops to self-correct the JSX, but does not fix
operational errors on its own and does not invent URLs.

## Communicating with the user

JSX, internal IDs, and rowVersion are internal details of the Generator–Ops interaction.
In a normal dialogue with a CSM, use "email", "email layout", "email content",
"preview", and "saving" — not JSX, `mailingInternalId`, `variantInternalId`,
`formatInternalId`, `rowVersion`, or `visualTemplateRowVersion`. Do not replace the terms Active/Draft:
if they are needed to pick the exact version, use Active/Draft verbatim.
Do not show raw JSX or GUIDs unless the user explicitly requested code, an export,
markup, or technical details. Return backend errors verbatim, even if they
contain technical terms, tag names, line numbers, or identifiers.

## Not implemented (deliberately)

- **Do not use `variant`.** Theme sync is currently disabled, so theme presets are not part of the DSL and are not activated on request. Set styles via `style={{...}}` (Text) or `simpleTextStyles={{...}}` (Button); when asked to use a preset, explain the limitation and offer explicit styles.
- **Do not use** `<Theme>` — the email theme is not accessible from the DSL; styles are set via `style` on Text and `simpleTextStyles` on Button.
- **Do not set** `targeting` on Block/Row — it is an external setting, not accessible from the DSL.
- **Do not use** `mobile={{…}}` — mobile values are written inside the attribute's JSON structure (for example `innerSpacing={{ top: 24, mobile: { top: 12 } }}`).
- **Do not use** the `<Var>` tag and do not insert arbitrary personalization (`{{name}}`, `${Customer...}`, `${Order...}`) into text or URLs. If the user asks for personalization — offer static text. Existing personalization in an email is preserved on round-trip. The only permitted new exception is the exact token `${Message.UnsubscribeLink}` in the `href` of an `<a>` link inside `<Text>` per the rules of the "Unsubscribe link" section.
- **`<Image>` is allowed only with a source.** Write the full form `image={{ mode: "static", static: { url, fileName } }}`; bare `<Image />` is forbidden, because the backend substitutes a base64 placeholder. Source rules are in the "Images" section.
- **`<BulletList>` without `bulletIcon` breaks the layout.** The default system marker renders as a giant black circle: the backend inserts SVG into `src` without escaping quotes. Always set an HTTPS icon explicitly. For a small dot use the live-verified flat form `bulletIcon={{ url, fileName }}` — it renders a marker 4px wide. For a large editable marker/number badge use the constructor-compatible form `bulletIcon={{ type: "custom", url, fileName, size: N }}` — the stored template and live preview/HTML confirmed an actual width of `N`. The form `{{ mode: "static", static: {...} }}` is silently ignored; a string crashes the preview with `Internal server error`.
- **Standalone** `<Timer>`, `<Video>`, `<BulletItem>` have no safe shorthand. `<BulletItem>…</BulletItem>` works as an item only inside `<BulletList>`; simplify a timer or video down to `<Text>` or `<Button>`.
- **`<Html>` is a fallback only.** Always try to build the design with the standard flexible blocks first (`Text`, `Button`, `Image`, `Menu`, `BulletList`, `Socials`, `Split` with spacing/backgrounds/grid) — they are responsive and survive manual edits in the editor. Switch to `<Html>` only if what is needed cannot be expressed with standard blocks (table-based layout, non-standard entities) **or the user explicitly asks for arbitrary HTML**. The content is a single quoted string only: `<Html>{"<table>…</table>"}</Html>`; the live backend rejects direct JSX inside `<Html>` (`<Html> may only contain text`). Warn that manually editing such a block is unsafe.

## Workflow

1. Analyze the text description: identify the blocks (heading, body, CTA, image, divider). Separately recognize a request for an unsubscribe link and apply the "Unsubscribe link" section — do not disguise it as a regular URL.
   **If a reference is given** (a website, a brand, a screenshot, "like on our landing page"), fix before generation: 2–3 brand colors in `#RRGGBB`, a contrasting pair of sections (dark/light), and three text size levels — heading, subheading, body — and apply them throughout the email. A reference is carried over via section structure, background, and color, not just via text: a branded email cannot consist of sections with no background and text of a single size. The default styles are a stand-in for when nothing is known about the style, not the target look.
2. **Resolve all images first.** Every `<Image>` needs a confirmed HTTPS URL: an external URL from the user (as is) or a URL from the gallery/search MCP workflow that Ops returns. If there is no source — request an upload/search via `maestra-email-ops` before generating JSX. If the result must be saved into a specific campaign, Ops starts the image lookup/upload only after `campaign_get`, target selection, and `visual_template_get`/bootstrap discovery; the "images before JSX" rule still holds.
3. Generate JSX following the hierarchy: `Template → Block → FlexRow → Column → Text|Button|Divider|Html|Image|Menu|BulletList|Socials|Split`. `Template` must contain at least one `Block`, `Block` at least one `FlexRow`, `FlexRow` at least one `Column`; an empty `Column` is allowed. For groups, respect the item types and the Split grid rule. Try to express every visual device with standard blocks first; `<Html>` is a fallback only (see "Not implemented").
4. For text styles use `style={{...}}` with partial merge — write only the fields you are changing. For a button — `simpleTextStyles={{...}}`. Partial merge is about economy of edits, not about skipping styling: set color, size, and background wherever the design requires them.
   Do not carry a new `font.family` over from a layout by name and do not guess: the MCP cannot
   fetch the list of standard/custom fonts available in the editor. Preserve
   the existing `font.family` on round-trip. Set a new family only after explicit
   confirmation from the user that it is already uploaded or available in the editor; otherwise
   keep the theme's family and reproduce the style via size, color, weight, line-height,
   and alignment.
   Assemble lists of features, plans, benefits, metrics as a **grid** — a `FlexRow` of 6+6 or 4+4+4 with `background` and `borderRadius` on the `Column` — not as a vertical list. Reserve `BulletList` for short one-liners and explicitly styled numbered-point/badge elements per the dedicated pattern below.
5. Check yourself against the Self-check checklist.
6. For handoff to Ops, the Generator's result is **JSX only** — no Markdown fences, no comments, no explanations. Do not show this JSX to the user in a normal dialogue; show raw code only on an explicit request for code/export/markup/technical diagnostics. Clarifying questions and messages about limitations should be in the user's language.
7. If the request includes verification, preview, diagnostics, or saving, step 6 is not the end: hand the JSX to Ops. Ops does not call preview automatically after every edit. After a JSX change, the previous widget/link is stale: the user gets the message "the previous preview no longer matches the current version; if you like, I can show a new one". `visual_template_preview` is called only when the user asks for a preview, HTML/PNG QA, desktop/mobile/debug, or comments on specific content/rendering. In a supporting host, the HTML preview opens an MCP App widget and provides a fallback link; local HTML is downloaded only for HTML QA/debug, and Ops obtains the PNG preview via a separate MCP function as desktop/mobile links. Fix backend preview/save errors in the JSX and repeat only the requested check. Never assemble HTML/preview by hand. The primary preview for the user is the MCP App widget/fallback link before save and the editor canvas after save; save is allowed after explicit confirmation with the preview status.
8. If the user asks to create/save a new campaign with metadata, do not handle
   this in the Generator: pass it to Ops. The Generator is responsible for the JSX; Ops handles
   `campaign_create`/`campaign_edit_content`/`campaign_edit` and separately reports that
   recipients/send/activate are configured in the UI.
9. Accept a "backend unavailable" status only from Ops after a call to the specific MCP
   tool of the current operation (`campaign_get`, `visual_template_get`,
   `visual_template_preview`, or `visual_template_save`) and an actual error/status.
   Do not transfer the result of a ping, the root, or a neighboring host onto the needed MCP route.

## Hierarchy (13 tags)

```text
Template         exactly one root
└─ Block         1..n, email section
   └─ FlexRow    1..n, row (grid container)
       └─ Column  1..n, size is required; the sum of size within one FlexRow == 12
             └─ Text | Button | Divider | Html | Image | Menu | BulletList | Socials | Split    0..n elements
```

`Menu`, `BulletList`, and `Socials` contain direct item lines without `<Column>`; for `Split` the items are `<Column size={N}>`. A group may stand in a regular column or in a `Split` column, except `Split` inside `Split`.

## Allowlist

| Tag | Required attribute | Optional attributes | Purpose |
|-----|----------------------|----------------------|------------|
| `Template` | — | — | Root (exactly one) |
| `Block` | — | `background`, `border`, `borderRadius`, `innerSpacing`, `gapAfterBlock`, `externalBackground`, `visibilityOnDevices` | Email section |
| `FlexRow` | — | `background`, `border`, `borderRadius`, `innerSpacing`, `columnsGap`, `rowsGap`, `verticalAlign`, `isColumnsMobileAdaptive`, `columnVerticalDirection`, `visibilityOnDevices` | Row (grid container) |
| `Column` | `size={1..12}` | `background`, `border`, `borderRadius`, `innerSpacing` | Grid column |
| `Text` | — | `style`, `innerSpacing`, `background`, `border`, `borderRadius`, `visibilityOnDevices` | Text block (supports HTML markup inside) |
| `Button` | — | `url`, `align`, `innerSpacing`, `buttonSize`, `background`, `simpleTextStyles`, `border`, `borderRadius`, `iconSrc`, `iconAlt`, `iconDisplay`, `iconSizeInPercents`, `visibilityOnDevices` | CTA button; `url` is required for generation by policy |
| `Divider` | — | `innerSpacing`, `border`, `visibilityOnDevices` | Divider line (self-closing) |
| `Html` | — | `visibilityOnDevices` | Arbitrary HTML block |
| `Image` | `image` | `url`, `size`, `align`, `innerSpacing`, `border`, `borderRadius`, `visibilityOnDevices` | Image with a confirmed source URL (self-closing); `size`/`align` control the image itself, `url` makes it clickable; do not set `background` — the backend rejects it |
| `Menu` | — | `align`, `itemsGap`, `innerSpacing`, `background`, `border`, `borderRadius`, `visibilityOnDevices` | Menu; children are only `<Text>` or only `<Button>` |
| `BulletList` | `bulletIcon` | `background`, `border`, `borderRadius`, `innerSpacing`, `itemsGap`, `iconTextGap`, `iconTopPadding`, `visibilityOnDevices` | Short single-line lists; children are `<BulletItem>…</BulletItem>`. Assemble features with a heading and a description as a grid, not a list |
| `Socials` | — | `background`, `align`, `innerSpacing`, `itemsGap`, `imageSize`, `border`, `borderRadius`, `visibilityOnDevices` | Social links; children are `<Image image={{...}} />` with the URL of each icon |
| `Split` | — | `columnsGap`, `verticalAlign`, `innerSpacing`, `background`, `border`, `borderRadius`, `visibilityOnDevices` | Children are `<Column size={N}>`; the sum of `size` == 12, 0..1 element per column |

**Forbidden:** `Var`, `MenuItem`, `SplitColumn`, `Theme`, any other tags. Do not generate bare `<Image />`, standalone `<Timer>`, `<Video>`, `<BulletItem>`.

## Images

For a new `<Image>` always write the self-closing form:

```jsx
<Image image={{ mode: "static", static: { url: "https://cdn.example.com/banner.png", fileName: "banner.png" } }} />
```

`https://cdn.example.com/banner.png` here is only an illustration: in your response use a URL
only from the user or one returned by Ops from the gallery. Do not convert an external URL into
an internal one yourself: an external HTTPS URL is inserted as is, and the backend will process it on save.

Set the size and alignment of a standalone image on the `Image` itself; do not imitate them
with extra columns:

```jsx
<Image
  align={{ align: "center", mobile: { align: "center" } }}
  size={{ type: "fixed", width: 120, mobile: { type: "fixed", width: 80 } }}
  image={{ mode: "static", static: { url: "https://cdn.example.com/icon.png", fileName: "icon.png" } }}
/>
```

`size.equalizedImageMaxWidth` occurs in editor templates and survives round-trip;
preserve it unchanged when editing existing JSX, but do not compute or
invent it for a new fixed-size Image. Inside `<Socials>`, set the items' size via
`Socials.imageSize` and alignment via `Socials.align`.

`Image.url` is an optional HTTPS link that is followed when the image is clicked; it is not
the image source. Create it only from an explicit URL given by the user. Do not insert a
placeholder. Preserve an existing `Image.url` on round-trip unless the user
asked to change the link. Stored JSX may contain serialization artifacts:
an `Image.url` with a bare `https://` and no path, or a URL inside `fileName` — do not treat these as
defects and do not "fix" them without a user request.

### External URL from the user

- Accept only a direct HTTPS URL and insert it as is.
- `fileName` is taken from the name given by the user, or from a non-empty unambiguous basename of the URL path.
  If the name cannot be determined unambiguously — ask, do not invent.

### An attached file or a gallery image — via Ops

The Generator does not upload files and does not access gallery/search tools itself. Delegate to `maestra-email-ops`:

- **An attached file:** pass the file path to Ops. After the MCP upload link and HTTP 200, Ops
  returns the source as `url: fileUrl`; if the JSX needs a `fileName`, it is only
  a service name from the original file, not the image source. On an upload error, do not
  pick an asset silently — stop and inform the user.
- **An already uploaded image:** ask Ops to search by name. With a single candidate, Ops
  returns `{url, fileName}`; with several — show the user the safe metadata
  (`name`, extension, size/date if available, system/project source) and ask. Do not pick by name automatically.
- If Ops reports an upload/list error — stop, do not generate JSX with the image, and do not
  pick an image by name.

### Hard rules

- Do not invent URLs. Author-supplied `data:`, `base64`, `blob:`, `file:`, and `cid:` are forbidden.
- The image URL must be HTTPS by skill policy. This is not a statement about the converter's
  runtime validation for Image.
- Bare `<Image />` is forbidden both in new and in edited JSX: replace it with a confirmed URL
  (via Ops) before writing it back.
- `<Html>` does not bypass the image rules: if the quoted HTML contains `<img>`, its `src` must
  be a confirmed HTTPS URL; prefer `<Image>`.
- Do not place important text, a price, a CTA, or terms only inside an image.

## Fonts

- `style.font.family` on `Text` and `simpleTextStyles.font.family` on `Button` exist
  in the DSL, but the mere presence of the string in JSX does not mean that such a font is installed in
  the editor or available in the email.
- When editing an existing email, preserve the already stored `font.family` unless
  the user asked to change the font.
- Do not add a new family by name from a layout, a website, or a "set the font to X" request.
  First tell the user that the MCP cannot check the font catalog, and ask them to confirm
  that X is already uploaded/available in the editor. Without confirmation, do not write the family.
- If the font is unavailable or its availability is unknown, keep the theme's family and convey
  the character of the typography via `fontSize`, `inscription`, `color`, `lineHeight`, text case,
  and `align`.

## Editable numbered points / badges

- If a number, dot, or badge must remain a separate editable element
  of the editor, do not draw it with a styled `<span>` inside `<Text>` and do not use
  `<Html>`. Such a rich-text/CSS trick may look right in the email, but it does not give
  the user a proper separate editor element.
- Use only separate editor elements: `<BulletList>` or `<Image>` +
  `<Text>`; the choice of form, the rule about distinct digits, and the mobile settings are not duplicated in the core.
- If the digit/icon asset is missing, first find/upload it via Ops or offer
  the user a simple confirmed bullet; do not draw a replacement with inline CSS.
- **Before any numbered-point block, you MUST read
  `references/examples.md` §14**: without it, it is easy to apply one icon to all the digits,
  lose the mobile setting, or again end up with a non-editable CSS badge.

## Spacing between blocks

- In a new or modified layout, do not use `gapAfterBlock` by default for
  ordinary vertical spacing. Create the spacing via `innerSpacing.top/bottom`
  on the `Block`, `FlexRow`, or `Column` itself, so the section background continues under the spacing.
- `gapAfterBlock` creates an outer inter-block gap. Use it only when
  the user explicitly asks for an outer gap or the layout clearly shows a stripe/gap
  in the outer background color that differs from the background of the adjacent blocks.
- On round-trip, do not remove an existing `gapAfterBlock` in a part of the email the
  user did not ask to change. The rule governs new/modified layout; it does not
  authorize incidentally reworking the entire email.

## Unsubscribe link

- On an explicit request for an unsubscribe link/button, add the canonical rich-text anchor inside `<Text>`.
- Use only the exact `href="${Message.UnsubscribeLink}"`. The correct form is
  `<p style="margin: 0;">… <a href="${Message.UnsubscribeLink}">unsubscribe from this mailing list</a></p>`
  inside `<Text>`; if the link text is not specified, use the standard text:
  "If you no longer want these emails — unsubscribe from this mailing list".
- The full example and the explanation of why the literal token in the preview is not a defect are in
  `references/dsl-surface.md` §"Unsubscribe link"; open it when diagnostics are needed.
- Do not use `<Button url="${Message.UnsubscribeLink}">`, fake URLs (`/unsubscribe`, `#`,
  `https://example.com/unsubscribe`), or any other `${...}` token.
- If the user asks for a visual unsubscribe button, explain that the confirmed mechanism is
  a text link, and offer it.
- If the canonical link already exists, do not add a second one. When editing, preserve the existing
  text, position, and styling unless the user asked to change them.

## Divider and placeholder links

- `<Divider />` is fully supported. But set `border` in full (`type`, `color`, all four
  `size` sides, thickness `1` in `size.top`) and do not zero out `innerSpacing` — otherwise the line exists in
  the markup but is not visible in the email. A full-width divider is its own `FlexRow` with `<Column size={12}>`.
- If a divider was in the description or reference and the user requested preview/QA — verify
  that it is **visible in the preview**, not merely present in the JSX.
- Do not generate placeholder URLs (`https://`, `#`, `/`, `about:blank`, `https://example.com`).
  If there is no address for the CTA or the image click — one clarifying question; do not create the button/`Image.url`.
- On round-trip of an existing email, keep placeholders as is, but list them to the user.

```jsx
<FlexRow><Column size={12}>
  <Divider innerSpacing={{ top: 18, bottom: 18, mobile: { top: 12, bottom: 12 } }} border={{ type: "solid", color: "#cfcfcf", size: { top: 1, right: 0, bottom: 0, left: 0 } }} />
</Column></FlexRow>
```

## Value rules (partial merge)

**Write only what you are changing.** Objects are filled in from the new node's defaults, not from a
previously saved email; arrays are replaced wholesale. Write strings in quotes, numbers/objects in
`{}`.

Copy-safe forms of common attributes (the numbers and colors below are illustrative; the syntax is valid):

```jsx
background={{ type: "color", value: "#F5F5F5" }}
background={{ type: "transparent" }}
border={{ type: "solid", color: "#CCCCCC", size: { top: 1, right: 1, bottom: 1, left: 1 } }}
border={{ type: "none" }}
borderRadius={{ topLeft: 12, topRight: 12, bottomLeft: 12, bottomRight: 12, mobile: { topLeft: 8, topRight: 8, bottomLeft: 8, bottomRight: 8 } }}
innerSpacing={{ top: 24, bottom: 24, left: 24, right: 24, mobile: { top: 16, bottom: 16, left: 16, right: 16 } }}
style={{ fontSize: 16, color: "#111111", inscription: ["bold"], align: "left", mobile: { fontSize: 14, align: "left" } }}
simpleTextStyles={{ fontSize: 16, color: "#FFFFFF", inscription: ["bold"], mobile: { fontSize: 14 } }}
```

For other forms — `buttonSize`, the standalone `align`, `gapAfterBlock`, `verticalAlign`,
as well as `Image.size`/`align`/`url`, `image`, and `bulletIcon` — **you MUST check
`references/formats.md` before generating**: their exact value shapes are not
duplicated in the core, and a guessed shape produces a bare `Internal server error` on
convert/preview with no line number.

**Gap attributes are an object, not a number.** `itemsGap`, `columnsGap`, `rowsGap`, and `iconTextGap`
take `{ size: N, mobile: { size: N } }`. A scalar (`itemsGap={12}`, `columnsGap={24}`)
is rejected by the backend with a bare `Internal server error` — no attribute name, no line number,
no hint about the expected type. This error is easy to mistake for a broken component, so
check the shape of the gap value before changing the block structure.

## Text — markup inside text

`<Text>` supports HTML markup inside the tag. Write the markup directly:

```jsx
<Text>
  <p style="margin: 0;">Summer <strong>sale</strong>, <a href="https://shop.example">see more</a></p>
</Text>
```

Available tags: `p`, `h1`–`h6`, `blockquote`, `ul`, `ol`, `li`, `strong`, `em`, `u`, `s`, `span`, `a`, `code`, `pre`, `br`, `hr`, `personalization-parameter`. The live backend rejects `div` and tables (`table`, `thead`, `tbody`, `tr`, `td`, `th`) inside `<Text>` (`<div> is not allowed in a text`) — move table-based layout out into `<Html>{"<table>…</table>"}</Html>`. In explicit JSX markup, write `<br/>` and `<hr/>`. Do not generate `img`, `iframe`, `script`, `style` without a separate live check; prefer an image via standalone `<Image>` or inside `<Socials>`.
Available attributes: `style`, `align`, `href`, `target`, `rel`, `model`, `data-rich-*`. Attributes inside rich-text markup must be plain strings or value-less markers only: `<p style="margin: 0;">`, `<a href="https://...">`, `<span data-rich-text>` are correct. `<p style={{ margin: 0 }}>`, spread attributes, and expressions are not allowed — the live backend returns the error `Attribute \`...\` on <...> must be a plain string`.

Plain text (with no markup of its own) is automatically wrapped in `<p style="margin: 0">…</p>`.

The style of the text as a whole (font, size, color) is set via `style={{...}}` on `<Text>` — not to be confused with inline markup like `<strong>` inside it.

## Cards with aligned CTAs

If you need cards in a row with buttons at the same height, do not assemble each card entirely within its own `Column` — column heights are independent, and the CTAs will drift. Assemble **synchronized rows** instead: separate `FlexRow`s (4+4+4 or 6+6) for images, headings, descriptions, and buttons — then all the CTAs sit in one row at the same top coordinate. The cost: on mobile stacking, the order becomes "all images → all headings → …" rather than card by card; if a card-by-card mobile order matters, that is a product decision (separate mobile rows via `visibilityOnDevices`) — discuss it with the user. Full example: `references/examples.md` §12.

## visibilityOnDevices and "blurred" blocks in the canvas

Blocks hidden for the current device (`visibilityOnDevices="mobile"`/`"desktop"`) are shown by the Maestra canvas editor as **blurred — this is an editor visualization, not a defect in the email**: in the sent HTML, hiding works via media queries, and the PNG preview at desktop viewport shows only the desktop variant. Therefore:

- do not remove device variants just to clean up the canvas — doing so silently sacrifices the mobile layout;
- if the user is alarmed by "blurred cards" in the editor — explain that these are device-hidden duplicates, not broken images;
- the decision to drop the responsive variants and keep a single layout is a product decision — discuss it with the user explicitly.

## Self-check (mandatory before output)

- **Visual hierarchy** (for emails longer than one section): at least two sections with an opaque `background`, at least one of them contrasting with the rest; at least three different `fontSize` values; the CTA has a brand `background` set, if the brand or reference is known; lists are assembled as a grid, not a single column. An email made of sections with no background, text of a single size, and a black-and-white button is unfinished, even if valid.
- **Grid:** the sum of `size` across all columns in every `FlexRow` and `<Split>` **equals 12** (strictly ==, not ≤). For example: `12` (one), `6+6` (two), `4+4+4` (three), `8+4`, `3+3+6`.
- **Inter-block spacing:** in a new/modified layout, ordinary spacing is done via
  `innerSpacing`, so the section background is preserved. Every new `gapAfterBlock` is justified by an
  explicit request or a visible outer color gap in the layout; an untouched existing
  gap is preserved on an unrelated edit.
- **Runtime-required attribute:** `Column.size`. For a new CTA, `Button.url` is required by policy, but the converter only validates the URL if the attribute is present.
- **Minimum nesting:** `Template` ≥ 1 `Block`, `Block` ≥ 1 `FlexRow`, `FlexRow` ≥ 1 `Column`.
- **Root tag:** exactly one `<Template>`, nothing outside it.
- **Button.url is validated** by the converter: `https://`, `tel:`, `mailto:`; survey links are an error. A separate HTTPS policy from the "Images" section applies to Image.
- **Values:** strings in quotes, numbers and objects in `{}`. Objects are partial merge (only changed fields). Arrays are a full replacement.
- **Gap attributes:** for every `*Gap` (`itemsGap`, `columnsGap`, `rowsGap`, `iconTextGap`), the value is an object `{ size: N }`, not a number.
- **Mobile typography:** for every `<Text>` where `style.fontSize` or `style.align` is set, `style.mobile` is specified with deliberate `fontSize`/`align`. A `<Button>` with `simpleTextStyles.fontSize` set has `simpleTextStyles.mobile.fontSize`. After convert, there is no unexpected `{ fontSize: 18, align: "left" }` for important desktop text.
- **Fonts:** no new `font.family` is present unless the user confirmed that the
  family is already available in the editor; an existing family is not changed on round-trip
  without a request.
- **Escaping in text:** write markup inside `<Text>` only as explicit JSX tags (`<br/>`, `<strong>…</strong>`). A quoted string in `<Text>` is **literal text**: the live backend escapes it (a `<p>` becomes visible text, not a paragraph). Move raw HTML fragments (an unclosed `<br>`, a comment, an `&nbsp;` entity, a table) out into `<Html>{"…"}</Html>`. Do not mix bare text and a quoted string in one element — live rejects it (`<Text> may only contain text`).
- **Button content:** plain text only, no markup.
- **Divider:** self-closing `<Divider />`, content forbidden; `border` set in full with thickness `1` in `size.top`, `innerSpacing` not zeroed out, a full-width divider is in its own `FlexRow`; if preview/QA is performed, the line is visible in the preview.
- **Links:** no placeholder URL in any new `Button`/`<a>`/`Image.url`; a clickable
  `Image.url` is set only from an explicit HTTPS URL given by the user; placeholders from an existing
  email are preserved and listed to the user.
- **Groups:** at least one item. In `<Menu>`, all items are either only `<Text>` or only `<Button>` (do not mix); in `<BulletList>` — only `<BulletItem>`; in `<Socials>` — only `<Image image={{...}} />` with a confirmed URL.
- **`BulletList`:** a supported `bulletIcon` is set: a flat `{ url, fileName }` for
  a small 4px dot, or `{ type: "custom", url, fileName, size: N }` for a large
  marker/badge. Without it, the default marker breaks the layout. Different numbered icons are not
  placed as items in one list sharing a common icon; a list of ordinary features with a heading
  and description is assembled as a grid, not as a list.
- **Split:** contains only `<Column size={N}>`; a column has only `size` and 0..1 element. Do not nest `<Split>` inside `<Split>`.
- **Group visibility:** set `visibilityOnDevices` on `<Menu>`, `<BulletList>`, `<Socials>`, or `<Split>`, but not on their items.
- **Images:** every authored `<Image>` has `image={{ mode: "static", static: { url, fileName } }}`. The source URL starts with `https://` and came from the user or was returned by Ops from a confirmed gallery DTO; there is no bare Image, no author-supplied forbidden schemes, and no invented Socials URLs. If size/alignment of a standalone image was requested, they are set via `Image.size`/`Image.align`, not via extra columns; a fixed size has a deliberate mobile branch.
- **Unsubscribe:** the canonical link is not duplicated; a new `${Message.UnsubscribeLink}` is allowed only as the exact `href` of an `<a>` inside `<Text>`. No `<Button url="${Message.UnsubscribeLink}">`, fake `/unsubscribe`, preferences-as-unsubscribe, or other new `${...}`/`{{...}}` variables.

## Unsupported → decline or simplify

The prohibitions themselves are stated in "Not implemented" and the topical sections; this is
what to do instead, when a request runs into them.

- Arbitrary personalization and `<Var>` (rules in "Not implemented") → offer
  static text or decline; do not insert new variables.
- `<Theme>` and `variant` → offer explicit `style`/`simpleTextStyles`; do not emulate a
  theme preset through the DSL.
- `targeting` on Block/Row → explain that it is an external setting: it cannot be
  emulated via JSX and is configured outside the email.
- Dynamic content (RSS, a feed) → decline.
- An image without a confirmed HTTPS URL (rules in "Images") → ask for an HTTPS URL or hand the file to Ops for the gallery; do not substitute anything from a forbidden scheme.
- A bare `<Image />` in existing JSX → ask for a URL or obtain one via Ops per the gallery rules and replace the Image before writing it back.
- A timer or video → explain the limitation and offer Text/Button.
- An unclear CTA or a clickable image with no URL → ask one clarifying question.
  No `https://example.com`, `https://`, `#`; do not create a `<Button>`
  or `Image.url` without a link. A clickable image is expressed via `Image.url`.
- A divider with zeroed-out `border` or `innerSpacing` → do not hand it off as a finished result: the line will not be visible.
- An explicitly styled `<Button>`-as-unsubscribe → explain that only the rich-text link is confirmed, and offer it. Do not generate fake URLs or arbitrary tokens.
- Editing an existing campaign "by ID only" → hand the task to Ops:
  `campaign_get` → `visual_template_get`. If the template cannot be expressed in JSX or there is no
  visual format, do not run a workaround JSON conversion: suggest the UI. A separately
  provided JSX can be edited/shown, but do not write it into an unconfirmed or
  incompatible format. Do not invent `mailingInternalId`, `variantInternalId`, or
  `formatInternalId`.

## Where to go for details

| Situation / signal | File | What's there |
|---|---|---|
| Any value shapes beyond the copy-safe forms in the "Value rules" section — MANDATORY before generating | `references/formats.md` | Exact value shapes: `buttonSize`, standalone `align`, `gapAfterBlock`, `verticalAlign`, `Image.size`/`align`/`url`, `bulletIcon` |
| Unsure which tag/attribute to use, need the full markup grammar | `references/dsl-surface.md` | Full DSL specification: attributes, hierarchy, grid, text markup |
| First numbered-point block — MANDATORY before generating | `references/examples.md` §14 | Sample `BulletList` custom icon and notes on mobile |
| Need a typical email fragment as a sample | `references/examples.md` | Input→output examples by block type |
