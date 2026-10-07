"""Calage justificatif heures de conduite (Y PyMuPDF depuis le haut)."""

PAGE_W = 595.28
PAGE_H = 841.89

FONT = "Conduite-Verdana"
FONT_BOLD = "Conduite-Verdana-Bold"
FONT_DEJAVU = "Conduite-DejaVuSans"
FONT_TREBUCHET = "Conduite-TrebuchetMS"
FONT_HELV = "Helvetica"

FONT_FILE = "Verdana.ttf"
FONT_BOLD_FILE = "Verdana-Bold.ttf"
FONT_DEJAVU_FILE = "DejaVuSans.ttf"
FONT_TREBUCHET_FILE = "TrebuchetMS.ttf"

FONT_ASCENT = 1005
FONT_DESCENT = -210
FONT_BBOX = (-560, -303, 1523, 1051)

FONT_BOLD_ASCENT = 1005
FONT_BOLD_DESCENT = -210
FONT_BOLD_BBOX = (-550, -303, 1707, 1072)

FONT_DEJAVU_ASCENT = 928
FONT_DEJAVU_DESCENT = -236
FONT_DEJAVU_BBOX = (-1021, -463, 1793, 1232)
FONT_DEJAVU_CAP = 729

FONT_TREB_ASCENT = 939
FONT_TREB_DESCENT = -222
FONT_TREB_BBOX = (-532, -262, 1311, 985)

COLOR = "#000000"
COLOR_MUTED = "#2D2D2D"
COLOR_WHITE = "#FFFFFF"
COLOR_GRID = "#000000"

SIZE_TITLE = 15.0
SIZE_NOTICE = 8.0
SIZE_EDITION = 8.0
SIZE_NAME = 10.0
SIZE_HEAD = 8.0
SIZE_CELL = 7.0
SIZE_SCHOOL = 12.0
SIZE_LEGAL = 6.0

LOGO_FILE = "cfrvitry.png"
LOGO_X = 14.173
LOGO_Y = 21.725
LOGO_W = 102.047
LOGO_H = 41.59

TITLE_X = 205.45
TITLE_Y = 48.49
NOTICE_X = 172.81
NOTICE_Y = 102.49
EDITION_X = 17.05
EDITION_Y = 82.33
NAME_X = 445.09
NAME_Y = 176.89

HEAD_Y = 198.13
HEAD_DATE_X = 54.97
HEAD_START_X = 121.45
HEAD_END_X = 164.41
HEAD_ACT_X = 266.65
HEAD_COM_X = 442.81

DATE_X = 17.0
START_X = 124.57
END_X = 161.0
ACT_X = 192.25
# même retrait que Activité depuis le bord gauche de la cellule
COM_X = 381.477

FILL_XS = (14.173, 116.923, 153.15, 189.374, 378.601, 581.102)
HEAD_FILL_Y = (187.086, 202.688)
HEAD_U = (
    (14.315, 116.923),
    (117.065, 153.15),
    (153.292, 189.374),
    (189.516, 378.601),
)
HEAD_U_Y = (187.228, 202.547)
HEAD_LAST_RE = (378.742, 187.228, 580.96, 202.546)

DATA_CELLS = (
    (14.315, 116.782, "right"),
    (117.065, 153.008, "right"),
    (153.292, 189.232, "right"),
    (189.516, 378.459, "right"),
    (378.742, 580.96, "left"),
)
DATA_OUTER = (14.315, 580.961)
DATA_FILL_Y0 = 202.683
DATA_FILL_H = 16.971
DATA_STROKE_Y0 = 202.824
DATA_STROKE_H = 16.69
DATA_LINE_H = 16.688
DATA_STEP = 16.974
GRID_W = 0.283
GRID_DASH = (0.24, 0.82)

FOOTER_FILL = (14.173, 752.17, 581.102, 827.773)
FOOTER_STROKE_W = 0.312
FOOTER_PATH = (
    ("m", 24.996, 752.326),
    ("l", 573.114, 752.326),
    ("c", 577.44, 752.326, 580.946, 755.833, 580.946, 760.158),
    ("l", 580.946, 797.842),
    ("c", 580.946, 802.168, 577.44, 805.674, 573.114, 805.674),
    ("l", 24.996, 805.674),
    ("c", 20.67, 805.674, 17.164, 802.168, 17.164, 797.842),
    ("l", 17.164, 760.158),
    ("c", 17.164, 755.833, 20.67, 752.326, 24.996, 752.326),
)

SCHOOL_X = 263.17
SCHOOL_Y = 767.05
ADDR_X = 155.0
ADDR_Y = 778.89
LEGAL1_X = 48.13
LEGAL1_Y = 786.97
LEGAL2_X = 192.61
LEGAL2_Y = 794.17
LEGAL3_X = 274.09
LEGAL3_Y = 801.37

MAX_ELEVE = 40
MAX_EDITION = 24
MAX_JOUR = 4
MAX_DATE = 10
MAX_TIME = 5
MAX_ACTIVITE = 40
MAX_COMMENT = 50
MAX_ROWS = 20
DATE_GAP = 1.0

JOURS = ("Lun.", "Mar.", "Mer.", "Jeu.", "Ven.", "Sam.", "Dim.")

# date DejaVu / heures+activité Verdana
_ROW_TEXT = (
    (212.89, 213.97, 213.97, 213.97),
    (228.89, 230.89, 230.89, 230.89),
    (245.89, 247.93, 247.93, 247.93),
)


def data_fill_ys(i: int) -> tuple[float, float]:
    y0 = DATA_FILL_Y0 + i * DATA_STEP
    return y0, y0 + DATA_FILL_H


def data_stroke_ys(i: int) -> tuple[float, float, float]:
    y0 = DATA_STROKE_Y0 + i * DATA_STEP
    return y0, y0 + DATA_STROKE_H, y0 + DATA_LINE_H


def row_text_ys(i: int) -> tuple[float, float, float, float]:
    if i < len(_ROW_TEXT):
        return _ROW_TEXT[i]
    delta = (i - 2) * DATA_STEP
    date_y, hour_y, _end_y, _act_y = _ROW_TEXT[2]
    return date_y + delta, hour_y + delta, hour_y + delta, hour_y + delta

