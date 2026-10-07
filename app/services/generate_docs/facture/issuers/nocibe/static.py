from . import layout, paint

# ----------------------------------------------------------------------

def draw(c, doc):
    paint.draw_rect(c, 0, 0, layout.PAGE_W, layout.PAGE_H, fill_color=(1.0, 1.0, 1.0))
