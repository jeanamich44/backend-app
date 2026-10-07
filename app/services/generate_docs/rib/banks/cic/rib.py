"""Clé RIB et IBAN FR (norme AFNOR)."""

import re

_LETTER = {}
for _i, _group in enumerate(("AJ", "BKS", "CLT", "DMU", "ENV", "FOW", "GPX", "HQY", "IRZ"), start=1):
    for _ch in _group:
        _LETTER[_ch] = _i


def rib_digits(value: str) -> str:
    out = []
    for ch in (value or "").upper():
        if ch.isdigit():
            out.append(ch)
        elif ch in _LETTER:
            out.append(str(_LETTER[ch]))
    return "".join(out) or "0"


def cle_rib(banque: str, guichet: str, compte: str) -> str:
    n = (
        89 * int(rib_digits(banque))
        + 15 * int(rib_digits(guichet))
        + 3 * int(rib_digits(compte))
    )
    return f"{97 - (n % 97):02d}"


def _iban_digits(value: str) -> str:
    out = []
    for ch in value:
        if ch.isdigit():
            out.append(ch)
        elif ch.isalpha():
            out.append(str(ord(ch.upper()) - 55))
    return "".join(out)


def iban_fr(banque: str, guichet: str, compte: str, cle: str) -> str:
    bban = f"{banque}{guichet}{compte}{cle}"
    chk = 98 - (int(_iban_digits(bban + "FR00")) % 97)
    raw = f"FR{chk:02d}{bban}"
    return format_groups(raw, 4)


def compact(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", value or "").upper()


def format_groups(value: str, n: int = 4) -> str:
    raw = compact(value)
    return " ".join(raw[i : i + n] for i in range(0, len(raw), n))


def format_wide(value: str, n: int = 4, gap: int = 7) -> str:
    raw = compact(value)
    parts = [raw[i : i + n] for i in range(0, len(raw), n)]
    return (" " * gap).join(parts)


def iban_ok(iban: str) -> bool:
    raw = compact(iban)
    if len(raw) < 15:
        return False
    rearr = raw[4:] + raw[:4]
    try:
        return int(_iban_digits(rearr)) % 97 == 1
    except Exception:
        return False
