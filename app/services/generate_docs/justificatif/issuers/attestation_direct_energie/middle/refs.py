"""Référence client — label chrome + n° dummy."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_refs:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.CLIENT_LABEL_X, layout.CLIENT_Y,
        texts.CLIENT_LABEL, layout.FONT, layout.CLIENT_SIZE,
    )
    num = (doc.card.num_client or "").strip()
    draw_string(
        c, layout.CLIENT_VAL_X, layout.CLIENT_Y,
        f": {num}" if num else ":",
        layout.FONT, layout.CLIENT_SIZE,
    )
