"""Fills du gabarit (colonne crème, filets orange/cyan, pastilles)."""

from ..paint import fill_ops
from . import vectors


def draw(c, doc):
    for color, ops in vectors.FILLS:
        fill_ops(c, ops, color)
