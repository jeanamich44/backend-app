"""Helpers dessin (Y ReportLab, JPEG, clip). Texte fill only (gabarit sans 2 Tr)."""

from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth

from app.services.generate_docs.common.paths import LOGOS_DIR

from . import layout


def y_up(y_top: float) -> float:
    return layout.PAGE_H - y_top


def fill(c, hex_color: str):
    color = HexColor(hex_color)
    c.setFillColor(color)
    c.setStrokeColor(color)


def width(text, font, size) -> float:
    return stringWidth(text or "", font, size)


def clip(text, font, size, max_width):
    text = text or ""
    if max_width is None or width(text, font, size) <= max_width:
        return text
    while text and width(text, font, size) > max_width:
        text = text[:-1]
    return text


def draw_string(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None, justify_to=None,
):
    text = clip(text, font, size, max_width)
    if not text:
        return
    word_space = None
    if justify_to is not None:
        spaces = text.count(" ")
        extra = justify_to - width(text, font, size)
        if spaces and extra > 0:
            word_space = extra / spaces
    c.setFont(font, size)
    c.drawString(x, y_up(y_origin), text, wordSpace=word_space)


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
    max_width=None,
):
    limit = max_width if max_width is not None else (x1 - x0)
    text = clip(text, font, size, limit)
    if not text:
        return
    x = x0 + (x1 - x0 - width(text, font, size)) / 2.0
    c.setFont(font, size)
    c.drawString(x, y_up(y_origin), text)


def draw_right(
    c, right_x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None,
):
    text = clip(text, font, size, max_width)
    if not text:
        return
    x = right_x - width(text, font, size)
    c.setFont(font, size)
    c.drawString(x, y_up(y_origin), text)


def stroke_line(c, x0: float, y: float, x1: float, width: float, hex_color: str):
    c.saveState()
    c.setStrokeColor(HexColor(hex_color))
    c.setLineWidth(width)
    c.setLineCap(0)
    c.setDash([])
    yu = y_up(y)
    c.line(x0, yu, x1, yu)
    c.line(x1, yu, x0, yu)
    c.restoreState()


def stroke_vline(c, x: float, y0: float, y1: float, width: float, hex_color: str):
    c.saveState()
    c.setStrokeColor(HexColor(hex_color))
    c.setLineWidth(width)
    c.setLineCap(0)
    c.setDash([])
    a, b = y_up(y0), y_up(y1)
    c.line(x, a, x, b)
    c.line(x, b, x, a)
    c.restoreState()


def draw_image(c, filename: str, x: float, y_top: float, w: float, h: float, mask=None):
    c.drawImage(
        str(LOGOS_DIR / filename),
        x, y_up(y_top + h),
        width=w, height=h, mask=mask,
    )


def draw_zapf_pct(c, x: float, y_origin: float, size: float):
    """Octet 0x25 dans ZapfDingbats, comme le gabarit `(%)Tj`."""
    yu = y_up(y_origin)
    c.setFont(layout.FONT_DINGBAT, size)
    font_ref = c._doc.getInternalFontName(layout.FONT_DINGBAT)
    c._code.append(
        f"BT {font_ref} {size:g} Tf 1 0 0 1 {x:.3f} {yu:.3f} Tm (%)Tj ET"
    )
