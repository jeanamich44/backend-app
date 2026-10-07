"""Encadré d'aide : Fnac.com + technique (en ligne) ou technique seul (magasin)."""

from .. import copy as texts
from .. import layout, rules
from ..paint import draw_string, fill


def draw(c, doc, plan):
    if not doc.visible.footer_help:
        return
    fill(c, layout.COLOR)
    web = plan.footer_kind == rules.FOOTER_WEB
    if web:
        draw_string(
            c, layout.PILL_TEXT_X, layout.PILL_TEXT_Y, texts.PILL,
            layout.FONT_BOLD, layout.SIZE_7,
        )
    else:
        draw_string(
            c, layout.PILL_TEXT_X_MAG, layout.PILL_TEXT_Y_MAG, texts.PILL,
            layout.FONT_BOLD, layout.SIZE_7,
        )
    if web:
        draw_string(
            c, layout.HELP_TITLE_X, layout.HELP_WEB_Y,
            texts.HELP_WEB_TITLE, layout.FONT_BOLD, layout.SIZE_7,
        )
        draw_string(
            c, layout.HELP_BODY_X, layout.HELP_WEB_Y,
            texts.HELP_WEB_BODY, layout.FONT, layout.SIZE_7, max_width=445,
        )
    draw_string(
        c, layout.HELP_TITLE_X, layout.HELP_TECH_Y,
        texts.HELP_TECH_TITLE, layout.FONT_BOLD, layout.SIZE_7,
    )
    draw_string(
        c, layout.HELP_BODY_X, layout.HELP_TECH_Y,
        texts.HELP_TECH_1, layout.FONT, layout.SIZE_7, max_width=445,
    )
    draw_string(
        c, layout.HELP_BODY_X, layout.HELP_TECH_Y2,
        texts.HELP_TECH_2, layout.FONT, layout.SIZE_7, max_width=445,
    )
