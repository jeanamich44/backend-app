"""Bandeau bas : icône + textes Chèque Énergie + filet tireté original."""

from .. import copy as texts
from .. import layout
from ..chrome.footer_paths import CHEQUE_OPS, STROKE_W
from ..paint import draw_image, draw_string, fill, stroke_ops


def draw(c, doc):
    if not doc.visible.footer_cheque:
        return
    stroke_ops(c, CHEQUE_OPS, layout.BLUE, STROKE_W, cap=0)
    draw_image(
        c, layout.CHEQUE_ICON,
        layout.CHEQUE_ICON_X, layout.CHEQUE_ICON_Y,
        layout.CHEQUE_ICON_W, layout.CHEQUE_ICON_H,
    )
    fill(c, layout.COLOR_BLUE)
    draw_string(
        c, layout.CHEQUE_LABEL_X, layout.CHEQUE_LABEL_Y,
        texts.CHEQUE_LABEL, layout.FONT_BOLD, layout.SIZE_CHEQUE_LABEL,
        max_width=layout.CHEQUE_LABEL_MAX_W,
    )
    fill(c, layout.COLOR)
    draw_string(
        c, layout.CHEQUE_BODY_X, layout.CHEQUE_LABEL_Y,
        texts.CHEQUE_BODY, layout.FONT, layout.SIZE_CHEQUE,
        max_width=layout.CHEQUE_BODY_MAX_W,
    )
    draw_string(
        c, layout.CHEQUE_NOTE_X, layout.CHEQUE_NOTE_Y,
        texts.CHEQUE_NOTE, layout.FONT, layout.SIZE_CHEQUE,
        max_width=layout.CHEQUE_NOTE_MAX_W,
    )
