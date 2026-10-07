"""Helpers dessin (Y ReportLab depuis le haut PyMuPDF)."""

from reportlab.lib.colors import Color, HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth

from . import layout


def y_up(y_top: float) -> float:
    return layout.PAGE_H - y_top


def to_color(color):
    if isinstance(color, Color):
        return color
    if isinstance(color, str):
        return HexColor(color)
    r, g, b = color[0], color[1], color[2]
    alpha = color[3] if len(color) > 3 else 1
    return Color(r, g, b, alpha=alpha)


def fill(c, color):
    c.setFillColor(to_color(color))


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
