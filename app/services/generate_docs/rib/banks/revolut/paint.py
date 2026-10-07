"""Helpers dessin (Y ReportLab, Roboto Regular, 2 Tr labels, filets remplis)."""

from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth

from app.services.generate_docs.common.paths import LOGOS_DIR

from . import layout

CHROME_DIR = Path(__file__).resolve().parent / "chrome"


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
    max_width=None, stroke=False,
):
    text = clip(text, font, size, max_width)
    if not text:
        return
    c.setFont(font, size)
    if stroke:
        c.setLineWidth(size * layout.STROKE_RATIO)
        mode = 2
    else:
        c.setLineWidth(1)
        mode = 0
    c.drawString(x, y_up(y_origin), text, mode=mode)
    if stroke:
        c.setLineWidth(1)


def draw_label(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None,
):
    """Titres et libellés : Regular + 2 Tr une fois, trait = 0.04 × corps."""
    fill(c, layout.COLOR)
    draw_string(c, x, y_origin, text, font, size, max_width=max_width, stroke=True)


def draw_value(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None,
):
    """Valeurs : fill-only 0 Tr, une fois."""
    fill(c, layout.COLOR)
    draw_string(c, x, y_origin, text, font, size, max_width=max_width, stroke=False)


def fill_rect(c, x0: float, y0: float, x1: float, y1: float, hex_color: str):
    c.saveState()
    c.setFillColor(HexColor(hex_color))
    c.setLineWidth(0)
    top, bot = min(y0, y1), max(y0, y1)
    left, right = min(x0, x1), max(x0, x1)
    c.rect(left, y_up(bot), right - left, bot - top, stroke=0, fill=1)
    c.restoreState()


def stroke_dash(
    c, x0: float, x1: float, y: float, weight: float, dash: float, hex_color: str,
    clip_y0=None, clip_y1=None,
):
    """Trait pointillé du gabarit : 1.5 w + [0.75 0.75], clippé à 0.75 pt de haut."""
    c.saveState()
    if clip_y0 is not None and clip_y1 is not None:
        top, bot = min(clip_y0, clip_y1), max(clip_y0, clip_y1)
        clip_path = c.beginPath()
        clip_path.rect(x0, y_up(bot), x1 - x0, bot - top)
        c.clipPath(clip_path, stroke=0, fill=0)
    c.setStrokeColor(HexColor(hex_color))
    c.setLineWidth(weight)
    c.setDash(dash, dash)
    c.setLineCap(0)
    c.setLineJoin(2)
    yu = y_up(y)
    c.line(x0, yu, x1, yu)
    c.restoreState()


def _png(c, path: Path, x: float, y_top: float, w: float, h: float):
    c.drawImage(str(path), x, y_up(y_top + h), width=w, height=h, mask="auto")


def draw_image(c, filename: str, x: float, y_top: float, w: float, h: float):
    _png(c, LOGOS_DIR / filename, x, y_top, w, h)


def draw_chrome(c, filename: str, x: float, y_top: float, w: float, h: float):
    _png(c, CHROME_DIR / filename, x, y_top, w, h)
