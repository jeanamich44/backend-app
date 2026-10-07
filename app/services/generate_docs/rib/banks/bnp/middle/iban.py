"""Case IBAN : cadre vecteur + label + valeur."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill, stroke_rect


def draw(c, doc, dy=0):
    if not doc.visible.middle_iban:
        return
    x0, y0, x1, y1 = layout.IBAN_BOX
    stroke_rect(c, x0, y0 + dy, x1, y1 + dy, layout.BOX_STROKE, fill_hex="#ffffff")
    fill(c, layout.COLOR)
    draw_string(
        c, layout.LABEL_IBAN_XY[0], layout.LABEL_IBAN_XY[1] + dy,
        texts.LABEL_IBAN, layout.FONT, layout.FONT_SIZE,
    )
    draw_string(
        c, layout.REF_IBAN_XY[0], layout.REF_IBAN_XY[1] + dy,
        texts.REF_1, layout.FONT, layout.FONT_REF_SIZE,
    )
    if doc.card.iban:
        draw_string(
            c, layout.IBAN_X, layout.IBAN_Y + dy, doc.card.iban,
            layout.FONT_BOLD, layout.FONT_SIZE,
            max_width=layout.IBAN_W,
        )
