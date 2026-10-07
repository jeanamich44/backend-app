"""BIC : libellé gris (2× fill) + valeur fill+stroke."""

from .. import copy as texts
from .. import layout
from ..paint import draw_label, draw_value, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_bic:
        return
    fill(c, layout.LABEL_COLOR)
    draw_label(
        c, layout.FIELD_X, layout.BIC_LABEL_Y + dy, texts.LABEL_BIC + " ",
        layout.FONT, layout.SIZE_FIELD,
    )
    draw_label(
        c, layout.BIC_SUP_X, layout.BIC_SUP_Y + dy, texts.SUP_BIC,
        layout.FONT, layout.SIZE_SUP,
    )
    draw_label(
        c, layout.BIC_COLON_X, layout.BIC_LABEL_Y + dy, texts.COLON,
        layout.FONT, layout.SIZE_FIELD,
    )
    if not doc.card.bic:
        return
    draw_value(
        c, layout.BIC_X, layout.BIC_LABEL_Y + dy, doc.card.bic,
        layout.FONT, layout.SIZE_FIELD,
    )
