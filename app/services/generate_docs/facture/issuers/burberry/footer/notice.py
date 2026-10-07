"""Notice récupération au dos — retrait magasin seulement."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.footer_notice:
        return
    if not rules.retrait_magasin(doc.card):
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.NOTICE_X, layout.NOTICE_Y,
        texts.NOTICE, layout.FONT_BOLD, layout.SIZE_BODY,
        max_width=layout.NOTICE_MAX_W,
    )
