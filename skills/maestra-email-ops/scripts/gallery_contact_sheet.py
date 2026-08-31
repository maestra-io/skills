#!/usr/bin/env python3
"""
Contact sheet from the Maestra gallery with images embedded as base64.

Why: an artifact/widget in the Cowork side panel renders in a sandbox with CSP,
external domains are blocked, so <img src="https://..."> won't load there.
Solution: download, downscale if needed, and embed thumbnails as data: URLs.

Input  — a JSON list [{"name","fileExtension","isSystem","url"}, ...]
          exactly as returned by MCP gallery_images_list.
Output — self-contained HTML with no external requests.

Usage:
    python3 gallery_contact_sheet.py images.json out.html [--max-px 96] [--quality 80]

The base64/data URLs in the result are for the preview contact sheet only.
Always use the original url from the input JSON in email JSX.
"""

import argparse
import base64
import html
import io
import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

try:
    from PIL import Image
except ImportError:
    print(
        "Pillow is not installed: self-contained contact sheet unavailable. "
        "Install Pillow in the sandbox or use the remote HTML fallback.",
        file=sys.stderr,
    )
    sys.exit(2)


MAX_EMBED_BYTES = 60_000  # if the data URL is still bigger than this after resizing — compress harder


def fetch(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def to_data_url(raw: bytes, max_px: int, quality: int) -> tuple[str, str]:
    """Returns (data_url, note). Animated GIFs are not recompressed."""
    try:
        im = Image.open(io.BytesIO(raw))
    except Exception as e:
        raise RuntimeError(f"not an image: {e}")

    is_animated = getattr(im, "is_animated", False)
    if is_animated:
        b64 = base64.b64encode(raw).decode()
        return f"data:image/gif;base64,{b64}", f"animated gif, {len(raw) // 1024} KB"

    orig = im.size
    if max(orig) > max_px:
        im.thumbnail((max_px, max_px), Image.LANCZOS)

    # keep PNGs with transparency as PNG, everything else becomes JPEG (smaller)
    has_alpha = im.mode in ("RGBA", "LA", "P") and (
        "transparency" in im.info or im.mode in ("RGBA", "LA")
    )
    buf = io.BytesIO()
    if has_alpha:
        im.convert("RGBA").save(buf, format="PNG", optimize=True)
        mime = "image/png"
    else:
        im.convert("RGB").save(buf, format="JPEG", quality=quality, optimize=True)
        mime = "image/jpeg"
    data = buf.getvalue()

    # second pass if it's still heavy
    if len(data) > MAX_EMBED_BYTES:
        im2 = im.copy()
        im2.thumbnail((max(48, max_px // 2), max(48, max_px // 2)), Image.LANCZOS)
        buf = io.BytesIO()
        if has_alpha:
            im2.convert("RGBA").save(buf, format="PNG", optimize=True)
        else:
            im2.convert("RGB").save(buf, format="JPEG", quality=60, optimize=True)
        data = buf.getvalue()

    b64 = base64.b64encode(data).decode()
    note = f"{orig[0]}×{orig[1]} → {im.size[0]}×{im.size[1]}, {len(data) // 1024 or 1} KB"
    return f"data:{mime};base64,{b64}", note


def file_name(item: dict) -> str:
    name, ext = item.get("name", ""), item.get("fileExtension", "")
    return name if name.endswith(ext) else name + ext


def process(idx_item, max_px, quality):
    idx, item = idx_item
    row = {
        "n": idx,
        "fileName": file_name(item),
        "url": item["url"],
        "isSystem": bool(item.get("isSystem")),
        "data_url": None,
        "note": "",
    }
    try:
        row["data_url"], row["note"] = to_data_url(fetch(item["url"]), max_px, quality)
    except Exception as e:
        row["note"] = f"error: {e}"
    return row


CSS = """:root { color-scheme: light }
body{margin:24px;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;background:#f6f7f9;color:#202124}
h1{margin:0 0 8px;font-size:22px;font-weight:500}
.hint{margin:0 0 20px;color:#666;font-size:14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:16px}
.card{background:#fff;border:1px solid #dde1e6;border-radius:12px;padding:12px}
.thumb{display:flex;align-items:center;justify-content:center;height:120px;border-radius:8px;
 background:linear-gradient(45deg,#eee 25%,transparent 25%),linear-gradient(-45deg,#eee 25%,transparent 25%),
 linear-gradient(45deg,transparent 75%,#eee 75%),linear-gradient(-45deg,transparent 75%,#eee 75%);
 background-size:18px 18px;background-position:0 0,0 9px,9px -9px,-9px 0;margin-bottom:10px}
.thumb img{max-width:96px;max-height:96px;object-fit:contain}
.num{display:inline-block;min-width:28px;font-weight:500;color:#3f6bff}
.name{font-size:13px;line-height:1.25;word-break:break-word}
.meta{margin-top:6px;font-size:12px;color:#667085}
.err{color:#a32d2d}"""


def build_html(rows, title):
    cards = []
    for r in rows:
        escaped_name = html.escape(r["fileName"])
        if r["data_url"]:
            img = f'<img src="{r["data_url"]}" alt="{escaped_name}">'
        else:
            img = '<span class="meta err">failed to load</span>'
        src = "system icon" if r["isSystem"] else "project asset"
        note = html.escape(r["note"])
        cards.append(
            f'<article class="card"><div class="thumb">{img}</div>'
            f'<div class="name"><span class="num">#{r["n"]}</span> {escaped_name}</div>'
            f'<div class="meta">{src} · {note}</div></article>'
        )
    escaped_title = html.escape(title)
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f"<title>{escaped_title}</title><style>{CSS}</style></head><body>"
        f"<h1>{escaped_title}</h1>"
        '<p class="hint">Images are embedded in the file as base64 (downscaled previews), '
        "so the HTML works with no network access — including in the side panel. "
        "The original URLs from the gallery are unchanged and are in the JSON output.</p>"
        f'<main class="grid">{"".join(cards)}</main></body></html>'
    )


def load_items(path: str):
    with open(path, encoding="utf-8") as f:
        items = json.load(f)
    if isinstance(items, dict):
        items = items.get("images") or items.get("items") or []
    if not isinstance(items, list):
        raise RuntimeError("images_json must be a JSON list or an object with images/items")
    return items


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("images_json")
    p.add_argument("out_html")
    p.add_argument("--max-px", type=int, default=96)
    p.add_argument("--quality", type=int, default=80)
    p.add_argument("--title", default="Maestra gallery preview")
    args = p.parse_args()

    items = load_items(args.images_json)
    os.makedirs(os.path.dirname(os.path.abspath(args.out_html)), exist_ok=True)

    with ThreadPoolExecutor(max_workers=8) as ex:
        rows = list(
            ex.map(
                lambda x: process(x, args.max_px, args.quality),
                enumerate(items, start=1),
            )
        )

    html_text = build_html(rows, args.title)
    with open(args.out_html, "w", encoding="utf-8") as f:
        f.write(html_text)

    ok = sum(1 for r in rows if r["data_url"])
    print(f"{ok}/{len(rows)} embedded, HTML {len(html_text) // 1024} KB -> {args.out_html}")
    for r in rows:
        if not r["data_url"]:
            print(f"  #{r['n']} {r['fileName']}: {r['note']}", file=sys.stderr)


if __name__ == "__main__":
    main()
