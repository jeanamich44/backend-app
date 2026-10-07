"""Cachet électronique : image 2D-DOC du gabarit, filets, légendes aux glyphes."""

from .. import copy as texts
from .. import layout
from ..chrome import vectors
from ..paint import draw_chrome, draw_glyphs, draw_string, fill, stroke_ops

_FIELDS = ("cachet_l1", "cachet_l2", "cachet_l3")

# Origines PyMuPDF de chaque lettre (gabarit), hors espaces.
_CAPTIONS = (
    (
        708.560,
        (
            ("C", 472.800), ("a", 477.840), ("c", 481.680), ("h", 485.280),
            ("e", 489.120), ("t", 492.960),
            ("É", 496.800), ("l", 501.360), ("e", 503.040), ("c", 506.880),
            ("t", 510.480), ("r", 512.400), ("o", 514.800), ("n", 518.640),
            ("i", 522.480), ("q", 524.160), ("u", 528.000), ("e", 531.840),
        ),
    ),
    (
        716.720,
        (
            ("V", 466.800), ("i", 471.360), ("s", 473.040), ("i", 476.640),
            ("b", 478.320), ("l", 482.160), ("e", 483.840),
            ("d", 489.600), ("'", 493.440), ("a", 494.880), ("u", 498.720),
            ("t", 502.560), ("h", 504.480), ("e", 508.320), ("n", 512.160),
            ("t", 516.000), ("i", 517.920), ("f", 519.600), ("i", 521.520),
            ("c", 523.200), ("a", 526.800), ("t", 530.640), ("i", 532.560),
            ("o", 534.240), ("n", 538.080),
        ),
    ),
    (
        724.880,
        (
            ("d", 479.520), ("e", 483.360),
            ("c", 489.120), ("e", 492.720),
            ("d", 498.480), ("o", 502.320), ("c", 506.160), ("u", 509.760),
            ("m", 513.600), ("e", 519.600), ("n", 523.440), ("t", 527.280),
        ),
    ),
)


def draw(c, doc):
    if not doc.visible.footer_cachet:
        return
    draw_chrome(
        c, layout.CACHET_FILE,
        layout.CACHET_X, layout.CACHET_Y,
        layout.CACHET_W, layout.CACHET_H,
    )
    for color, width, cap, ops in vectors.STROKES:
        stroke_ops(c, ops, color, width, cap)
    fill(c, layout.COLOR)
    for (y, glyphs), field in zip(_CAPTIONS, _FIELDS):
        default = getattr(texts, field.upper())
        text = getattr(doc.card, field, default)
        if not text:
            continue
        if text == default:
            draw_glyphs(c, y, glyphs, layout.FONT_H, 7.0)
        else:
            draw_string(c, glyphs[0][1], y, text, layout.FONT_H, 7.0)
