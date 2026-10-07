from .. import copy
from ..font_dior import enc_chunk
from ..layout import CLIENT_LEADING, CLIENT_SIZE, CLIENT_X, CLIENT_Y
from ..paint import draw_raw_tj, draw_string

# ----------------------------------------------------------------------

def draw(c, doc):
    lines = [
        doc.header.client_nom,
        doc.header.client_email,
        doc.header.client_tel,
    ]
    default_lines = [copy.CLIENT_NOM, copy.CLIENT_EMAIL, copy.CLIENT_TEL]
    for i, line in enumerate(lines):
        if not line:
            continue
        y = CLIENT_Y - i * CLIENT_LEADING
        if line == default_lines[i]:
            body = enc_chunk(line)
            draw_raw_tj(c, "TT0", CLIENT_SIZE, CLIENT_X, y, body)
        else:
            draw_string(c, "TT0", CLIENT_SIZE, CLIENT_X, y, line)
