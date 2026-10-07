from .. import copy
from ..layout import CASH_X, CASH_Y
from ..paint import draw_cash_logo, draw_string

# ----------------------------------------------------------------------

def draw(c, doc):
    method = doc.middle.payment_method
    if not method:
        return
    if method == copy.PAYMENT_METHOD:
        draw_cash_logo(c)
    else:
        draw_string(c, "TT0", 14.0, CASH_X, CASH_Y, method)
