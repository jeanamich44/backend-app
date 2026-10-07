from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_issuer:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.ISSUER_X, layout.ISSUER_Y[0],
        texts.ISSUER_NOM, layout.FONT_BOLD, layout.SIZE_BODY,
        max_width=layout.ISSUER_MAX_W,
    )
    for y, line in zip(layout.ISSUER_Y[1:], texts.ISSUER_LIGNES):
        draw_string(
            c, layout.ISSUER_X, y,
            line, layout.FONT, layout.SIZE_BODY,
            max_width=layout.ISSUER_MAX_W,
        )
