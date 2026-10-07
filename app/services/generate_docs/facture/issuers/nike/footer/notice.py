"""Notice retours + lien www.nike.com souligné."""

from .. import copy as texts
from .. import layout
from ..paint import draw_kerned, fill, fill_rect, kerned_width


def draw(c, doc):
    if not doc.visible.footer_notice:
        return
    fill(c, layout.COLOR)
    draw_kerned(
        c, layout.FOOTER_X, layout.NOTICE_Y[0],
        texts.NOTICE_1, layout.FONT_BOLD, layout.SIZE_BODY,
        max_width=layout.FOOTER_MAX_W,
    )
    y = layout.NOTICE_Y[1]
    prefix = texts.NOTICE_PREFIX
    link = texts.NOTICE_LINK
    suffix = texts.NOTICE_SUFFIX
    x = layout.FOOTER_X
    draw_kerned(c, x, y, prefix, layout.FONT_BOLD, layout.SIZE_BODY)
    x += kerned_width(prefix, layout.FONT_BOLD, layout.SIZE_BODY)
    fill(c, layout.COLOR_LINK)
    draw_kerned(c, x, y, link, layout.FONT_BOLD, layout.SIZE_BODY)
    link_w = kerned_width(link, layout.FONT_BOLD, layout.SIZE_BODY)
    fill_rect(
        c, x, layout.LINK_UNDERLINE[0],
        x + link_w, layout.LINK_UNDERLINE[1],
        layout.COLOR_LINK,
    )
    fill(c, layout.COLOR)
    draw_kerned(
        c, x + link_w, y, suffix,
        layout.FONT_BOLD, layout.SIZE_BODY,
    )
