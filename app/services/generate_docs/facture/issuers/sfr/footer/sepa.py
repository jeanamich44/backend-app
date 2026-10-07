from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.footer_sepa:
        return
    card = doc.card
    font = layout.FONT
    sz = layout.SIZE_TEXT_SM
    col = layout.COLOR_TEXT
    x = layout.FOOTER_X

    if card.sepa_ligne1:
        paint.draw_string(c, x, layout.FOOTER_Y_SEPA1, card.sepa_ligne1, font, sz, col)
    if card.sepa_ligne2:
        paint.draw_string(c, x, layout.FOOTER_Y_SEPA2, card.sepa_ligne2, font, sz, col)
