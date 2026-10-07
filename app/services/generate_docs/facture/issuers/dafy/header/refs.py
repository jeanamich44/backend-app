from .. import copy as texts
from .. import layout
from ..chrome import vectors
from ..paint import draw_right, draw_string, fill, fill_subpaths


def draw(c, doc):
    if not doc.visible.header_refs:
        return
    fill_subpaths(c, vectors.REF_PATHS, layout.COLOR_GRAY)
    card = doc.card
    values = (
        card.num_client,
        card.date_commande,
        card.date_facture,
        card.num_commande,
        card.payment,
    )
    fill(c, layout.COLOR)
    for y, label, value in zip(layout.REF_Y, texts.REF_LABELS, values):
        draw_string(
            c, layout.REF_LABEL_X, y,
            label, layout.FONT_BOLD, layout.SIZE_BODY,
            max_width=layout.REF_LABEL_MAX_W,
        )
        draw_right(
            c, layout.REF_VALUE_RIGHT, y,
            value, layout.FONT_BOLD, layout.SIZE_BODY,
            max_width=layout.REF_VALUE_MAX_W,
        )
