"""Colonne droite : économies + facture en ligne."""

from .. import copy as texts
from .. import layout
from ..chrome.economies_paths import (
    ECONO_BOX_OPS,
    ECONO_HEAD_OPS,
    ECONO_INNER1_OPS,
    ECONO_INNER2_OPS,
    ECONO_LINE_OPS,
    STROKE_W,
)
from ..paint import draw_image, draw_spans, fill_ops, stroke_ops

_L = layout.PICTO_L

IMAGES = (
    ("gaz_picto_conso.jpg", 316.06298828125, 596.3226318359375, _L, _L, None),
    ("gaz_picto_thermo.jpg", 316.06298828125, 641.677001953125, _L, _L, None),
)


def _spans():
    b, r = layout.FONT_BOLD, layout.FONT
    head, body, note = layout.SIZE_HEAD, layout.SIZE_BODY, layout.SIZE_NOTE
    white, black = layout.COLOR_WHITE, layout.COLOR
    t = texts
    return (
        (361.8590087890625, 568.53076171875, t.ECONO_HEAD_1, b, head, white),
        (355.55389404296875, 580.03076171875, t.ECONO_HEAD_2, b, head, white),
        (347.244140625, 605.18994140625, t.ECONO_CONSO_1, r, body, black),
        (347.244140625, 614.3900146484375, t.ECONO_CONSO_2, r, body, black),
        (417.94952392578125, 614.3900146484375, t.ECONO_CONSO_BOLD, b, body, black),
        (347.244140625, 621.7778930664062, t.ECONO_CONSO_NOTE, r, note, black),
        (347.244140625, 654.026123046875, t.ECONO_THERMO_1, r, body, black),
        (347.244140625, 663.226318359375, t.ECONO_THERMO_2, r, body, black),
        (509.13555908203125, 663.226318359375, t.ECONO_THERMO_APOS, r, body, black),
        (510.9117431640625, 663.226318359375, t.ECONO_THERMO_3, r, body, black),
        (313.2282409667969, 704.1180419921875, t.ECONO_LINE_BOLD, b, body, black),
        (409.71612548828125, 704.1180419921875, t.ECONO_LINE_1, r, body, white),
        (313.2282409667969, 713.318115234375, t.ECONO_LINE_2, r, body, white),
        (313.2282409667969, 722.517822265625, t.ECONO_LINE_3, r, body, white),
    )


def draw(c, doc):
    if not doc.visible.footer_economies:
        return
    stroke_ops(c, ECONO_BOX_OPS, layout.BLUE, STROKE_W, cap=0)
    fill_ops(c, ECONO_HEAD_OPS, layout.BLUE, even_odd=True)
    stroke_ops(c, ECONO_INNER1_OPS, layout.TEAL, STROKE_W, cap=0)
    stroke_ops(c, ECONO_INNER2_OPS, layout.TEAL, STROKE_W, cap=0)
    fill_ops(c, ECONO_LINE_OPS, layout.BLUE, even_odd=True)
    for filename, x, y, w, h, smask in IMAGES:
        draw_image(c, filename, x, y, w, h, smask=smask)
    draw_spans(c, _spans())
