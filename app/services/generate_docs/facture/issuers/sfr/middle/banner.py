from .. import copy as texts
from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.middle_banner:
        return
    x0 = layout.BANNER_X0
    x1 = layout.BANNER_X1
    y0 = layout.BANNER_Y0
    y1 = layout.BANNER_Y1

    paint.fill_rect(c, x0, y0, x1, y1, layout.COLOR_RED)
    paint.fill_rect(c, x0, y0, x1, y0 + 0.6, layout.COLOR_TEXT)
    paint.fill_rect(c, x0, y1 - 0.59, x1, y1, layout.COLOR_TEXT)

    paint.draw_string(
        c,
        layout.BANNER_TEXT_X,
        layout.BANNER_TEXT_Y,
        texts.BANNER_TITLE,
        layout.FONT,
        layout.SIZE_TEXT_LG,
        layout.COLOR_WHITE,
    )
