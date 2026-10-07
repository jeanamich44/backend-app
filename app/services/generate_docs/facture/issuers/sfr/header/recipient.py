from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.header_recipient:
        return
    card = doc.card
    font = layout.FONT
    sz = layout.SIZE_TEXT_XL
    col = layout.COLOR_TEXT
    x = layout.RECIPIENT_X

    y0 = layout.RECIPIENT_Y0
    paint.draw_string(c, x, y0, card.destinataire_nom, font, sz, col)

    y1 = y0 + layout.RECIPIENT_LINE_H
    paint.draw_string(c, x, y1, card.destinataire_adresse, font, sz, col)

    y2 = y1 + layout.RECIPIENT_LINE_H
    paint.draw_string(c, x, y2, card.destinataire_cp_ville, font, sz, col)
