from .. import layout
from ..paint import draw_string

# ----------------------------------------------------------------------


def draw(c, doc=None):
    emp = getattr(doc, "employeur", None)
    draw_string(c, 33.78, 229.86, "Convention collective :", layout.FONT_ARIAL, 8.22, char_space=-0.0040)
    if emp and emp.convention_collective_court:
        draw_string(c, 118.92, 229.77, emp.convention_collective_court, layout.FONT_ARIAL, 8.22)
