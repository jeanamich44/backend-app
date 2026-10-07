"""En-tête de colonnes du tableau."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, plan):
    if not doc.visible.middle_columns:
        return
    fill(c, layout.COLOR)
    y = layout.COL_HEAD_Y
    xs = layout.COL_HEAD_X
    labels = (
        texts.COL_TVA, texts.COL_EAN, texts.COL_REF, texts.COL_QTE,
        texts.COL_LIB, texts.COL_HT, texts.COL_TTC, texts.COL_MT,
    )
    for x, label in zip(xs, labels):
        draw_string(c, x, y, label, layout.FONT, layout.SIZE_7)
