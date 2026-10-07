"""BIC : label outlined + valeur."""

from .. import layout
from ..paint import draw_label, draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_bic:
        return
    draw_label(c, layout.LABEL_BIC)
    text = doc.card.bic
    if text:
        fill(c, layout.COLOR_TEXT)
        draw_string(
            c, layout.BIC_X, layout.BIC_Y, text,
            layout.FONT, layout.FONT_SIZE,
            max_width=layout.BIC_W,
        )
