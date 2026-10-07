"""Logo Crédit Agricole : vecteurs du gabarit (pas le SVG svglib)."""

import json
from pathlib import Path

from reportlab.pdfgen.canvas import FILL_EVEN_ODD, FILL_NON_ZERO

from ..paint import y_up

_SHAPES = json.loads(
    (Path(__file__).resolve().parents[1] / "chrome" / "logo.json").read_text(encoding="utf-8")
)


def draw(c, doc, dy=0):
    if not doc.visible.header_logo:
        return
    for shape in _SHAPES:
        path = c.beginPath()
        c.setFillColorRGB(*shape["fill"])
        for op in shape["ops"]:
            kind = op[0]
            if kind == "m":
                path.moveTo(op[1], y_up(op[2] + dy))
            elif kind == "l":
                path.lineTo(op[1], y_up(op[2] + dy))
            elif kind == "c":
                path.curveTo(
                    op[1], y_up(op[2] + dy),
                    op[3], y_up(op[4] + dy),
                    op[5], y_up(op[6] + dy),
                )
            elif kind == "re":
                x0, y0, x1, y1 = op[1], op[2], op[3], op[4]
                top, bot = min(y0, y1), max(y0, y1)
                path.rect(x0, y_up(bot + dy), x1 - x0, bot - top)
        mode = FILL_EVEN_ODD if shape["even_odd"] else FILL_NON_ZERO
        c.drawPath(path, stroke=0, fill=1, fillMode=mode)
