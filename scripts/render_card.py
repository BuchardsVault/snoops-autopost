"""Render a quote as an X-style tweet screenshot (1080x1350 JPEG, 4:5).

Usage:
  python scripts/render_card.py --text "quote" --out docs/cards/x.jpg [--theme dark|light]
Config (display name, handle, avatar, verified, theme) lives in config.json.
"""
import argparse
import json
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_REG = os.path.join(ROOT, "assets/fonts/Inter-Regular.otf")
FONT_BOLD = os.path.join(ROOT, "assets/fonts/Inter-Bold.otf")

W, H = 1080, 1350
THEMES = {
    "dark": {"bg": (0, 0, 0), "text": (231, 233, 234), "muted": (113, 118, 123)},
    "light": {"bg": (255, 255, 255), "text": (15, 20, 25), "muted": (83, 100, 113)},
}
X_BLUE = (29, 155, 240)


def load_config():
    with open(os.path.join(ROOT, "config.json")) as f:
        return json.load(f)


def wrap(draw, text, font, max_w):
    lines = []
    for para in text.split("\n"):
        words, line = para.split(), ""
        for w in words:
            trial = f"{line} {w}".strip()
            if draw.textlength(trial, font=font) <= max_w:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = w
        lines.append(line)
    return lines


def avatar(cfg, size, theme):
    path = os.path.join(ROOT, cfg.get("avatar", "assets/avatar.png"))
    if os.path.exists(path):
        img = Image.open(path).convert("RGB")
        side = min(img.size)  # center-crop to square so non-square photos aren't squashed
        left, top = (img.width - side) // 2, (img.height - side) // 2
        img = img.crop((left, top, left + side, top + side)).resize((size, size), Image.LANCZOS)
    else:  # placeholder: initials on a gray circle
        img = Image.new("RGB", (size, size), (51, 54, 57) if theme == "dark" else (207, 217, 222))
        d = ImageDraw.Draw(img)
        f = ImageFont.truetype(FONT_BOLD, size // 3)
        initials = "".join(p[0] for p in cfg["display_name"].split()[:2]).upper() or "S"
        d.text((size / 2, size / 2), initials, font=f, fill=(255, 255, 255), anchor="mm")
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    return img, mask


def draw_verified(draw, x, y, s):
    # simple blue badge with a white check
    draw.ellipse((x, y, x + s, y + s), fill=X_BLUE)
    draw.line([(x + s * .28, y + s * .52), (x + s * .44, y + s * .68), (x + s * .74, y + s * .34)],
              fill=(255, 255, 255), width=max(3, s // 8), joint="curve")


def render(text, out, theme=None):
    cfg = load_config()
    theme = theme or cfg.get("theme", "dark")
    c = THEMES[theme]
    img = Image.new("RGB", (W, H), c["bg"])
    d = ImageDraw.Draw(img)

    margin = 90
    max_w = W - 2 * margin
    # shrink font until text block fits comfortably
    for size in range(62, 33, -2):
        body = ImageFont.truetype(FONT_REG, size)
        lines = wrap(d, text, body, max_w)
        line_h = int(size * 1.32)
        if len(lines) * line_h <= 700:
            break

    av = 120
    header_h = av
    gap = 48
    block_h = header_h + gap + len(lines) * line_h
    top = (H - block_h) // 2

    a_img, a_mask = avatar(cfg, av, theme)
    img.paste(a_img, (margin, top), a_mask)

    name_f = ImageFont.truetype(FONT_BOLD, 40)
    handle_f = ImageFont.truetype(FONT_REG, 36)
    nx = margin + av + 28
    d.text((nx, top + 18), cfg["display_name"], font=name_f, fill=c["text"])
    if cfg.get("verified"):
        draw_verified(d, nx + d.textlength(cfg["display_name"], font=name_f) + 10, top + 22, 38)
    d.text((nx, top + 70), "@" + cfg["handle"], font=handle_f, fill=c["muted"])

    y = top + header_h + gap
    for ln in lines:
        d.text((margin, y), ln, font=body, fill=c["text"])
        y += line_h

    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    img.save(out, "JPEG", quality=92)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--theme", choices=["dark", "light"])
    a = ap.parse_args()
    print(render(a.text, a.out, a.theme))
