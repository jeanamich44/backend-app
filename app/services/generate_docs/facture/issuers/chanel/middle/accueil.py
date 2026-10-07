from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.middle_accueil:
        return
    paint.draw_line(c, layout.DIVIDER_LINE_X1, layout.DIVIDER_LINE_Y, layout.DIVIDER_LINE_X2, layout.DIVIDER_LINE_Y, layout.DIVIDER_LINE_W)
    paint.draw_text(c, layout.ACCUEIL_X, layout.ACCUEIL_Y, doc.middle.accueil_text, layout.FONT_REGULAR, layout.MIDDLE_SIZE)
