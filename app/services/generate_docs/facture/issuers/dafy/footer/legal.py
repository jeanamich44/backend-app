from .. import layout
from ..chrome import vectors
from ..paint import draw_glyphs, fill


def draw(c, doc):
    if not doc.visible.footer_legal:
        return
    fill(c, layout.COLOR_BLACK)
    for y, glyphs in vectors.LEGAL_GLYPHS:
        draw_glyphs(c, y, glyphs, layout.FONT_H, layout.SIZE_FOOTER)
