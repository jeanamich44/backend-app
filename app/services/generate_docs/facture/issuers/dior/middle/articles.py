from .. import copy
from ..font_dior import enc_chunk, text_width_tt0
from ..layout import (
    ARTICLE_SIZE,
    ARTICLE_Y,
    COUNT_SIZE,
    COUNT_X,
    COUNT_Y,
    DESC_X,
    QTY_X,
    REF_X,
    TOTAL_FACTURE_LABEL_X,
    TOTAL_FACTURE_SIZE,
    TOTAL_FACTURE_Y,
    TOTAL_X,
    UNIT_X,
)
from ..paint import draw_raw_tj, draw_string

# ----------------------------------------------------------------------

def draw(c, doc):
    items = getattr(doc.middle, "items", None)
    if not items:
        return
    items = items[:3]
    dy = (len(items) - 1) * 16.8

    for i, item in enumerate(items):
        y = ARTICLE_Y - i * 16.8
        ref = item.ref
        desc = item.desc
        qty = item.qty
        unit = item.unit_price
        total = item.total

        if (
            i == 0
            and ref == copy.ARTICLE_REF
            and desc == copy.ARTICLE_DESC
            and qty == copy.ARTICLE_QTY
            and unit == copy.ARTICLE_UNIT_PRICE
            and total == copy.ARTICLE_TOTAL
        ):
            c1 = enc_chunk("K")
            c2 = enc_chunk("C1322VNI ")
            c3 = enc_chunk("S799 / T40 SNEAKERS T")
            c4 = enc_chunk("OILE ET VEA")
            c5 = enc_chunk(f"U    {qty}                {unit}           {total}")
            tj_body = f"{c1}75 {c2}-2206.3 {c3}47.4 {c4}45.7 {c5}"
            draw_raw_tj(c, "TT0", ARTICLE_SIZE, REF_X, y, tj_body)
        else:
            if ref:
                draw_string(c, "TT0", ARTICLE_SIZE, REF_X, y, ref)
            if desc:
                draw_string(c, "TT0", ARTICLE_SIZE, DESC_X, y, desc)
            if qty:
                draw_string(c, "TT0", ARTICLE_SIZE, QTY_X, y, qty)
            if unit:
                uw = text_width_tt0(unit, ARTICLE_SIZE)
                draw_string(c, "TT0", ARTICLE_SIZE, max(QTY_X + 25, 493.2 - uw), y, unit)
            if total:
                tw = text_width_tt0(total, ARTICLE_SIZE)
                draw_string(c, "TT0", ARTICLE_SIZE, max(UNIT_X + 25, 569.2 - tw), y, total)

    count_lbl = doc.middle.count_label
    y_count = COUNT_Y - dy
    if count_lbl:
        if count_lbl == copy.ARTICLE_COUNT and dy == 0:
            c1 = enc_chunk("1 pr")
            c2 = enc_chunk("oduit(s)")
            draw_raw_tj(c, "TT1", COUNT_SIZE, COUNT_X, y_count, f"{c1}19.8 {c2}")
        else:
            draw_string(c, "TT1", COUNT_SIZE, COUNT_X, y_count, count_lbl)

    tot_fac = doc.middle.total_facture
    y_tf = TOTAL_FACTURE_Y - dy
    if tot_fac:
        if tot_fac == copy.TOTAL_FACTURE and dy == 0:
            c1 = enc_chunk("T")
            c2 = enc_chunk("O")
            c3 = enc_chunk("T")
            c4 = enc_chunk("AL F")
            c5 = enc_chunk("actur")
            c6 = enc_chunk("e ")
            c7 = enc_chunk(f"       {tot_fac}")
            tj_tf = f"{c1}46.1 {c2}28.1 {c3}84.2 {c4}55.7 {c5}10.5 {c6}-874.9 {c7}"
            draw_raw_tj(c, "TT0", TOTAL_FACTURE_SIZE, TOTAL_FACTURE_LABEL_X, y_tf, tj_tf)
        else:
            draw_string(c, "TT0", TOTAL_FACTURE_SIZE, TOTAL_FACTURE_LABEL_X, y_tf, "TOTAL Facture")
            fw = text_width_tt0(tot_fac, TOTAL_FACTURE_SIZE)
            draw_string(c, "TT0", TOTAL_FACTURE_SIZE, max(TOTAL_FACTURE_LABEL_X + 50, 569.2 - fw), y_tf, tot_fac)
