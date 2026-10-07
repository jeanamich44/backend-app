"""Légende (1)(2)(3) sous les cases."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_legend:
        return
    fill(c, layout.COLOR)
    labels = (texts.LEGEND_IBAN, texts.LEGEND_BIC, texts.LEGEND_RIB)
    refs = (texts.REF_1, texts.REF_2, texts.REF_3)
    for (x, y), text in zip(layout.LEGEND_XY, labels):
        draw_string(c, x, y + dy, text, layout.FONT, layout.FONT_SIZE)
    for (x, y), text in zip(layout.LEGEND_REF_XY, refs):
        draw_string(c, x, y + dy, text, layout.FONT, layout.FONT_REF_SIZE)
