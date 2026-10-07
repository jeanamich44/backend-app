from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.header_logo:
        return
    paint.draw_image(
        c,
        layout.LOGO_FILE,
        layout.LOGO_X,
        layout.LOGO_Y,
        layout.LOGO_W,
        layout.LOGO_H,
    )
