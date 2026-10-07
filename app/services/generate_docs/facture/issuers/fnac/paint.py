"""Helpers dessin (Y ReportLab depuis le haut PyMuPDF)."""

from reportlab.lib.colors import Color, HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import FILL_EVEN_ODD

from app.services.generate_docs.common.pdf_image import draw_indexed_html, draw_logo

from . import layout, logo_stream


def y_up(y_top: float) -> float:
    return layout.PAGE_H - y_top


def is_web(c) -> bool:
    return bool(getattr(c, "_fnac_web", True))


def to_color(color):
    if isinstance(color, Color):
        return color
    if isinstance(color, str):
        return HexColor(color)
    r, g, b = color[0], color[1], color[2]
    alpha = color[3] if len(color) > 3 else 1
    return Color(r, g, b, alpha=alpha)


def _pdf_num(value):
    if abs(value - round(value)) < 1e-12:
        return str(int(round(value)))
    return ("%.10f" % value).rstrip("0").rstrip(".")


def _rgb_tuple(color):
    col = to_color(color)
    return col.red, col.green, col.blue


def _fmt_rgb(rgb, web: bool) -> str:
    parts = []
    for value in rgb:
        if abs(value) < 1e-12:
            parts.append("0")
        elif abs(value - 1) < 1e-12:
            parts.append("1")
        elif web:
            parts.append("%.8f" % value)
        else:
            parts.append("%.3f" % value)
    return " ".join(parts)


def fill(c, color):
    rgb = _rgb_tuple(color)
    c._fillColorObj = Color(*rgb)
    token = _fmt_rgb(rgb, is_web(c))
    if is_web(c):
        c._code.append("/DeviceRGB cs")
        c._code.append("%s sc" % token)
    else:
        c._code.append("%s rg" % token)


def stroke(c, color):
    rgb = _rgb_tuple(color)
    c._strokeColorObj = Color(*rgb)
    token = _fmt_rgb(rgb, is_web(c))
    if is_web(c):
        c._code.append("/DeviceRGB CS")
        c._code.append("%s SC" % token)
    else:
        c._code.append("%s RG" % token)


def channel_green(c):
    return layout.COLOR_GREEN_WEB if is_web(c) else layout.COLOR_GREEN_MAG


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


def _write_rect(c, x0: float, y0: float, x1: float, y1: float):
    left, right = min(x0, x1), max(x0, x1)
    top, bot = min(y0, y1), max(y0, y1)
    yb, yt = y_up(bot), y_up(top)
    c._code.append("%s %s m" % (_pdf_num(left), _pdf_num(yb)))
    c._code.append("%s %s l" % (_pdf_num(right), _pdf_num(yb)))
    c._code.append("%s %s l" % (_pdf_num(right), _pdf_num(yt)))
    c._code.append("%s %s l" % (_pdf_num(left), _pdf_num(yt)))
    c._code.append("h")


def _write_rect_pdf4net(c, x0: float, y0: float, x1: float, y1: float):
    """Sens PDF4NET : haut-gauche → haut-droit → bas-droit → bas-gauche (Y PyMuPDF)."""
    left, right = min(x0, x1), max(x0, x1)
    top, bot = min(y0, y1), max(y0, y1)
    c._code.append("%s %s m" % (_pdf_num(left), _pdf_num(y_up(top))))
    c._code.append("%s %s l" % (_pdf_num(right), _pdf_num(y_up(top))))
    c._code.append("%s %s l" % (_pdf_num(right), _pdf_num(y_up(bot))))
    c._code.append("%s %s l" % (_pdf_num(left), _pdf_num(y_up(bot))))
    c._code.append("h")


def fill_stroke_rect(c, x0, y0, x1, y1, fill_color, stroke_color, line_w):
    fill(c, fill_color)
    stroke(c, stroke_color)
    c.setLineWidth(line_w)
    _write_rect_pdf4net(c, x0, y0, x1, y1)
    c._code.append("B")


def clip_rect(c, x0: float, y0: float, x1: float, y1: float):
    _write_rect(c, x0, y0, x1, y1)
    c._code.append("W")
    c._code.append("n")


def draw_string(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None, color=None, char_space=0,
):
    text = clip(text, font, size, max_width)
    if not text:
        return
    if color is not None:
        fill(c, color)
    if char_space:
        t = c.beginText()
        t.setFont(font, size)
        t.setCharSpace(char_space)
        t.setTextOrigin(x, y_up(y_origin))
        t.textOut(text)
        c.drawText(t)
        return
    c.setFont(font, size)
    c.drawString(x, y_up(y_origin), text)


def draw_vertical(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    color=None,
):
    """Baseline verticale 90° CCW, origin = bas du mot (Y PyMuPDF)."""
    text = text or ""
    if not text:
        return
    c.saveState()
    if color is not None:
        fill(c, color)
    c.setFont(font, size)
    c.translate(x, y_up(y_origin))
    c.rotate(90)
    c.drawString(0, 0, text)
    c.restoreState()


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


def draw_money(
    c, euro_x: float, y: float, number: str, font: str, size: float,
    slot_w: float, above: float, below: float, gap: float = None,
):
    """Nombre calé à gauche du €, glyphe € clippé comme PDF4NET / fnac1."""
    if gap is None:
        gap = layout.EURO_GAP
    if number:
        draw_right(c, euro_x - gap, y, number, font, size)
    c.saveState()
    clip_rect(c, euro_x, y - above, euro_x + slot_w, y + below)
    draw_string(c, euro_x, y, "€", font, size)
    c.restoreState()


def draw_center(
    c, x: float, y_origin: float, text: str, font: str, size: float,
    max_width=None, color=None,
):
    text = clip(text, font, size, max_width)
    if not text:
        return
    if color is not None:
        fill(c, color)
    c.setFont(font, size)
    c.drawCentredString(x, y_up(y_origin), text)


def fill_rect(c, x0: float, y0: float, x1: float, y1: float, color):
    fill(c, color)
    _write_rect(c, x0, y0, x1, y1)
    c._code.append("f")


def fill_poly(c, points, color):
    if len(points) < 3:
        return
    fill(c, color)
    path = c.beginPath()
    x0, y0 = points[0]
    path.moveTo(x0, y_up(y0))
    for x, y in points[1:]:
        path.lineTo(x, y_up(y))
    path.close()
    c.drawPath(path, stroke=0, fill=1, fillMode=FILL_EVEN_ODD)


def stroke_line(
    c, x0: float, y0: float, x1: float, y1: float,
    line_w: float, color, cap: int = 0,
):
    stroke(c, color)
    c.setLineWidth(line_w)
    c._code.append("%s %s m" % (_pdf_num(x0), _pdf_num(y_up(y0))))
    c._code.append("%s %s l" % (_pdf_num(x1), _pdf_num(y_up(y1))))
    c._code.append("S")


def stroke_rect(c, x0: float, y0: float, x1: float, y1: float, line_w: float, color):
    stroke_line(c, x0, y0, x1, y0, line_w, color)
    stroke_line(c, x0, y1, x1, y1, line_w, color)
    stroke_line(c, x0, y0, x0, y1, line_w, color)
    stroke_line(c, x1, y0, x1, y1, line_w, color)


def draw_image(c, filename: str, x: float, y_top: float, w: float, h: float):
    if filename == layout.LOGO_FILE:
        draw_indexed_html(
            c,
            logo_stream.WIDTH, logo_stream.HEIGHT,
            logo_stream.INDEX_FLATE, logo_stream.PALETTE_FLATE,
            layout.PAGE_H, x, y_top + h, w, h,
        )
        return
    draw_logo(c, filename, x, y_up(y_top + h), w, h)
