"""Subset TTF en gardant les glyph IDs du gabarit (hinter fpgm/prep/cvt)."""

from reportlab.pdfbase.ttfonts import (
    GF_ARG_1_AND_2_ARE_WORDS,
    GF_MORE_COMPONENTS,
    GF_WE_HAVE_A_SCALE,
    GF_WE_HAVE_AN_X_AND_Y_SCALE,
    GF_WE_HAVE_A_TWO_BY_TWO,
    TTFontMaker,
    _set_ushort,
    pack,
    unpack,
)


def make_subset_keep_ids(self, subset):
    output = TTFontMaker()
    glyphMap = list(range(self.numGlyphs))
    glyphSet = {i: i for i in glyphMap}
    codeToGlyph = {}
    for code in subset:
        codeToGlyph[code] = self.charToGlyph.get(code, 0) if self.charToGlyph else 0

    for tag in ("name", "OS/2", "cvt ", "fpgm", "prep", "gasp", "hdmx", "VDMX"):
        try:
            output.add(tag, self.get_table(tag))
        except KeyError:
            pass

    post = b"\x00\x03\x00\x00" + self.get_table("post")[4:16] + b"\x00" * 16
    output.add("post", post)

    numGlyphs = len(glyphMap)
    hmtx = []
    for n in range(numGlyphs):
        aw, lsb = self.hmetrics[glyphMap[n]]
        hmtx.append(int(aw))
        hmtx.append(int(lsb))
    n = len(hmtx) - 2
    while n and hmtx[n] == hmtx[n - 2]:
        n -= 2
    n += 2
    numberOfHMetrics = n >> 1
    hmtx = hmtx[:n] + hmtx[n + 1::2]
    output.add("hmtx", pack(*([">%dH" % len(hmtx)] + hmtx)))

    hhea = _set_ushort(self.get_table("hhea"), 34, numberOfHMetrics)
    output.add("hhea", hhea)

    maxp = _set_ushort(self.get_table("maxp"), 4, numGlyphs)
    output.add("maxp", maxp)

    entryCount = len(subset)
    length = 10 + entryCount * 2
    cmap = [0, 1, 1, 0, 0, 12, 6, length, 0, 0, entryCount] + list(
        map(codeToGlyph.get, subset)
    )
    output.add("cmap", pack(*([">%dH" % len(cmap)] + cmap)))

    glyphData = self.get_table("glyf")
    offsets = []
    glyf = []
    pos = 0
    start = self.get_table_pos("glyf")[0]
    for n in range(numGlyphs):
        offsets.append(pos)
        originalGlyphIdx = glyphMap[n]
        glyphPos = self.glyphPos[originalGlyphIdx]
        glyphLen = self.glyphPos[originalGlyphIdx + 1] - glyphPos
        data = glyphData[glyphPos:glyphPos + glyphLen]
        if glyphLen > 2 and unpack(">h", data[:2])[0] < 0:
            pos_in_glyph = 10
            flags = GF_MORE_COMPONENTS
            while flags & GF_MORE_COMPONENTS:
                flags = unpack(">H", data[pos_in_glyph:pos_in_glyph + 2])[0]
                glyphIdx = unpack(">H", data[pos_in_glyph + 2:pos_in_glyph + 4])[0]
                data = _set_ushort(data, pos_in_glyph + 2, glyphSet[glyphIdx])
                pos_in_glyph += 4
                if flags & GF_ARG_1_AND_2_ARE_WORDS:
                    pos_in_glyph += 4
                else:
                    pos_in_glyph += 2
                if flags & GF_WE_HAVE_A_SCALE:
                    pos_in_glyph += 2
                elif flags & GF_WE_HAVE_AN_X_AND_Y_SCALE:
                    pos_in_glyph += 4
                elif flags & GF_WE_HAVE_A_TWO_BY_TWO:
                    pos_in_glyph += 8
        glyf.append(data)
        pos += glyphLen
        if pos % 4 != 0:
            padding = 4 - pos % 4
            glyf.append(b"\0" * padding)
            pos += padding
        _ = start
    offsets.append(pos)
    output.add("glyf", b"".join(glyf))

    loca = []
    if (pos + 1) >> 1 > 0xFFFF:
        indexToLocFormat = 1
        loca = pack(*([">%dL" % len(offsets)] + offsets))
    else:
        indexToLocFormat = 0
        loca = pack(*([">%dH" % len(offsets)] + [offset >> 1 for offset in offsets]))
    output.add("loca", loca)
    output.add("head", _set_ushort(self.get_table("head"), 50, indexToLocFormat))
    return output.makeStream()


def bind_keep_ids(face):
    face.makeSubset = make_subset_keep_ids.__get__(face, type(face))
