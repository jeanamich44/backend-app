from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    paint.draw_rect(
        c,
        layout.COMMANDE_BG_X,
        layout.COMMANDE_BG_Y,
        layout.COMMANDE_BG_W,
        layout.COMMANDE_BG_H,
        fill_color=layout.COLOR_CMD_BG,
    )
    lines = [
        doc.card.commande_date,
        doc.card.commande_mode,
        doc.card.commande_expedition,
        doc.card.commande_etat,
    ]
    for i, text in enumerate(lines):
        if text:
            y = layout.COMMANDE_TEXT_Y + (i * layout.COMMANDE_TEXT_LEADING)
            paint.draw_text(
                c,
                layout.COMMANDE_TEXT_X,
                y,
                text,
                layout.FONT_SANS,
                layout.COMMANDE_TEXT_SIZE,
                layout.COLOR_GREY,
                char_space=layout.CHAR_SPACE_SANS,
            )
