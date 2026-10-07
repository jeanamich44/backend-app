"""Note importante — masquée par défaut."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.footer_note:
        return
    fill(c, layout.COLOR_BLACK)
    draw_string(
        c, layout.NOTE_X, layout.NOTE_Y,
        texts.NOTE, layout.FONT, layout.SIZE_NOTE,
        max_width=layout.NOTE_MAX_W,
    )
