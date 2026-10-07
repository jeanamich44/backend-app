"""Corps de lettre : salutations, confirmation, adresse, clôture."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_body:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.BODY_X, layout.GREET_Y,
        texts.GREETING, layout.FONT, layout.BODY_SIZE,
    )
    draw_string(
        c, layout.BODY_X, layout.CONFIRM_Y[0],
        texts.confirm_line(doc.card.depuis),
        layout.FONT, layout.BODY_SIZE,
        max_width=layout.BODY_MAX_W,
    )
    draw_string(
        c, layout.BODY_X, layout.CONFIRM_Y[1],
        texts.CONFIRM_TAIL, layout.FONT, layout.BODY_SIZE,
    )
    for y, line in zip(layout.ADDR_Y, rules.body_lines(doc.card)):
        draw_string(
            c, layout.BODY_X, y, line,
            layout.FONT, layout.BODY_SIZE,
            max_width=layout.ADDR_MAX_W,
        )
    draw_string(
        c, layout.BODY_X, layout.RIGHT_Y,
        texts.RIGHT, layout.FONT, layout.BODY_SIZE,
    )
    for y, line in zip(layout.ADVICE_Y, texts.ADVICE):
        draw_string(
            c, layout.BODY_X, y, line,
            layout.FONT, layout.BODY_SIZE,
            max_width=layout.BODY_MAX_W,
        )
    draw_string(
        c, layout.BODY_X, layout.CLOSE_Y,
        texts.CLOSING, layout.FONT, layout.BODY_SIZE,
        max_width=layout.BODY_MAX_W,
    )
