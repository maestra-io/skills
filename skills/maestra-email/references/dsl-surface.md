# DSL surface — what you can write in JSX

**When to read:** when it is unclear which tag/attribute to use or how the allowed
JSX/rich-text markup is structured. Exact value shapes are picked separately via the `SKILL.md` router.
**Return to:** Workflow / Self-check in `SKILL.md`.

This is a reference for the JSX markup used to generate and edit Maestra emails. It covers only what can be expressed in the markup; everything else (UUID, envelope, email subject, targeting, globalProps, materialization, etc.) is added by the serializer itself or ignored.

This reference describes the currently accepted DSL; the mandatory backend check is performed via `convert` in `maestra-email-ops`.

## 1. Structure

The four outer containers always go in this order; after `<Column>` comes an element, including a group:

```
Template  →  Block  →  FlexRow  →  Column  →  Text | Button | Divider | Html | Image | Menu | BulletList | Socials | Split
```

```jsx
<Template>
  <Block>
    <FlexRow>
      <Column size={8}><Text>Main column</Text></Column>
      <Column size={4}><Text>Side column</Text></Column>
    </FlexRow>
  </Block>
</Template>
```

Rules:

- **Exactly one `<Template>`** per document, and nothing outside it. Use only `<Template>` as the root. `<Email>`, `<Root>`, or any other root tag is rejected: `The root element must be <Template>`.
- **Each container holds only its own kind of child.** `<Template>` — blocks; `<Block>` — rows; `<FlexRow>` — columns; only `<Column>` — elements or groups. Putting `<Text>` directly into `<FlexRow>` is an error, not a shortcut.
- **Use `<FlexRow>`, not `<Row>`.** The row tag in the production converter is `FlexRow`. `<Row>` is rejected as `Unknown element <Row>`.
- **Every container requires at least one child** — except the column. An empty `<Template>`, `<Block>`, or `<FlexRow>` is an error. An empty `<Column>` is allowed.
- **A column requires `size`** — an integer from 1 to 12. The `size` values of the columns in one `<FlexRow>` must sum to 12 (see §5).
- **A group requires at least one line.** `<Menu>` contains only `<Text>` or only `<Button>`; `<BulletList>` — only `<BulletItem>`; `<Socials>` — only `<Image image={{...}} />`.
- **`<Split>` contains only `<Column size={N}>`.** Their `size` values sum to 12; a Split column carries only `size` and contains 0..1 element. Any group is allowed inside it, except `<Split>`.

## 2. Value grammar — literals only

Attributes accept only strings, numbers, JSON objects, and arrays; do not generate expressions,
spread, imports, executable code, comments, or Markdown fences. This file is responsible
for the allowed tags/attributes and the markup structure; for value shapes go back to the
`SKILL.md` router.

## 3. Write only what you are changing

JSX → template creates a new node with defaults. An attribute changes the specified setting; omitting one
does not restore the value from a previously saved email.

```jsx
<Divider innerSpacing={{ top: 30 }} />
```

Objects are filled in from defaults key by key; lists are replaced wholesale. To reset, specify
an explicit empty/zero value, `{ type: "none" }` for a border, or `{ type: "transparent" }`
for a background.

## 4. Containers — attributes

Only these attributes. Anything else is `Unknown attribute` (not a silent drop).

| Container | Attribute | What it does |
|---|---|---|
| `Block` | `background` | Background. JSON: `{ type: "color", value: "#f5f5f5" }` or `{ type: "transparent" }` |
| `Block` | `border` | Border. JSON: `{ type: "solid", color: "#cccccc", size: { top: 1, right: 1, bottom: 1, left: 1 } }` or `{ type: "none" }` |
| `Block` | `borderRadius` | Corner rounding. JSON: `{ topLeft: 0, topRight: 0, bottomLeft: 0, bottomRight: 0, mobile: { … } }` |
| `Block` | `innerSpacing` | Inner padding. JSON: `{ top, bottom, left, right, mobile: { … } }`. **Do not write `padding`** — no such attribute exists; use `innerSpacing` |
| `Block` | `gapAfterBlock` | Outer gap after the block. JSON: `{ desktop, mobile }`. For ordinary spacing inside a colored section, use `innerSpacing` by default; a new `gapAfterBlock` — only on explicit request or when a visible gap showing the outer background color is intended |
| `Block` | `externalBackground` | Outer background |
| `Block` | `visibilityOnDevices` | Visibility. String: `"all"` (default), `"desktop"`, `"mobile"` |
| `FlexRow` | `background` | same as `Block` |
| `FlexRow` | `border` | same as `Block` |
| `FlexRow` | `borderRadius` | same as `Block` |
| `FlexRow` | `innerSpacing` | same as `Block`. **Not `padding`** |
| `FlexRow` | `columnsGap` | Gap between columns. JSON: `{ size: 20, mobile: { size: 20 } }` |
| `FlexRow` | `rowsGap` | Gap between rows (mobile-stacked) |
| `FlexRow` | `verticalAlign` | Vertical alignment. JSON: `{ align: "middle", mobile: { align: "middle" } }` |
| `FlexRow` | `isColumnsMobileAdaptive` | Adaptive mobile layout |
| `FlexRow` | `columnVerticalDirection` | Column direction |
| `FlexRow` | `visibilityOnDevices` | same as `Block` |
| `Column` | `size` | **Required.** Integer 1..12 |
| `Column` | `background` | same as `Block` |
| `Column` | `border` | same as `Block` |
| `Column` | `borderRadius` | same as `Block` |
| `Column` | `innerSpacing` | same as `Block`. **Not `padding`** |

`Column.size` is the only required attribute among containers. The attribute `flexColumnSize` must not be used — that is the internal prop name; write `size`.

`innerSpacing` and `gapAfterBlock` are not interchangeable: `innerSpacing` keeps the container's
background under the spacing, `gapAfterBlock` shows the outer background between sections. When
creating/editing, do ordinary vertical spacing via `innerSpacing`; do not remove an untouched
existing `gapAfterBlock` during an unrelated round-trip edit.

Two settings are deliberately excluded from the DSL: **targeting** and **theme sync** (synchronization with the tenant theme). They point outward from the email, stay as they are, and writing them is an error.

## 5. Grid

The `size` values of the columns in each `<FlexRow>` and `<Split>` **must sum to 12**.

```jsx
<FlexRow><Column size={6}>…</Column><Column size={6}>…</Column></FlexRow>
<FlexRow><Column size={4}>…</Column><Column size={4}>…</Column><Column size={4}>…</Column></FlexRow>
```

Do not write `size={6}` on a lone column of a multi-column row — the sum will not reach 12 and it will be an error. For a single column spanning the whole row use `size={12}`. Rows and Split are independent: each sums to 12 separately.

## 6. Elements

Elements live inside `<Column>`. Fully supported: `<Text>`, `<Button>`, `<Divider>`, `<Html>`, `<Image>`, `<Menu>`, `<BulletList>`, `<Socials>`, `<Split>`. Do not generate `<Timer>` or `<Video>` without a separately verified stored schema; `<BulletItem>…</BulletItem>` is allowed only as a line of `<BulletList>`.

Empty nodes are emitted self-closing: `<Column size={4} />`, `<Html />`, `<Divider />`, `<Image ... />`. On write, both forms (`<Column size={4}></Column>` and `<Column size={4} />`) are read identically.

### Text

Content: the text itself or HTML markup, between the tags (see §7). The `style` attribute — typography of the text as a whole.

```jsx
<Text>Summer sale starts today</Text>
<Text innerSpacing={{ top: 24, bottom: 24 }} background={{ type: "color", value: "#f5f5f5" }}>
  Text with spacing and background
</Text>
<Text style={{ fontSize: 24, inscription: ["bold"] }}>
  <p style="margin: 0;">Summer <strong>sale</strong>, <a href="https://shop.example">see the offers</a></p>
</Text>
```

| Attribute | What it does |
|---|---|
| `style` | Typography of the whole text (font, fontSize, color, inscription, link, align, mobile). JSON. **Do not write `fontSize`, `color`, `align` as separate attributes** — they do not exist; nest them inside `style={{ … }}`. If `fontSize` or `align` is set, set `style.mobile` deliberately. A new `font.family` — only for a font the user has confirmed as already available in the Maestra editor; an existing family is preserved on round-trip |
| `innerSpacing` | same as `Block` |
| `background` | same as `Block` |
| `border` | same as `Block` |
| `borderRadius` | same as `Block`. **Not `radius`** |
| `visibilityOnDevices` | same as `Block` |

### Button

Content: the button label, between the tags. **Plain text only.** Markup inside `<Button>` is forbidden — `<strong>…</strong>` yields `<Button> may only contain text`.

```jsx
<Button url="https://shop.example/sale">Shop now</Button>
<Button url="mailto:hi@example.com" buttonSize={{ width: 240 }} borderRadius={{ topLeft: 24, topRight: 24, bottomLeft: 24, bottomRight: 24 }}>
  Write to us
</Button>
```

| Attribute | What it does |
|---|---|
| `url` | Link. Write `url`, **not `href`** — `href` is rejected as `Unknown attribute`. For a new CTA, `url` is required by policy; when the attribute is absent the converter leaves the default. `https://`, `tel:`, `mailto:` (the type is inferred from the value) |
| `align` | Alignment. JSON: `{ align: "center", mobile: { align: "center" } }` |
| `innerSpacing` | same as `Block` |
| `buttonSize` | Size. JSON: `{ height, heightMobile, widthType: "percent", width: 100, widthMobile: 100 }` |
| `background` | same as `Block`. Default `{ type: "color", value: "#000000" }` |
| `simpleTextStyles` | Label typography. JSON: `{ font: { family: "Arial" }, fontSize: 14, color: "#ffffff", inscription: [], mobile: { fontSize: 14 } }`. `family` here illustrates an existing/confirmed font, not permission to guess a new one. If a desktop `fontSize` is set, set `mobile.fontSize` deliberately |
| `border` | same as `Block` |
| `borderRadius` | same as `Block`. Default 8 on each corner |
| `iconSrc` | Icon next to the label. JSON: `{ url: "https://cdn.example.com/cart.png" }` |
| `iconAlt` | Icon alt text |
| `iconDisplay` | JSON: `{ position: "EMPTY" }` (default — no icon) |
| `iconSizeInPercents` | JSON: `{ widthInPercents: 30 }` |
| `visibilityOnDevices` | same as `Block` |

### Divider

A horizontal line. No content, always a single tag: `<Divider />`.

```jsx
<Divider />
<Divider innerSpacing={{ top: 18, bottom: 18 }} border={{ type: "solid", color: "#cccccc", size: { top: 1, right: 0, bottom: 0, left: 0 } }} />
```

| Attribute | What it does |
|---|---|
| `innerSpacing` | same as `Block`. Default `{ top: 20, bottom: 20, left: 0, right: 0, mobile: { … } }` |
| `border` | The line as a whole. JSON: `{ type: "solid", color: "#000000", size: { top: 1, right: 1, bottom: 1, left: 1 } }`. **Do not write `color` and `thickness` as separate attributes** — they do not exist; nest `color` and `size` inside `border={{ … }}`. **Specify the whole object** — with a partial merge, `border={{ color: "…" }}` takes `type` and `size` from the default and the line becomes barely visible. Keep the visible thickness in `size.top` (usually `1`) |
| `visibilityOnDevices` | same as `Block` |

### Html

Arbitrary HTML between the tags. Order of preference: standard flexible blocks first (`Text`/`Button`/`Image`/`Menu`/`BulletList`/`Socials`/`Split`); `<Html>` is only a fallback when what is needed cannot be expressed otherwise, or on the user's direct request. Text, a button, and an image will survive manual edits in the Maestra editor; an html block will not.

```jsx
<Html>{"<table><tr><td>Raw table markup</td></tr></table>"}</Html>
```

There is one form: a single quoted string (`<Html>{"<table>…</table>"}</Html>`). Use it for
required raw markup that cannot be expressed with standard blocks. Direct JSX inside
`<Html>` is rejected by the backend; an empty `<Html />` creates a library placeholder.

| Attribute | What it does |
|---|---|
| `visibilityOnDevices` | same as `Block` |

### Image

`<Image>` is a standalone image or a line of `<Socials>`. A complete source is required:

```jsx
<Image image={{ mode: "static", static: { url: "https://cdn.example.com/banner.png", fileName: "banner.png" } }} />
<Image
  url="https://shop.example/item"
  align={{ align: "center", mobile: { align: "center" } }}
  size={{ type: "fixed", width: 120, mobile: { type: "fixed", width: 80 } }}
  image={{ mode: "static", static: { url: "https://cdn.example.com/icon.png", fileName: "icon.png" } }}
/>
```

The URL in the example is illustrative. The URL source and the rules for choosing a gallery asset are defined in
`SKILL.md`; the allowed shape of `image` and `fileName` is shown in the example and the table below.

| Attribute | What it does |
|---|---|
| `image` | **Required.** `{ mode: "static", static: { url: "<HTTPS URL>", fileName: "<name>" } }` |
| `url` | Optional HTTPS click-through link for the image. This is not the image source; do not write a placeholder |
| `size` | Size of a standalone image. Fixed: `{ type: "fixed", width: N, mobile: { type: "fixed", width: N } }`. Stored constructor templates also round-trip `{ equalizedImageMaxWidth: "N" }`; preserve this field, but do not invent it |
| `align` | Alignment of a standalone image: `{ align: "left"|"center"|"right", mobile: { align: "…" } }` |
| `innerSpacing` | same as `Block` |
| `border` | same as `Block` |
| `borderRadius` | same as `Block` |
| `visibilityOnDevices` | same as `Block` |

Do not generate `background` (the backend rejects it), or the HTML attributes `src`, `href`, `alt`,
`width`, or `radius`. Use `image` for the source, the constructor attr `url` for the click,
`size` for the size, and `align` for alignment. For `<Socials>` lines, size and
alignment are set on the parent `Socials.imageSize`/`Socials.align`.
A bare `<Image />` is forbidden by policy, because the backend substitutes a base64 placeholder.

### Timer, Video, BulletItem

Do not generate `<Timer>` or `<Video>` without a verified stored schema. `<BulletItem>text</BulletItem>`
works only inside `<BulletList>`.

### Group elements: Menu, BulletList, Socials, Split

A group is a single element with direct lines. It requires at least one line; `visibilityOnDevices` is set only on the group, not on a line. `globalThemeSync` may appear in a JSON fixture, but it is not part of the DSL.

#### Menu

In a menu all lines are of one kind: only `<Text>` or only `<Button>`, no mixing.

| Menu attributes |
|---|
| `align`, `itemsGap`, `innerSpacing`, `background`, `border`, `borderRadius`, `visibilityOnDevices` |

#### BulletList

`<BulletList>` contains only `<BulletItem>…</BulletItem>`. `align` on the list is not confirmed and is not part of the DSL.

**Always** set `bulletIcon`: the system default serializes as a `data:` SVG, but the backend does not
escape the quotes inside `src`, the attribute gets cut off, and the marker renders as a giant black circle.
There are two confirmed authored forms:

```jsx
bulletIcon={{ url: "https://cdn.example.com/dot.png", fileName: "dot.png" }}
bulletIcon={{ type: "custom", url: "https://cdn.example.com/one.png", fileName: "one.png", size: 40 }}
```

The flat form renders a small marker 4px wide and is suitable for a dot/circle.
`type: "custom"` + `size` round-trips from the Maestra editor, and the live preview/HTML renders
the actual `size` width; use it for a separately editable numbered badge.
`{{ mode: "static", static: {...} }}` is silently ignored, and a string crashes the preview with
`Internal server error`. All URLs must be confirmed HTTPS assets.

One group applies a shared `bulletIcon` to all lines. For different icons 1/2/3,
use a separate BulletList per item, or a standalone fixed-size Image + Text. Do not
draw a structural badge via a styled span inside Text or via Html if it must
be editable in the Maestra editor. A custom marker has one `size` for desktop/mobile,
so visually check mobile; if a separate mobile size is needed, use a
standalone Image with `size.mobile.width`.

| BulletList attributes |
|---|
| `bulletIcon` (always set it; flat 4px dot or a custom `size` badge), `background`, `border`, `borderRadius`, `innerSpacing`, `itemsGap`, `iconTextGap`, `iconTopPadding`, `visibilityOnDevices` |

#### Socials

`<Socials>` contains only `<Image image={{...}} />` lines. The URLs below are illustrative;
the source rules are the same as for a regular Image.

| Socials attributes |
|---|
| `background`, `align`, `innerSpacing`, `itemsGap`, `imageSize`, `border`, `borderRadius`, `visibilityOnDevices` |

#### Split

`<Split>` contains only `<Column size={N}>`; the sum of all `size` values is strictly 12. A Split column carries only `size`, contains 0..1 element, and may be empty. Simple elements and groups are allowed inside it, except `<Split>`.

| Split attributes |
|---|
| `columnsGap`, `verticalAlign`, `innerSpacing`, `background`, `border`, `borderRadius`, `visibilityOnDevices` |

The exact `itemsGap` defaults depend on the kind of group, so they are not fixed: specify a value only when you need to change the gap.

## 7. Text — content and inline markup

`<Text>` is two places at once: what is written (with markup) between the tags, and how it looks as a whole (font, size, color, links) — in the `style` attribute.

### Plain text — auto-wrapped in `<p>`

Text without its own markup is written as words:

```jsx
<Text>Summer sale starts today</Text>
```

The converter itself wraps such words in a paragraph: the result becomes `<p style="margin: 0">Summer sale starts today</p>`. Such a paragraph comes back in the same form on read. Auto-wrapping fires only if there is no block tag among the top-level children: if the markup already contains a block element, the converter wraps nothing.

### Full HTML markup

Markup is written as markup, exactly as the email stores it. **Do not rewrite what you did not come to change**: the email wraps text in its own way, and replacing that wrapper edits the email invisibly.

```jsx
<Text>
  <p style="margin: 0;"><span data-rich-text>Inspiring <u>stories</u> of people, </span><a data-rich-link href="https://example.com/stories">read them</a></p>
</Text>
```

**Tags you may use:** paragraphs and headings (`p`, `h1`–`h6`, `blockquote`), lists (`ul`, `ol`, `li`), inline marks (`strong`, `em`, `u`, `s`, `span`, `a`, `code`, `pre`), breaks (`br`, `hr`), and `personalization-parameter`. The live backend rejects `div` and tables (`table`, `thead`, `tbody`, `tr`, `td`, `th`) inside `<Text>` (`<div> is not allowed in a text`) — move table and div layout into `<Html>` as a quoted string (§6). Write explicit JSX void tags self-closing: `<br/>`, `<hr/>`. Do not generate `img`, `iframe`, `script`, `style` without a separate live check. Put an image in `<Image>` standalone or inside `<Socials>`.

**Attributes you may use:** `style`, `align`, `href`, `target`, `rel`, `model`, `data-name`, and the `data-rich-*` markers that the editor sets. Attributes inside rich-text markup are only plain strings or a marker without a value: correct is `<p style="margin: 0;">`, `<a href="https://...">`, `<span data-rich-text>`. Not allowed: `<p style={{ margin: 0 }}>`, spread attributes, expressions — the live backend returns `Attribute \`...\` on <...> must be a plain string`.

### Quoted string in `<Text>` — literal text

A quoted string in `<Text>` is **literal text, not markup**. The live backend escapes it: `<Text>{"<p>One<br>Next</p>"}</Text>` serializes as `<p style="margin: 0"><span data-rich-text>&lt;p&gt;One&lt;br&gt;Next&lt;/p&gt;</span></p>` — the tags become visible text in the email. So write markup only with explicit JSX tags from the allowlist above, and move raw HTML (tables, an unclosed `<br>`, comments, entities) into `<Html>{"…"}</Html>`. Do not mix bare text and a quoted string in one element — live rejects it (`<Text> may only contain text`). The quoted string remains necessary for literal text with special characters (`"`, `{`, `}`, a line break) and for existing personalization (§7).

### `data-rich-*` markers

The markers `data-rich-text` (on `<span>`), `data-rich-link` (on `<a>`), `data-rich-list-item` (on `<li>`) are placed by the converter — **do not write them when creating**. When reading existing text — **leave them in place, do not move them**: a missing marker is restored, but a moved marker is not removed and breaks styling (for example, `data-rich-text` on an `<a>` styles the link both as text and as a link). A marker without a value is stored as `data-rich-text=""`.

### Personalization — round-trip only, except the canonical unsubscribe link

Do not add new arbitrary personalization: an unknown parameter may remain literal text.
Recognize existing fragments and preserve them unchanged:

```jsx
<Text>{"Hello, ${Customer.FirstName}!"}</Text>
```

or as the tag the editor inserts:

```jsx
<Text><p style="margin: 0;">Hello, <personalization-parameter model="Customer.FirstName"></personalization-parameter>!</p></Text>
```

#### Unsubscribe link

The only permitted new exception to the personalization ban is the canonical unsubscribe
link: the exact `${Message.UnsubscribeLink}` as the plain-string `href` value of an `<a>`
inside `<Text>`.

Correct:

```jsx
<Text>
  <p style="margin: 0;">If you no longer want these emails — <a href="${Message.UnsubscribeLink}">unsubscribe</a></p>
</Text>
```

Incorrect:

```jsx
<Button url="${Message.UnsubscribeLink}">Unsubscribe</Button>
```

```jsx
<Text><p style="margin: 0;">Hello, ${Customer.FirstName}</p></Text>
```

```jsx
<Text><p style="margin: 0;"><a href="/unsubscribe">Unsubscribe</a></p></Text>
```

In the backend preview HTML the token may remain as the string `${Message.UnsubscribeLink}`:
its substitution happens at send time. Do not treat the literal token as a preview defect and
do not replace it with a fake URL. Preserve an existing canonical token, its label, and its placement
unchanged, unless the user asked to change the link.

### `style` — typography of the whole text

The `style` attribute holds what the editor's bottom panel edits — it applies to the text as a whole, not to a fragment:

```jsx
<Text style={{ fontSize: 16, color: "#111111", link: { color: "#0000E7", inscription: ["underlined"] }, mobile: { fontSize: 16, align: "left" } }}>
  Styled from end to end
</Text>
```

The same rule as everywhere: write the fields you are changing, the rest stay. If you change
`fontSize` or `align`, set `style.mobile`: without it, the backend may substitute
`{ fontSize: 18, align: "left" }` and break the mobile hierarchy.

Note the two kinds of "bold". `<strong>` inside the markup makes one word bold; `inscription: ["bold"]` in `style` makes the whole text bold. They are stored in different places and do not replace each other.

## 8. Theme presets

`variant` and `<Theme>` are not part of the current DSL: theme sync is disabled. Write styles explicitly via
`style={{ … }}` (Text) or `simpleTextStyles={{ … }}` (Button):

```jsx
<Text style={{ fontSize: 32, inscription: ["bold"], color: "#111111", mobile: { fontSize: 28, align: "left" } }}>Heading</Text>

<Button url="https://shop.example" background={{ type: "color", value: "#ff6600" }} simpleTextStyles={{ color: "#ffffff" }}>Buy now</Button>
```

## 9. URL

`Button.url` accepts `https://`, `tel:`, and `mailto:`; the backend validates the format and rejects
survey links. Write a simple link as a string: `url="https://shop.example"`; a URL with
special characters (`&`, `=`, quotes) — as a JSON string in an expression:
`url={"https://shop.example/?from=email&utm=sale"}`.

## 10. What the serializer adds itself

All service fields of the JSON (UUID, envelope, email subject, targeting, globalProps, sampling, materialization, etc.) are added by the serializer automatically. You only need what is listed in §4–§6: tags, hierarchy, column `size`, and element attributes.

## 11. Runtime validation and self-check

The backend checks the structure, the tag/attribute allowlist, literal-only values, the grid,
group composition, Button URL, and the allowed content of leaf elements. Report an error as
stage + status/code + a short message; the full response body is needed only for separate diagnostics.

The Generator itself additionally checks policy that the backend does not guarantee:

- the Image URL is confirmed by the user or Ops and uses HTTPS;
- no bare Image, no fake unsubscribe, no new personalization;
- colors are written as `#RRGGBB`, numeric values are reasonable;
- if a desktop `style.fontSize`/`style.align` or `simpleTextStyles.fontSize` is set, the mobile branch is set deliberately;
- device variants and mobile ordering match the request;
- the JSX contains no comments, imports, or executable expressions.
