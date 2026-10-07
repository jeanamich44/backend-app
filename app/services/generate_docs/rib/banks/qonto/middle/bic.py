"""BIC/SWIFT : label Bold 8.25 #999896, valeur Regular 10.5."""

from .. import copy as texts
from .. import glyphs
from .. import layout
from ..paint import draw_glyphs, draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_bic:
        return
    fill(c, layout.COLOR_MUTED)
    draw_string(
        c, layout.BIC_X, layout.IBAN_LABEL_Y, texts.LABEL_BIC,
        layout.FONT_BOLD, layout.SIZE_LABEL,
    )
    if not doc.card.bic:
        return
    fill(c, layout.COLOR)
    bic = doc.card.bic
    if bic == glyphs.BIC_TEXT:
        draw_glyphs(
            c, layout.IBAN_VALUE_Y, glyphs.BIC,
            layout.FONT, layout.SIZE_VALUE,
        )
    else:
        draw_string(
            c, layout.BIC_X, layout.IBAN_VALUE_Y, bic,
            layout.FONT, layout.SIZE_VALUE,
            max_width=layout.BIC_W,
        )
