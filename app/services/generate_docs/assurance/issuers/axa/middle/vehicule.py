from reportlab.lib.colors import HexColor

from .. import copy, layout
from ..paint import draw_static_block, draw_string, y_up

# ----------------------------------------------------------------------


def draw(c, doc):
    m = doc.middle

    if m.vehicule_title == copy.VEHICULE_TITLE:
        draw_static_block(c, 30)
    else:
        c.setFillColor(HexColor(layout.COLOR_BLUE_DARK))
        draw_string(c, 255.36, 335.80, m.vehicule_title, layout.FONT_BOLD, 6.84)

    c.saveState()
    c.setFillColor(HexColor(layout.COLOR_GREY_BOXES))
    p4 = c.beginPath()
    p4.rect(51.36, y_up(378.16), 218.40, 27.72)
    p4.rect(288.72, y_up(378.16), 233.64, 27.72)
    c.drawPath(p4, stroke=0, fill=1)
    c.restoreState()

    if m.info_title == copy.INFO_TITLE:
        draw_static_block(c, 31)
    else:
        c.setFillColor(HexColor(layout.COLOR_RED_TITLE))
        draw_string(c, 52.20, 348.88, m.info_title, layout.FONT_BOLD, 5.88)

    if m.vehicule_subtitle == copy.VEHICULE_SUBTITLE:
        draw_static_block(c, 16)
    else:
        c.setFillColor(HexColor(layout.COLOR_RED_TITLE))
        draw_string(c, 290.04, 348.88, m.vehicule_subtitle, layout.FONT_BOLD, 5.88)

    c.setFillColor(HexColor(layout.COLOR_BLUE_DARK))
    draw_string(c, 52.00, 356.00, f"N\u00b0 client : {m.info_client}", layout.FONT_REGULAR, 5.88)
    draw_string(c, 52.00, 365.00, f"N\u00b0 contrat : {m.info_contrat}", layout.FONT_REGULAR, 5.88)
    draw_string(c, 52.00, 373.00, f"Date d'effet du contrat : {m.info_effet}", layout.FONT_REGULAR, 5.88)
    draw_string(c, 290.00, 356.00, f"Marque et mod\u00e8le : {m.vehicule_marque}", layout.FONT_CARLITO, 5.88)
    draw_string(c, 290.00, 363.00, f"N\u00b0 immatriculation v\u00e9hicule : {m.vehicule_immat}", layout.FONT_CARLITO, 5.88)
