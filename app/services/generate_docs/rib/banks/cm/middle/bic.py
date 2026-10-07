"""BIC centré dans la case de droite."""

from .. import copy as texts
from .. import layout
from ..paint import draw_centered, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_bic:
        return
    fill(c, layout.COLOR)
    draw_centered(
        c, layout.RIGHT_X0, layout.RIGHT_X1, layout.BIC_LABEL_Y + dy,
        texts.LABEL_BIC, layout.LABEL_FONT, layout.SIZE_LABEL,
    )
    if not doc.card.bic:
        return
    draw_centered(
        c, layout.RIGHT_X0, layout.RIGHT_X1, layout.BIC_Y + dy,
        doc.card.bic, layout.VALUE_FONT, layout.SIZE_VALUE,
        max_width=layout.RIGHT_X1 - layout.RIGHT_X0,
    )
