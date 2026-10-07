from .. import layout
from ..paint import draw_line, draw_string, fill

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.middle_delivery:
        return
    fill(c, layout.COLOR_BLACK)
    draw_string(c, layout.DELIVERY_LABEL_X, layout.DELIVERY_LABEL_Y, doc.middle.label_delivery, layout.FONT_BOLD, layout.FONT_SIZE_BODY)
    draw_line(c, layout.DELIVERY_LINE_X1, layout.DELIVERY_LINE_Y, layout.DELIVERY_LINE_X2, layout.DELIVERY_LINE_Y, layout.LINE_WIDTH, layout.COLOR_BLACK, cap=1)
    fill(c, layout.COLOR_GREY)
    draw_string(c, layout.DELIVERY_VAL_X, layout.DELIVERY_VAL_Y, doc.middle.val_delivery, layout.FONT_REGULAR, layout.FONT_SIZE_BODY)
