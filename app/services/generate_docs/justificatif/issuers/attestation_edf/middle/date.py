"""Date et conseillère."""

from .. import copy as texts
from .. import layout
from ..paint import draw_glyphs, draw_string, fill

_MARIE = (
    ("M", 530.259), ("a", 537.756), ("r", 542.760), ("i", 545.757), ("e", 547.755),
)
_LABEL = (
    ("V", 463.851), ("o", 469.854), ("t", 474.858), ("r", 477.360), ("e", 480.357),
    ("c", 488.520), ("o", 493.020), ("n", 498.024), ("s", 503.028), ("e", 507.528),
    ("i", 512.532), ("l", 514.530), ("l", 516.528), ("è", 518.526), ("r", 523.530),
    ("e", 526.527),
    ("E", 534.773), ("D", 540.776), ("F", 547.274),
)


def draw(c, doc):
    if not doc.visible.middle_date:
        return
    fill(c, layout.COLOR)
    line = texts.date_line(doc.card.ville, doc.card.date)
    draw_string(c, layout.DATE_X, layout.DATE_Y, line, layout.FONT, layout.BODY_SIZE)
    prenom = doc.card.conseillere or ""
    if prenom == texts.CONSEILLERE:
        draw_glyphs(c, layout.CONSEIL_PRENOM_Y, _MARIE, layout.FONT, layout.BODY_SIZE)
    elif prenom:
        draw_string(
            c, layout.CONSEIL_PRENOM_X, layout.CONSEIL_PRENOM_Y,
            prenom, layout.FONT, layout.BODY_SIZE,
        )
    label = doc.card.conseillere_libelle or ""
    if label == texts.CONSEILLERE_LIBELLE:
        draw_glyphs(c, layout.CONSEIL_Y, _LABEL, layout.FONT, layout.BODY_SIZE)
    elif label:
        draw_string(
            c, layout.CONSEIL_X, layout.CONSEIL_Y,
            label, layout.FONT, layout.BODY_SIZE,
        )
