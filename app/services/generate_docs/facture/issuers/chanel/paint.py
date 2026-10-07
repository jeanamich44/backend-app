from app.services.generate_docs.common.paths import LOGOS_DIR
from . import layout

# ----------------------------------------------------------------------

def draw_logo(c):
    path = LOGOS_DIR / "chanel.png" if (LOGOS_DIR / "chanel.png").is_file() else LOGOS_DIR / "channel.png"
    c.drawImage(str(path), layout.LOGO_X, layout.LOGO_Y, layout.LOGO_W, layout.LOGO_H, mask="auto")

# ----------------------------------------------------------------------

def draw_text(c, x: float, y: float, text: str, font_name: str = layout.FONT_REGULAR, font_size: float = layout.STORE_SIZE):
    c.setFont(font_name, font_size)
    c.drawString(x, y, text)

# ----------------------------------------------------------------------

def draw_right_text(c, x: float, y: float, text: str, font_name: str = layout.FONT_REGULAR, font_size: float = layout.STORE_SIZE):
    c.setFont(font_name, font_size)
    c.drawRightString(x, y, text)

# ----------------------------------------------------------------------

def draw_center_text(c, x: float, y: float, text: str, font_name: str = layout.FONT_REGULAR, font_size: float = layout.STORE_SIZE):
    c.setFont(font_name, font_size)
    c.drawCentredString(x, y, text)

# ----------------------------------------------------------------------

def draw_line(c, x1: float, y1: float, x2: float, y2: float, width: float = 1.0):
    c.saveState()
    c.setStrokeColorRGB(0.0, 0.0, 0.0)
    c.setLineWidth(width)
    c.setLineCap(0)
    c.line(x1, y1, x2, y2)
    c.restoreState()

