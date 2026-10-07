from .. import copy
from ..font_dior import enc_chunk
from ..layout import (
    FOOTER_LINE_0_X,
    FOOTER_LINE_0_Y,
    FOOTER_LINE_1_X,
    FOOTER_LINE_1_Y,
    FOOTER_LINE_2_X,
    FOOTER_LINE_2_Y,
    FOOTER_LINE_3_X,
    FOOTER_LINE_3_Y,
    FOOTER_LINE_4_X,
    FOOTER_LINE_4_Y,
    FOOTER_SIZE,
)
from ..paint import draw_raw_tj, draw_string

# ----------------------------------------------------------------------

def draw(c, doc):
    l0 = doc.footer.line_0
    if l0:
        if l0 == copy.LEGAL_LINE_0:
            c1 = enc_chunk("L")
            c2 = enc_chunk("’éc")
            c3 = enc_chunk("hange d’un pr")
            c4 = enc_chunk("oduit peut se fair")
            c5 = enc_chunk("e uniquement dans une boutique Dior en F")
            c6 = enc_chunk("rance , sur présenta")
            c7 = enc_chunk("tion de ce document")
            tj0 = f"{c1}56.2 {c2}11.4 {c3}19.6 {c4}11.8 {c5}58.2 {c6}11.3 {c7}"
            draw_raw_tj(c, "TT0", FOOTER_SIZE, FOOTER_LINE_0_X, FOOTER_LINE_0_Y, tj0)
        else:
            draw_string(c, "TT0", FOOTER_SIZE, FOOTER_LINE_0_X, FOOTER_LINE_0_Y, l0)

    l1 = doc.footer.line_1
    if l1:
        if l1 == copy.LEGAL_LINE_1:
            c1 = enc_chunk("et dans un délai maximal de 1 mois")
            c2 = enc_chunk(". A")
            c3 = enc_chunk("ucun r")
            c4 = enc_chunk("etour n")
            c5 = enc_chunk("’est possib")
            c6 = enc_chunk("le en cas de détax")
            c7 = enc_chunk("e r")
            c8 = enc_chunk("embour")
            c9 = enc_chunk("sée")
            c10 = enc_chunk(".")
            tj1 = f"{c1}20.3 {c2}18.8 {c3}9.6 {c4}28.8 {c5}9.3 {c6}12 {c7}10.5 {c8}-9.2 {c9}29.3 {c10}"
            draw_raw_tj(c, "TT0", FOOTER_SIZE, FOOTER_LINE_1_X, FOOTER_LINE_1_Y, tj1)
        else:
            draw_string(c, "TT0", FOOTER_SIZE, FOOTER_LINE_1_X, FOOTER_LINE_1_Y, l1)

    l2 = doc.footer.line_2
    if l2:
        if l2 == copy.LEGAL_LINE_2:
            c1 = enc_chunk("Items ma")
            c2 = enc_chunk("y be e")
            c3 = enc_chunk("x")
            c4 = enc_chunk("c")
            c5 = enc_chunk("hanged sho")
            c6 = enc_chunk("wing this r")
            c7 = enc_chunk("eceipt, only in a Dior stor")
            c8 = enc_chunk("e in F")
            c9 = enc_chunk("rance")
            c10 = enc_chunk(", within 30 da")
            c11 = enc_chunk("ys of")
            c12 = enc_chunk(" pur")
            c13 = enc_chunk("c")
            c14 = enc_chunk("hase")
            c15 = enc_chunk(".")
            tj2 = f"{c1}10 {c2}10.3 {c3}9.8 {c4}10.9 {c5}9.6 {c6}9.5 {c7}10.8 {c8}56.1 {c9}29.3 {c10}9.8 {c11}-145 {c12}19.3 {c13}11 {c14}28.8 {c15}"
            draw_raw_tj(c, "TT0", FOOTER_SIZE, FOOTER_LINE_2_X, FOOTER_LINE_2_Y, tj2)
        else:
            draw_string(c, "TT0", FOOTER_SIZE, FOOTER_LINE_2_X, FOOTER_LINE_2_Y, l2)

    l3 = doc.footer.line_3
    if l3:
        if l3 == copy.LEGAL_LINE_3:
            c1 = enc_chunk("R")
            c2 = enc_chunk("etur")
            c3 = enc_chunk("ne on r")
            c4 = enc_chunk("efunded tax is not possib")
            c5 = enc_chunk("le")
            c6 = enc_chunk(".")
            tj3 = f"{c1}45.9 {c2}-25.6 {c3}10 {c4}10 {c5}29.6 {c6}"
            draw_raw_tj(c, "TT0", FOOTER_SIZE, FOOTER_LINE_3_X, FOOTER_LINE_3_Y, tj3)
        else:
            draw_string(c, "TT0", FOOTER_SIZE, FOOTER_LINE_3_X, FOOTER_LINE_3_Y, l3)

    l4 = doc.footer.line_4
    if l4:
        if l4 == copy.LEGAL_LINE_4:
            c1 = enc_chunk("R")
            c2 = enc_chunk("ela")
            c3 = enc_chunk("tions Clientèle : + 33 (0) 1 40 73 73 73 - Contactdior@dior")
            c4 = enc_chunk(".com")
            tj4 = f"{c1}45.9 {c2}10.8 {c3}107.8 {c4}"
            draw_raw_tj(c, "TT0", FOOTER_SIZE, FOOTER_LINE_4_X, FOOTER_LINE_4_Y, tj4)
        else:
            draw_string(c, "TT0", FOOTER_SIZE, FOOTER_LINE_4_X, FOOTER_LINE_4_Y, l4)
