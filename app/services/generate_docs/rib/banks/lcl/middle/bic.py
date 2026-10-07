"""BIC / Adresse Swift : cellule droite."""

from .. import copy as texts
from .. import layout
from ..paint import draw_centered, draw_string, fill


def draw(c, doc, i=0):
    if not doc.visible.middle_bic:
        return
    d = layout.dy(i)
    fill(c, layout.COLOR)
    x0, x1 = layout.INTL_COLS[1]
    draw_string(
        c, layout.INTL_HEAD_X[1], layout.INTL_HEAD_Y + d, texts.LABEL_BIC,
        layout.FONT_BOLD, layout.SIZE_FIELD,
        max_width=x1 - layout.INTL_HEAD_X[1],
    )
    if doc.card.bic:
        draw_centered(
            c, x0, x1, layout.INTL_VAL_Y + d, doc.card.bic,
            layout.FONT_BOLD, layout.SIZE_FIELD,
        )
