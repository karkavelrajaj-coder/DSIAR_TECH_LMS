"""Generates a certificate PNG on the fly — direct port of
utils/certificate_image.py. Fonts and logo are read from this backend's own
assets/ folder (bundled into the Docker image / repo), same pattern as the
Streamlit app: no HTTP fetch, so it works regardless of repo visibility.
"""

import io
import os
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(BACKEND_ROOT, "assets", "fonts")

LOGO_PATH = os.path.join(BACKEND_ROOT, "assets", "dsiar-logo.png")
SIGNATURE_PATH = os.path.join(BACKEND_ROOT, "assets", "signature.png")
SIGNER_NAME = "D'siar Tech"
SIGNER_TITLE = "Authorized Signatory"

WIDTH, HEIGHT = 1754, 1240
NAVY = (20, 36, 71)
GOLD = (188, 145, 60)
GRAY = (120, 120, 120)
LIGHT_GOLD = (232, 214, 174)


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
        img = img.resize((max_width, int(img.height * ratio)))
        return img
    except Exception:
        return None


def build_certificate(student_name: str, course_title: str, cert_id: str, issued_at: datetime) -> bytes:
    img = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    outer = 36
    draw.rectangle([outer, outer, WIDTH - outer, HEIGHT - outer], outline=GOLD, width=5)
    inner = 58
    draw.rectangle([inner, inner, WIDTH - inner, HEIGHT - inner], outline=LIGHT_GOLD, width=1)
    tick = 34
    for cx, cy, dx, dy in [(inner, inner, 1, 1), (WIDTH - inner, inner, -1, 1),
                            (inner, HEIGHT - inner, 1, -1), (WIDTH - inner, HEIGHT - inner, -1, -1)]:
        draw.line([(cx, cy + dy * tick), (cx, cy), (cx + dx * tick, cy)], fill=GOLD, width=3)

    content_w = WIDTH - 2 * inner

    y = 90
    logo = _load_local_image(LOGO_PATH, max_width=150)
    if logo:
        img.paste(logo, (int((WIDTH - logo.width) / 2), y), logo)
        y += logo.height + 34
    else:
        _center_text(draw, y, "D'SIAR TECH", _playfair(46, 700), NAVY)
        y += 80

    _center_text(draw, y, "CERTIFICATE OF COMPLETION", _playfair(46, 700), NAVY)
    y += 78

    div_w = 220
    draw.line([((WIDTH - div_w) / 2, y), ((WIDTH + div_w) / 2, y)], fill=GOLD, width=3)
    y += 56

    _center_text(draw, y, "This certifies that", _lato(26), GRAY)
    y += 62

    _center_text(draw, y, student_name, _playfair(64, 700), GOLD)
    y += 96

    _center_text(draw, y, "has successfully completed the course", _lato(26), GRAY)
    y += 62

    course_font = _playfair(40, 700)
    bbox = draw.textbbox((0, 0), course_title, font=course_font)
    if bbox[2] - bbox[0] > content_w - 80:
        course_font = _playfair(32, 700)
    _center_text(draw, y, course_title, course_font, NAVY)
    y += 90

    div_w2 = 150
    draw.line([((WIDTH - div_w2) / 2, y), ((WIDTH + div_w2) / 2, y)], fill=GOLD, width=2)
    y += 50

    date_str = issued_at.strftime("%B %d, %Y")
    _center_text(draw, y, f"Issued on {date_str}", _lato(23), GRAY)

    footer_y = HEIGHT - inner - 130

    draw.text((inner + 50, footer_y + 90), f"Certificate ID: {cert_id}", font=_lato(18), fill=GRAY)

    sig_block_w = 380
    sig_x = WIDTH - inner - 50 - sig_block_w
    signature_img = _load_local_image(SIGNATURE_PATH, max_width=sig_block_w)
    if signature_img:
        img.paste(signature_img, (sig_x + int((sig_block_w - signature_img.width) / 2), footer_y - 10), signature_img)
    else:
        sig_text_w = draw.textbbox((0, 0), SIGNER_NAME, font=_script(48))[2]
        draw.text((sig_x + (sig_block_w - sig_text_w) / 2, footer_y - 20), SIGNER_NAME, font=_script(48), fill=NAVY)

    draw.line([(sig_x, footer_y + 62), (sig_x + sig_block_w, footer_y + 62)], fill=NAVY, width=2)
    title_w = draw.textbbox((0, 0), SIGNER_TITLE, font=_lato(18))[2]
    draw.text((sig_x + (sig_block_w - title_w) / 2, footer_y + 74), SIGNER_TITLE, font=_lato(18), fill=GRAY)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
