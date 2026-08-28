# Examples (curated)

**When to read:** you need a proven sample of a typical block; §14 is mandatory before
the first numbered-point block.
**Return to:** Workflow / Self-check in `SKILL.md`.

The patterns below cover the typical cases. Each example is self-contained, with a "why it's done this way" explanation.

## 1. Text block (heading + body)

**User description:** "Heading '50% off', body 'This week only'"

```jsx
<Template>
  <Block>
    <FlexRow>
      <Column size={12}>
        <Text style={{ fontSize: 32, inscription: ["bold"], align: "center", mobile: { fontSize: 28, align: "center" } }}>50% off</Text>
        <Text>This week only</Text>
      </Column>
    </FlexRow>
  </Block>
</Template>
```

**Why it's done this way:**
- `style={{ fontSize: 32, inscription: ["bold"], align: "center", mobile: { fontSize: 28, align: "center" } }}` — the heading is defined with an explicit size, alignment, and a mobile branch, not with `variant` (the DSL has no theme presets).
- `size={12}` — a single full-width column.
- Plain text — no `<b>`, no `<a>`, no HTML markup.
- `Text` without `style` — regular text with the theme defaults.

## 2. CTA button

**User description:** "A 'Buy now' button linking to https://shop.example.com"

```jsx
<Template>
  <Block>
    <FlexRow>
      <Column size={12}>
        <Button url="https://shop.example.com">Buy now</Button>
      </Column>
    </FlexRow>
  </Block>
</Template>
```

**Why it's done this way:**
- For a new CTA, `url` is required by policy; the converter validates the value if the attribute is present. Use `https://`, `tel:`, or `mailto:`.
- The button label is plain text, no markup.
- The default alignment is `center` (no need to specify it).
- The default `background` is black and `color` is white. That is a fallback for when nothing is known about the styling, not a finished solution: if a brand or a reference is given, set the brand `background` and `simpleTextStyles.color` explicitly.

## 3. Rich text with markup

**User description:** "Text with a link and a bold word"

```jsx
<Template>
  <Block>
    <FlexRow>
      <Column size={12}>
        <Text>
          <p style="margin: 0;">Summer <strong>sale</strong>, <a href="https://shop.example">see more</a></p>
        </Text>
      </Column>
    </FlexRow>
  </Block>
</Template>
```

**Why it's done this way:**
- HTML markup inside `<Text>` — `<p>`, `<strong>`, `<a>` — just like in the editor.
- `<p style="margin: 0;">` — the paragraph wrapper, preserves the text structure.
- No `style` on `<Text>` — theme default styles apply.
- `href` inside `<a>` — the link lives in the markup, not in an element attribute.

## 4. Two-column layout (6+6)

**User description:** "Text on the left, a button on the right"

```jsx
<Template>
  <Block>
    <FlexRow>
      <Column size={6}>
        <Text>Left column</Text>
      </Column>
      <Column size={6}>
        <Button url="https://example.com">Button</Button>
      </Column>
    </FlexRow>
  </Block>
</Template>
```

**Why it's done this way:**
- `6+6=12` — the `size` values within one `FlexRow` must sum to exactly 12.
- Order in JSX = left-to-right order in the email.
- `Text` and `Button` in separate columns are independent elements.
- No percentage `width` anywhere — width is set only via `size`.

## 5. Block with background and padding

**User description:** "A section with a gray background and 24px padding"

```jsx
<Template>
  <Block background={{ type: "color", value: "#f5f5f5" }} innerSpacing={{ top: 24, bottom: 24, left: 24, right: 24 }}>
    <FlexRow>
      <Column size={12}>
        <Text>Text inside</Text>
      </Column>
    </FlexRow>
  </Block>
</Template>
```

**Why it's done this way:**
- `background` is a JSON object `{ type: "color", value: "#f5f5f5" }`, not a string.
- `innerSpacing` is a JSON object with `top`, `bottom`, `left`, `right` fields; partial merge — specify only what changes, the remaining fields come from the prop default.
- `Block` is an email section; the background and padding apply to the whole section.
- `Block.innerSpacing` creates space around the row; `Column` keeps its own defaults.
- `background` also exists on `FlexRow` and `Column`: a background on a `Column` combined with `borderRadius` makes a card, and alternating backgrounds on adjacent `Block`s create section contrast. Don't settle for a single gray background across the whole email (example §13).
- Regular vertical spacing is done with `innerSpacing`, not
  `gapAfterBlock`, so the section color extends under the padding. `gapAfterBlock`
  would only be needed for a deliberate break exposing the outer background color.

## 6. Arbitrary HTML

**User description:** "Insert arbitrary HTML — a table with an unclosed `<br>` and a comment"

```jsx
<Template>
  <Block>
    <FlexRow>
      <Column size={12}>
        <Html>{"<table><tr><td>A table, a comment, an unclosed <br> — anything</td></tr></table>"}</Html>
      </Column>
    </FlexRow>
  </Block>
</Template>
```

**Why it's done this way:**
- `<Html>` accepts only a quoted string: the live backend rejects direct JSX (`<Html><div>…</div></Html>`) with `<Html> may only contain text`.
- The quoted string exists for required raw markup that cannot be expressed with the standard blocks: e.g. tables, Outlook conditionals, entities, and unclosed tags.
- Emails are stored as JSON; the JSON→JSX read may emit a quoted string — no data is lost.
- Use `<Html>` only when nothing else fits — text, a button, and an image survive manual edits, an html block does not.

## 7. Menu built from Text lines

**User description:** "A horizontal menu: Catalog and Sale"

```jsx
<Template>
  <Block>
    <FlexRow>
      <Column size={12}>
        <Menu align={{ align: "center", mobile: { align: "center" } }} itemsGap={{ size: 16, mobile: { size: 16 } }}>
          <Text>Catalog</Text>
          <Text>Sale</Text>
        </Menu>
      </Column>
    </FlexRow>
  </Block>
</Template>
```

**Why it's done this way:**
- `<Menu>` contains direct lines without `<Column>`.
- All lines are of the same type: only `<Text>` here.

## 8. Bulleted list

**User description:** "A list of two short benefits"

```jsx
<Template>
  <Block>
    <FlexRow>
      <Column size={12}>
        <BulletList bulletIcon={{ url: "https://cdn.example.com/dot.png", fileName: "dot.png" }}>
          <BulletItem>Free shipping</BulletItem>
          <BulletItem>30-day returns</BulletItem>
        </BulletList>
      </Column>
    </FlexRow>
  </Block>
</Template>
```

**Why it's done this way:**
- `<BulletList>` contains only `<BulletItem>` and at least one line.
- `<BulletItem>` here does not need a standalone stored schema: the group creates the line.
- `bulletIcon` is set **mandatorily**: without it the system marker renders as a giant black circle. The shape is a flat object `{ url, fileName }`; `{{ mode: "static", static: {...} }}` is silently ignored, a plain string breaks the preview. The URL here is illustrative — take a confirmed one (icons are available in the gallery's system folder).
- In this flat form the marker width is 4px, so the icon should be a dot or a simple circle.
  For a large marker, use the separate custom form with `size` — §14.
- This format is for **short one-liners**. A feature set with a heading and a description is built as a card grid — §13.

## 9. Social networks

**User description:** "Three social network icons, 40px wide"

```jsx
<Template>
  <Block>
    <FlexRow>
      <Column size={12}>
        <Socials imageSize={{ type: "fixed", width: 40, mobile: { type: "fixed", width: 40 } }}>
          <Image image={{ mode: "static", static: { url: "https://cdn.example.com/vk.png", fileName: "vk.png" } }} />
          <Image image={{ mode: "static", static: { url: "https://cdn.example.com/tg.png", fileName: "tg.png" } }} />
          <Image image={{ mode: "static", static: { url: "https://cdn.example.com/fb.png", fileName: "fb.png" } }} />
        </Socials>
      </Column>
    </FlexRow>
  </Block>
</Template>
```

**Why it's done this way:**
- `<Socials>` contains only `<Image image={{...}} />` lines; each icon has its own URL.
- `imageSize` is set on the group, not on individual Image lines.
- All `cdn.example.com` URLs here are illustrative. In a real answer, substitute each with only a URL
  the user provided or one returned by an unambiguously selected gallery DTO.

## 10. Split 5+7

**User description:** "Text on the left, a button on the right, in a 5+7 layout"

```jsx
<Template>
  <Block>
    <FlexRow>
      <Column size={12}>
        <Split>
          <Column size={5}><Text>Offer terms</Text></Column>
          <Column size={7}><Button url="https://shop.example">Buy</Button></Column>
        </Split>
      </Column>
    </FlexRow>
  </Block>
</Template>
```

**Why it's done this way:**
- `5+7=12`: column sizes inside `<Split>` must sum to 12.
- Each Split column has only `size` and exactly one element.

## 11. Image from an external HTTPS URL

**User description:** "Place a banner from my HTTPS link"

```jsx
<Template>
  <Block>
    <FlexRow>
      <Column size={12}>
        <Image image={{ mode: "static", static: { url: "https://cdn.example.com/banner.png", fileName: "banner.png" } }} />
      </Column>
    </FlexRow>
  </Block>
</Template>
```

**Why it's done this way:**
- `<Image>` is self-closing and contains a required `image` with `url` and `fileName`.
- An external HTTPS URL is inserted as is; the skill does not convert it to an internal URL.
- `https://cdn.example.com/banner.png` is an illustration. Generate it only when the user gave
  a specific URL; otherwise use a confirmed URL from a gallery DTO.

## 12. Cards with aligned CTAs (synchronized rows)

**User description:** "Two cards side by side, buttons at exactly the same height"

```jsx
<Template>
  <Block>
    <FlexRow>
      <Column size={6}><Image image={{ mode: "static", static: { url: "https://cdn.example.com/a.jpg", fileName: "a.jpg" } }} /></Column>
      <Column size={6}><Image image={{ mode: "static", static: { url: "https://cdn.example.com/b.jpg", fileName: "b.jpg" } }} /></Column>
    </FlexRow>
    <FlexRow>
      <Column size={6}><Text style={{ fontSize: 18, mobile: { fontSize: 16, align: "left" } }}>River cruises</Text></Column>
      <Column size={6}><Text style={{ fontSize: 18, mobile: { fontSize: 16, align: "left" } }}>Parks and estates</Text></Column>
    </FlexRow>
    <FlexRow>
      <Column size={6}><Text>Three evening river routes with stops at the best viewpoints.</Text></Column>
      <Column size={6}><Text>Historic estates and quiet corners of the city's green spaces.</Text></Column>
    </FlexRow>
    <FlexRow>
      <Column size={6}><Button url="https://example.com/river">River routes</Button></Column>
      <Column size={6}><Button url="https://example.com/parks">Green map</Button></Column>
    </FlexRow>
  </Block>
</Template>
```

**Why it's done this way:**
- Don't put each whole card into its own `Column`: column heights are computed independently,
  text wraps differently, and the buttons "drift" vertically. Fixed heights via
  `<Html>` tables are fragile — the renderer wraps components in its own tables/cells.
- Synchronized rows (images → headings → descriptions → buttons) guarantee the same top
  coordinate for all CTAs — they're in one `FlexRow`. This generalizes to 4+4+4 and any number of rows.
- **The cost of this pattern is mobile order.** With adaptive column stacking, the mobile
  user will see "all images → all headings → all descriptions → all buttons," not
  the cards one after another. If per-card mobile order matters, that's a product decision
  (e.g. separate mobile rows via `visibilityOnDevices`) — raise it with the user,
  don't decide it silently.
- The card headings change the desktop `fontSize`, so each has a mobile branch; without it the backend may substitute `{ fontSize: 18, align: "left" }`.
- `cdn.example.com` URLs are illustrative — in a real answer, use only a URL from the user or a gallery DTO.

## 13. Card section: background, contrast, accent

**User description:** "A block about the service's features, in the brand style from the website"

```jsx
<Template>
  <Block background={{ type: "color", value: "#1f2933" }} innerSpacing={{ top: 32, bottom: 32, left: 24, right: 24 }}>
    <FlexRow>
      <Column size={12}>
        <Text style={{ fontSize: 28, color: "#ffffff", align: "center", mobile: { fontSize: 22, align: "center" } }}>
          <h1 style="margin: 0;">What's included in the service</h1>
        </Text>
      </Column>
    </FlexRow>
    <FlexRow columnsGap={{ size: 16, mobile: { size: 12 } }} rowsGap={{ size: 16 }}>
      <Column size={6} background={{ type: "color", value: "#2c3844" }} borderRadius={{ topLeft: 12, topRight: 12, bottomLeft: 12, bottomRight: 12 }} innerSpacing={{ top: 20, bottom: 20, left: 20, right: 20 }}>
        <Text style={{ fontSize: 18, color: "#f2b705", mobile: { fontSize: 16, align: "left" } }}>Delivery</Text>
        <Text style={{ fontSize: 14, color: "#d5dbe1", mobile: { fontSize: 14, align: "left" } }}>We pick up and drop off at a time that works for you</Text>
      </Column>
      <Column size={6} background={{ type: "color", value: "#2c3844" }} borderRadius={{ topLeft: 12, topRight: 12, bottomLeft: 12, bottomRight: 12 }} innerSpacing={{ top: 20, bottom: 20, left: 20, right: 20 }}>
        <Text style={{ fontSize: 18, color: "#f2b705", mobile: { fontSize: 16, align: "left" } }}>Support</Text>
        <Text style={{ fontSize: 14, color: "#d5dbe1", mobile: { fontSize: 14, align: "left" } }}>We answer in chat, seven days a week</Text>
      </Column>
    </FlexRow>
  </Block>
</Template>
```

**Why it's done this way:**
- This is what listing features looks like by default — as a grid, not a `BulletList`. Generalizes to 4+4+4; with an odd number of cards, the last row is padded with an empty `<Column>`.
- Background + `borderRadius` + `innerSpacing` on `Column` make a card; the `Block` background provides contrast with neighboring sections.
- Copy **the roles of the colors, not the values**: section background → card background (one step lighter or darker than the section background) → heading accent → muted description color. The specific hex values come from the client's reference. The section doesn't have to be dark: for a light brand, the section background is light and the text is dark — contrast matters more than direction.
- Three size levels (28 / 18 / 14) create hierarchy; the numbers themselves also adapt to the layout.
- Styles are set only via `style` — `<Theme>` and `variant` are forbidden in the DSL.
- Every `<Text>` with `fontSize` has a mobile branch, otherwise the backend will substitute its own values.
- **The font is not set from the layout:** it's assigned by the tenant's theme, and different components may get a different typeface (for example `Menu` and `BulletList` don't get the same family as `Text`). If unified typography matters for the email, that's configured in the editor, not in the layout.
- Verified live: the preview accepts this section and returns correct HTML.

## 14. Editable numbered point

```jsx
<Template>
  <Block innerSpacing={{ top: 20, bottom: 20, left: 24, right: 24, mobile: { top: 16, bottom: 16, left: 16, right: 16 } }}>
    <FlexRow>
      <Column size={12}>
        <BulletList
          iconTextGap={{ size: 12, mobile: { size: 12 } }}
          bulletIcon={{ type: "custom", url: "https://cdn.example.com/one.png", fileName: "one.png", size: 40 }}
        >
          <BulletItem>Light morning movement instead of intense workouts</BulletItem>
        </BulletList>
      </Column>
    </FlexRow>
  </Block>
</Template>
```

**Why it's done this way:**

- `bulletIcon.type="custom"` + `size={40}` creates a separate editor marker;
  the stored template and live HTML confirm an actual width of 40px.
- Don't substitute a styled `<span>` marker inside `<Text>` or `<Html>`: those render, but
  don't give the user a separate editable element.
- One BulletList uses one icon for all its lines. For different numerals, create
  a separate BulletList per point, or use a separate fixed-size `<Image>` and `<Text>`.
- The URL is a placeholder: before generating, get a confirmed asset through Ops.
- A custom marker has one `size` for desktop/mobile, so before saving, visually
  check the point on mobile too; if a separate mobile size is needed, use a standalone
  fixed-size Image with `size.mobile.width`.
- The benchmark for "verified on mobile": the marker stays 40px, the text doesn't slide under it,
  and `iconTextGap.mobile` matches desktop. If the marker overlaps the text, reduce
  `size` or switch to a standalone Image.
