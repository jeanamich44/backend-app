"""Helpers dessin (Y ReportLab, fill-only, pas de Tr)."""

from reportlab.lib.colors import Color, white
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import FILL_NON_ZERO

from . import layout

_LIGA_FONTS = {layout.FONT, layout.FONT_BOLD}


def liga(text: str, font: str = None) -> str:
    if not text:
        return text
    if font is not None and font not in _LIGA_FONTS:
        return text
    return text.replace("fi", "\ufb01").replace("ff", "\ufb00")


def y_up(y_top: float) -> float:
    return layout.PAGE_H - y_top


def rgb_color(rgb, alpha=1):
    return Color(rgb[0], rgb[1], rgb[2], alpha=alpha)


def fill_rgb(c, rgb, alpha=1):
    c.setFillColor(rgb_color(rgb, alpha))


def width(text, font, size) -> float:
    return stringWidth(liga(text or "", font), font, size)


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
    text = liga(clip(text, font, size, max_width), font)
    if not text:
        return
    c.setFont(font, size)
    c.drawString(x, y_up(y_origin), text, mode=0)


def draw_right(c, x: float, y_origin: float, text: str, font: str, size: float):
    text = liga(text or "", font)
    if not text:
        return
    c.setFont(font, size)
    c.drawRightString(x, y_up(y_origin), text, mode=0)


def wrap_lines(text: str, font: str, size: float, max_width: float) -> list[str]:
    """Coupe sur les espaces (y compris doubles, comme « que  NOM »)."""
    tokens = liga(text or "", font).split(" ")
    lines = []
    current: list[str] = []
    for token in tokens:
        trial = current + [token]
        if width(" ".join(trial), font, size) <= max_width or not current:
            current = trial
            continue
        lines.append(" ".join(current))
        current = [token]
    if current:
        lines.append(" ".join(current))
    return lines or [""]


def fill_rect(c, x: float, y_top: float, w: float, h: float, rgb=None):
    c.saveState()
    if rgb is None:
        c.setFillColor(white)
    else:
        fill_rgb(c, rgb)
    c.rect(x, y_up(y_top + h), w, h, stroke=0, fill=1)
    c.restoreState()


def _add_item(path, item):
    kind = item[0]
    if kind == "m":
        path.moveTo(item[1], y_up(item[2]))
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


def fill_groups(c, groups):
    """Un f par groupe (couleurs FO1)."""
    for rgb, subs in groups:
        c.saveState()
        fill_rgb(c, rgb)
        path = c.beginPath()
        for sub in subs:
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


def stroke_line(c, x0, x1, y, weight, rgb, cap=0, join=0):
    c.saveState()
    c.setStrokeColor(rgb_color(rgb))
    c.setLineWidth(weight)
    c.setLineCap(cap)
    c.setLineJoin(join)
    c.setDash([], 0)
    yu = y_up(y)
    c.line(x0, yu, x1, yu)
    c.restoreState()
