"""Helpers dessin (Y ReportLab). Quicksand fill-only, wordmark et cadre vectoriels."""

from reportlab.lib.colors import Color, HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import FILL_NON_ZERO

from . import layout

# CID original 0x0206 = ligature fi (même avance que f+i, glyphe collé).
_LIGA_FONTS = {layout.FONT, layout.FONT_NARROW, layout.FONT_BOLD}


def liga(text: str, font: str) -> str:
    if not text or font not in _LIGA_FONTS:
        return text
    return text.replace("fi", "\ufb01")


def y_up(y_top: float) -> float:
    return layout.PAGE_H - y_top


_STREAM = {
    "#131312": Color(0.07599, 0.07599, 0.07399, alpha=1),
    "#000000": Color(0, 0, 0, alpha=1),
}


def stream_color(hex_color: str):
    return _STREAM.get(hex_color.upper(), HexColor(hex_color))


def rgb_color(rgb, alpha=1):
    return Color(rgb[0], rgb[1], rgb[2], alpha=alpha)


def fill(c, hex_color: str):
    c.setFillColor(stream_color(hex_color))


def fill_rgb(c, rgb, alpha=1):
    c.setFillColor(rgb_color(rgb, alpha))


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
    text = liga(text, font)
    text = clip(text, font, size, max_width)
    if not text:
        return
    c.setFont(font, size)
    y = y_up(y_origin)
    if char_space:
        cursor = x
        for ch in text:
            c.drawString(cursor, y, ch, mode=0)
            cursor += width(ch, font, size) + char_space
    else:
        c.drawString(x, y, text, mode=0)


def draw_runs(
    c, x: float, y_origin: float, runs, font: str, size: float,
    word_space_em: float = 0.0,
):
    """Rejoue un TJ du gabarit : kerning en millièmes d’em, Tw en unités texte."""
    if not runs:
        return
    y = y_up(y_origin)
    word_pt = word_space_em * size
    cursor = x
    t = c.beginText()
    t.setFont(font, size)
    t.setTextRenderMode(0)
    if word_pt:
        t.setWordSpace(word_pt)
    for text, tj in runs:
        text = liga(text, font)
        if text:
            t.setTextOrigin(cursor, y)
            t.textOut(text)
            cursor += width(text, font, size) + word_pt * text.count(" ")
        cursor -= float(tj) / 1000.0 * size
    c.drawText(t)


def _add_item(path, item, dy):
    kind = item[0]
    if kind == "m":
        path.moveTo(item[1], y_up(item[2] + dy))
    elif kind == "l":
        path.lineTo(item[1], y_up(item[2] + dy))
    elif kind == "c":
        a, b, d = item[1], item[2], item[3]
        path.curveTo(
            a[0], y_up(a[1] + dy),
            b[0], y_up(b[1] + dy),
            d[0], y_up(d[1] + dy),
        )
    elif kind == "h":
        path.close()


def fill_fills(c, fills, hex_color: str, dy: float = 0.0):
    """Rejoue les fills du gabarit (sous-chemins imbriqués, Y depuis le haut)."""
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
                    path.moveTo(item[1], y_up(item[2] + dy))
                    started = True
                elif kind == "l":
                    path.lineTo(item[1], y_up(item[2] + dy))
                elif kind == "c":
                    a, b, d = item[1], item[2], item[3]
                    path.curveTo(
                        a[0], y_up(a[1] + dy),
                        b[0], y_up(b[1] + dy),
                        d[0], y_up(d[1] + dy),
                    )
                elif kind == "h":
                    path.close()
                    started = False
        c.drawPath(path, stroke=0, fill=1, fillMode=FILL_NON_ZERO)
    c.restoreState()


def fill_items(c, fills, rgb, dy: float = 0.0, alpha: float = 1.0):
    """Fills à plat (plusieurs sous-chemins par path, winding nonzero)."""
    c.saveState()
    c.setFillColor(rgb_color(rgb, alpha))
    for items in fills:
        path = c.beginPath()
        for item in items:
            _add_item(path, item, dy)
        c.drawPath(path, stroke=0, fill=1, fillMode=FILL_NON_ZERO)
    c.restoreState()


def _subpaths(items):
    cur = []
    for item in items:
        cur.append(item)
        if item[0] == "h":
            yield cur
            cur = []
    if cur:
        yield cur


def _bbox(sub):
    xs, ys = [], []
    for item in sub:
        if item[0] in ("m", "l"):
            xs.append(item[1])
            ys.append(item[2])
    if not xs:
        return None
    return min(xs), min(ys), max(xs), max(ys)


def fill_union(c, fills, rgb, dy: float = 0.0, pad: float = 0.0):
    """Un seul f opaque : plus de filets AA entre modules."""
    c.saveState()
    c.setFillColor(rgb_color(rgb, 1))
    c.setLineWidth(0)
    path = c.beginPath()
    for items in fills:
        for sub in _subpaths(items):
            box = _bbox(sub)
            if (
                pad
                and box
                and (box[2] - box[0]) < 6
                and (box[3] - box[1]) < 6
            ):
                x0, y0, x1, y1 = box
                sub = (
                    ("m", x0 - pad, y0 - pad),
                    ("l", x1 + pad, y0 - pad),
                    ("l", x1 + pad, y1 + pad),
                    ("l", x0 - pad, y1 + pad),
                    ("h",),
                )
            for item in sub:
                _add_item(path, item, dy)
    c.drawPath(path, stroke=0, fill=1, fillMode=FILL_NON_ZERO)
    c.restoreState()


def stroke_items(
    c, items, rgb, weight: float, dy: float = 0.0, cap: int = 1, join: int = 0,
    miter: float = 4.0, alpha: float = 1.0, dash=None,
):
    c.saveState()
    c.setStrokeColor(rgb_color(rgb, alpha))
    c.setLineWidth(weight)
    c.setLineCap(cap)
    c.setLineJoin(join)
    c.setMiterLimit(miter)
    if dash:
        c.setDash(list(dash), 0)
    else:
        c.setDash([], 0)
    path = c.beginPath()
    for item in items:
        _add_item(path, item, dy)
    c.drawPath(path, stroke=1, fill=0)
    c.restoreState()


def stroke_line(
    c, x0, x1, y, weight, rgb, dy=0.0, cap=0, dash=None, alpha=1.0,
):
    c.saveState()
    c.setStrokeColor(rgb_color(rgb, alpha))
    c.setLineWidth(weight)
    c.setLineCap(cap)
    if dash:
        c.setDash(list(dash), 0)
    else:
        c.setDash([], 0)
    yu = y_up(y + dy)
    c.line(x0, yu, x1, yu)
    c.restoreState()
