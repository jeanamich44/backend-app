from .. import copy
from ..font_dior import enc_chunk
from ..layout import CONTACT_LEADING, CONTACT_SIZE, CONTACT_X, CONTACT_Y
from ..paint import draw_raw_tj, draw_string

# ----------------------------------------------------------------------

def draw(c, doc):
    lines = [
        doc.header.contact_line_0,
        doc.header.contact_line_1,
        doc.header.contact_line_2,
        doc.header.contact_line_3,
        doc.header.contact_line_4,
    ]
    for i, line in enumerate(lines):
        if not line:
            continue
        y = CONTACT_Y - i * CONTACT_LEADING
        if line == copy.CONTACT_LINES[i]:
            if i == 0:
                c1 = enc_chunk("Christian Dior Coutur")
                c2 = enc_chunk("e P")
                c3 = enc_chunk("aris")
                body = f"{c1}11 {c2}28.9 {c3}"
            elif i == 1:
                c1 = enc_chunk("30 A")
                c2 = enc_chunk("v")
                c3 = enc_chunk("en")
                c4 = enc_chunk("ue Montaigne")
                body = f"{c1}55.9 {c2}18.5 {c3}10.1 {c4}"
            elif i == 2:
                body = enc_chunk("FR 612 035 832")
            elif i == 3:
                c1 = enc_chunk("75008 P")
                c2 = enc_chunk("aris")
                body = f"{c1}28.3 {c2}"
            elif i == 4:
                body = enc_chunk("Tél : 01 45 63 12 51")
            draw_raw_tj(c, "TT0", CONTACT_SIZE, CONTACT_X, y, body)
        else:
            draw_string(c, "TT0", CONTACT_SIZE, CONTACT_X, y, line)
