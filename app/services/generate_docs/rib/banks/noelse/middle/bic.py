"""BIC : labels Light (TJ) + valeur Bold."""

from .. import copy as texts
from .. import layout
from ..paint import draw_runs, draw_string, fill, fill_rgb


def draw(c, doc, i=0):
    if not doc.visible.middle_bic:
        return
    fill(c, layout.COLOR)
    draw_runs(
        c, layout.RIGHT_X, layout.BIC_LABEL_Y[i],
        texts.LABEL_BIC_RUNS, layout.FONT, layout.SIZE_LABEL,
    )
    fill_rgb(c, layout.COLOR_MUTED)
    draw_string(
        c, layout.RIGHT_X, layout.BIC_SUB_Y[i], texts.LABEL_BIC_EN,
        layout.FONT_NARROW, layout.SIZE_SUB,
    )
    if not doc.card.bic:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.BIC_X[i], layout.IBAN_Y[i], doc.card.bic,
        layout.FONT_BOLD, layout.SIZE_VALUE,
        max_width=layout.BIC_W,
    )
