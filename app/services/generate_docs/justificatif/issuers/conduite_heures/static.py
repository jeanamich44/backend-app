"""Spans statiques (origines PyMuPDF). Sans PII élève."""

from . import copy as texts
from . import layout
from .paint import draw_string, fill

_FONTS = {"r": layout.FONT, "b": layout.FONT_BOLD}
_LAYER_OK = {
    "banner": lambda v: v.header and v.header_banner,
    "middle": lambda v: v.middle,
    "footer": lambda v: v.footer,
}

SPANS = (
    (layout.TITLE_X, layout.TITLE_Y, texts.TITLE, "b", 15.0, "#000000", "banner"),
    (layout.NOTICE_X, layout.NOTICE_Y, texts.NOTICE, "r", 8.0, "#000000", "banner"),
    (layout.HEAD_DATE_X, layout.HEAD_Y, texts.HEAD_DATE, "b", 8.0, "#000000", "middle"),
    (layout.HEAD_START_X, layout.HEAD_Y, texts.HEAD_START, "b", 8.0, "#000000", "middle"),
    (layout.HEAD_END_X, layout.HEAD_Y, texts.HEAD_END, "b", 8.0, "#000000", "middle"),
    (layout.HEAD_ACT_X, layout.HEAD_Y, texts.HEAD_ACT, "b", 8.0, "#000000", "middle"),
    (layout.HEAD_COM_X, layout.HEAD_Y, texts.HEAD_COM, "b", 8.0, "#000000", "middle"),
    (layout.SCHOOL_X, layout.SCHOOL_Y, texts.SCHOOL, "r", 12.0, "#000000", "footer"),
    (layout.LEGAL1_X, layout.LEGAL1_Y, texts.LEGAL_1, "r", 6.0, "#000000", "footer"),
    (layout.LEGAL2_X, layout.LEGAL2_Y, texts.LEGAL_2, "r", 6.0, "#000000", "footer"),
    (layout.LEGAL3_X, layout.LEGAL3_Y, texts.LEGAL_3, "r", 6.0, "#000000", "footer"),
)


def draw(c, doc):
    vis = doc.visible
    last_color = None
    for x, y, text, font, size, color, layer_name in SPANS:
        if not _LAYER_OK[layer_name](vis):
            continue
        if color != last_color:
            fill(c, color)
            last_color = color
        draw_string(c, x, y, text, _FONTS[font], size)
