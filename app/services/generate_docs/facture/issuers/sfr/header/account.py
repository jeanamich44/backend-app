from .. import copy as texts
from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.header_account:
        return
    card = doc.card
    font = layout.FONT
    sz = layout.SIZE_TEXT_SM
    col = layout.COLOR_TEXT

    paint.draw_string(c, 72.71, layout.ACCOUNT_Y_TITULAIRE, texts.ACCOUNT_TITULAIRE_LABEL, font, sz, col)
    paint.draw_string(c, layout.ACCOUNT_VAL_X, layout.ACCOUNT_Y_TITULAIRE, card.titulaire_ligne, font, sz, col)

    paint.draw_string(c, 57.18, layout.ACCOUNT_Y_COMPTE, texts.ACCOUNT_COMPTE_LABEL, font, sz, col)
    paint.draw_string(c, layout.ACCOUNT_VAL_X, layout.ACCOUNT_Y_COMPTE, card.num_compte_client, font, sz, col)

    facture_ref = f"{card.date_facture} - {card.num_facture}"
    paint.draw_string(c, 60.77, layout.ACCOUNT_Y_FACTURE, texts.ACCOUNT_FACTURE_LABEL, font, sz, col)
    paint.draw_string(c, layout.ACCOUNT_VAL_X, layout.ACCOUNT_Y_FACTURE, facture_ref, font, sz, col)
