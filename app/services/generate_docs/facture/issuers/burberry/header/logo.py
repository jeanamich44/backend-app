"""Logo wordmark BURBERRY / LONDON ENGLAND."""

from .. import layout
from ..paint import clip_rect, draw_image


def draw(c, doc):
    if not doc.visible.header_logo:
        return
    c.saveState()
    clip_rect(
        c, layout.LOGO_CLIP_X, layout.LOGO_CLIP_Y,
        layout.LOGO_CLIP_W, layout.LOGO_CLIP_H,
    )
    draw_image(
        c, layout.LOGO_FILE,
        layout.LOGO_X, layout.LOGO_Y,
        layout.LOGO_W, layout.LOGO_H,
    )
    c.restoreState()
