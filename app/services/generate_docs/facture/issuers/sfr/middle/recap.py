from .. import copy as texts
from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.middle_recap:
        return
    card = doc.card
    font = layout.FONT
    sz = layout.SIZE_TEXT_MD
    col = layout.COLOR_TEXT

    paint.fill_rect(
        c,
        layout.RECAP_X_LEFT,
        layout.RECAP_Y_TOP,
        layout.RECAP_X_RIGHT,
        layout.RECAP_Y_TOP + 0.6,
        layout.COLOR_GRAY_TABLE,
    )
    paint.fill_rect(
        c,
        layout.RECAP_X_LEFT,
        layout.RECAP_Y_BOT,
        layout.RECAP_X_RIGHT,
        layout.RECAP_Y_BOT + 0.6,
        layout.COLOR_GRAY_TABLE,
    )
    paint.fill_rect(
        c,
        layout.RECAP_X_LEFT,
        layout.RECAP_Y_TOP,
        layout.RECAP_X_LEFT + 0.59,
        layout.RECAP_Y_BOT + 0.6,
        layout.COLOR_GRAY_TABLE,
    )
    paint.fill_rect(
        c,
        layout.RECAP_X_RIGHT - 0.59,
        layout.RECAP_Y_TOP,
        layout.RECAP_X_RIGHT,
        layout.RECAP_Y_BOT + 0.6,
        layout.COLOR_GRAY_TABLE,
    )

    paint.fill_rect(c, 279.45, 257.94, layout.RECAP_X_RIGHT, 258.54, layout.COLOR_TEXT)

    lbl_x = layout.RECAP_X_LABEL
    val_x = layout.RECAP_X_VALUE

    y1 = 199.39
    paint.draw_string(c, lbl_x, y1, texts.RECAP_L1_LABEL, font, sz, col)
    paint.draw_right(c, val_x, y1, card.montant_ht, font, sz, col)

    y2 = 210.74
    tva_lbl = f"Montant total TVA ({card.taux_tva}) :"
    paint.draw_string(c, lbl_x, y2, tva_lbl, font, sz, col)
    paint.draw_right(c, val_x, y2, card.montant_tva, font, sz, col)

    y3 = 222.09
    paint.draw_string(c, lbl_x, y3, texts.RECAP_L3_LABEL, font, sz, col)
    paint.draw_right(c, val_x, y3, card.total_ttc, font, sz, col)

    y4 = 233.44
    paint.draw_string(c, lbl_x, y4, texts.RECAP_L4_LABEL, font, sz, col)
    paint.draw_right(c, val_x, y4, card.solde_ht, font, sz, col)

    y5 = 244.80
    paint.draw_string(c, lbl_x, y5, texts.RECAP_L5_LABEL, font, sz, col)
    paint.draw_right(c, val_x, y5, card.solde_ttc, font, sz, col)

    y6 = 256.15
    paint.draw_string(c, lbl_x, y6, texts.RECAP_L6_LABEL, font, sz, col)
    paint.draw_right(c, val_x, y6, card.net_a_payer_ht, font, sz, col)

    y7 = 267.50
    paint.draw_string(c, lbl_x, y7, texts.RECAP_L7_LABEL, font, sz, col)
    paint.draw_right(c, val_x, 268.10, card.net_a_payer_ttc, font, sz, col)
