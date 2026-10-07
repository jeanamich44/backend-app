"""Dates d'exemple : toujours relatives à maintenant (Europe/Paris)."""

from datetime import datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo

    TZ = ZoneInfo("Europe/Paris")
except Exception:
    TZ = None

FR_MONTHS = (
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
)
FR_MONTHS_CAP = tuple(name[:1].upper() + name[1:] for name in FR_MONTHS)
EN_MONTHS = (
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
)
JOURS = ("Lun.", "Mar.", "Mer.", "Jeu.", "Ven.", "Sam.", "Dim.")

# Leçons déjà effectuées : dernier samedi, dimanche, mercredi (ordre chrono).
_LESSON_WEEKDAYS = (5, 6, 2)
_LESSON_SLOTS = (("13:00", "16:00"), ("15:00", "18:00"), ("10:00", "13:00"))
_LESSON_ACTIVITY = "LECON PLATEAU"


def now() -> datetime:
    if TZ is not None:
        return datetime.now(TZ)
    return datetime.now().astimezone()


def _last_weekday(today, weekday: int):
    delta = (today.weekday() - weekday) % 7
    if delta == 0:
        delta = 7
    return today - timedelta(days=delta)


def _pad(value: int, width: int = 2) -> str:
    return f"{value:0{width}d}"


def adidas_invoice(moment: datetime | None = None) -> str:
    """Date de facture Adidas : jour de l'achat / émission (aujourd'hui)."""
    d = moment or now()
    return f"{_pad(d.day)}.{_pad(d.month)}.{d.year}"


def adidas_delivery(moment: datetime | None = None) -> str:
    """Livraison boutique en ligne : même jour que la facture."""
    return adidas_invoice(moment)


def amazon_invoice(moment: datetime | None = None) -> str:
    """Date de facture / livraison Amazon : aujourd'hui."""
    d = moment or now()
    return f"{d.day} {FR_MONTHS[d.month - 1]} {d.year}"


def amazon_order(moment: datetime | None = None) -> str:
    """Commande Amazon : la veille (passée avant la facture)."""
    return amazon_invoice((moment or now()) - timedelta(days=1))


def fnac_web(moment: datetime | None = None) -> str:
    """Fnac.com : commande, facture et échéance le jour même (JJ/MM/AA)."""
    d = moment or now()
    return f"{_pad(d.day)}/{_pad(d.month)}/{_pad(d.year % 100)}"


def fnac_magasin(moment: datetime | None = None) -> str:
    """Magasin Fnac : même logique, format JJ/MM/AAAA."""
    d = moment or now()
    return f"{_pad(d.day)}/{_pad(d.month)}/{d.year}"


def maxance_delivrance(moment: datetime | None = None) -> str:
    """Mémo délivré aujourd'hui."""
    d = moment or now()
    return f"{_pad(d.day)}/{_pad(d.month)}/{d.year}"


def maxance_effet(moment: datetime | None = None) -> tuple[str, str, str]:
    """Prise d'effet : la veille de la délivrance."""
    d = (moment or now()) - timedelta(days=1)
    return _pad(d.day), _pad(d.month), str(d.year)


def ca_edition(moment: datetime | None = None) -> str:
    """RIB CA : date d'édition du document (aujourd'hui)."""
    d = moment or now()
    return f"{_pad(d.day)}/{_pad(d.month)}/{d.year}"


def sumup_document(moment: datetime | None = None) -> str:
    """Relevé SumUp : horodatage GMT du document."""
    d = (moment or now()).astimezone(timezone.utc)
    return (
        f"{_pad(d.day)} {EN_MONTHS[d.month - 1]} {d.year}, "
        f"{_pad(d.hour)}:{_pad(d.minute)} GMT"
    )


def sumup_opening(moment: datetime | None = None) -> str:
    """Ouverture de compte SumUp : il y a 6 mois (compte déjà actif)."""
    d = moment or now()
    month = d.month - 6
    year = d.year
    while month <= 0:
        month += 12
        year -= 1
    day = min(d.day, 28)
    return f"{_pad(day)} {EN_MONTHS[month - 1]} {year}"


def mypos_edition(moment: datetime | None = None) -> str:
    """Certificat myPOS : date d'émission (aujourd'hui)."""
    d = moment or now()
    return f"{FR_MONTHS_CAP[d.month - 1]} {_pad(d.day)} {d.year}"


def nike_invoice(moment: datetime | None = None) -> str:
    """Facture Nike : jour d'émission, sans zéro initial (gabarit)."""
    d = moment or now()
    return f"{d.day}/{d.month}/{d.year}"


def ami_invoice(moment: datetime | None = None) -> str:
    """Facture AMI : date du jour JJ/MM/AAAA."""
    d = moment or now()
    return f"{_pad(d.day)}/{_pad(d.month)}/{d.year}"


def burberry_order(moment: datetime | None = None) -> str:
    """Burberry : commande et expédition le jour même (JJ/MM/AA)."""
    d = moment or now()
    return f"{_pad(d.day)}/{_pad(d.month)}/{_pad(d.year % 100)}"


def edf_attestation(moment: datetime | None = None) -> str:
    """Attestation EDF : « 31 Août 2026 » (jour non paddé)."""
    d = moment or now()
    return f"{d.day} {FR_MONTHS_CAP[d.month - 1]} {d.year}"


def conduite_edition(moment: datetime | None = None) -> str:
    """Horodatage d'édition de la liste (maintenant)."""
    d = moment or now()
    return f"{_pad(d.day)}/{_pad(d.month)}/{d.year} {_pad(d.hour)}:{_pad(d.minute)}"


def conduite_lessons(moment: datetime | None = None) -> list[dict]:
    """Trois leçons déjà faites : dernier samedi, dimanche et mercredi."""
    today = (moment or now()).date()
    days = sorted(_last_weekday(today, weekday) for weekday in _LESSON_WEEKDAYS)
    rows = []
    for index, day in enumerate(days):
        start, end = _LESSON_SLOTS[index]
        rows.append({
            "jour": JOURS[day.weekday()],
            "date": f"{_pad(day.day)}/{_pad(day.month)}/{day.year}",
            "debut": start,
            "fin": end,
            "activite": _LESSON_ACTIVITY,
            "commentaire": "",
        })
    return rows


def dior_invoice(moment: datetime | None = None) -> str:
    d = moment or now()
    mois = FR_MONTHS_CAP[d.month - 1].replace("é", "e")
    return f"{d.day}-{mois}-{d.year} {d.strftime('%H:%M:%S')}"


def dior_date(moment: datetime | None = None) -> str:
    d = moment or now()
    return f"{_pad(d.day)}/{_pad(d.month)}/{d.year}"


def dior_time(moment: datetime | None = None) -> str:
    d = moment or now()
    return f"{_pad(d.hour)}:{_pad(d.minute)}"


def jacquemus_invoice(moment: datetime | None = None) -> str:
    d = moment or now()
    en_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{en_months[d.month - 1]} {d.day},{d.year}"


def jacquemus_date(moment: datetime | None = None) -> str:
    d = moment or now()
    return f"{d.day} {FR_MONTHS[d.month - 1]} {d.year}"


def jacquemus_time(moment: datetime | None = None) -> str:
    d = moment or now()
    return f"{_pad(d.hour)}:{_pad(d.minute)}"


def chanel_date(moment: datetime | None = None) -> str:
    d = moment or now()
    return f"{_pad(d.day)}/{_pad(d.month)}/{d.year}"


def chanel_time(moment: datetime | None = None) -> str:
    d = moment or now()
    return f"{_pad(d.hour)}:{_pad(d.minute)}"


def chanel_invoice(moment: datetime | None = None) -> str:
    d = moment or now()
    return f"{_pad(d.day)}/{_pad(d.month)}/{d.year} {_pad(d.hour)}:{_pad(d.minute)}"


def fred_date_lieu(moment: datetime | None = None, ville: str = "Neuilly Sur Marne") -> str:
    d = moment or now()
    jours = ("Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche")
    return f"{ville}, {jours[d.weekday()]} {d.day} {FR_MONTHS_CAP[d.month - 1]} {d.year}"


def fred_date(moment: datetime | None = None) -> str:
    d = moment or now()
    return f"{_pad(d.day)}/{_pad(d.month)}/{d.year}"


def nocibe_date(moment: datetime | None = None) -> str:
    d = moment or now()
    return f"{_pad(d.day)}/{_pad(d.month)}/{d.year}"





