"""Valeurs identité (libellés rejoués via static.spans)."""

from .. import layout
from ..paint import draw_string, fill


def _value(c, x, y, text, size, max_width=None, color=None):
    if not text:
        return
    fill(c, color or layout.COLOR)
    draw_string(c, x, y, text, layout.FONT, size, max_width=max_width)


def draw(c, doc):
    if not doc.visible.header_identity:
        return
    card = doc.card
    _value(c, layout.CLIENT_VALUE_X, layout.CLIENT_VALUE_Y, card.num_client, layout.SIZE_LABEL)
    _value(
        c, layout.CONTRAT_ID_VALUE_X, layout.CONTRAT_ID_VALUE_Y,
        card.num_contrat, layout.SIZE_LABEL,
    )
    _value(
        c, layout.COURTIER_VALUE_X, layout.COURTIER_VALUE_Y,
        card.courtier, layout.SIZE_LABEL,
        max_width=layout.HOLDER_X - layout.COURTIER_VALUE_X - 8,
    )
    _value(c, layout.ORIAS_VALUE_X, layout.ORIAS_VALUE_Y, card.num_orias, layout.SIZE_LABEL)
    _value(
        c, layout.DATE_VALUE_X, layout.DATE_VALUE_Y,
        card.date_delivrance, layout.SIZE_LABEL,
    )
    _value(
        c, layout.HOLDER_X, layout.HOLDER_NOM_Y,
        card.titulaire, layout.SIZE_HOLDER, max_width=230, color=layout.COLOR_NAME,
    )
    _value(
        c, layout.HOLDER_X, layout.HOLDER_ADR_Y,
        card.adresse, layout.SIZE_HOLDER, max_width=230,
    )
    _value(
        c, layout.HOLDER_X, layout.HOLDER_VILLE_Y,
        card.cp_ville, layout.SIZE_HOLDER, max_width=230,
    )
    _value(
        c, layout.HOLDER_X, layout.HOLDER_PAYS_Y,
        card.pays, layout.SIZE_HOLDER, max_width=230,
    )
