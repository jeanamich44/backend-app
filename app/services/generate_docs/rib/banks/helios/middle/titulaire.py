"""Titulaire : préfixe et adresse peints deux fois (fill-only), nom une fois."""

from .. import layout
from ..paint import draw_string, fill, width

PREFIXES = {"Mr", "Mrs", "Ms", "Mme", "Mlle", "Dr", "M.", "Mr."}


def _split_prefix(nom: str):
    parts = (nom or "").split(None, 1)
    if not parts:
        return "", ""
    token = parts[0]
    if token in PREFIXES or token.rstrip(".") in {"M", "Mr", "Mrs", "Ms", "Mme", "Mlle", "Dr"}:
        return token, (parts[1] if len(parts) > 1 else "")
    return "", nom


def draw(c, doc, dy=0):
    if not doc.visible.middle_titulaire:
        return
    card = doc.card
    fill(c, layout.COLOR)
    font, size, max_w = layout.FONT, layout.SIZE_ADDR, layout.TITULAIRE_W
    if card.titulaire_nom:
        prefix, rest = _split_prefix(card.titulaire_nom)
        x = layout.TITULAIRE_X
        y = layout.TITULAIRE_Y + dy
        if prefix:
            draw_string(c, x, y, prefix, font, size, times=2)
            if rest:
                gap = width(prefix + " ", font, size)
                draw_string(c, x + gap, y, rest, font, size, max_width=max_w - gap)
        else:
            draw_string(c, x, y, rest, font, size, max_width=max_w)
    if card.titulaire_adresse:
        draw_string(
            c, layout.TITULAIRE_X, layout.TITULAIRE_Y + layout.TITULAIRE_LEADING + dy,
            card.titulaire_adresse, font, size, max_width=max_w, times=2,
        )
