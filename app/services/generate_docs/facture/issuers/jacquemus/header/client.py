from .. import layout
from ..paint import draw_string, fill

# ----------------------------------------------------------------------

def client_lines(header) -> list[str]:
    lines = []
    if getattr(header, "client_nom", "").strip():
        lines.append(header.client_nom.strip())
    if getattr(header, "client_rue", "").strip():
        lines.append(header.client_rue.strip())
    if getattr(header, "client_complement", "").strip():
        lines.append(header.client_complement.strip())
    if getattr(header, "client_ville_cp", "").strip():
        lines.append(header.client_ville_cp.strip())
    if getattr(header, "client_pays", "").strip():
        lines.append(header.client_pays.strip())
    if getattr(header, "client_tel", "").strip():
        tel = header.client_tel.strip()
        lines.append(tel if tel.startswith("T:") else f"T: {tel}")
    if not lines and hasattr(header, "client_lines") and header.client_lines:
        raw = header.client_lines
        if isinstance(raw, str):
            lines = [l.strip() for l in raw.splitlines() if l.strip()]
        elif isinstance(raw, (list, tuple)):
            lines = [str(l).strip() for l in raw if str(l).strip()]
    return lines

# ----------------------------------------------------------------------

def draw(c, doc):
    if not doc.visible.header_client:
        return
    lines = client_lines(doc.header)
    if not lines:
        return
    fill(c, layout.COLOR_GREY)
    y = layout.CLIENT_Y_START
    for line in lines:
        draw_string(
            c,
            layout.CLIENT_X,
            y,
            str(line),
            layout.FONT_REGULAR,
            layout.FONT_SIZE_BODY,
        )
        y += layout.CLIENT_LEADING
