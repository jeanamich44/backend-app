from .. import copy
from ..font_dior import enc_chunk
from ..layout import META_LEADING, META_SIZE, META_X, META_Y
from ..paint import draw_raw_tj, draw_string

# ----------------------------------------------------------------------

def draw(c, doc):
    title = doc.header.vente_title
    if title:
        y0 = META_Y
        if title == copy.VENTE_TITLE:
            draw_raw_tj(c, "TT0", META_SIZE, META_X, y0, enc_chunk(title))
        else:
            draw_string(c, "TT0", META_SIZE, META_X, y0, title)

    oper = doc.header.oper
    if oper:
        y1 = META_Y - 1 * META_LEADING
        line1 = f"Oper : {oper}"
        if oper == copy.OPER:
            draw_raw_tj(c, "TT0", META_SIZE, META_X, y1, enc_chunk(line1))
        else:
            draw_string(c, "TT0", META_SIZE, META_X, y1, line1)

    trans = doc.header.trans
    if trans:
        y2 = META_Y - 2 * META_LEADING
        line2 = f"Trans : {trans}"
        if trans == copy.TRANS:
            c1 = enc_chunk("T")
            c2 = enc_chunk("rans : 10738")
            draw_raw_tj(c, "TT0", META_SIZE, META_X, y2, f"{c1}74.5 {c2}")
        else:
            draw_string(c, "TT0", META_SIZE, META_X, y2, line2)

    store = doc.header.store
    num = doc.header.store_num
    if store or num:
        y3 = META_Y - 3 * META_LEADING
        if store == copy.STORE and num == copy.STORE_NUM:
            c1 = enc_chunk("Stor")
            c2 = enc_chunk("e : FRpar01 ")
            c3 = enc_chunk("3")
            draw_raw_tj(c, "TT0", META_SIZE, META_X, y3, f"{c1}11 {c2}-952.3 {c3}")
        else:
            line3 = f"Store : {store}   {num}".rstrip()
            draw_string(c, "TT0", META_SIZE, META_X, y3, line3)

    date_str = doc.header.date_str
    if date_str:
        y4 = META_Y - 4 * META_LEADING
        if date_str == copy.DATE_STR:
            c1 = enc_chunk("2-F")
            c2 = enc_chunk("e")
            c3 = enc_chunk("vrier")
            c4 = enc_chunk("-2019 13:12:14")
            draw_raw_tj(c, "TT0", META_SIZE, META_X, y4, f"{c1}74.5 {c2}10.2 {c3}19.6 {c4}")
        else:
            draw_string(c, "TT0", META_SIZE, META_X, y4, date_str)
