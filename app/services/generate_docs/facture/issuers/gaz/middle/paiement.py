"""Colonne droite bas : mode de paiement."""

from .. import copy as texts
from .. import layout
from ..chrome.middle_paths import PAY_BOX_OPS, STROKE_W
from ..paint import draw_string, fill, stroke_ops


def draw(c, doc):
    if not doc.visible.middle_paiement:
        return
    stroke_ops(c, PAY_BOX_OPS, layout.BLUE, STROKE_W, cap=0)
    fill(c, layout.COLOR)
    draw_string(
        c, 435.23175048828125, 433.99285888671875,
        texts.PAY_TITLE, layout.FONT_BOLD, layout.SIZE_PREST,
        max_width=140,
    )
    draw_string(
        c, 434.54815673828125, 443.43658447265625,
        texts.PAY_L1, layout.FONT, layout.SIZE_BODY, max_width=140,
    )
    draw_string(
        c, 431.2162780761719, 452.6366882324219,
        texts.PAY_L2, layout.FONT, layout.SIZE_BODY, max_width=140,
    )
    draw_string(
        c, 473.46832275390625, 461.8367919921875,
        texts.PAY_L3, layout.FONT, layout.SIZE_BODY, max_width=80,
    )
    compte = (doc.card.compte or "").strip()
    if compte:
        draw_string(
            c, 443.456298828125, 471.03656005859375,
            compte, layout.FONT, layout.SIZE_BODY, max_width=120,
        )
    draw_string(
        c, 447.672119140625, 489.436767578125,
        texts.PAY_L5, layout.FONT, layout.SIZE_BODY, max_width=120,
    )
    draw_string(
        c, 472.3562316894531, 498.6368713378906,
        texts.PAY_L6, layout.FONT, layout.SIZE_BODY, max_width=80,
    )
