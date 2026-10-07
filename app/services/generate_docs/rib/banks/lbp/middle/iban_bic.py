"""Cases IBAN et BIC."""

from .. import copy as texts
from .. import layout
from ..paint import draw_centred, draw_string, fill, stroke_line


def draw(c, doc, dy=0):
    if not doc.visible.middle_iban_bic:
        return
    card = doc.card
    for x0, y0, x1, y1, width in layout.IBAN_LINES:
        stroke_line(c, x0, y0 + dy, x1, y1 + dy, width)

    fill(c, layout.BRAND_TITLE_COLOR)
    draw_string(
        c, layout.IBAN_TITLE_X, layout.IBAN_TITLE_Y + dy,
        texts.IBAN_TITLE, layout.TABLE_VAL_FONT, layout.IBAN_TITLE_SIZE,
    )
    draw_string(
        c, layout.BIC_TITLE_X, layout.IBAN_TITLE_Y + dy,
        texts.BIC_TITLE, layout.TABLE_VAL_FONT, layout.IBAN_TITLE_SIZE,
    )

    fill(c, layout.LINE_BLACK)
    if card.iban:
        draw_centred(
            c, layout.IBAN_CX, layout.IBAN_VAL_Y + dy, card.iban,
            layout.TABLE_VAL_FONT, layout.IBAN_VAL_SIZE,
            max_width=layout.IBAN_W,
        )
    if card.bic:
        draw_centred(
            c, layout.BIC_CX, layout.IBAN_VAL_Y + dy, card.bic,
            layout.TABLE_VAL_FONT, layout.IBAN_VAL_SIZE,
            max_width=layout.IBAN_W,
        )
