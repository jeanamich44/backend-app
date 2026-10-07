PAGE_W = 595.28
PAGE_H = 841.89

# ----------------------------------------------------------------------

FONT_COURIER = "Courier"
FONT_COURIER_SIZE = 8.3
CHAR_W = 4.98
LINE_LEADING = 12.7

FONT_HELVETICA = "Helvetica"
FONT_FOOTER_SIZE = 5.3

# ----------------------------------------------------------------------

COLOR_BLACK = (0.0, 0.0, 0.0)
COLOR_ORANGE = (0.9118, 0.3059, 0.0588)
COLOR_GREY = (0.2667, 0.2784, 0.2863)
COLOR_CYAN = (0.0, 0.6157, 0.7216)
COLOR_SIDEBAR_BG = (0.8314, 0.8392, 0.8471)

# ----------------------------------------------------------------------

LOGO_X = 16.456
LOGO_Y_TOP = 30.724
LOGO_W = 153.783
LOGO_H = 105.111

BARCODE_X = 32.0
BARCODE_Y_TOP = 218.0
BARCODE_W = 134.4
BARCODE_H = 32.0
BARCODE_Y_ORIGIN = 592.0

SIDEBAR_X = 17.01
SIDEBAR_Y_TOP = 277.91
SIDEBAR_W = 153.03
SIDEBAR_H = 489.59

# ----------------------------------------------------------------------

PAD_COLUMNS = 37
PAD_TOTALS = 67
PAD_NOTICE_CUMUL = 51
PAD_NOTICE_MERCI = 67
PAD_NOTICE_GARANTIE = 59
PAD_NOTICE_PRODUIT = 74

LEFT_COLUMN_WIDTH = 40

COL_DESC = 38
COL_CODE = 10
COL_QTY = 5
COL_PU = 10
COL_TVA = 7
COL_TOTAL = 10

COL_TOTALS_LABEL = 40
COL_TOTALS_AMOUNT = 10

COL_REGLEMENT_TITRE = 30
COL_REGLEMENT_LABEL = 40
COL_REGLEMENT_AMOUNT = 10

MAX_ITEMS = 3
MIN_ITEMS = 1

# ----------------------------------------------------------------------

CODE39_PATTERNS = {
    "0": "bsbSBsBsb", "1": "BsbSbsbsB", "2": "bsBSbsbsB", "3": "BsBSbsbsb",
    "4": "bsbSBsbsB", "5": "BsbSBsbsb", "6": "bsBSBsbsb", "7": "bsbSbsBsB",
    "8": "BsbSbsBsb", "9": "bsBSbsBsb", "A": "BsbsbSbsB", "B": "bsBsbSbsB",
    "C": "BsBsbSbsb", "D": "bsbsBSbsB", "E": "BsbsBSbsb", "F": "bsBsBSbsb",
    "G": "bsbsbSBsB", "H": "BsbsbSBsb", "I": "bsBsbSBsb", "J": "bsbsBSBsb",
    "K": "BsbsbsbSB", "L": "bsBsbsbSB", "M": "BsBsbsbSb", "N": "bsbsBsbSB",
    "O": "BsbsBsbSb", "P": "bsBsBsbSb", "Q": "bsbsbsBSB", "R": "BsbsbsBSb",
    "S": "bsBsbsBSb", "T": "bsbsBsBSb", "U": "BSbsbsbsB", "V": "bSBsbsbsB",
    "W": "BSBsbsbsb", "X": "bSbsBsbsB", "Y": "BSBsbsbsb", "Z": "bSBsBsbsb",
    "-": "bSbsbsBsB", ".": "BSbsbsBsb", " ": "bSBsbsBsb", "*": "bSbsBsBsb",
    "$": "bSbSbSbsb", "/": "bSbSbsbSb", "+": "bSbsbSbSb", "%": "bsbSbSbSb",
}

# ----------------------------------------------------------------------

def get_barcode_bars(value: str | None = None, narrow: float = 0.8, wide: float = 1.6, gap: float = 0.8):
    raw = (value or "F905FQ09058").strip().upper()
    val = "".join(c for c in raw if c in CODE39_PATTERNS and c != "*")
    full_text = f"*{val}*"
    
    bars = []
    x = 0.0
    for char_idx, ch in enumerate(full_text):
        pat = CODE39_PATTERNS.get(ch, CODE39_PATTERNS["-"])
        for el_idx in range(9):
            is_bar = (el_idx % 2 == 0)
            symbol = pat[el_idx]
            w = wide if symbol in ("B", "S") else narrow
            if is_bar:
                bars.append((round(x, 3), round(w, 3)))
            x += w
        if char_idx < len(full_text) - 1:
            x += gap
    return bars
