from .. import layout
from ..paint import draw_line, draw_string, fill

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.middle_payment:
        return
    fill(c, layout.COLOR_BLACK)
    draw_string(c, layout.PAYMENT_LABEL_X, layout.PAYMENT_LABEL_Y, doc.middle.label_payment, layout.FONT_BOLD, layout.FONT_SIZE_BODY)
    draw_line(c, layout.PAYMENT_LINE_X1, layout.PAYMENT_LINE_Y, layout.PAYMENT_LINE_X2, layout.PAYMENT_LINE_Y, layout.LINE_WIDTH, layout.COLOR_BLACK, cap=1)
    fill(c, layout.COLOR_GREY)
    draw_string(c, layout.PAYMENT_VAL_X, layout.PAYMENT_VAL_Y, doc.middle.val_payment, layout.FONT_REGULAR, layout.FONT_SIZE_BODY)
