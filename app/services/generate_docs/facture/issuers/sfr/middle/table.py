from .. import copy as texts
from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.middle_table:
        return
    card = doc.card
    font = layout.FONT
    col = layout.COLOR_TEXT

    paint.draw_string(c, layout.TABLE_HEAD_X_NUM, layout.TABLE_HEAD_Y, texts.COL_NUM_LIGNE, font, layout.SIZE_TEXT_MD, col, bold=True)
    paint.draw_string(c, layout.TABLE_HEAD_X_DESC, layout.TABLE_HEAD_Y, texts.COL_DESCRIPTION, font, layout.SIZE_TEXT_MD, col, bold=True)
    paint.draw_string(c, layout.TABLE_HEAD_X_DATE, layout.TABLE_HEAD_Y, texts.COL_DATE, font, layout.SIZE_TEXT_MD, col, bold=True)
    paint.draw_string(c, 528.61, 331.43, texts.COL_MONTANT_L1, font, layout.SIZE_TEXT_SM, col, bold=True)
    paint.draw_string(c, 535.18, 339.20, texts.COL_MONTANT_L2, font, layout.SIZE_TEXT_SM, col, bold=True)

    paint.fill_rect(c, layout.BANNER_X0, 343.98, layout.BANNER_X1, 344.58, col)

    items = card.items or []
    for idx, it in enumerate(items[: layout.MAX_ITEMS]):
        y_row = layout.ROW_Y0 + idx * layout.ROW_PITCH
        if it.numero_ligne:
            paint.draw_string(c, layout.TABLE_HEAD_X_NUM, y_row, it.numero_ligne, font, layout.SIZE_TEXT_SM, col)
        if it.description:
            paint.draw_string(c, layout.TABLE_HEAD_X_DESC, y_row, it.description, font, layout.SIZE_TEXT_SM, col, max_width=270.0)
        if it.date:
            paint.draw_string(c, layout.TABLE_HEAD_X_DATE, y_row, it.date, font, layout.SIZE_TEXT_SM, col)
        if it.montant_ttc:
            paint.draw_right(c, layout.TABLE_HEAD_X_MONTANT, y_row, it.montant_ttc, font, layout.SIZE_TEXT_SM, col)

    x0 = layout.BANNER_X0
    x1 = layout.BANNER_X1

    paint.fill_rect(c, x0, layout.TOTAL_HT_Y, x1, layout.TOTAL_HT_Y + layout.TOTAL_ROW_H, layout.COLOR_GRAY_ROW)
    paint.fill_rect(c, x0, layout.TOTAL_HT_Y, x1, layout.TOTAL_HT_Y + 0.6, col)

    paint.draw_string(c, 46.43, layout.TOTAL_TEXT_Y_HT, texts.TOTAL_HT_LABEL, font, layout.SIZE_TEXT_LG, col)
    paint.draw_right(c, layout.TOTAL_VAL_X, layout.TOTAL_VAL_Y_HT, card.total_facture_ht, font, layout.SIZE_TEXT_MD, col)

    paint.fill_rect(c, x0, layout.TOTAL_TTC_Y, x1, layout.TOTAL_TTC_Y + layout.TOTAL_ROW_H, layout.COLOR_GRAY_ROW)
    paint.fill_rect(c, x0, layout.TOTAL_TTC_Y, x1, layout.TOTAL_TTC_Y + 0.6, col)

    paint.draw_string(c, 46.43, layout.TOTAL_TEXT_Y_TTC, texts.TOTAL_TTC_LABEL, font, layout.SIZE_TEXT_LG, col)
    paint.draw_right(c, layout.TOTAL_VAL_X, layout.TOTAL_VAL_Y_TTC, card.total_facture_ttc, font, layout.SIZE_TEXT_MD, col)

    if card.mention_encaissement:
        paint.draw_string(c, layout.ENCAISSEMENT_X, layout.ENCAISSEMENT_Y, card.mention_encaissement, font, layout.SIZE_TEXT_SM, col)
