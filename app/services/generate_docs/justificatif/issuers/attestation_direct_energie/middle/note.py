"""Note justificatif de domicile — chrome 8 pt."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.middle_note:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.NOTE_X, layout.NOTE_Y,
        texts.NOTE, layout.FONT, layout.NOTE_SIZE,
        max_width=layout.NOTE_MAX_W,
    )
