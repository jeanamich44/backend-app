"""Helpers dessin (Y ReportLab, SVG logo, clip)."""

from functools import lru_cache
from pathlib import Path

from PIL import Image as PILImage
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Image as RLImage
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from svglib.svglib import svg2rlg

from app.services.generate_docs.common.paths import LOGOS_DIR

from . import layout

CHROME_DIR = Path(__file__).resolve().parent / "chrome"

_svg = {}
_raster_readers = {}


@lru_cache(maxsize=8)
def _image_reader(path: str) -> ImageReader:
    return ImageReader(str(path))


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


def draw_centred(c, x: float, y_origin: float, text: str, font: str, size: float, max_width=None):
    text = clip(text, font, size, max_width)
    c.setFont(font, size)
    c.drawCentredString(x, y_up(y_origin), text)


def stroke_line(c, x0, y0, x1, y1, width, hex_color="#000000", dash=None, phase=0):
    c.saveState()
    c.setStrokeColor(HexColor(hex_color))
    c.setLineWidth(width)
    if dash:
        c.setDash(list(dash), phase)
    c.line(x0, y_up(y0), x1, y_up(y1))
    c.restoreState()


def stroke_rect(c, x0, y0, x1, y1, width, hex_color="#000000", fill_hex=None):
    c.saveState()
    c.setStrokeColor(HexColor(hex_color))
    c.setLineWidth(width)
    fill_flag = 0
    if fill_hex:
        c.setFillColor(HexColor(fill_hex))
        fill_flag = 1
    top, bot = min(y0, y1), max(y0, y1)
    left, right = min(x0, x1), max(x0, x1)
    c.rect(left, y_up(bot), right - left, bot - top, stroke=1, fill=fill_flag)
    c.restoreState()


def draw_image(c, filename: str, x: float, y_top: float, w: float, h: float):
    path = CHROME_DIR / filename
    c.drawImage(_image_reader(str(path)), x, y_up(y_top + h), width=w, height=h, mask="auto")


def _flatten_svg_rasters(obj):
    """Les pixels transparents du PNG (0,0,0,0) deviennent un trait noir via svglib."""
    if isinstance(obj, RLImage):
        im = obj.path
        if hasattr(im, "mode") and im.mode == "RGBA":
            bg = PILImage.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
            obj.path = bg
        obj.fillColor = None
        obj.strokeColor = None
        obj.strokeWidth = 0
    for child in getattr(obj, "contents", None) or []:
        _flatten_svg_rasters(child)


def _first_raster(obj):
    if isinstance(obj, RLImage) and obj.path is not None:
        return obj.path
    for child in getattr(obj, "contents", None) or []:
        found = _first_raster(child)
        if found is not None:
            return found
    return None


def _load_svg(path: Path):
    key = str(path)
    if key not in _svg:
        loaded = svg2rlg(str(path))
        if loaded is None:
            raise FileNotFoundError(f"SVG introuvable : {path}")
        _flatten_svg_rasters(loaded)
        _svg[key] = loaded
    return _svg[key]


def draw_svg(c, filename: str, x: float, y_top: float, w: float, h: float, dx: float = 0.0):
    path = LOGOS_DIR / filename
    key = str(path)
    drawing = _load_svg(path)
    if key not in _raster_readers:
        raster = _first_raster(drawing)
        _raster_readers[key] = ImageReader(raster) if raster is not None else None
    reader = _raster_readers[key]
    if reader is not None:
        c.drawImage(
            reader,
            x + dx,
            y_up(y_top + h),
            width=w,
            height=h,
            mask="auto",
        )
        return
    if not drawing.width or not drawing.height:
        return
    c.saveState()
    c.translate(x + dx, y_up(y_top + h))
    c.scale(w / drawing.width, h / drawing.height)
    renderPDF.draw(drawing, c, 0, 0, showBoundary=0)
    c.restoreState()
