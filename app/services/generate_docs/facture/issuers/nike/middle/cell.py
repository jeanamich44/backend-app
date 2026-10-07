"""Bords de cellule PDF4NET (clip W + trait 1 pt), coords locales HTML."""

import struct

from ..paint import stroke_html_border


def f32(value: float) -> float:
    return struct.unpack("f", struct.pack("f", float(value)))[0]


def sides(
    col_w: float,
    height: float,
    *,
    left_outer=False,
    right_outer=False,
    top=None,
    bottom=None,
    origin_inset=True,
    left=True,
    right=True,
):
    """top/bottom : None, 'full', 'join', 'last'."""
    inset = 0.5 if origin_inset else 0.0
    w = f32(col_w - inset)
    h = f32(height)
    w0 = f32(w - 0.5)
    w1 = f32(w + 0.5) if right_outer else w
    h0 = f32(h - 0.5)
    h_mid = f32(9.6)
    h_bot = f32(10.1)
    h_end = f32(10.6)
    out = []
    if top == "full":
        if left_outer:
            clip = (
                (f32(-0.5), 0.5), (f32(-1), 0), (w1, 0),
                (w1 if right_outer else w, 0.5),
                (w if right_outer else w0, 1), (0, 1),
            )
            start = (f32(-1), 0.5)
        elif origin_inset:
            clip = (
                (f32(-0.5), 0.5), (f32(-0.5), 0), (w1, 0),
                (w if right_outer else w, 0.5),
                (w0, 1), (0, 1),
            )
            start = (f32(-0.5), 0.5)
        else:
            clip = (
                (0, 0.5), (0, 0), (w1, 0), (w, 0.5), (w0, 1), (0, 1),
            )
            start = (0, 0.5)
        out.append((clip, start, (w1, 0.5)))
    elif top == "join":
        out.append((
            ((f32(-0.5), 0.5), (w, 0.5), (w0, 1), (0, 1)),
            (f32(-0.5), 0.5), (w, 0.5),
        ))
    if right and right_outer:
        if bottom == "last":
            clip = (
                (w, 0), (w1, 0), (w1, h_end), (w, h_bot), (w0, h_mid), (w0, 0),
            )
            out.append((clip, (w, 0), (w, h_end)))
        elif top == "full":
            clip = ((w, 0.5), (w1, 0), (w1, h), (w, h), (w0, h0), (w0, 1))
            out.append((clip, (w, 0), (w, h)))
        elif top:
            clip = ((w, 0.5), (w1, 0.5), (w1, h), (w, h), (w0, h), (w0, 1))
            out.append((clip, (w, 0.5), (w, h)))
        else:
            clip = ((w, 0), (w1, 0), (w1, h), (w, h), (w0, h), (w0, 0))
            out.append((clip, (w, 0), (w, h)))
    elif right:
        if top == "full":
            out.append((((w, 0.5), (w, h), (w0, h0), (w0, 1)), (w, 0.5), (w, h)))
        elif top == "join":
            out.append((((w, 0.5), (w, h), (w0, h), (w0, 1)), (w, 0.5), (w, h)))
        elif bottom == "last":
            out.append((((w, 0), (w, h_bot), (w0, h_mid), (w0, 0)), (w, 0), (w, h_bot)))
        else:
            out.append((((w, 0), (w, h), (w0, h), (w0, 0)), (w, 0), (w, h)))
    if bottom == "full":
        out.append((
            ((w, h), (f32(-0.5), h), (0, h0), (w0, h0)),
            (f32(-0.5), h), (w, h),
        ))
    elif bottom == "last":
        if left_outer:
            clip = (
                (w, h_bot), (w, h_end), (f32(-1), h_end), (f32(-0.5), h_bot),
                (0, h_mid), (w0, h_mid),
            )
            start = (f32(-1), h_bot)
            end = (w, h_bot)
        elif right_outer:
            x0 = 0 if not origin_inset else f32(-0.5)
            clip = (
                (w, h_bot), (w1, h_end), (x0, h_end), (x0, h_bot),
                (0, h_mid), (w0, h_mid),
            )
            start = (x0, h_bot)
            end = (w1, h_bot)
        else:
            clip = (
                (w, h_bot), (w, h_end), (f32(-0.5), h_end), (f32(-0.5), h_bot),
                (0, h_mid), (w0, h_mid),
            )
            start = (f32(-0.5), h_bot)
            end = (w, h_bot)
        out.append((clip, start, end))
    if left_outer:
        if top == "full":
            clip = (
                (f32(-0.5), h), (f32(-1), h), (f32(-1), 0),
                (f32(-0.5), 0.5), (0, 1), (0, h0),
            )
            out.append((clip, (f32(-0.5), 0), (f32(-0.5), h)))
        elif top == "join":
            clip = (
                (f32(-0.5), h), (f32(-1), h), (f32(-1), 0.5),
                (f32(-0.5), 0.5), (0, 1), (0, h),
            )
            out.append((clip, (f32(-0.5), 0.5), (f32(-0.5), h)))
        elif bottom == "last":
            clip = (
                (f32(-0.5), h_bot), (f32(-1), h_end), (f32(-1), 0),
                (f32(-0.5), 0), (0, 0), (0, h_mid),
            )
            out.append((clip, (f32(-0.5), 0), (f32(-0.5), h_end)))
        else:
            clip = (
                (f32(-0.5), h), (f32(-1), h), (f32(-1), 0),
                (f32(-0.5), 0), (0, 0), (0, h),
            )
            out.append((clip, (f32(-0.5), 0), (f32(-0.5), h)))
    elif left:
        if top == "full":
            out.append((
                ((f32(-0.5), h), (f32(-0.5), 0.5), (0, 1), (0, h0)),
                (f32(-0.5), 0.5), (f32(-0.5), h),
            ))
        elif top == "join":
            out.append((
                ((f32(-0.5), h), (f32(-0.5), 0.5), (0, 1), (0, h)),
                (f32(-0.5), 0.5), (f32(-0.5), h),
            ))
        elif bottom == "last":
            out.append((
                ((f32(-0.5), h_bot), (f32(-0.5), 0), (0, 0), (0, h_mid)),
                (f32(-0.5), 0), (f32(-0.5), h_bot),
            ))
        else:
            out.append((
                ((f32(-0.5), h), (f32(-0.5), 0), (0, 0), (0, h)),
                (f32(-0.5), 0), (f32(-0.5), h),
            ))
    return tuple(out)


def draw_cell(c, col_w, height, color, **edges):
    stroke_html_border(c, sides(col_w, height, **edges), 1.0, color)
