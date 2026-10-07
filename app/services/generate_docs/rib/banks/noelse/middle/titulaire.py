"""Titulaire : labels Light + 4 lignes Bold (casse titre du gabarit)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_runs, draw_string, fill, fill_rgb


def draw(c, doc, i=0):
    if not doc.visible.middle_titulaire:
        return
    fill(c, layout.COLOR)
    draw_runs(
        c, layout.LEFT_X, layout.TITULAIRE_LABEL_Y[i],
        texts.LABEL_TITULAIRE_RUNS, layout.FONT, layout.SIZE_LABEL,
    )
    fill_rgb(c, layout.COLOR_MUTED)
    draw_string(
        c, layout.LEFT_X, layout.OWNER_SUB_Y[i], texts.LABEL_OWNER,
        layout.FONT_NARROW, layout.SIZE_SUB,
    )
    fill(c, layout.COLOR)
    x = layout.HOLDER_X[i]
    lines = (
        texts.title_case(doc.card.titulaire_nom),
        texts.title_case(doc.card.titulaire_rue),
        texts.title_case(doc.card.titulaire_ville),
        texts.title_case(doc.card.titulaire_pays) if doc.card.titulaire_pays else "",
    )
    for y, text in zip(layout.HOLDER_YS[i], lines):
        if text:
            draw_string(
                c, x, y, text, layout.FONT_BOLD, layout.SIZE_VALUE,
                max_width=layout.HOLDER_W,
            )
