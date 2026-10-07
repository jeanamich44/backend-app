"""IBAN : labels Light (TJ) + 7 groupes Bold."""

from .. import copy as texts
from .. import layout
from .. import rib
from ..paint import draw_runs, draw_string, fill, fill_rgb


def draw(c, doc, i=0):
    if not doc.visible.middle_iban:
        return
    fill(c, layout.COLOR)
    draw_runs(
        c, layout.LEFT_X, layout.IBAN_LABEL_Y[i],
        texts.LABEL_IBAN_RUNS, layout.FONT, layout.SIZE_LABEL,
    )
    fill_rgb(c, layout.COLOR_MUTED)
    draw_runs(
        c, layout.LEFT_X, layout.IBAN_SUB_Y[i],
        texts.LABEL_IBAN_EN_RUNS, layout.FONT_NARROW, layout.SIZE_SUB,
    )
    raw = rib.format_groups(doc.card.iban) if doc.card.iban else ""
    parts = raw.split()
    fill(c, layout.COLOR)
    y = layout.IBAN_Y[i]
    for x, part in zip(layout.IBAN_XS[i], parts):
        draw_string(
            c, x, y, part, layout.FONT_BOLD, layout.SIZE_VALUE,
            max_width=layout.GROUP_W,
        )
