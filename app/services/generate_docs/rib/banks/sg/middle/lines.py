"""Cadre RIB : 4 trapèzes fills (onglets 45°, gabarit `h f`)."""

from .. import layout
from ..paint import fill_poly

# Y depuis le haut, premier coupon. Stream : 137.93/494.4 × 679.39–637.72.
_BOX = (
    (
        (137.93, 162.49),
        (494.40, 162.49),
        (493.65, 163.24),
        (138.68, 163.24),
    ),
    (
        (494.40, 204.16),
        (137.93, 204.16),
        (138.68, 203.41),
        (493.65, 203.41),
    ),
    (
        (137.93, 204.16),
        (137.93, 162.49),
        (138.68, 163.24),
        (138.68, 203.41),
    ),
    (
        (494.40, 162.49),
        (494.40, 204.16),
        (493.65, 203.41),
        (493.65, 163.24),
    ),
)


def draw(c, doc, dy=0):
    if not doc.visible.middle_lines:
        return
    for pts in _BOX:
        fill_poly(c, [(x, y + dy) for x, y in pts], layout.COLOR)
