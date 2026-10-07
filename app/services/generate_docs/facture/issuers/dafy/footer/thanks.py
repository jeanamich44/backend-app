from .. import layout
from ..chrome import vectors
from ..paint import draw_glyphs, fill


def draw(c, doc):
    if not doc.visible.footer_thanks:
        return
    extra = layout.middle_shift(doc.card) if doc.visible.middle else 0.0
    fill(c, layout.COLOR)
    draw_glyphs(
        c, vectors.THANKS_Y + extra, vectors.THANKS_GLYPHS,
        layout.FONT_OBLIQUE, layout.SIZE_BODY,
    )
