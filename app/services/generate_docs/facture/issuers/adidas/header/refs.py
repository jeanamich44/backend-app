"""N° commande / facture / dates."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.header_refs:
        return
    card = doc.card
    fill(c, layout.COLOR)
    draw_string(
        c, layout.ASK_X, layout.ASK_Y,
        texts.ASK, layout.FONT_BOLD, layout.SIZE_SERVICE,
    )
    values = (
        layout.REF_PREFIX + (card.num_commande or ""),
        layout.REF_PREFIX + (card.num_facture or ""),
        layout.REF_PREFIX + (card.date_facture or ""),
        layout.REF_PREFIX + (card.date_livraison or ""),
    )
    for y, label, value in zip(layout.REF_Y, texts.REF_LABELS, values):
        draw_string(c, layout.REF_LABEL_X, y, label, layout.FONT, layout.SIZE_BODY)
        draw_string(
            c, layout.REF_VALUE_X, y, value,
            layout.FONT, layout.SIZE_BODY, max_width=layout.REF_MAX_W,
        )
