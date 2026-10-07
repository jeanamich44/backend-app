from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    paint.fill_rect(
        c,
        layout.CARD_X0,
        layout.CARD_Y0,
        layout.CARD_X1,
        layout.CARD_Y1,
        layout.COLOR_WHITE,
    )
