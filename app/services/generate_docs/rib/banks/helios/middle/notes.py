"""Notes de bas de cadre (1) (2) (3)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_label, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_notes:
        return
    fill(c, layout.LABEL_COLOR)
    draw_label(
        c, layout.NOTE1_X, layout.NOTES_Y + dy, texts.NOTE1,
        layout.FONT, layout.SIZE_BODY,
    )
    draw_label(
        c, layout.NOTE2_X, layout.NOTES_Y + dy, texts.NOTE2,
        layout.FONT, layout.SIZE_BODY,
    )
    draw_label(
        c, layout.NOTE3_X, layout.NOTES_Y + dy, texts.NOTE3,
        layout.FONT, layout.SIZE_BODY,
    )
