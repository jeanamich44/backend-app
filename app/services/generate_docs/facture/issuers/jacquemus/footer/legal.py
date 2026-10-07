from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.footer_legal:
        return
    fill(c, layout.COLOR_BLACK)
    lines = getattr(doc.footer, "legal_lines", texts.LEGAL_LINES)
    y = layout.FOOTER_LEGAL_Y
    for line in lines:
        draw_string(c, layout.FOOTER_LEGAL_X, y, line, layout.FONT_BOLD, layout.FONT_SIZE_FOOTER)
        y += layout.FOOTER_LEGAL_LEADING
