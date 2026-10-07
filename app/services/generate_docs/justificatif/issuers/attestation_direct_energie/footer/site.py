"""www.direct-energie.com — Gotham Rounded Bold jaune."""

from .. import copy as texts
from .. import layout
from ..paint import draw_string, fill


def draw(c, doc):
    if not doc.visible.footer_site:
        return
    fill(c, layout.COLOR_SITE)
    draw_string(
        c, layout.SITE_X, layout.SITE_Y,
        texts.SITE, layout.FONT_GOTHAM_BOLD, layout.SITE_SIZE,
    )
