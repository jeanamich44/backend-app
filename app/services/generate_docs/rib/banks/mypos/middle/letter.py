"""Salutation, paragraphe de confirmation, consigne de virement."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill_rgb, wrap_lines


def _body_lines(card) -> list[str]:
    lines = []
    font, size, max_w = layout.FONT, layout.SIZE_BODY, layout.BODY_W
    for block in texts.confirm_blocks(card):
        lines.extend(wrap_lines(block, font, size, max_w))
    return lines[: layout.BODY_MAX_LINES]


def draw(c, doc):
    if not doc.visible.middle_letter:
        return
    fill_rgb(c, layout.COLOR)
    font, size = layout.FONT, layout.SIZE_BODY
    draw_string(c, layout.LEFT_X, layout.GREET_Y, texts.GREETING, font, size)
    y = layout.BODY_Y
    for line in _body_lines(doc.card):
        draw_string(c, layout.LEFT_X, y, line, font, size)
        y += layout.BODY_LEADING
    draw_string(
        c, layout.LEFT_X, layout.TRANSFER_Y, texts.TRANSFER, font, size,
        max_width=layout.RIGHT_X - layout.LEFT_X,
    )
