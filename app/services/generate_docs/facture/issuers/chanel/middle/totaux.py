from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.middle_totaux:
        return
    paint.draw_right_text(c, layout.RIGHT_MARGIN, layout.TOTAL_HT_Y, doc.middle.total_ht, layout.FONT_REGULAR, layout.MIDDLE_SIZE)
    paint.draw_right_text(c, layout.RIGHT_MARGIN, layout.TOTAL_TVA_Y, doc.middle.total_tva, layout.FONT_REGULAR, layout.MIDDLE_SIZE)
    paint.draw_right_text(c, layout.RIGHT_MARGIN, layout.TOTAL_TTC_Y, doc.middle.total_ttc, layout.FONT_BOLD, layout.MIDDLE_SIZE)
