"""Adresse école aux origines du gabarit (DejaVu + espaces Helvetica)."""

from .. import layout
from ..paint import draw_string, fill

# x, texte, h = Helvetica, d = DejaVu
_SPANS = (
    (155.0, "4", "d"),
    (158.0, " ", "h"),
    (159.0, "Bis", "d"),
    (167.0, " ", "h"),
    (168.0, "Place", "d"),
    (183.0, " ", "h"),
    (184.0, "Paul", "d"),
    (196.0, " ", "h"),
    (197.0, "Froment\u202094400\u2020VITRY", "d"),
    (264.0, " ", "h"),
    (265.0, "SUR", "d"),
    (277.0, " ", "h"),
    (278.0, "SEINE", "d"),
    (295.0, " ", "h"),
    (296.0, "-", "d"),
    (298.0, " ", "h"),
    (299.0, "TÈl", "d"),
    (308.0, " ", "h"),
    (309.0, "01.44.65.73.61", "d"),
    (354.0, " ", "h"),
    (355.0, "-", "d"),
    (357.0, " ", "h"),
    (358.0, "cfrvitry2@gmail.com", "d"),
)


def draw(c, doc):
    fill(c, layout.COLOR)
    for x, text, kind in _SPANS:
        font = layout.FONT_HELV if kind == "h" else layout.FONT_DEJAVU
        draw_string(c, x, layout.ADDR_Y, text, font, layout.SIZE_LEGAL)
