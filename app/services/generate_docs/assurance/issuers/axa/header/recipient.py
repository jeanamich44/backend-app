from reportlab.lib.colors import HexColor

from .. import layout
from ..paint import draw_string

# ----------------------------------------------------------------------


def draw(c, doc):
    h = doc.header
    c.setFillColor(HexColor(layout.COLOR_BLACK))
    draw_string(c, 300.00, 92.00, h.destinataire_l1, layout.FONT_CARLITO, 5.88)
    draw_string(c, 300.00, 100.00, h.destinataire_l2, layout.FONT_CARLITO, 5.88)
    draw_string(c, 300.00, 109.00, h.destinataire_l3, layout.FONT_REGULAR, 5.88)
    draw_string(c, 439.32, 128.92, h.edition_date, layout.FONT_REGULAR, 5.88)
