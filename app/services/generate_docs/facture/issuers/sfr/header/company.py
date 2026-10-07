from .. import copy as texts
from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.header_company:
        return
    card = doc.card
    font = layout.FONT
    sz = layout.SIZE_TEXT_SM
    col = layout.COLOR_TEXT

    y0 = layout.COMPANY_Y0
    paint.draw_string(c, layout.COMPANY_LABEL_X, y0, texts.COMPANY_BRAND, font, sz, col)
    paint.draw_string(c, layout.COMPANY_VAL_X, y0, card.company_name, font, sz, col)

    y1 = y0 + layout.COMPANY_LINE_H
    paint.draw_string(c, 78.09, y1, texts.COMPANY_INFO, font, sz, col)
    paint.draw_string(c, layout.COMPANY_VAL_X, y1, card.company_address, font, sz, col)

    y2 = y1 + layout.COMPANY_LINE_H
    paint.draw_string(c, layout.COMPANY_VAL_X, y2, card.company_capital_rcs, font, sz, col)

    y3 = y2 + layout.COMPANY_LINE_H
    paint.draw_string(c, layout.COMPANY_VAL_X, y3, card.company_tva_ape, font, sz, col)
