"""Helpers dessin (Y ReportLab, SVG chrome, clip)."""

from pathlib import Path

from reportlab.graphics import renderPDF
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from svglib.svglib import svg2rlg

from app.services.generate_docs.common.paths import LOGOS_DIR

from . import layout

CHROME_DIR = Path(__file__).resolve().parent / "chrome"

_svg = {}


def y_up(y_top: float) -> float:
    return layout.PAGE_H - y_top


def fill(c, hex_color: str):
    c.setFillColor(HexColor(hex_color))


def clip(text, font, size, max_width):
    text = text or ""
    if max_width is None or stringWidth(text, font, size) <= max_width:
        return text
    while text and stringWidth(text, font, size) > max_width:
        text = text[:-1]
    return text


def draw_string(c, x: float, y_origin: float, text: str, font: str, size: float, max_width=None):
    text = clip(text, font, size, max_width)
    c.setFont(font, size)
    c.drawString(x, y_up(y_origin), text)


def _load_svg(path: Path):
    key = str(path)
    if key not in _svg:
        loaded = svg2rlg(str(path))
        if loaded is None:
            raise FileNotFoundError(f"SVG introuvable : {path}")
        _svg[key] = loaded
    return _svg[key]


def _draw_svg_file(c, path: Path, x: float, y_top: float, w: float, h: float, dx: float = 0.0):
    if not path.is_file():
        raise FileNotFoundError(f"SVG introuvable : {path}")
    drawing = _load_svg(path)
    if not drawing.width or not drawing.height:
        return
    c.saveState()
    c.translate(x + dx, y_up(y_top + h))
    c.scale(w / drawing.width, h / drawing.height)
    renderPDF.draw(drawing, c, 0, 0)
    c.restoreState()


def draw_svg(c, filename: str, x: float, y_top: float, w: float, h: float, dx: float = 0.0):
    _draw_svg_file(c, CHROME_DIR / filename, x, y_top, w, h, dx)


def draw_logo(c, filename: str, x: float, y_top: float, w: float, h: float):
    _draw_svg_file(c, LOGOS_DIR / filename, x, y_top, w, h)


def draw_label(c, spec: tuple):
    filename, x, y_top, w, h = spec
    draw_svg(c, filename, x, y_top, w, h)
