"""Helpers dessin (Y ReportLab depuis le haut PyMuPDF)."""

from functools import lru_cache

from fontTools.ttLib import TTFont
from PIL import Image
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

from app.services.generate_docs.common.pdf_image import draw_indexed_html
from app.services.generate_docs.common.paths import FONTS_DIR, LOGOS_DIR

from . import layout, logo_stream


def _pdf_num(value):
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return ("%.10f" % value).rstrip("0").rstrip(".")


@lru_cache(maxsize=16)
def _image(path: str) -> ImageReader:
    im = Image.open(path)
    if im.mode == "RGBA":
        red, green, blue, alpha = im.split()
        reader = ImageReader(Image.merge("RGB", (red, green, blue)))
        reader.getRGBData()
        reader._dataA = ImageReader(alpha)
        return reader
    return ImageReader(im)


def y_up(y_top: float) -> float:
    return layout.PAGE_H - y_top


def to_color(color):
    if isinstance(color, Color):
        return color
    if isinstance(color, str):
        return HexColor(color)
    if isinstance(color, (int, float)):
        return Color(color, color, color)
    r, g, b = color[0], color[1], color[2]
    alpha = color[3] if len(color) > 3 else 1
    return Color(r, g, b, alpha=alpha)


def fill(c, color):
    c.setFillColor(to_color(color))


def stroke(c, color):
    c.setStrokeColor(to_color(color))


@lru_cache(maxsize=4)
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


def width(text, font, size) -> float:
    return stringWidth(text or "", font, size)


def kerned_width(text, font, size) -> float:
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
    text = clip(text, font, size, max_width)
    if not text:
        return
    c.setFont(font, size)
    c.drawString(x, y_up(y_origin), text)


def draw_right(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None,
):
    text = clip(text, font, size, max_width)
    if not text:
        return
    c.setFont(font, size)
    c.drawRightString(x, y_up(y_origin), text)


def draw_center(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None,
):
    text = clip(text, font, size, max_width)
    if not text:
        return
    c.setFont(font, size)
    c.drawCentredString(x, y_up(y_origin), text)


def _clip_kerned(text, font, size, max_width):
    text = text or ""
    if max_width is None or kerned_width(text, font, size) <= max_width:
        return text
    while text and kerned_width(text, font, size) > max_width:
        text = text[:-1]
    return text


def draw_kerned(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None,
):
    """Crénage table kern Arial (TJ du gabarit), pas de Tc global."""
    text = _clip_kerned(text, font, size, max_width)
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


def draw_center_kerned(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None,
):
    text = _clip_kerned(text, font, size, max_width)
    if not text:
        return
    draw_kerned(
        c, x - kerned_width(text, font, size) / 2.0, y_origin,
        text, font, size,
    )


def fill_rect(c, x0: float, y0: float, x1: float, y1: float, color):
    c.saveState()
    c.setFillColor(to_color(color))
    top, bot = min(y0, y1), max(y0, y1)
    left, right = min(x0, x1), max(x0, x1)
    c.rect(left, y_up(bot), right - left, bot - top, stroke=0, fill=1)
    c.restoreState()


def stroke_line(
    c, x0: float, y0: float, x1: float, y1: float,
    line_w: float, color, cap: int = 0,
):
    c.saveState()
    c.setStrokeColor(to_color(color))
    c.setLineWidth(line_w)
    c.setLineCap(cap)
    c.setLineJoin(0)
    c.setDash([], 0)
    c.line(x0, y_up(y0), x1, y_up(y1))
    c.restoreState()


def html_frame(c, x: float, y_down: float):
    """Repère PDF4NET : Y vers le bas, origine coin haut-gauche de la page."""
    c.translate(0, layout.PAGE_H)
    c.scale(1, -1)
    c.translate(x, y_down)


def stroke_html_border(c, sides, line_w, color):
    """Quatre bords clippés du gabarit (coords locales HTML)."""
    stroke(c, color)
    for clip_pts, start, end in sides:
        c.saveState()
        x0, y0 = clip_pts[0]
        c._code.append("%s %s m" % (_pdf_num(x0), _pdf_num(y0)))
        for x, y in clip_pts[1:]:
            c._code.append("%s %s l" % (_pdf_num(x), _pdf_num(y)))
        c._code.append("h")
        c._code.append("W")
        c._code.append("n")
        c.setLineWidth(line_w)
        c.setLineCap(0)
        c.setLineJoin(0)
        c.setDash([], 0)
        c._code.append("%s %s m" % (_pdf_num(start[0]), _pdf_num(start[1])))
        c._code.append("%s %s l" % (_pdf_num(end[0]), _pdf_num(end[1])))
        c._code.append("S")
        c.restoreState()


def fill_html_rect(c, x: float, y: float, w: float, h: float, color):
    """Rectangle dans le repère html_frame (Y vers le bas)."""
    fill(c, color)
    c.rect(x, y, w, h, stroke=0, fill=1)


def draw_string_html(c, tm_x: float, tm_y: float, text: str, font: str, size: float):
    """Tm 1 0 0 -1 comme PDF4NET, dans le repère html_frame courant."""
    if not text:
        return
    t = c.beginText()
    t.setFont(font, size)
    t.setTextTransform(1, 0, 0, -1, tm_x, tm_y)
    t.textOut(text)
    c.drawText(t)


def draw_kerned_html(
    c, tm_x: float, tm_y: float, text: str, font: str, size: float,
    max_width=None,
):
    text = _clip_kerned(text, font, size, max_width)
    if not text:
        return
    cursor = tm_x
    n = len(text)
    for i, ch in enumerate(text):
        draw_string_html(c, cursor, tm_y, ch, font, size)
        cursor += stringWidth(ch, font, size)
        if i + 1 < n:
            cursor += _kern_pt(font, ch, text[i + 1], size)


def html_center_x(col_w: float, text: str, font: str, size: float) -> float:
    return (col_w - kerned_width(text, font, size)) / 2.0 - 0.5


def html_right_x(col_w: float, text: str, font: str, size: float, inset=0.5) -> float:
    return col_w - inset - kerned_width(text, font, size)


def wrap_kerned(text: str, font: str, size: float, max_width: float, max_lines: int):
    lines = []
    for para in (text or "").replace("\r", "").split("\n"):
        words = para.split()
        if not words:
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if kerned_width(trial, font, size) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines[:max_lines]


def draw_image(c, filename: str, x: float, y_top: float, w: float, h: float):
    if filename == layout.LOGO_FILE:
        draw_indexed_html(
            c,
            logo_stream.WIDTH, logo_stream.HEIGHT,
            logo_stream.INDEX_FLATE, logo_stream.PALETTE_FLATE,
            layout.PAGE_H, x, y_top + h, w, h,
            color_mask=logo_stream.COLOR_MASK,
        )
        return
    c.saveState()
    c.drawImage(
        _image(str(LOGOS_DIR / filename)),
        x, y_up(y_top + h),
        width=w, height=h, mask="auto",
        preserveAspectRatio=False, anchor="c",
    )
    c.restoreState()
