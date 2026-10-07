"""IBAN compact / contrôle (compte irlandais myPOS, pas de RIB FR)."""

import re


def compact(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", value or "").upper()


def format_groups(value: str, n: int = 4) -> str:
    raw = compact(value)
    return " ".join(raw[i : i + n] for i in range(0, len(raw), n))


def _iban_digits(value: str) -> str:
    out = []
    for ch in value:
        if ch.isdigit():
            out.append(ch)
        elif ch.isalpha():
            out.append(str(ord(ch.upper()) - 55))
    return "".join(out)


def iban_ok(iban: str) -> bool:
    raw = compact(iban)
    if len(raw) < 15:
        return False
    rearr = raw[4:] + raw[:4]
    try:
        return int(_iban_digits(rearr)) % 97 == 1
    except Exception:
        return False
