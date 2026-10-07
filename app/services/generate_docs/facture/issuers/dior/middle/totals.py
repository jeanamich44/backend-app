from .. import copy
from ..font_dior import enc_chunk, text_width_tt0
from ..layout import TOTALS_SIZE, TOTALS_X
from ..paint import draw_raw_tj, draw_string

# ----------------------------------------------------------------------

RIGHT_X = 569.2

# ----------------------------------------------------------------------

def _draw_row(c, y: float, label_x: float, label: str, val: str):
    if label:
        draw_string(c, "TT0", TOTALS_SIZE, label_x, y, label)
    if val:
        val_w = text_width_tt0(val, TOTALS_SIZE)
        draw_string(c, "TT0", TOTALS_SIZE, max(label_x + 20, RIGHT_X - val_w), y, val)

# ----------------------------------------------------------------------

def draw(c, doc):
    pay_amt = doc.middle.payment_amount
    if pay_amt:
        if pay_amt == copy.PAYMENT_AMOUNT:
            tj0 = f"{enc_chunk(' ')}-2321.4 {enc_chunk(' ')}-2321.4 {enc_chunk(' ')}-2321.4 {enc_chunk(' ')}-2321.5 {enc_chunk('EUR ')}-196.4 {enc_chunk('        800,00')}"
            draw_raw_tj(c, "TT0", TOTALS_SIZE, TOTALS_X, 452.1553, tj0)
        else:
            _draw_row(c, 452.1553, 465.1521, "EUR", pay_amt)

    rendu = doc.middle.rendu_amount
    if rendu:
        if rendu == copy.RENDU_AMOUNT:
            tj1 = f"{enc_chunk(' ')}-2321.4 {enc_chunk(' ')}-2321.4 {enc_chunk(' ')}-2321.4 {enc_chunk(' ')}-2321.5 {enc_chunk('R')}45.8 {enc_chunk('endu        10,00')}"
            draw_raw_tj(c, "TT0", TOTALS_SIZE, TOTALS_X, 435.3553, tj1)
        else:
            _draw_row(c, 435.3553, 465.1521, "Rendu", rendu)

    tot_ht = doc.middle.total_ht
    if tot_ht:
        if tot_ht == copy.TOTAL_HT:
            tj2 = f"{enc_chunk(' ')}-2321.4 {enc_chunk(' ')}-2321.4 {enc_chunk(' ')}-2321.4 {enc_chunk(' ')}-2321.5 {enc_chunk(' HT            658,33')}"
            draw_raw_tj(c, "TT0", TOTALS_SIZE, TOTALS_X, 401.7553, tj2)
        else:
            _draw_row(c, 401.7553, 468.6521, "HT", tot_ht)

    tva_p = doc.middle.tva_product
    tva_r = doc.middle.tva_rate
    tva_a = doc.middle.tva_amount
    if tva_p or tva_r or tva_a:
        if tva_p == copy.TVA_PRODUCT and tva_r == copy.TVA_RATE and tva_a == copy.TVA_AMOUNT:
            tj3 = f"{enc_chunk('TV')}120.4 {enc_chunk('A FR Pr')}19.8 {enc_chunk('oduct ')}-529.9 {enc_chunk('        TV')}120.3 {enc_chunk('A 20%     131,67')}"
            draw_raw_tj(c, "TT0", TOTALS_SIZE, TOTALS_X, 384.9553, tj3)
        else:
            lbl = f"{tva_p}         {tva_r}".strip()
            _draw_row(c, 384.9553, TOTALS_X, lbl, tva_a)

    tot_ttc = doc.middle.total_ttc
    if tot_ttc:
        if tot_ttc == copy.TOTAL_TTC:
            tj4 = f"{enc_chunk(' ')}-2321.4 {enc_chunk(' ')}-2321.4 {enc_chunk(' ')}-2321.4 {enc_chunk('T')}46 {enc_chunk('O')}28.1 {enc_chunk('T')}84.2 {enc_chunk('AL TT')}37.4 {enc_chunk('C      790,00')}"
            draw_raw_tj(c, "TT0", TOTALS_SIZE, TOTALS_X, 351.3553, tj4)
        else:
            _draw_row(c, 351.3553, 429.1511, "TOTAL TTC", tot_ttc)
