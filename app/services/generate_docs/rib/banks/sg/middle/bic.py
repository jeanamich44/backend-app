"""BIC : label Bold 10.5, valeur Regular 12."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_bic:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.LABEL_X, layout.BIC_LABEL_Y + dy, texts.LABEL_BIC,
        layout.FONT_BOLD, layout.SIZE_LABEL,
    )
    if not doc.card.bic:
        return
    draw_string(
        c, layout.BIC_X, layout.BIC_Y + dy, doc.card.bic,
        layout.FONT, layout.SIZE_VALUE,
        max_width=layout.BIC_W,
    )
