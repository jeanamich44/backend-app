"""Boîte grise totaux + mode de paiement."""

from .. import copy as texts
from .. import layout, rules
from ..paint import (
    draw_kerned_html, fill, fill_html_rect, html_frame, html_right_x,
)
from .cell import draw_cell

_Y = (-0.5, 10.1, 19.7, 29.3, 38.9, 48.5, 58.1)
_H = (10.6, 9.6, 9.6, 9.6, 9.6, 9.6, 10.6)


def _left_edges(i):
    top = "full" if i == 0 else None
    bottom = "last" if i == 6 else None
    return {"left_outer": True, "right_outer": False, "top": top, "bottom": bottom, "right": False}


def _right_edges(i):
    top = "full" if i == 0 else None
    bottom = "last" if i == 6 else None
    return {
        "left_outer": False, "right_outer": True, "top": top, "bottom": bottom,
        "origin_inset": False, "left": False,
    }


def _tm(i):
    return layout.TM_Y_HEAD if i == 0 else layout.TM_Y


def draw(c, doc):
    if not doc.visible.middle_totals:
        return
    hors, tva, ttc = rules.invoice_totals(doc.card.items)
    card_tot = getattr(doc.card, "total", None)
    if card_tot and str(card_tot).strip():
        parsed = rules.parse_money(card_tot)
        if parsed > 0:
            ttc = parsed
            hors = round(ttc / 1.20, 2)
            tva = round(ttc - hors, 2)
    c.saveState()
    html_frame(c, layout.TOTALS_X, layout.TOTALS_Y)
    c.saveState()
    c.translate(layout.TOTALS_DX, 0)
    fill_html_rect(c, 0, 0, layout.TOTALS_BOX_W, layout.TOTALS_BOX_H, layout.COLOR_GRAY)
    lw, rw = layout.TOTALS_LEFT_W, layout.TOTALS_RIGHT_W
    pay = doc.card.payment
    rows = (
        (0, texts.TOTAL_HT, rules.format_euro(hors), None),
        (1, texts.TOTAL_VAT, rules.format_euro(tva), None),
        (2, None, None, None),
        (3, texts.TOTAL_TTC, rules.format_euro(ttc), None),
        (4, None, None, None),
        (5, texts.PAY_LABEL, rules.format_euro(ttc), pay),
        (6, None, None, None),
    )
    for i, label, amount, method in rows:
        y, h = _Y[i], _H[i]
        c.saveState()
        c.translate(0.5, y)
        draw_cell(c, lw, h, layout.COLOR, **_left_edges(i))
        fill(c, layout.COLOR)
        if label:
            draw_kerned_html(c, 0, _tm(i), label, layout.FONT_BOLD, layout.SIZE_BODY)
        c.restoreState()
        c.saveState()
        c.translate(lw, y)
        draw_cell(c, rw, h, layout.COLOR, **_right_edges(i))
        fill(c, layout.COLOR)
        if method:
            draw_kerned_html(c, 0, _tm(i), method, layout.FONT, layout.SIZE_BODY)
            if amount:
                x = layout.TOTALS_PAY_DX + html_right_x(
                    rw - layout.TOTALS_PAY_DX, amount, layout.FONT, layout.SIZE_BODY, 0,
                )
                draw_kerned_html(c, x, _tm(i), amount, layout.FONT, layout.SIZE_BODY)
        elif amount:
            inset = 0.5
            x = html_right_x(rw, amount, layout.FONT, layout.SIZE_BODY, inset)
            draw_kerned_html(c, x, _tm(i), amount, layout.FONT, layout.SIZE_BODY)
        c.restoreState()
    c.restoreState()
    c.restoreState()
