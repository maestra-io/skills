# Verification, preview, and QA

**When to read this:** you need an HTML download, a PNG, desktop/mobile, QA/debug, or
diagnosis of a specific rendering or fallback problem. For a simple "show/refresh
preview," the invariants in `SKILL.md` are enough — don't open this file.
**Return to:** step 3 "Edits, freshness, and optional preview/QA" of the canonical
workflow in `SKILL.md`, or back to the user with the QA result.

```text
visual_template_preview(jsx) → temporary htmlUrl + MCP App widget in a supporting host
```

- **Preview is no longer an automatic step after every edit.** Each call to
  `visual_template_preview` opens a new MCP App widget in a supporting host;
  old widgets are not refreshed. So don't call preview "just in case," and don't
  run it after every JSX modification.
- **The preview has a freshness status.** After any JSX change, the previous
  link/panel no longer proves the current state of the email. Tell the user:
  "The previous preview no longer matches the current version. I can show you a
  new preview if you'd like." If there hasn't been a preview yet, say that one
  hasn't been opened yet. Don't create a new preview until the user asks, or
  until QA/diagnostics starts under the rules below.
- **When to call `visual_template_preview`:**
  1. the user explicitly asks to show/refresh the preview;
  2. the user asks to check the email, HTML, PNG, desktop/mobile, or rendering;
  3. the user comments on specific content or a visual problem in an
     already-shown/generated campaign;
  4. preview is needed as a read-only action for a campaign that can't be saved.
- **Return preview/editor errors to the generator verbatim; silent repair is
  forbidden.** If preview wasn't called and `visual_template_save` returned an
  error, pass that on to the generator verbatim too — it's a backend check of the
  current JSX on the write path.
- **A bare `Internal server error` with no line number** — suspect the format of
  an attribute value (a scalar instead of an object), not the block structure.
- **The tool returns a temporary `htmlUrl`, not inline HTML.** Once preview has
  been called, show the user the link as a fallback to the MCP App widget. In a
  host without MCP App, this is the only preview available to the user. If
  preview hasn't been called since the last edit, say plainly that there's no
  fresh backend preview.
- **HTML isn't downloaded automatically.** Only download HTML for HTML QA or
  diagnostics where you need to read the HTML. For PNG QA, HTML is no longer
  needed: MCP provides the PNG. First pin down the absolute `<projectRoot>`;
  don't rely on the runner's cwd. For a campaign, use the name
  `<mailingInternalId>.html`:

  ```bash
  # macOS/Linux
  curl --fail --location --silent --show-error "<htmlUrl>" \
    --output "<projectRoot>/<mailingInternalId>.html"

  # Windows PowerShell
  & curl.exe --fail --location --silent --show-error "<htmlUrl>" `
    --output "<projectRoot>/<mailingInternalId>.html"
  ```

  The campaign GUID needs no name sanitizing and prevents collisions between
  different campaigns. A new QA/debug download of the same campaign replaces the
  previous local file: that's expected — the file represents the latest
  downloaded backend render, not necessarily the latest JSX edit. Don't use just
  the campaign name, and don't invent your own name without `mailingInternalId`.
  If the download fails, keep the `htmlUrl`, report the `curl` error, and don't
  substitute in old HTML.
  Only count a download as successful when the exit code is `0` and the output
  file is non-empty.
  A download failure doesn't invalidate a successful backend preview and does
  not by itself block save. HTML QA is unavailable until the download is
  retried successfully; PNG QA via MCP doesn't depend on the HTML download.
  For a standalone preview with no target campaign and no `mailingInternalId`,
  use `<projectRoot>/standalone-preview.html`; it represents the latest
  standalone render and should not be used as an artifact of a specific
  campaign.
- **The preview shown to the user is the MCP App widget + fallback link before
  save, and the editor canvas after save.** If preview hasn't been called since
  the last edit, don't present the old link as current: mark it stale and offer
  to refresh it.
- **Never hand-assemble the email's HTML/preview.** Don't produce an
  approximate HTML, even if the backend is temporarily unavailable: fix the
  cause, or report the status.
- **QA/debug is a separate capability, not part of a routine edit.** If the user
  asks to check the email, asks for PNG/mobile/desktop, or talks about specific
  text, a link, an image, cropping, responsiveness, or other rendering — that's
  already a diagnostics request: call an HTML preview of the current JSX, show
  the link/widget, download the HTML if needed, and call the MCP PNG preview for
  PNG. Don't ask a separate question about whether it's OK to open the
  HTML/get a PNG.
- **A routine edit without QA:** after changing the JSX, just write that the
  previous preview is stale and offer to show a new one. If the user doesn't ask
  for preview/QA, don't call `visual_template_preview`, don't download HTML, and
  don't request a PNG.
- **Before save**, show the exact target, the change, and the preview's
  freshness status. If there's no fresh preview, say explicitly: "The preview
  hasn't been refreshed since the last edit; I can save without a new preview or
  show it first." A save confirmation is valid only after this warning.

  Example of a routine post-edit message:

  ```text
  The change is ready. The previous preview no longer matches the current version.
  I can show you a new preview in the panel if you'd like. I can also run a full
  check with HTML and desktop/mobile PNG links.
  ```

  Example of a write confirmation without a fresh preview:

  ```text
  Campaign: <name>
  Format: Active
  Change: <brief>
  Preview: not refreshed since the last edit.
  Choose: 1) show a new preview; 2) run a full QA with HTML and PNG;
  3) save without a new preview.
  ```

  After option 1 or 2, report the result and ask for save confirmation
  separately; preview/QA never implies consent to write. HTML QA reads the
  downloaded file selectively and checks the expected text, links, images,
  personalization/unsubscribe, and obvious escaping/structure issues against the
  user's request. Don't read the entire HTML into the model's context
  unnecessarily. In the preview HTML, `${Message.UnsubscribeLink}` may remain a
  literal string until send: don't treat this as a defect, and don't replace it
  with a fake URL. PNG QA uses the MCP desktop/mobile links and visually checks
  content, cropping, the responsive branch, and image loading. This is
  best-effort QA, not a full Outlook/Gmail compatibility test.
- **PNG preview is provided by MCP.** When PNG/mobile/desktop is requested, call
  the MCP PNG preview tool for the current JSX. This is a separate MCP function,
  analogous to HTML preview: it returns temporary links to PNG files — desktop
  and mobile. Don't use a local screenshot as the standard path: the standard
  source for PNGs is the MCP preview links. The exception is the Cowork fallback
  below, if MCP PNG preview is unavailable or returns no links.
  If the user asks for only mobile or only desktop, you can show just that
  link; for a full responsive diagnosis, show both. Take field names in the
  response from the actual MCP tool output; when talking to the user, call them
  the "desktop snapshot" and the "mobile snapshot."
- **Fallback if MCP doesn't return a PNG.** If MCP PNG preview is unavailable,
  returns an error, or returns no links, and the user still needs a visual
  check, in Cowork you can use Claude in Chrome as an emergency fallback to
  view/capture the HTML preview. Tell the user explicitly that this is a
  fallback, not the standard MCP PNG. Don't fall back to the removed legacy path
  through local PNG scripts.
- **How to use the PNG links.** Show the user the desktop/mobile PNG links and
  use them for a visual check if the current host allows opening/viewing
  images. If the host can't render a PNG from a link, say plainly that the PNGs
  were obtained but an agent-side visual check isn't available in this
  environment; the user can open the links themselves.
- **Diagnosing a follow-up complaint.** If the user reports a content/rendering
  problem in a generated campaign, get the current JSX, call a fresh HTML
  preview, download the HTML only if you need to check HTML fragments; for a
  visual/responsive problem, also call the MCP PNG preview and check the
  desktop/mobile PNG links. Only use existing local HTML if it's provably fresh
  for the same JSX.

If additional QA finds a defect and the Generator changes the JSX, the previous
`htmlUrl`, MCP App widget, local HTML, and PNG links no longer prove the state of
the new JSX. Mark the preview as stale. If the user continues QA/debug, repeat the
HTML preview, the needed HTML download, and/or the MCP PNG preview; if not, just
offer to refresh the preview.

Don't edit the JSX yourself — run preview/QA only per this policy, keep the
artifacts, and carry out save.
