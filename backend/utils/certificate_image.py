"""Generates a certificate PNG on the fly — direct port of
utils/certificate_image.py. Fonts and logo are read from this backend's own
assets/ folder (bundled into the Docker image / repo), same pattern as the
Streamlit app: no HTTP fetch, so it works regardless of repo visibility.
"""

import io
import os
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

from utils.tracks import track_meta

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(BACKEND_ROOT, "assets", "fonts")

LOGO_PATH = os.path.join(BACKEND_ROOT, "assets", "dsiar-logo.png")
SIGNATURE_PATH = os.path.join(BACKEND_ROOT, "assets", "signature.png")
MSME_LOGO_PATH = os.path.join(BACKEND_ROOT, "assets", "msme-logo.png")
SIGNER_NAME = "D'siar Tech"
SIGNER_TITLE = "Authorized Signatory"

WIDTH, HEIGHT = 1754, 1240
INK_900 = (17, 24, 39)
INK_500 = (107, 114, 128)
WHITE = (255, 255, 255)


def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _tint(rgb, amount: float) -> tuple[int, int, int]:
    """Lighten a color toward white by `amount` (0-1) — used for the inner
    border/flourish (0.86) and the very subtle corner wash (0.93)."""
    return tuple(int(c + (255 - c) * amount) for c in rgb)


def _playfair(size, weight=400):
    f = ImageFont.truetype(os.path.join(FONT_DIR, "PlayfairDisplay-Variable.ttf"), size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def _lato(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "Lato-Regular.ttf"), size)


def _script(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "GreatVibes-Regular.ttf"), size)


def _center_text(draw, y, text, font, fill, canvas_width=WIDTH):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((canvas_width - w) / 2, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def _load_local_image(path, max_width):
    try:
        if not os.path.isfile(path):
            return None
        img = Image.open(path).convert("RGBA")
        ratio = max_width / img.width
        return img.resize((max_width, int(img.height * ratio)))
    except Exception:
        return None


def _load_local_image_by_height(path, target_height):
    try:
        if not os.path.isfile(path):
            return None
        img = Image.open(path).convert("RGBA")
        ratio = target_height / img.height
        return img.resize((int(img.width * ratio), target_height))
    except Exception:
        return None


def _diamond(draw, cx, cy, r, fill):
    draw.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=fill)


def build_certificate(student_name: str, course_title: str, cert_id: str, issued_at: datetime, track: str = "course") -> bytes:
    meta = track_meta(track)
    accent = _hex_to_rgb(meta["accent"])
    accent_900 = tuple(int(c * 0.62) for c in accent)  # darker shade — corner brackets, signature
    accent_100 = _tint(accent, 0.86)                    # light tint — inner border, flourish rules
    wash_color = _tint(accent, 0.93)                    # very subtle corner wash

    img = Image.new("RGB", (WIDTH, HEIGHT), WHITE)

    # Subtle accent-tinted wash in two opposite corners — adds depth without noise.
    wash = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    wash_draw = ImageDraw.Draw(wash)
    wash_draw.ellipse([-260, -260, 340, 340], fill=wash_color + (255,))
    wash_draw.ellipse([WIDTH - 340, HEIGHT - 340, WIDTH + 260, HEIGHT + 260], fill=wash_color + (255,))
    img.paste(Image.alpha_composite(img.convert("RGBA"), wash).convert("RGB"), (0, 0))

    draw = ImageDraw.Draw(img)

    outer = 40
    draw.rectangle([outer, outer, WIDTH - outer, HEIGHT - outer], outline=accent, width=4)
    inner = 60
    draw.rectangle([inner, inner, WIDTH - inner, HEIGHT - inner], outline=accent_100, width=1)

    tick = 42
    for cx, cy, dx, dy in [(inner, inner, 1, 1), (WIDTH - inner, inner, -1, 1),
                            (inner, HEIGHT - inner, 1, -1), (WIDTH - inner, HEIGHT - inner, -1, -1)]:
        draw.line([(cx, cy + dy * tick), (cx, cy), (cx + dx * tick, cy)], fill=accent_900, width=4)

    content_w = WIDTH - 2 * inner
    y = 92

    logo = _load_local_image(LOGO_PATH, max_width=150)
    if logo:
        img.paste(logo, (int((WIDTH - logo.width) / 2), y), logo)
        y += logo.height + 30
    else:
        _center_text(draw, y, "D'SIAR TECH", _playfair(46, 700), accent_900)
        y += 80

    _center_text(draw, y, meta["cert_heading"], _playfair(50, 700), accent_900)
    y += 80

    div_w = 220
    draw.line([((WIDTH - div_w) / 2, y), ((WIDTH + div_w) / 2, y)], fill=accent, width=3)
    y += 64

    _center_text(draw, y, "This certifies that", _lato(27), INK_500)
    y += 66

    _center_text(draw, y, student_name, _playfair(80, 700), accent)
    y += 116

    _center_text(draw, y, meta["cert_body"], _lato(27), INK_500)
    y += 66

    course_font = _playfair(46, 700)
    bbox = draw.textbbox((0, 0), course_title, font=course_font)
    if bbox[2] - bbox[0] > content_w - 80:
        course_font = _playfair(36, 700)
    _center_text(draw, y, course_title, course_font, INK_900)
    y += 100

    div_w2 = 150
    draw.line([((WIDTH - div_w2) / 2, y), ((WIDTH + div_w2) / 2, y)], fill=accent, width=2)
    y += 54

    date_str = issued_at.strftime("%B %d, %Y")
    _center_text(draw, y, f"Issued on {date_str}", _lato(24), INK_500)
    y += 70

    # Flourish: rule - diamond - diamond(bigger) - diamond - rule, centered.
    # Fills the gap before the footer with something intentional-looking
    # instead of empty space, without needing any extra image asset.
    flourish_w = 260
    fx0, fx1 = (WIDTH - flourish_w) / 2, (WIDTH + flourish_w) / 2
    draw.line([(fx0, y), (fx0 + 70, y)], fill=accent_100, width=2)
    draw.line([(fx1 - 70, y), (fx1, y)], fill=accent_100, width=2)
    _diamond(draw, fx0 + 70 + 24, y, 5, accent)
    _diamond(draw, (fx0 + fx1) / 2, y, 8, accent)
    _diamond(draw, fx1 - 70 - 24, y, 5, accent)

    footer_y = HEIGHT - inner - 150

    # --- Footer left: Certificate ID + MSME trust mark (small, quiet) ------
    # Kept clear of the corner bracket (which spans roughly x=[60,102],
    # y=[1138,1180]) and well above the inner border.
    footer_left_x = inner + 100
    draw.text((footer_left_x, footer_y + 44), f"Certificate ID: {cert_id}", font=_lato(18), fill=INK_500)

    msme_logo = _load_local_image_by_height(MSME_LOGO_PATH, target_height=40)
    if msme_logo:
        msme_y = footer_y + 44 + 30
        img.paste(msme_logo, (footer_left_x, msme_y), msme_logo)
        draw.text((footer_left_x + msme_logo.width + 14, msme_y + msme_logo.height // 2 - 16),
                   "MSME", font=_lato(14), fill=INK_500)
        draw.text((footer_left_x + msme_logo.width + 14, msme_y + msme_logo.height // 2 - 1),
                   "Registered", font=_lato(14), fill=INK_500)

    # --- Footer right: signature block -------------------------------------
    sig_block_w = 380
    sig_x = WIDTH - inner - 50 - sig_block_w
    signature_img = _load_local_image(SIGNATURE_PATH, max_width=sig_block_w)
    if signature_img:
        img.paste(signature_img, (sig_x + int((sig_block_w - signature_img.width) / 2), footer_y - 26), signature_img)
    else:
        sig_text_w = draw.textbbox((0, 0), SIGNER_NAME, font=_script(56))[2]
        draw.text((sig_x + (sig_block_w - sig_text_w) / 2, footer_y - 26), SIGNER_NAME, font=_script(56), fill=accent_900)

    draw.line([(sig_x, footer_y + 62), (sig_x + sig_block_w, footer_y + 62)], fill=accent_900, width=2)
    title_w = draw.textbbox((0, 0), SIGNER_TITLE, font=_lato(18))[2]
    draw.text((sig_x + (sig_block_w - title_w) / 2, footer_y + 74), SIGNER_TITLE, font=_lato(18), fill=INK_500)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
