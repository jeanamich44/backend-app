from pathlib import Path
from reportlab.pdfbase.pdfdoc import (
    PDFArray,
    PDFDictionary,
    PDFName,
    PDFObject,
    PDFStream,
)
from .font_dior import build_tj_winansi
from .layout import BG_ALPHA, BG_BBOX

# ----------------------------------------------------------------------

CHROME_DIR = Path(__file__).resolve().parent / "chrome"

# ----------------------------------------------------------------------

class FormXObject(PDFObject):
    def __init__(self, stream: bytes, bbox: list):
        self.stream = stream
        self.bbox = bbox

    def format(self, document):
        gs0 = PDFDictionary({
            "Type": PDFName("ExtGState"),
            "AIS": False,
            "BM": PDFName("Normal"),
            "OP": False,
            "OPM": 1,
            "SA": True,
            "SMask": PDFName("None"),
            "ca": 1,
            "CA": 1,
            "op": False,
        })
        gs0_ref = document.Reference(gs0)
        res = PDFDictionary({"ExtGState": PDFDictionary({"GS0": gs0_ref})})
        group = PDFDictionary({
            "Type": PDFName("Group"),
            "S": PDFName("Transparency"),
            "I": False,
            "K": False,
        })
        d = {
            "Type": PDFName("XObject"),
            "Subtype": PDFName("Form"),
            "BBox": PDFArray(self.bbox),
            "Group": group,
            "Matrix": PDFArray([1, 0, 0, 1, 0, 0]),
            "Resources": res,
        }
        return PDFStream(dictionary=PDFDictionary(d), content=self.stream, filters=[]).format(document)

# ----------------------------------------------------------------------

def draw_string(c, font_name: str, size: float, x: float, y: float, text: str):
    tag = "/TT1" if "bold" in font_name.lower() or "tt1" in font_name.lower() else "/TT0"
    tj_body = build_tj_winansi(text)
    c._code.append(
        f"BT 0 0 0 1 k {tag} 1 Tf {size:.4f} 0 0 {size:.4f} {x:.4f} {y:.4f} Tm [{tj_body}]TJ ET"
    )

# ----------------------------------------------------------------------

def draw_raw_tj(c, font_name: str, size: float, x: float, y: float, tj_body: str):
    tag = "/TT1" if "bold" in font_name.lower() or "tt1" in font_name.lower() else "/TT0"
    c._code.append(
        f"BT 0 0 0 1 k {tag} 1 Tf {size:.4f} 0 0 {size:.4f} {x:.4f} {y:.4f} Tm [{tj_body}]TJ ET"
    )

# ----------------------------------------------------------------------

def draw_boutique_logo(c):
    path = CHROME_DIR / "dior_logo.stream.bin"
    if path.is_file():
        with open(path, "rb") as f:
            stream = f.read().decode("latin1")
        c.saveState()
        c._code.append(f"0 0 0 1 k\n{stream}")
        c.restoreState()

# ----------------------------------------------------------------------

def draw_cash_logo(c):
    path = CHROME_DIR / "dior_cash.stream.bin"
    if path.is_file():
        with open(path, "rb") as f:
            stream = f.read().decode("latin1")
        c.saveState()
        c._code.append(f"0 0 0 1 k\n{stream}")
        c.restoreState()

# ----------------------------------------------------------------------

def draw_code_stream(c):
    path = CHROME_DIR / "dior_code.stream.bin"
    if path.is_file():
        with open(path, "rb") as f:
            stream = f.read().decode("latin1")
        c.saveState()
        c._code.append(f"0 0 0 1 k\n{stream}")
        c.restoreState()

# ----------------------------------------------------------------------

def draw_middle_line(c):
    c.saveState()
    c._code.append(
        "q 0 841.89 595.276 -841.89 re W n 0 0 0 1 K 0.25 w q 1 0 0 1 397.2969 471.7728 cm 0 0 m 171.93 0 l S Q Q"
    )
    c.restoreState()

# ----------------------------------------------------------------------

def draw_vector_bg(c):
    path = CHROME_DIR / "dior_bg.stream.bin"
    if not path.is_file():
        return
    with open(path, "rb") as f:
        stream = f.read()
    form = FormXObject(stream, BG_BBOX)
    name = "Fm0"
    reg = c._doc.getXObjectName(name)
    existing = c._doc.idToObject.get(reg)
    if existing is None:
        c._setXObjects(form)
        c._doc.Reference(form, reg)
        c._doc.addForm(name, form)
    c._formsinuse.append(name)
    c.saveState()
    c.setFillAlpha(BG_ALPHA)
    c.setStrokeAlpha(BG_ALPHA)
    c._code.append(f"/{reg} Do")
    c.restoreState()
