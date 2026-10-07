from reportlab.lib.colors import HexColor

from .. import copy, layout
from ..paint import draw_centred, draw_rect, draw_static_block, draw_string, y_up

# ----------------------------------------------------------------------


def draw(c, doc):
    m = doc.middle

    draw_rect(c, 99.36, 431.20, 423.00, 26.28, fill_color=layout.COLOR_GREY_BOXES)

    c.saveState()
    c.setFillColor(HexColor(layout.COLOR_BLACK))
    p9 = c.beginPath()
    p9.rect(98.88, y_up(457.84), 0.96, 27.12)
    p9.rect(521.76, y_up(457.84), 0.96, 26.16)
    c.drawPath(p9, stroke=0, fill=1)

    p10 = c.beginPath()
    p10.rect(99.84, y_up(431.68), 422.88, 0.96)
    p10.rect(99.84, y_up(457.84), 422.88, 0.96)
    c.drawPath(p10, stroke=0, fill=1)
    c.restoreState()

    if (
        m.assureur_title == copy.ASSUREUR_TITLE
        and m.assureur_nom == copy.ASSUREUR_NOM
        and m.assureur_adresse == copy.ASSUREUR_ADRESSE
    ):
        draw_static_block(c, 10)
        draw_static_block(c, 17)
    else:
        c.setFillColor(HexColor(layout.COLOR_RED_TITLE))
        draw_string(c, 56.04, 436.48, m.assureur_title, layout.FONT_BOLD, 5.88)
        c.setFillColor(HexColor(layout.COLOR_BLUE_DARK))
        draw_centred(c, 310.86, 436.48, m.assureur_nom, layout.FONT_REGULAR, 5.88)
        draw_centred(c, 310.86, 445.96, m.assureur_adresse, layout.FONT_REGULAR, 5.88)
