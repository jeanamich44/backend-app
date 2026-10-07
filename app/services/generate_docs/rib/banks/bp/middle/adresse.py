"""Adresse : label gras + « : » + lignes (texte live, Y fixes)."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc, dy=0):
    if not doc.visible.middle_adresse:
        return
    fill(c, layout.COLOR)
    draw_string(
        c, layout.LABEL_X, layout.ADRESSE_Y + dy,
        texts.LABEL_ADRESSE, layout.FONT_BOLD, layout.SIZE,
    )
    draw_string(
        c, layout.ADRESSE_COLON_X, layout.ADRESSE_Y + dy,
        " :", layout.FONT, layout.SIZE,
    )
    card = doc.card
    opt = (card.titulaire_opt or "").strip()
    rue = (card.titulaire_rue or "").strip()
    ville = (card.titulaire_ville or "").strip()
    if opt:
        rows = (
            (layout.ADRESSE_OPT_Y, opt),
            (layout.ADRESSE_RUE_Y, rue),
            (layout.ADRESSE_VILLE_Y, ville),
        )
    else:
        lead = layout.ADRESSE_VILLE_Y - layout.ADRESSE_RUE_Y
        rows = []
        y = layout.ADRESSE_Y
        for text in (rue, ville):
            if text:
                rows.append((y, text))
                y += lead
    for y, text in rows:
        if not text:
            continue
        draw_string(
            c, layout.ADDR_X, y + dy, text,
            layout.FONT, layout.SIZE, max_width=layout.MAX_LINE,
        )
