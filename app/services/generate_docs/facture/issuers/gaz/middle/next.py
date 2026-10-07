"""Colonne droite haut : prochaine facture + télé-relevé."""

from .. import copy as texts
from .. import layout, rules
from ..chrome.middle_paths import LINE_W, NEXT_BOX_OPS, NEXT_RULE1_OPS, NEXT_RULE2_OPS, STROKE_W
from ..paint import draw_image, draw_string, fill, stroke_ops


def draw(c, doc):
    if not doc.visible.middle_next:
        return
    stroke_ops(c, NEXT_BOX_OPS, layout.BLUE, STROKE_W, cap=0)
    stroke_ops(c, NEXT_RULE1_OPS, layout.BLUE, LINE_W, cap=0)
    stroke_ops(c, NEXT_RULE2_OPS, layout.BLUE, LINE_W, cap=0)
    draw_image(
        c, layout.NEXT_ICON,
        layout.NEXT_ICON_X, layout.NEXT_ICON_Y,
        layout.NEXT_ICON_S, layout.NEXT_ICON_S,
    )
    fill(c, layout.COLOR_BLUE)
    draw_string(
        c, 459.46881103515625, 358.1141357421875,
        texts.NEXT_LABEL, layout.FONT_BOLD, layout.SIZE_PREST,
        max_width=90,
    )
    draw_string(
        c, 464.4591369628906, 383.07769775390625,
        texts.TELE_LABEL, layout.FONT_BOLD, layout.SIZE_PREST,
        max_width=90,
    )
    draw_string(
        c, 477.9200134277344, 407.13494873046875,
        texts.DETAIL_P2, layout.FONT, layout.SIZE_BODY,
        max_width=50,
    )
    fill(c, layout.COLOR_CYAN)
    draw_string(
        c, 447.0, 366.8900146484375,
        rules.next_invoice_line(doc.card), layout.FONT_H, layout.SIZE_HELV,
        max_width=120,
    )
    draw_string(
        c, 446.0, 392.8900146484375,
        rules.each_month_line(doc.card), layout.FONT_H, layout.SIZE_HELV,
        max_width=120,
    )
