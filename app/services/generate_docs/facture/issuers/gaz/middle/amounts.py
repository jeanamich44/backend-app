"""Colonne gauche : gaz, prestations, TTC, barre montant."""

from .. import copy as texts
from .. import layout, rules
from ..chrome.middle_paths import (
    AMOUNTS_BOT_OPS,
    AMOUNTS_TOP_OPS,
    STROKE_W,
    TOTAL_LEFT_OPS,
    TOTAL_PILL_OPS,
    TOTAL_RIGHT_OPS,
)
from ..paint import draw_image, draw_right, draw_string, fill, fill_ops, stroke_ops


def draw(c, doc):
    if not doc.visible.middle_amounts:
        return
    stroke_ops(c, AMOUNTS_TOP_OPS, layout.BLUE, STROKE_W, cap=0)
    stroke_ops(c, AMOUNTS_BOT_OPS, layout.BLUE, STROKE_W, cap=0)
    fill_ops(c, TOTAL_LEFT_OPS, layout.BLUE, even_odd=True)
    fill_ops(c, TOTAL_RIGHT_OPS, layout.BLUE, even_odd=True)
    fill_ops(c, TOTAL_PILL_OPS, (1.0, 1.0, 1.0), even_odd=True)
    draw_image(
        c, layout.GAS_ICON,
        layout.GAS_ICON_X, layout.GAS_ICON_Y,
        layout.GAS_ICON_S, layout.GAS_ICON_S,
    )
    card = doc.card
    fill(c, layout.COLOR_BLUE)
    draw_string(
        c, 70.86602783203125, 350.51641845703125,
        texts.GAZ_LABEL, layout.FONT_BOLD, layout.SIZE_AMOUNT,
        max_width=80,
    )
    draw_string(
        c, 341.489501953125, 350.51641845703125,
        texts.PLUS, layout.FONT_BOLD, layout.SIZE_AMOUNT,
    )
    draw_right(
        c, layout.AMOUNT_RIGHT, 350.51641845703125,
        rules.format_euro(card.montant_gaz),
        layout.FONT_BOLD, layout.SIZE_AMOUNT, max_width=70,
    )
    draw_string(
        c, 70.86602783203125, 372.287353515625,
        texts.PREST_LABEL, layout.FONT_BOLD, layout.SIZE_PREST,
        max_width=80,
    )
    draw_string(
        c, 341.489501953125, 373.19363403320312,
        texts.PLUS, layout.FONT_BOLD, layout.SIZE_AMOUNT,
    )
    draw_right(
        c, layout.AMOUNT_RIGHT, 373.19363403320312,
        rules.format_euro(card.montant_prestations),
        layout.FONT_BOLD, layout.SIZE_AMOUNT, max_width=70,
    )
    fill(c, layout.COLOR)
    draw_string(
        c, 51.023590087890625, 401.3812561035156,
        texts.TTC_LABEL, layout.FONT_BOLD, layout.SIZE_AMOUNT,
        max_width=80,
    )
    draw_string(
        c, 332.9854736328125, 401.3812561035156,
        texts.EQUAL, layout.FONT_BOLD, layout.SIZE_AMOUNT,
    )
    draw_right(
        c, layout.AMOUNT_RIGHT, 401.3812561035156,
        rules.format_ttc(card),
        layout.FONT_BOLD, layout.SIZE_AMOUNT, max_width=70,
    )
    draw_string(
        c, 62.27349090576172, 413.9040832519531,
        rules.hors_tva_line(card), layout.FONT, layout.SIZE_BODY,
        max_width=280,
    )
    draw_string(
        c, 62.273475646972656, 423.10418701171875,
        rules.tva_line(card), layout.FONT, layout.SIZE_BODY,
        max_width=280,
    )
    draw_string(
        c, 111.0, 400.8900146484375,
        rules.echeance_line(card), layout.FONT_H, layout.SIZE_HELV_ECHEANCE,
        max_width=160,
    )
    fill(c, layout.COLOR_WHITE)
    draw_string(
        c, 51.023529052734375, 495.0820007324219,
        texts.TOTAL_LABEL, layout.FONT_BOLD, layout.SIZE_TOTAL,
        max_width=200,
    )
    draw_string(
        c, 160.0, 493.8900146484375,
        rules.preleve_line(card), layout.FONT_HB, layout.SIZE_HELV_PRELEVE,
        max_width=180,
    )
    fill(c, layout.COLOR_BLUE)
    draw_right(
        c, layout.AMOUNT_RIGHT, 495.0820007324219,
        rules.format_ttc(card),
        layout.FONT_BOLD, layout.SIZE_TOTAL, max_width=80,
    )
