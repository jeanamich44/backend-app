import datetime
import re
from typing import Any
from fastapi import HTTPException

FR_MONTHS_MAP = {
    "janvier": 1, "janv": 1, "jan": 1,
    "fevrier": 2, "février": 2, "fevr": 2, "févr": 2, "fev": 2, "fév": 2, "feb": 2,
    "mars": 3, "mar": 3,
    "avril": 4, "avr": 4, "apr": 4,
    "mai": 5, "may": 5,
    "juin": 6, "jun": 6,
    "juillet": 7, "juil": 7, "jul": 7,
    "aout": 8, "août": 8, "aou": 8, "aug": 8,
    "septembre": 9, "sept": 9, "sep": 9,
    "octobre": 10, "oct": 10,
    "novembre": 11, "nov": 11,
    "decembre": 12, "décembre": 12, "dec": 12, "déc": 12,
}


def validate_calendar_date(val: Any, label: str = "Date") -> None:
    if not val:
        return
    s = str(val).strip()
    if not s or s.lower() in ("true", "false", "none"):
        return

    s_clean = re.sub(r"^(?:fait\s+à\s+|à\s+)?[A-Za-zÀ-ÿ\s'-]+,\s*(?:le\s*)?", "", s, flags=re.IGNORECASE).strip()
    s_clean = re.sub(r"^(?:lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche|mon|tue|wed|thu|fri|sat|sun)\.?\s*", "", s_clean, flags=re.IGNORECASE).strip()
    s_clean = re.sub(r"^(?:du|le|date(?:\s+de|\s+d['’])?\s+\w*\s*:?)\s*", "", s_clean, flags=re.IGNORECASE).strip()
    s_clean = re.sub(r"[,\s]+(?:\d{1,2}:\d{2}(?::\d{2})?(?:\s*(?:gmt|utc))?).*$", "", s_clean, flags=re.IGNORECASE).strip()

    day, month, year = None, None, None

    m_iso = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})$", s_clean)
    if m_iso:
        year, month, day = int(m_iso.group(1)), int(m_iso.group(2)), int(m_iso.group(3))
    else:
        m_slash = re.match(r"^(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})$", s_clean)
        if m_slash:
            day, month = int(m_slash.group(1)), int(m_slash.group(2))
            year = int(m_slash.group(3))
            if year < 100:
                year += 2000
        else:
            m_text = re.match(r"^(\d{1,2})(?:er)?[\s-]+([A-Za-zÀ-ÿ.]+?)[\s-]+(\d{4})$", s_clean)
            if m_text:
                day = int(m_text.group(1))
                m_name = m_text.group(2).rstrip(".").lower()
                month = FR_MONTHS_MAP.get(m_name)
                year = int(m_text.group(3))
            else:
                m_en = re.match(r"^([A-Za-zÀ-ÿ.]+?)[\s-]+(\d{1,2}),?[\s-]+(\d{4})$", s_clean)
                if m_en:
                    m_name = m_en.group(1).rstrip(".").lower()
                    month = FR_MONTHS_MAP.get(m_name)
                    day = int(m_en.group(2))
                    year = int(m_en.group(3))

    if day is None or month is None or year is None:
        m_search_text = re.search(r"\b(\d{1,2})(?:er)?[\s-]+([A-Za-zÀ-ÿ.]+?)[\s-]+(\d{4})\b", s)
        if m_search_text:
            m_name = m_search_text.group(2).rstrip(".").lower()
            if m_name in FR_MONTHS_MAP:
                day = int(m_search_text.group(1))
                month = FR_MONTHS_MAP[m_name]
                year = int(m_search_text.group(3))
        if day is None or month is None or year is None:
            m_search_slash = re.search(r"\b(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})\b", s)
            if m_search_slash:
                day = int(m_search_slash.group(1))
                month = int(m_search_slash.group(2))
                year = int(m_search_slash.group(3))
                if year < 100:
                    year += 2000
            elif not (day and month and year):
                m_search_iso = re.search(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b", s)
                if m_search_iso:
                    year = int(m_search_iso.group(1))
                    month = int(m_search_iso.group(2))
                    day = int(m_search_iso.group(3))

    if day is None or month is None or year is None:
        raise HTTPException(
            status_code=400,
            detail=f"{label} invalide : '{val}'. Format de date non reconnu.",
        )

    if not (1 <= month <= 12):
        raise HTTPException(
            status_code=400,
            detail=f"{label} invalide : mois {month} incorrect.",
        )

    if not (1900 <= year <= 2100):
        raise HTTPException(
            status_code=400,
            detail=f"{label} invalide : année {year} incorrecte.",
        )

    try:
        datetime.date(year, month, day)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"{label} invalide : date calendaire inexistante ({day:02d}/{month:02d}/{year}).",
        )


def validate_time_format(val: Any, label: str = "Heure") -> None:
    if not val:
        return
    s = str(val).strip()
    if not s or s.lower() in ("true", "false", "none"):
        return

    m = re.match(r"^(\d{1,2}):(\d{2})(?::(\d{2}))?$", s)
    if not m:
        raise HTTPException(
            status_code=400,
            detail=f"{label} invalide : '{val}'. Format attendu : HH:MM ou HH:MM:SS.",
        )
    h, minute = int(m.group(1)), int(m.group(2))
    sec = int(m.group(3)) if m.group(3) is not None else 0
    if not (0 <= h <= 23):
        raise HTTPException(status_code=400, detail=f"{label} invalide : heure {h} incorrecte (0-23).")
    if not (0 <= minute <= 59):
        raise HTTPException(status_code=400, detail=f"{label} invalide : minute {minute} incorrecte (0-59).")
    if not (0 <= sec <= 59):
        raise HTTPException(status_code=400, detail=f"{label} invalide : seconde {sec} incorrecte (0-59).")
