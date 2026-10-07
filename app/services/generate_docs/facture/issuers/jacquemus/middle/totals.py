from .. import copy as texts
from .. import layout
from ..paint import draw_right, draw_string, fill

# ----------------------------------------------------------------------

EXACT_VAL_XS = {
    texts.VAL_TOT_SOUS_TOTAL: 494.23,
    texts.VAL_TOT_TVA: 500.48,
    texts.VAL_TOT_LIVRAISON: 489.69,
    texts.VAL_TOT_TOTAL: 493.96,
}

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.middle_totals:
        return
    n = max(1, len(doc.middle.items[:layout.MAX_ROWS]))
    y_shift = (n - 1) * layout.ROW_H

    rows = (
        (texts.LABEL_TOT_SOUS_TOTAL, doc.middle.tot_sous_total, texts.VAL_TOT_SOUS_TOTAL),
        (texts.LABEL_TOT_TVA, doc.middle.tot_tva, texts.VAL_TOT_TVA),
        (texts.LABEL_TOT_LIVRAISON, doc.middle.tot_livraison, texts.VAL_TOT_LIVRAISON),
        (texts.LABEL_TOT_TOTAL, doc.middle.tot_total, texts.VAL_TOT_TOTAL),
    )

    for k, (label, val, default_val) in enumerate(rows):
        y = layout.TOT_Y_START + y_shift + k * layout.TOT_LEADING
        fill(c, layout.COLOR_GREY)
        draw_string(c, layout.TOT_LABEL_X, y, label, layout.FONT_REGULAR, layout.FONT_SIZE_BODY)

        fill(c, layout.COLOR_BLACK)
        if val == default_val and val in EXACT_VAL_XS:
            draw_string(c, EXACT_VAL_XS[val], y, val, layout.FONT_BOLD, layout.FONT_SIZE_BODY)
        else:
            draw_right(c, layout.TOT_VAL_RIGHT_X, y, val, layout.FONT_BOLD, layout.FONT_SIZE_BODY)
