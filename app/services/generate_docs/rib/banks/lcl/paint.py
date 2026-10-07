"""Helpers dessin LCL : Verdana fill-only + crénage TTF, filets Skia."""

from fontTools.ttLib import TTFont
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth

from app.services.generate_docs.common.paths import FONTS_DIR, LOGOS_DIR

from . import layout


def _kern_pairs(filename: str):
    font = TTFont(str(FONTS_DIR / filename))
    upem = float(font["head"].unitsPerEm)
    raw = {}
    if "kern" in font:
        for sub in font["kern"].kernTables:
            raw.update(sub.kernTable)
    names = {}
    for code, glyph in (font.getBestCmap() or {}).items():
        names.setdefault(glyph, []).append(chr(code))
    pairs = {}
    for (left, right), units in raw.items():
        for a in names.get(left, ()):
            inner = pairs.setdefault(a, {})
            for b in names.get(right, ()):
                inner[b] = units
    return upem, pairs


_KERN = {
    layout.FONT: _kern_pairs(layout.FONT_FILE),
    layout.FONT_BOLD: _kern_pairs(layout.FONT_BOLD_FILE),
}


def _kern_pt(font: str, a: str, b: str, size: float) -> float:
    packed = _KERN.get(font)
    if not packed:
        return 0.0
    upem, pairs = packed
    units = pairs.get(a, {}).get(b)
    if not units:
        return 0.0
    return units * size / upem


def y_up(y_top: float) -> float:
    return round(layout.PAGE_H - y_top, 2)


def fill(c, hex_color: str):
    color = HexColor(hex_color)
    c.setFillColor(color)
    c.setStrokeColor(color)


def width(text, font, size) -> float:
    text = text or ""
    total = 0.0
    n = len(text)
    for i, ch in enumerate(text):
        total += stringWidth(ch, font, size)
        if i + 1 < n:
            total += _kern_pt(font, ch, text[i + 1], size)
    return total


def clip(text, font, size, max_width):
    text = text or ""
    if max_width is None or width(text, font, size) <= max_width:
        return text
    while text and width(text, font, size) > max_width:
        text = text[:-1]
    return text


def draw_string(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None,
):
    """Crénage table kern Verdana, mêmes advances que le gabarit."""
    text = clip(text, font, size, max_width)
    if not text:
        return
    y = y_up(y_origin)
    c.setFont(font, size)
    cursor = x
    n = len(text)
    for i, ch in enumerate(text):
        c.drawString(cursor, y, ch, mode=0)
        cursor += stringWidth(ch, font, size)
        if i + 1 < n:
            cursor += _kern_pt(font, ch, text[i + 1], size)


def wrap_lines(text: str, font: str, size: float, max_width: float) -> list[str]:
    lines = []
    current = ""
    for word in (text or "").split():
        trial = word if not current else f"{current} {word}"
        if width(trial, font, size) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def draw_centered(
    c, x0: float, x1: float, y_origin: float, text: str, font: str, size: float,
):
    text = clip(text, font, size, x1 - x0)
    if not text:
        return
    x = round(x0 + (x1 - x0 - width(text, font, size)) / 2.0, 2)
    draw_string(c, x, y_origin, text, font, size)


def fill_rect(c, x0: float, y0: float, x1: float, y1: float, hex_color: str):
    c.saveState()
    c.setFillColor(HexColor(hex_color))
    c.setLineWidth(0)
    top, bot = min(y0, y1), max(y0, y1)
    left, right = min(x0, x1), max(x0, x1)
    c.rect(left, y_up(bot), right - left, bot - top, stroke=0, fill=1)
    c.restoreState()


def fill_poly(c, points, hex_color: str):
    c.saveState()
    c.setFillColor(HexColor(hex_color))
    c.setLineWidth(0)
    p = c.beginPath()
    x, y = points[0]
    p.moveTo(x, y_up(y))
    for x, y in points[1:]:
        p.lineTo(x, y_up(y))
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()


def dashed_rule(
    c, x0: float, x1: float, y: float, h: float, on: float, gap: float,
    hex_color: str, clip_x1=None,
):
    """Tiret entier même s'il dépasse ; le clip raccourcit comme le gabarit."""
    limit = x1 if clip_x1 is None else clip_x1
    c.saveState()
    clip_path = c.beginPath()
    clip_path.rect(x0, y_up(y + 1.0), max(limit - x0, 0), 1.0)
    c.clipPath(clip_path, stroke=0, fill=0)
    fill_rect(c, x0, y, x1, y + 1.0, "#FFFFFF")
    c.setFillColor(HexColor(hex_color))
    c.setLineWidth(0)
    p = c.beginPath()
    yu, yv = y_up(y), y_up(y + h)
    x = x0
    while x < limit - 1e-6:
        end = x + on
        p.moveTo(x, yu)
        p.lineTo(end, yu)
        p.lineTo(end, yv)
        p.lineTo(x, yv)
        x += on + gap
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()


def bevel_box(c, x0: float, y0: float, x1: float, y1: float, t: float, dy=0, dy1=None):
    """Sombre = rects. Clair = chemins biseautés du gabarit Skia (pas un 2e trait)."""
    if dy1 is None:
        dy1 = dy
    y0, y1 = y0 + dy, y1 + dy1
    fill_rect(c, x0, y0, x1, y0 + t, layout.BEVEL_DARK)
    fill_rect(c, x0, y0, x0 + t, y1, layout.BEVEL_DARK)
    fill_poly(
        c,
        ((x0 + t, y1 - t), (x0, y1), (x1, y1), (x1, y1 - t)),
        layout.BEVEL_LIGHT,
    )
    fill_poly(
        c,
        ((x1 - t, y0 + t), (x1 - t, y1), (x1, y1), (x1, y0)),
        layout.BEVEL_LIGHT,
    )


def draw_image(c, filename: str, x: float, y_top: float, w: float, h: float, mask=None):
    c.drawImage(
        str(LOGOS_DIR / filename),
        x, y_up(y_top + h),
        width=w, height=h, mask=mask,
    )
