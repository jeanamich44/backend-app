import json
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth

from . import layout

# ----------------------------------------------------------------------

_STATIC_DATA = None
_FONT_MAP = {
    "CIDFont+F1": layout.FONT_ITALIC,
    "CIDFont+F2": layout.FONT_BOLD,
    "CIDFont+F3": layout.FONT_REGULAR,
    "CIDFont+F4": layout.FONT_LIGHT,
    "Carlito": layout.FONT_CARLITO,
    "ArialNarrow": layout.FONT_NARROW,
}


def _load_static_layout():
    global _STATIC_DATA
    if _STATIC_DATA is None and layout.STATIC_LAYOUT_JSON.is_file():
        _STATIC_DATA = json.loads(layout.STATIC_LAYOUT_JSON.read_text(encoding="utf-8"))


def draw_static_block(c, block_idx: int):
    _load_static_layout()
    if not _STATIC_DATA:
        return
    lines = _STATIC_DATA.get(str(block_idx), [])
    for line in lines:
        for ch in line:
            fn = _FONT_MAP.get(ch.get("font", ""), layout.FONT_REGULAR)
            c.setFont(fn, ch["size"])
            c.setFillColor(HexColor(ch["color"]))
            c.drawString(ch["x"], layout.PAGE_H - ch["y"], ch["c"])


def y_up(y_top: float) -> float:
    return layout.PAGE_H - y_top


def fill(c, hex_color: str):
    c.setFillColor(HexColor(hex_color))


def stroke(c, hex_color: str, width: float = 1.0):
    c.setStrokeColor(HexColor(hex_color))
    c.setLineWidth(width)


def clip(text: str, font: str, size: float, max_width: float | None = None) -> str:
    text = text or ""
    if max_width is None or stringWidth(text, font, size) <= max_width:
        return text
    while text and stringWidth(text, font, size) > max_width:
        text = text[:-1]
    return text


def draw_string(c, x: float, y_origin: float, text: str, font: str, size: float, max_width: float | None = None):
    text = clip(text, font, size, max_width)
    c.setFont(font, size)
    c.drawString(x, y_up(y_origin), text)


def draw_centred(c, x: float, y_origin: float, text: str, font: str, size: float, max_width: float | None = None):
    text = clip(text, font, size, max_width)
    c.setFont(font, size)
    c.drawCentredString(x, y_up(y_origin), text)


def draw_right(c, x: float, y_origin: float, text: str, font: str, size: float):
    text = text or ""
    c.setFont(font, size)
    c.drawRightString(x, y_up(y_origin), text)


def draw_justified_line(c, x: float, y_origin: float, text: str, font: str, size: float, target_w: float):
    text = text or ""
    natural = stringWidth(text, font, size)
    spaces = text.count(" ")
    extra = (target_w - natural) / spaces if spaces and target_w > natural else 0.0
    t = c.beginText(x, y_up(y_origin))
    t.setFont(font, size)
    t.setWordSpace(extra)
    t.textOut(text)
    c.drawText(t)


def stroke_line(c, x0: float, y0: float, x1: float, y1: float, width: float = 1.0, hex_color: str = "#000000"):
    c.saveState()
    c.setStrokeColor(HexColor(hex_color))
    c.setLineWidth(width)
    c.line(x0, y_up(y0), x1, y_up(y1))
    c.restoreState()


def draw_rect(c, x: float, y: float, w: float, h: float, fill_color: str | None = None, stroke_color: str | None = None, stroke_width: float = 1.0):
    c.saveState()
    if fill_color:
        c.setFillColor(HexColor(fill_color))
    if stroke_color:
        c.setStrokeColor(HexColor(stroke_color))
        c.setLineWidth(stroke_width)
    c.rect(x, y_up(y + h), w, h, fill=bool(fill_color), stroke=bool(stroke_color))
    c.restoreState()
