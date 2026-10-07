from .. import layout
from ..chrome import vectors
from ..paint import fill_ops


def draw(c, doc):
    if not doc.visible.header_logo:
        return
    for ops in vectors.LOGO_PATHS:
        fill_ops(c, ops, layout.COLOR_BLACK)
