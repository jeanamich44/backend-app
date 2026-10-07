import tempfile
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas


def new_pdf(filename: str | None = None, pagesize=A4, dest=None) -> tuple:
    if dest is None:
        tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        tmp.close()
        out = Path(tmp.name)
        return Canvas(str(out), pagesize=pagesize), out
    if hasattr(dest, "write"):
        return Canvas(dest, pagesize=pagesize), dest
    out = Path(dest)
    out.parent.mkdir(parents=True, exist_ok=True)
    return Canvas(str(out), pagesize=pagesize), out


def mm(value: float) -> float:
    return value * 72.0 / 25.4
