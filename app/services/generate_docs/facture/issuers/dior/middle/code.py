from .. import copy
from ..layout import CODE_X, CODE_Y
from ..paint import draw_code_stream, draw_string

# ----------------------------------------------------------------------

def draw(c, doc):
    code = doc.middle.code
    if not code:
        return
    if code == copy.CODE:
        draw_code_stream(c)
    else:
        draw_string(c, "TT0", 14.0, CODE_X, CODE_Y, code)
