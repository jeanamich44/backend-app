from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill, fill_ops
from . import vectors


def draw(c, doc):
    if not doc.visible.middle_columns:
        return
    dy = layout.article_shift(doc.card)
    for ops in vectors.HEAD_OPS:
        fill_ops(c, ops, layout.COLOR_GRAY, dy=dy)
    fill(c, layout.COLOR)
    for x, label in zip(layout.COL_X, texts.COL_LABELS):
        draw_string(
            c, x, layout.HEAD_TEXT_Y + layout.addr_shift(doc.card), label,
            layout.FONT_BOLD, layout.SIZE_BODY,
        )
