"""N° client dans la carte « NOUS CONTACTER »."""

from .. import layout, rules
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_contact:
        return
    fill(c, layout.COLOR_BLUE)
    draw_string(
        c, layout.CLIENT_SIDE_X, layout.CLIENT_SIDE_Y,
        rules.digits(doc.card.num_client), layout.FONT_H, layout.CLIENT_SIDE_SIZE,
    )
