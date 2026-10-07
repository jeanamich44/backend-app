from reportlab.lib.colors import HexColor

from .. import copy, layout
from ..paint import draw_rect, draw_static_block, draw_string

# ----------------------------------------------------------------------


def draw(c, doc):
    f = doc.footer

    if f.numeros_title == copy.NUMEROS_TITLE:
        draw_static_block(c, 14)
    else:
        c.setFillColor(HexColor(layout.COLOR_BLUE_DARK))
        draw_string(c, 260.40, 493.00, f.numeros_title, layout.FONT_BOLD, 6.84)

    if f.numeros_subtitle == copy.NUMEROS_SUBTITLE:
        draw_static_block(c, 1)
    else:
        c.setFillColor(HexColor(layout.COLOR_BLACK))
        draw_string(c, 108.48, 508.96, f.numeros_subtitle, layout.FONT_ITALIC, 5.88)

    draw_rect(c, 51.36, 528.28, 225.96, 75.60, fill_color=layout.COLOR_GREY_BOXES)
    draw_rect(c, 298.56, 528.28, 223.80, 75.60, fill_color=layout.COLOR_GREY_BOXES)

    default_boxes = (
        f.sinistre_header == copy.SINISTRE_HEADER
        and f.assistance_header == copy.ASSISTANCE_HEADER
        and f.sinistre_intro == copy.SINISTRE_INTRO
        and f.assistance_intro == copy.ASSISTANCE_INTRO
        and f.sinistre_service == copy.SINISTRE_SERVICE
        and f.sinistre_mail_label == copy.SINISTRE_MAIL_LABEL
        and f.sinistre_mail_val == copy.SINISTRE_MAIL_VAL
        and f.assistance_service == copy.ASSISTANCE_SERVICE
        and f.sinistre_tel_label == copy.SINISTRE_TEL_LABEL
        and f.assistance_france == copy.ASSISTANCE_FRANCE
        and f.assistance_etranger == copy.ASSISTANCE_ETRANGER
        and f.sinistre_horaires == copy.SINISTRE_HORAIRES
    )

    if default_boxes:
        for b in (2, 5, 6, 7, 9, 11, 12, 29):
            draw_static_block(c, b)
    else:
        c.setFillColor(HexColor(layout.COLOR_RED_TITLE))
        draw_string(c, 137.52, 526.36, f.sinistre_header, layout.FONT_BOLD, 6.84)
        draw_string(c, 370.20, 526.36, f.assistance_header, layout.FONT_BOLD, 6.84)

        c.setFillColor(HexColor(layout.COLOR_BLACK))
        draw_string(c, 90.60, 534.40, f.sinistre_intro, layout.FONT_REGULAR, 5.88)
        draw_string(c, 304.32, 543.88, f.assistance_intro, layout.FONT_REGULAR, 5.88)
        draw_string(c, 130.08, 545.20, f.sinistre_service, layout.FONT_REGULAR, 5.88)

        c.setFillColor(HexColor(layout.COLOR_BLUE_DARK))
        draw_string(c, 152.40, 554.44, f.sinistre_mail_label, layout.FONT_BOLD, 5.88)

        c.setFillColor(HexColor(layout.COLOR_BLACK))
        draw_string(c, 131.64, 564.64, f.sinistre_mail_val, layout.FONT_REGULAR, 5.88)
        draw_string(c, 382.32, 561.04, f.assistance_service, layout.FONT_REGULAR, 5.88)

        c.setFillColor(HexColor(layout.COLOR_BLUE_DARK))
        draw_string(c, 126.60, 577.36, f.sinistre_tel_label, layout.FONT_BOLD, 5.88)
        draw_string(c, 370.58, 577.36, f.assistance_france, layout.FONT_BOLD, 5.88)
        draw_string(c, 365.64, 586.12, f.assistance_etranger, layout.FONT_BOLD, 5.88)

        c.setFillColor(HexColor(layout.COLOR_BLACK))
        draw_string(c, 53.16, 597.52, f.sinistre_horaires, layout.FONT_REGULAR, 5.88)
