from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc, shift: float = 0.0):
    y_ht = layout.TOTAL_HT_Y + shift
    paint.draw_text(c, layout.TOTAL_LABEL_X, y_ht, "Total HT", layout.FONT_BOLD, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.TOTAL_VALUE_X, y_ht, doc.card.total_ht, layout.FONT_BOLD, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)

    y_d7 = layout.TOTAL_LINE_D7_Y + shift
    paint.draw_line(c, 468.94, y_d7, 580.04, y_d7, width=layout.LINE_WIDTH, color=layout.COLOR_LINE)

    y_tva = layout.TOTAL_TVA_Y + shift
    paint.draw_text(c, layout.TOTAL_LABEL_X, y_tva, "Total TVA", layout.FONT_BOLD, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.TOTAL_VALUE_X, y_tva, doc.card.total_tva, layout.FONT_BOLD, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)

    y_d8 = layout.TOTAL_LINE_D8_Y + shift
    paint.draw_line(c, 469.19, y_d8, 579.54, y_d8, width=layout.LINE_WIDTH, color=layout.COLOR_LINE)

    y_ttc = layout.TOTAL_TTC_Y + shift
    paint.draw_text(c, layout.TOTAL_LABEL_X + 0.20, y_ttc, "Total TTC", layout.FONT_BOLD, 9.01, layout.COLOR_MAGENTA, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.TOTAL_TTC_VALUE_X, y_ttc, doc.card.total_ttc, layout.FONT_BOLD, 9.01, layout.COLOR_MAGENTA, char_space=layout.CHAR_SPACE_ARIAL)

    y_d9 = layout.TOTAL_LINE_D9_Y + shift
    paint.draw_line(c, 40.75, y_d9, 579.71, y_d9, width=layout.LINE_WIDTH, color=layout.COLOR_LINE)
