from .. import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    paint.draw_text(c, layout.STORE_LINE_1_X, layout.STORE_LINE_1_Y, doc.header.store_line_1)
    paint.draw_text(c, layout.STORE_LINE_2_X, layout.STORE_LINE_2_Y, doc.header.store_line_2)
