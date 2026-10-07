"""Domiciliation banque (chrome) + (coming soon)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_runs, draw_string, fill, fill_rgb


def draw(c, doc, i=0):
    fill(c, layout.COLOR)
    draw_runs(
        c, layout.RIGHT_X, layout.DOM_LABEL_Y[i],
        texts.LABEL_DOM_RUNS, layout.FONT, layout.SIZE_LABEL,
    )
    fill_rgb(c, layout.COLOR_MUTED)
    draw_string(
        c, layout.RIGHT_X, layout.INST_SUB_Y[i], texts.LABEL_INSTITUTE,
        layout.FONT_NARROW, layout.SIZE_SUB,
    )
    fill(c, layout.COLOR)
    draw_string(
        c, layout.RIGHT_X, layout.DOM_RUE_Y[i], texts.DOM_RUE,
        layout.FONT, layout.SIZE_LABEL,
        max_width=layout.DOM_W,
    )
    draw_string(
        c, layout.RIGHT_X, layout.DOM_VILLE_Y[i], texts.DOM_VILLE,
        layout.FONT, layout.SIZE_LABEL,
        max_width=layout.DOM_W,
    )
    draw_string(
        c, layout.COMING_X, layout.COMING_Y[i], texts.COMING_SOON,
        layout.FONT_ITALIC, layout.SIZE_ITALIC,
    )
