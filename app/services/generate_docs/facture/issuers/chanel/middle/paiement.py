from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.middle_paiement:
        return
    paint.draw_right_text(c, layout.RIGHT_MARGIN, layout.PAIEMENT_Y, doc.middle.paiement, layout.FONT_REGULAR, layout.MIDDLE_SIZE)
