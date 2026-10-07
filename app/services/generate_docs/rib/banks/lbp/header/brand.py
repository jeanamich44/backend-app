"""Bandeau logo LBP + titre de carte (droite)."""

from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

from app.services.generate_docs.common.paths import LOGOS_DIR

from .. import layout
from ..paint import fill, y_up

_drawing = None


def _logo():
    global _drawing
    if _drawing is None:
        path = LOGOS_DIR / layout.LOGO_FILE
        loaded = svg2rlg(str(path))
        if loaded is None:
            raise FileNotFoundError(f"Logo introuvable : {path}")
        _drawing = loaded
    return _drawing


def draw_logo(c, dy=0):
    drawing = _logo()
    if not drawing.width or not drawing.height:
        return
    c.saveState()
    c.translate(layout.LOGO_X + layout.LOGO_SVG_DX, y_up(layout.LOGO_Y_TOP + dy + layout.LOGO_H))
    c.scale(layout.LOGO_W / drawing.width, layout.LOGO_H / drawing.height)
    renderPDF.draw(drawing, c, 0, 0)
    c.restoreState()


def draw_card_title(c, text, dy=0):
    if not text:
        return
    c.setFont(layout.BRAND_TITLE_FONT, layout.BRAND_TITLE_SIZE)
    fill(c, layout.BRAND_TITLE_COLOR)
    c.drawRightString(layout.MARGIN_RIGHT, y_up(layout.BRAND_TITLE_Y + dy), text)


def draw(c, doc):
    if not doc.visible.header_brand:
        return
    draw_logo(c, 0)
    draw_card_title(c, doc.header.brand_title, 0)
