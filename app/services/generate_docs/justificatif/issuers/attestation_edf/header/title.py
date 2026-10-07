"""Titre ATTESTATION TITULAIRE DE CONTRAT (origine de chaque glyphe)."""

from .. import layout
from ..paint import draw_glyphs, fill

_WORDS = (
    (
        ("A", 271.200), ("T", 279.840), ("T", 286.560), ("E", 293.280),
        ("S", 300.000), ("T", 306.720), ("A", 313.440), ("T", 322.080),
        ("I", 328.800), ("O", 332.160), ("N", 341.520),
    ),
    (
        ("T", 353.520), ("I", 360.240), ("T", 363.600), ("U", 370.320),
        ("L", 378.960), ("A", 384.960), ("I", 393.600), ("R", 396.960),
        ("E", 404.400),
    ),
    (("D", 414.480), ("E", 423.120)),
    (
        ("C", 433.200), ("O", 440.640), ("N", 450.000), ("T", 458.640),
        ("R", 465.360), ("A", 472.800), ("T", 481.440),
    ),
)


def draw(c, doc):
    if not doc.visible.header_title:
        return
    fill(c, layout.COLOR)
    for glyphs in _WORDS:
        draw_glyphs(c, layout.TITLE_Y, glyphs, layout.FONT_FB, layout.TITLE_SIZE)
