from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.footer_notes:
        return
    card = doc.card
    if card.footer_note:
        paint.draw_string(
            c,
            layout.FOOTER_X,
            layout.FOOTER_Y_NOTE,
            card.footer_note,
            layout.FONT,
            layout.SIZE_TEXT_SM,
            layout.COLOR_TEXT,
        )
