"""Helpers dessin (Y ReportLab). Helvetica Standard 14, fill-only, filets remplis."""

from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import FILL_NON_ZERO

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
    max_width=None,
):
    text = clip(text, font, size, max_width)
    if not text:
        return
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


def fill_rect(c, x0: float, y0: float, x1: float, y1: float, hex_color: str):
    c.saveState()
    c.setFillColor(HexColor(hex_color))
    c.setLineWidth(0)
    top, bot = min(y0, y1), max(y0, y1)
    left, right = min(x0, x1), max(x0, x1)
    c.rect(left, y_up(bot), right - left, bot - top, stroke=0, fill=1)
    c.restoreState()


def fill_poly(c, points, hex_color: str):
    """Fill nonzero, sans stroke (gabarit `h f`)."""
    if len(points) < 3:
        return
    c.saveState()
    c.setFillColor(HexColor(hex_color))
    c.setLineWidth(0)
    path = c.beginPath()
    x0, y0 = points[0]
    path.moveTo(x0, y_up(y0))
    for x, y in points[1:]:
        path.lineTo(x, y_up(y))
    path.close()
    c.drawPath(path, stroke=0, fill=1, fillMode=FILL_NON_ZERO)
    c.restoreState()


def stroke_dash(
    c, x0: float, x1: float, y: float, weight: float, dash, hex_color: str,
    clip_y0=None, clip_y1=None,
):
    """Pointillé gabarit : 1.5 w, [1.8 0.9], cap 0, join 2, RTL, clip 0.75 pt."""
    c.saveState()
    if clip_y0 is not None and clip_y1 is not None:
        top, bot = min(clip_y0, clip_y1), max(clip_y0, clip_y1)
        left, right = min(x0, x1), max(x0, x1)
        clip_path = c.beginPath()
        clip_path.rect(left, y_up(bot), right - left, bot - top)
        c.clipPath(clip_path, stroke=0, fill=0)
    c.setStrokeColor(HexColor(hex_color))
    c.setLineWidth(weight)
    pattern = list(dash) if not isinstance(dash, (int, float)) else [dash, dash]
    c.setDash(pattern, 0)
    c.setLineCap(0)
    c.setLineJoin(2)
    yu = y_up(y)
    c.line(max(x0, x1), yu, min(x0, x1), yu)
    c.restoreState()


def draw_image(c, filename: str, x: float, y_top: float, w: float, h: float):
    c.drawImage(
        str(LOGOS_DIR / filename),
        x, y_up(y_top + h),
        width=w, height=h, mask="auto",
    )
