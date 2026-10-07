"""Motif pixel droit : un seul fill opaque (le gabarit composite le Form à 15 %)."""

from .. import layout
from ..paint import fill_union
from .chrome_paths import PATTERN_FILLS


def draw(c, doc, dy=0):
    fill_union(c, PATTERN_FILLS, layout.PATTERN_PAINT, dy=dy, pad=0.0)
