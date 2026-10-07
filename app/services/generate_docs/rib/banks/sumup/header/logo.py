"""Wordmark SumUp : fills noirs du Form1, clip /BBox."""

from .. import layout
from ..paint import clip_rect, fill_fills
from .paths import FILLS


def draw(c, doc, dy=0):
    if not doc.visible.header_logo:
        return
    fills = FILLS
    if dy:
        shifted = []
        for fill in FILLS:
            subs = []
            for sub in fill:
                items = []
                for item in sub:
                    if item[0] == "m":
                        items.append(("m", item[1], item[2] + dy))
                    elif item[0] == "l":
                        items.append(("l", item[1], item[2] + dy))
                    elif item[0] == "c":
                        items.append((
                            "c",
                            (item[1][0], item[1][1] + dy),
                            (item[2][0], item[2][1] + dy),
                            (item[3][0], item[3][1] + dy),
                        ))
                    else:
                        items.append(item)
                subs.append(tuple(items))
            shifted.append(tuple(subs))
        fills = tuple(shifted)
    c.saveState()
    clip_rect(
        c,
        layout.LOGO_X,
        layout.LOGO_Y_TOP + dy,
        layout.LOGO_X + layout.LOGO_W,
        layout.LOGO_Y_TOP + layout.LOGO_H + dy,
    )
    fill_fills(c, fills, layout.LOGO_COLOR)
    c.restoreState()
