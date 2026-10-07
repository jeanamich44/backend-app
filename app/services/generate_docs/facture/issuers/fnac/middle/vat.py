"""Récap TVA, règlement, totaux (cadre fixe sous le tableau)."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_money, draw_string, fill


def _amount(c, web, euro_x, right, y, value, font, size, slot_w, above, below):
    draw_money(
        c, euro_x, y, rules.format_money(value),
        font, size, slot_w, above, below,
    )


def _vat(c, doc, web):
    card = doc.card
    fill(c, layout.COLOR)
    labels = (
        texts.VAT_CODE, texts.VAT_BASE, texts.VAT_TAX,
        texts.VAT_FRAIS, texts.VAT_FRAIS_TVA,
    )
    for x, label in zip(layout.VAT_HEAD_X, labels):
        draw_string(c, x, layout.VAT_HEAD_Y, label, layout.FONT, layout.SIZE_7)
    y = layout.VAT_ROW_Y
    cols = layout.VAT_COLS
    draw_string(c, layout.VAT_CODE_X, y, rules.tva_row_label(card), layout.FONT, layout.SIZE_7)
    ht = rules.recap_ht(card)
    tva = rules.recap_tva(card)
    frais = rules.frais_ht(card)
    tva_f = rules.tva_frais(card)
    slot7 = (layout.EURO_W_7, layout.EURO_ABOVE_7, layout.EURO_BELOW_7)
    _amount(
        c, web, layout.VAT_BASE_EURO_X, layout.VAT_BASE_RIGHT, y, ht,
        layout.FONT, layout.SIZE_7, *slot7,
    )
    _amount(
        c, web, layout.VAT_TAX_EURO_X, layout.VAT_TAX_RIGHT, y, tva,
        layout.FONT, layout.SIZE_7, *slot7,
    )
    if abs(frais) > 0:
        if abs(rules.eco_ht(card.items)) > 0:
            draw_string(c, cols[3] + 6, y, texts.DFFE, layout.FONT, layout.SIZE_7)
        frais_x = layout.VAT_FRAIS_EURO_X if web else layout.VAT_FRAIS_EURO_X_MAG
        frais_tva_x = layout.VAT_FRAIS_TVA_EURO_X if web else layout.VAT_FRAIS_TVA_EURO_X_MAG
        _amount(
            c, web, frais_x, cols[4] - layout.VAT_PAD, y, frais,
            layout.FONT, layout.SIZE_7, *slot7,
        )
        _amount(
            c, web, frais_tva_x, cols[5] - layout.VAT_PAD, y, tva_f,
            layout.FONT, layout.SIZE_7, *slot7,
        )


def _pay(c, doc, web):
    card = doc.card
    fill(c, layout.COLOR)
    draw_string(
        c, layout.PAY_TITLE_X, layout.PAY_TITLE_Y,
        texts.PAY_TITLE, layout.FONT, layout.SIZE_7,
    )
    draw_string(
        c, layout.PAY_MODE_X, layout.PAY_MODE_Y,
        texts.PAY_MODE, layout.FONT, layout.SIZE_7,
    )
    draw_string(
        c, layout.PAY_MONTANT_X, layout.PAY_MODE_Y,
        texts.PAY_MONTANT, layout.FONT, layout.SIZE_7,
    )
    mode_y = layout.PAY_MODE_VAL_Y_WEB if web else layout.PAY_MODE_VAL_Y_MAG
    amt_y = layout.PAY_MODE_VAL_Y_WEB if web else layout.PAY_AMT_Y_MAG
    pay_slot = (
        layout.EURO_W_7,
        layout.EURO_ABOVE_7_PAY if web else layout.EURO_ABOVE_7_PAY_MAG,
        layout.EURO_BELOW_7_PAY if web else layout.EURO_BELOW_7_PAY_MAG,
    )
    draw_string(
        c, layout.PAY_MODE_VAL_X, mode_y,
        card.payment_mode, layout.FONT, layout.SIZE_7, max_width=70,
    )
    total = rules.grand_total(card)
    _amount(
        c, web, layout.PAY_EURO_X, layout.PAY_MONTANT_VAL_X, amt_y, total,
        layout.FONT, layout.SIZE_7, *pay_slot,
    )
    ech = (card.echeance or "").strip()
    if ech:
        draw_string(
            c, layout.ECHEANCE_X, layout.ECHEANCE_Y,
            texts.ECHEANCE_PREFIX + ech,
            layout.FONT_BOLD, layout.SIZE_8, max_width=85,
        )


def _totals(c, doc, web):
    if not doc.visible.middle_totals:
        return
    card = doc.card
    fill(c, layout.COLOR)
    lx = layout.TOT_LABEL_X_WEB if web else layout.TOT_LABEL_X_MAG
    ht_y = layout.TOT_HT_Y_WEB if web else layout.TOT_HT_Y_MAG
    tax_y = layout.TOT_TAX_Y_WEB if web else layout.TOT_TAX_Y_MAG
    ht_amt_y = layout.TOT_HT_Y_WEB if web else layout.TOT_HT_AMT_Y_MAG
    tax_amt_y = layout.TOT_TAX_Y_WEB if web else layout.TOT_TAX_AMT_Y_MAG
    ht = rules.recap_ht(card)
    tva = rules.recap_tva(card)
    total = rules.grand_total(card)
    draw_string(
        c, lx, ht_y, texts.TOT_HT,
        layout.FONT_BOLD, layout.SIZE_10,
    )
    slot10 = (layout.EURO_W_10, layout.EURO_ABOVE_10, layout.EURO_BELOW_10)
    _amount(
        c, web, layout.TOT_EURO_X, layout.TOT_RIGHT, ht_amt_y, ht,
        layout.FONT, layout.SIZE_10, *slot10,
    )
    draw_string(
        c, lx, tax_y, texts.TOT_TAX,
        layout.FONT_BOLD, layout.SIZE_10,
    )
    _amount(
        c, web, layout.TOT_EURO_X, layout.TOT_RIGHT, tax_amt_y, tva,
        layout.FONT, layout.SIZE_10, *slot10,
    )
    if web:
        draw_string(
            c, lx, layout.TOT_GRAND_Y_WEB, texts.TOT_GRAND_WEB,
            layout.FONT_BOLD, layout.SIZE_10,
        )
        draw_string(
            c, lx, layout.TOT_EUR_Y_WEB, texts.EUR,
            layout.FONT_BOLD, layout.SIZE_10,
        )
        _amount(
            c, web, layout.TOT_GRAND_EURO_X, layout.TOT_EUR_RIGHT,
            layout.TOT_EUR_Y_WEB, total,
            layout.FONT_BOLD, layout.SIZE_10,
            layout.EURO_W_10_BOLD, layout.EURO_ABOVE_10, layout.EURO_BELOW_10,
        )
    else:
        draw_string(
            c, lx, layout.TOT_GRAND_Y_MAG, texts.TOT_GRAND_MAG,
            layout.FONT_BOLD, layout.SIZE_10,
        )
        draw_money(
            c, layout.TOT_EURO_X, layout.TOT_GRAND_AMT_Y_MAG,
            rules.format_money(total),
            layout.FONT_BOLD, layout.SIZE_10,
            layout.EURO_W_10, layout.EURO_ABOVE_10, layout.EURO_BELOW_10,
        )
        draw_string(
            c, lx, layout.TOT_EUR_Y_MAG, texts.EUR,
            layout.FONT_BOLD, layout.SIZE_10,
        )


def draw(c, doc, plan):
    if not doc.visible.middle_vat:
        return
    web = rules.en_ligne(doc.card)
    _vat(c, doc, web)
    _pay(c, doc, web)
    _totals(c, doc, web)
