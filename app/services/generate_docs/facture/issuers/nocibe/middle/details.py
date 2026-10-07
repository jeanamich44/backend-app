from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc, shift: float = 0.0):
    paint.draw_line(c, 41.50, 541.34 + shift, 286.97, 541.34 + shift, width=layout.LINE_WIDTH, color=layout.COLOR_LINE)
    paint.draw_line(c, 286.76, 541.35 + shift, 286.76, 589.40 + shift, width=layout.LINE_WIDTH, color=layout.COLOR_LINE)
    paint.draw_line(c, 41.50, 541.35 + shift, 41.50, 589.40 + shift, width=layout.LINE_WIDTH, color=layout.COLOR_LINE)
    paint.draw_line(c, 41.13, 589.23 + shift, 287.35, 589.37 + shift, width=layout.LINE_WIDTH, color=layout.COLOR_LINE)
    paint.draw_text(c, layout.BOX_TVA_TITLE_X, layout.BOX_TVA_TITLE_Y + shift, "Détail TVA", layout.FONT_BOLD, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.BOX_TVA_HDR_RATE_X, layout.BOX_TVA_HDR_Y + shift, "Taux TVA", layout.FONT_BOLD, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.BOX_TVA_HDR_BASE_X, layout.BOX_TVA_HDR_Y + shift, "Base HT", layout.FONT_BOLD, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.BOX_TVA_HDR_AMT_X, layout.BOX_TVA_HDR_Y + shift, "Montant TVA", layout.FONT_BOLD, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.BOX_TVA_VAL_RATE_X, layout.BOX_TVA_VAL_Y + shift + 0.07, doc.card.tva_rate_pct, layout.FONT_REGULAR, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.BOX_TVA_VAL_BASE_X, layout.BOX_TVA_VAL_Y + shift - 0.07, doc.card.tva_base_ht, layout.FONT_REGULAR, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.BOX_TVA_VAL_AMT_X, layout.BOX_TVA_VAL_Y + shift - 0.07, doc.card.tva_montant, layout.FONT_REGULAR, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)

    paint.draw_line(c, 333.30, 540.45 + shift, 578.77, 540.45 + shift, width=layout.LINE_WIDTH, color=layout.COLOR_LINE)
    paint.draw_line(c, 578.55, 540.45 + shift, 578.55, 588.50 + shift, width=layout.LINE_WIDTH, color=layout.COLOR_LINE)
    paint.draw_line(c, 333.29, 540.45 + shift, 333.29, 588.50 + shift, width=layout.LINE_WIDTH, color=layout.COLOR_LINE)
    paint.draw_line(c, 332.92, 588.33 + shift, 579.14, 588.47 + shift, width=layout.LINE_WIDTH, color=layout.COLOR_LINE)
    paint.draw_text(c, layout.BOX_PAY_TITLE_X, layout.BOX_PAY_TITLE_Y + shift, "Règlements", layout.FONT_BOLD, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.BOX_PAY_HDR_DATE_X, layout.BOX_PAY_HDR_Y + shift, "Date", layout.FONT_BOLD, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.BOX_PAY_HDR_MODE_X, layout.BOX_PAY_HDR_Y + shift, "Règlement", layout.FONT_BOLD, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.BOX_PAY_HDR_AMT_X, layout.BOX_PAY_HDR_Y + shift, "Montant ", layout.FONT_BOLD, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.BOX_PAY_VAL_DATE_X, layout.BOX_PAY_VAL_Y + shift, doc.card.reglement_date, layout.FONT_REGULAR, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.BOX_PAY_VAL_MODE_X, layout.BOX_PAY_VAL_Y + shift, doc.card.reglement_mode, layout.FONT_REGULAR, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)
    paint.draw_text(c, layout.BOX_PAY_VAL_AMT_X, layout.BOX_PAY_VAL_Y + shift, doc.card.reglement_montant, layout.FONT_REGULAR, 9.01, layout.COLOR_BLACK, char_space=layout.CHAR_SPACE_ARIAL)

    y_d18 = layout.LINE_D18_Y + shift
    paint.draw_line(c, 40.75, y_d18, 579.71, y_d18, width=layout.LINE_WIDTH, color=layout.COLOR_LINE)
