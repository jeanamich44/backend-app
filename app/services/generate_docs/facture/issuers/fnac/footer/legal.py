"""Mentions légales : 4 lignes Fnac Direct (en ligne) ou RCS seul (magasin)."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_string, fill


def draw(c, doc, plan):
    if not doc.visible.footer_legal:
        return
    fill(c, layout.COLOR)
    web = plan.footer_kind == rules.FOOTER_WEB
    if web:
        y = layout.LEGAL_Y0_WEB
        for line in texts.LEGAL_WEB:
            draw_string(
                c, layout.LEGAL_X, y, line,
                layout.FONT, layout.SIZE_7, max_width=190,
            )
            y += layout.LEGAL_PITCH
        return
    draw_string(
        c, layout.LEGAL_X, layout.LEGAL_Y_MAG, texts.LEGAL_MAG[0],
        layout.FONT, layout.SIZE_7, max_width=190,
    )
