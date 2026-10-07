"""Helpers dessin (Y ReportLab depuis le haut PyMuPDF)."""

from reportlab.lib.colors import Color, HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import FILL_EVEN_ODD

from app.services.generate_docs.common.pdf_image import draw_logo

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


def wrap_lines(text: str, font: str, size: float, max_width: float, max_lines=None):
    lines = []
    for paragraph in (text or "").replace("\r", "").split("\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        current = ""
        for word in paragraph.split():
            trial = word if not current else f"{current} {word}"
            if width(trial, font, size) <= max_width:
                current = trial
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
    if not lines:
        lines = [""]
    if max_lines is not None:
        lines = lines[:max_lines]
    return lines


def clip(text, font, size, max_width):
    text = text or ""
    if max_width is None or width(text, font, size) <= max_width:
        return text
    while text and width(text, font, size) > max_width:
        text = text[:-1]
    return text


def draw_string(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None, color=None,
):
    text = clip(text, font, size, max_width)
    if not text:
        return
    if color is not None:
        fill(c, color)
    c.setFont(font, size)
    c.drawString(x, y_up(y_origin), text)


def draw_right(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None, color=None,
):
    text = clip(text, font, size, max_width)
    if not text:
        return
    if color is not None:
        fill(c, color)
    c.setFont(font, size)
    c.drawRightString(x, y_up(y_origin), text)


def fill_rect(c, x0: float, y0: float, x1: float, y1: float, color):
    c.saveState()
    c.setFillColor(to_color(color))
    c.setLineWidth(0)
    top, bot = min(y0, y1), max(y0, y1)
    left, right = min(x0, x1), max(x0, x1)
    c.rect(left, y_up(bot), right - left, bot - top, stroke=0, fill=1)
    c.restoreState()


def fill_poly(c, points, color):
    if len(points) < 3:
        return
    c.saveState()
    c.setFillColor(to_color(color))
    c.setLineWidth(0)
    path = c.beginPath()
    x0, y0 = points[0]
    path.moveTo(x0, y_up(y0))
    for x, y in points[1:]:
        path.lineTo(x, y_up(y))
    path.close()
    c.drawPath(path, stroke=0, fill=1, fillMode=FILL_EVEN_ODD)
    c.restoreState()


def frame_miter(c, x0: float, y0: float, x1: float, y1: float, t: float, color):
    """Cadre 0.75 pt du gabarit HTML : 4 trapèzes mitrés, pas de rectangles qui se chevauchent."""
    fill_poly(c, [(x1, y0), (x0, y0), (x0 + t, y0 + t), (x1 - t, y0 + t)], color)
    fill_poly(c, [(x0 + t, y1 - t), (x0 + t, y0 + t), (x0, y0), (x0, y1)], color)
    fill_poly(c, [(x1 - t, y1 - t), (x0 + t, y1 - t), (x0, y1), (x1, y1)], color)
    fill_poly(c, [(x1, y0), (x1 - t, y0 + t), (x1 - t, y1 - t), (x1, y1)], color)


def draw_image(c, filename: str, x: float, y_top: float, w: float, h: float):
    draw_logo(c, filename, x, y_up(y_top + h), w, h)
