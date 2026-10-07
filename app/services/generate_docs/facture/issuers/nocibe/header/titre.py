from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    if doc.card.facture_num:
        paint.draw_text(
            c,
            layout.TITRE_NUM_X,
            layout.TITRE_NUM_Y,
            doc.card.facture_num,
            layout.FONT_BOLD,
            layout.TITRE_NUM_SIZE,
            layout.COLOR_BLACK,
            char_space=layout.CHAR_SPACE_TITLE,
        )
    if doc.card.date_emission:
        paint.draw_text(
            c,
            layout.TITRE_DATE_X,
            layout.TITRE_DATE_Y,
            doc.card.date_emission,
            layout.FONT_REGULAR,
            layout.TITRE_DATE_SIZE,
            layout.COLOR_BLACK,
            char_space=layout.CHAR_SPACE_DATE,
        )
