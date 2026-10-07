"""Helpers dessin (Y ReportLab). Arial fill-only, fills vectoriels, filets remplis."""

from reportlab.lib.colors import Color, HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import FILL_NON_ZERO

from . import layout


def y_up(y_top: float) -> float:
    return layout.PAGE_H - y_top


_STREAM = {
    "#1D1D1B": Color(0.1137, 0.1137, 0.1059, alpha=1),
    "#636360": Color(0.3882, 0.3882, 0.3765, alpha=1),
    "#999896": Color(0.6, 0.5961, 0.5882, alpha=1),
    "#EBEBE8": Color(0.9216, 0.9216, 0.9098, alpha=1),
    "#FFFFFF": Color(1, 1, 1, alpha=1),
    "#B8B8B5": Color(0.7216, 0.7216, 0.7098, alpha=1),
}


def stream_color(hex_color: str):
    return _STREAM.get(hex_color.upper(), HexColor(hex_color))


def fill(c, hex_color: str):
    c.setFillColor(stream_color(hex_color))


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
    max_width=None, char_space=0.0,
):
    """Même écriture que le gabarit : cm 0.75, Tf 1, Tm (size/0.75) 0 0 -(size/0.75)."""
    text = clip(text, font, size, max_width)
    if not text:
        return
    x_u = x / layout.CM_A
    y_u = (y_origin - layout.CM_TOP) / layout.CM_A
    size_u = size / layout.CM_A
    c.saveState()
    c.transform(layout.CM_A, 0, 0, -layout.CM_A, 0, layout.CM_TY)
    t = c.beginText()
    t.setTextRenderMode(0)
    t.setTextTransform(size_u, 0, 0, -size_u, x_u, y_u)
    t.setFont(font, 1)
    if char_space:
        t.setCharSpace(char_space)
    t.textOut(text)
    c.drawText(t)
    c.restoreState()


def draw_glyphs(c, y_origin, glyphs, font, size, char_space=0.0):
    """Un Tm par glyphe, origins du gabarit (TJ ±0.2)."""
    for ch, x in glyphs:
        if ch:
            draw_string(c, x, y_origin, ch, font, size, char_space=char_space)


def fill_rect(c, x0: float, y0: float, x1: float, y1: float, hex_color: str):
    c.saveState()
    c.setFillColor(stream_color(hex_color))
    c.setLineWidth(0)
    top, bot = min(y0, y1), max(y0, y1)
    left, right = min(x0, x1), max(x0, x1)
    c.rect(left, y_up(bot), right - left, bot - top, stroke=0, fill=1)
    c.restoreState()


def fill_dash_row(c, y0, y1, width, step, count, hex_color: str):
    """Un seul f, sous-chemins 4 points comme le gabarit (Y PDF 629.88 / 461.88)."""
    c.saveState()
    # Stream : 0.7216 0.7216 0.7098 sc
    c.setFillColor(Color(0.7216, 0.7216, 0.7098, alpha=1))
    c.setLineWidth(0)
    top, bot = min(y0, y1), max(y0, y1)
    yu_top, yu_bot = y_up(top), y_up(bot)
    path = c.beginPath()
    x = 0.0
    for _ in range(count):
        x1 = x + width
        path.moveTo(x, yu_top)
        path.lineTo(x1, yu_top)
        path.lineTo(x1, yu_bot)
        path.lineTo(x, yu_bot)
        path.close()
        x += step
    c.drawPath(path, stroke=0, fill=1, fillMode=FILL_NON_ZERO)
    c.restoreState()


def fill_fills(c, fills, hex_color: str):
    """Rejoue les fills du gabarit (sous-chemins = trous nonzero)."""
    c.saveState()
    c.setFillColor(stream_color(hex_color))
    for fill_ops in fills:
        path = c.beginPath()
        for sub in fill_ops:
            started = False
            for item in sub:
                kind = item[0]
                if kind == "m":
                    if started:
                        path.close()
                    path.moveTo(item[1], y_up(item[2]))
                    started = True
                elif kind == "l":
                    path.lineTo(item[1], y_up(item[2]))
                elif kind == "c":
                    a, b, d = item[1], item[2], item[3]
                    path.curveTo(
                        a[0], y_up(a[1]),
                        b[0], y_up(b[1]),
                        d[0], y_up(d[1]),
                    )
                elif kind == "h":
                    path.close()
                    started = False
        c.drawPath(path, stroke=0, fill=1, fillMode=FILL_NON_ZERO)
    c.restoreState()
