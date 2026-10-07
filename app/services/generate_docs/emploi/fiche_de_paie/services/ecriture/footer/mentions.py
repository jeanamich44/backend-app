from .. import layout
from ..paint import draw_string

# ----------------------------------------------------------------------


def draw(c, doc=None):
    draw_string(c, 190.50, 797.88, "Dans votre int\u00e9r\u00eat, conservez ce bulletin sans limitation de dur\u00e9e.", layout.FONT_ARIAL, 8.22, char_space=-0.0030)
    draw_string(c, 107.10, 809.10, "Pour la d\u00e9finition des termes employ", layout.FONT_ARIAL, 8.22, char_space=-0.0080, word_space=0.0040)
    draw_string(c, 239.58, 809.10, "\u00e9s, se reporter au site internet servicepublic.fr rubrique cotisations sociales", layout.FONT_ARIAL, 8.22, char_space=-0.0010, word_space=-0.0020)
    draw_string(c, 540.24, 808.74, "\u00a9Sage ", layout.FONT_ARIAL, 8.22, char_space=-0.0100)
