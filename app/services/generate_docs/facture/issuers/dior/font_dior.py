import zlib
from reportlab.pdfbase.pdfdoc import (
    PDFArray,
    PDFDictionary,
    PDFName,
    PDFStream,
    PDFString,
)
try:
    from core.paths import ASSETS_DIR
except ImportError:
    from app.services.generate_docs.common.paths import ASSETS_DIR

# ----------------------------------------------------------------------

KERNING_PAIRS = {
    ("A", "T"): 74.5,
    ("T", "A"): 84.2,
    ("r", "e"): 11.0,
    ("e", " "): 28.9,
    ("A", "v"): 55.9,
    ("v", "e"): 18.5,
    ("n", "u"): 10.1,
    ("P", "a"): 28.3,
    ("T", "r"): 74.5,
    ("F", "e"): 74.5,
    ("e", "v"): 10.2,
    ("r", "i"): 19.6,
    ("V", "e"): 120.1,
    ("K", "C"): 75.0,
    ("T", "O"): 47.4,
    ("A", "U"): 45.7,
    ("r", "o"): 19.8,
    ("O", "T"): 28.1,
    ("F", "a"): 55.7,
    ("u", "r"): 10.5,
    ("T", "V"): 120.4,
    ("V", "A"): 120.4,
    ("P", "r"): 19.8,
    ("T", "C"): 37.4,
    ("F", "r"): 58.2,
    ("t", "a"): 11.3,
    ("m", "a"): 10.0,
    ("a", "y"): 10.0,
    ("e", "x"): 10.3,
    ("x", "c"): 9.8,
    ("c", "h"): 10.9,
    ("o", "w"): 9.6,
    ("d", "a"): 9.8,
    ("R", "e"): 45.9,
    ("e", "l"): 10.8,
}

# ----------------------------------------------------------------------

TT0_WIDTHS = [
    250, 333, 408, 500, 500, 875, 778, 180, 240, 240, 500, 667, 250, 312, 250, 521,
    500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 250, 278, 564, 564, 564, 444,
    917, 677, 667, 719, 760, 625, 552, 722, 802, 354, 389, 781, 604, 927, 750, 823,
    562, 722, 729, 542, 698, 771, 729, 944, 722, 722, 611, 333, 278, 333, 469, 500,
    333, 469, 521, 427, 521, 438, 271, 469, 531, 250, 278, 500, 240, 802, 531, 500,
    521, 521, 365, 333, 292, 521, 458, 677, 479, 458, 444, 480, 200, 480, 541, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 250, 333, 500, 500, 500, 500, 200, 500, 333, 760, 276, 500, 564, 333,
    760, 500, 400, 549, 300, 300, 333, 576, 453, 333, 333, 300, 310, 500, 750, 750,
    750, 444, 722, 722, 722, 722, 722, 722, 889, 667, 611, 611, 611, 611, 333, 333,
    333, 333, 722, 722, 722, 722, 722, 722, 722, 564, 722, 722, 722, 722, 722, 722,
    556, 500, 444, 444, 444, 444, 444, 444, 667, 444, 438, 438,
]

# ----------------------------------------------------------------------

TT1_WIDTHS = [
    250, 333, 555, 500, 500, 1000, 833, 278, 344, 344, 500, 570, 250, 333, 250, 278,
    500, 542, 500, 500, 500, 500, 500, 500, 500, 500, 333, 333, 570, 570, 570, 500,
    930, 722, 667, 722, 722, 667, 611, 778, 778, 389, 500, 778, 667, 944, 722, 778,
    611, 778, 722, 556, 667, 722, 722, 1000, 722, 722, 667, 333, 278, 333, 581, 500,
    333, 500, 556, 444, 615, 444, 333, 500, 556, 333, 333, 556, 278, 833, 556, 562,
    615, 556, 479, 479, 365, 604, 500, 722, 500, 500, 444, 394, 220, 394, 520, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 250, 333, 500, 500, 500, 500, 220, 500, 333, 747, 300, 500, 570, 333,
    747, 500, 400, 549, 300, 300, 333, 576, 540, 333, 333, 300, 330, 500, 750, 750,
    750, 500, 722, 722, 722, 722, 722, 722, 1000, 722, 667, 667, 667, 667, 389, 389,
    389, 389, 722, 722, 778, 778, 778, 778, 778, 570, 778, 722, 722, 722, 722, 722,
    611, 556, 500, 500, 500, 500, 500, 500, 722, 444, 444, 444,
]

# ----------------------------------------------------------------------

def enc_winansi(text: str) -> str:
    raw = text.encode("cp1252", errors="replace")
    out = []
    for b in raw:
        if b == 40:
            out.append(r"\(")
        elif b == 41:
            out.append(r"\)")
        elif b == 92:
            out.append(r"\\")
        elif 32 <= b <= 126:
            out.append(chr(b))
        else:
            out.append(f"\\{b:03o}")
    return "".join(out)

# ----------------------------------------------------------------------

def enc_chunk(text: str) -> str:
    if not text:
        return ""
    return f"({enc_winansi(text)})"

# ----------------------------------------------------------------------

def build_tj_winansi(text: str) -> str:
    if not text:
        return ""
    chunks = []
    curr = []
    i = 0
    n = len(text)
    while i < n:
        curr.append(text[i])
        if i + 1 < n:
            pair = (text[i], text[i + 1])
            if pair in KERNING_PAIRS:
                chunks.append(enc_chunk("".join(curr)))
                chunks.append(str(KERNING_PAIRS[pair]))
                curr = []
        i += 1
    if curr:
        chunks.append(enc_chunk("".join(curr)))
    return " ".join(chunks)

# ----------------------------------------------------------------------

def attach_dior_fonts(c):
    basic_fonts = c._doc.idToObject.get("BasicFonts")
    if basic_fonts is None:
        return
    basic_fonts.dict.pop("F1", None)

    if "TT0" in basic_fonts.dict:
        return

    ttf_path0 = ASSETS_DIR / "fonts" / "Baskerville.ttf"
    with open(ttf_path0, "rb") as f:
        raw0 = f.read()
    comp0 = zlib.compress(raw0)
    ff0 = PDFStream(
        dictionary=PDFDictionary({"Length1": len(raw0), "Filter": PDFName("FlateDecode")}),
        content=comp0,
        filters=[],
    )
    ff0_ref = c._doc.Reference(ff0)

    desc0 = PDFDictionary({
        "Type": PDFName("FontDescriptor"),
        "FontName": PDFName("BUZULU+Baskerville"),
        "FontFamily": PDFString("Baskerville"),
        "FontStretch": PDFName("Normal"),
        "FontWeight": 400,
        "Flags": 34,
        "FontBBox": PDFArray([-506, -344, 1766, 961]),
        "ItalicAngle": 0,
        "Ascent": 961,
        "Descent": -344,
        "CapHeight": 669,
        "StemV": 68,
        "XHeight": 400,
        "FontFile2": ff0_ref,
    })
    desc0_ref = c._doc.Reference(desc0)

    font0 = PDFDictionary({
        "Type": PDFName("Font"),
        "Subtype": PDFName("TrueType"),
        "BaseFont": PDFName("BUZULU+Baskerville"),
        "Encoding": PDFName("WinAnsiEncoding"),
        "FirstChar": 32,
        "LastChar": 233,
        "Widths": PDFArray(TT0_WIDTHS),
        "FontDescriptor": desc0_ref,
    })
    font0_ref = c._doc.Reference(font0, "TT0")
    basic_fonts.dict["TT0"] = font0_ref

    ttf_path1 = ASSETS_DIR / "fonts" / "Baskerville-Bold.ttf"
    with open(ttf_path1, "rb") as f:
        raw1 = f.read()
    comp1 = zlib.compress(raw1)
    ff1 = PDFStream(
        dictionary=PDFDictionary({"Length1": len(raw1), "Filter": PDFName("FlateDecode")}),
        content=comp1,
        filters=[],
    )
    ff1_ref = c._doc.Reference(ff1)

    desc1 = PDFDictionary({
        "Type": PDFName("FontDescriptor"),
        "FontName": PDFName("BUZULU+Baskerville-Bold"),
        "FontFamily": PDFString("Baskerville"),
        "FontStretch": PDFName("Normal"),
        "FontWeight": 700,
        "Flags": 34,
        "FontBBox": PDFArray([-604, -389, 1897, 1022]),
        "ItalicAngle": 0,
        "Ascent": 1022,
        "Descent": -389,
        "CapHeight": 666,
        "StemV": 160,
        "XHeight": 400,
        "FontFile2": ff1_ref,
    })
    desc1_ref = c._doc.Reference(desc1)

    font1 = PDFDictionary({
        "Type": PDFName("Font"),
        "Subtype": PDFName("TrueType"),
        "BaseFont": PDFName("BUZULU+Baskerville-Bold"),
        "Encoding": PDFName("WinAnsiEncoding"),
        "FirstChar": 32,
        "LastChar": 233,
        "Widths": PDFArray(TT1_WIDTHS),
        "FontDescriptor": desc1_ref,
    })
    font1_ref = c._doc.Reference(font1, "TT1")
    basic_fonts.dict["TT1"] = font1_ref

# ----------------------------------------------------------------------

def text_width_tt0(text: str, size: float = 14.0) -> float:
    w = 0.0
    for ch in text:
        code = ord(ch)
        if 32 <= code <= 233:
            w += TT0_WIDTHS[code - 32]
        else:
            w += 500
    return w * size / 1000.0

