import json
from pathlib import Path

from .. import layout
from ..paint import y_up

# ----------------------------------------------------------------------

_BLUE_DATA = None
_RED_PTS = [
    (43.9148, 37.2370),
    (61.4102, 14.5190),
    (58.8262, 14.5190),
    (41.2730, 37.2370),
]


def _load_data():
    global _BLUE_DATA
    if _BLUE_DATA is None and layout.LOGO_AXA_JSON.is_file():
        raw = json.loads(layout.LOGO_AXA_JSON.read_text(encoding="utf-8"))
        if len(raw) >= 2:
            _BLUE_DATA = raw[1]


def draw(c, doc):
    _load_data()
    if not _BLUE_DATA:
        return

    c.saveState()
    c.setFillColorRGB(*_BLUE_DATA["fill"])
    p = c.beginPath()

    items = _BLUE_DATA["items"]
    r = items[0][1]
    p.rect(r[0], y_up(r[3]), r[2] - r[0], r[3] - r[1])

    def _add_subpath(sub_items):
        first = sub_items[0]
        p.moveTo(first[1][0], y_up(first[1][1]))
        for it in sub_items:
            kind = it[0]
            pts = it[1]
            if kind == "l":
                p.lineTo(pts[2], y_up(pts[3]))
            elif kind == "c":
                p.curveTo(pts[2], y_up(pts[3]), pts[4], y_up(pts[5]), pts[6], y_up(pts[7]))
        p.close()

    _add_subpath(items[1:58])
    _add_subpath(items[58:63])
    _add_subpath(items[63:67])
    _add_subpath(items[67:72])

    c.drawPath(p, fill=1, stroke=0)

    c.setFillColorRGB(1.0, 0.090074, 0.128893)
    pr = c.beginPath()
    pr.moveTo(_RED_PTS[0][0], y_up(_RED_PTS[0][1]))
    for pt in _RED_PTS[1:]:
        pr.lineTo(pt[0], y_up(pt[1]))
    pr.close()
    c.drawPath(pr, fill=1, stroke=0)
    c.restoreState()
