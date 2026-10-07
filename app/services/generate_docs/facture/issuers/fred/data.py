import datetime
import re
from dataclasses import dataclass, field
from typing import List

JOURS_FR = ("Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche")
MOIS_FR = (
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
)


COMMON_POSTAL_CODES = {
    "93330": "Neuilly Sur Marne",
    "92200": "Neuilly Sur Seine",
    "75001": "Paris",
    "75008": "Paris",
    "78150": "Le Chesnay-Rocquencourt",
    "92150": "Suresnes",
    "69001": "Lyon",
    "13001": "Marseille",
    "33000": "Bordeaux",
    "31000": "Toulouse",
    "44000": "Nantes",
    "59000": "Lille",
    "67000": "Strasbourg",
    "06000": "Nice",
    "34000": "Montpellier",
    "35000": "Rennes",
}


def format_fred_date_lieu(date_str: str, ville: str = "Neuilly Sur Marne") -> str:
    ville_clean = (ville or "Neuilly Sur Marne").strip()
    if ville_clean in COMMON_POSTAL_CODES:
        ville_clean = COMMON_POSTAL_CODES[ville_clean]
    s = (date_str or "").strip()
    if not s:
        d = datetime.date.today()
        return f"{ville_clean}, {JOURS_FR[d.weekday()]} {d.day} {MOIS_FR[d.month - 1]} {d.year}"

    day, month, year = None, None, None
    m_slash = re.match(r"^(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})$", s)
    if m_slash:
        day = int(m_slash.group(1))
        month = int(m_slash.group(2))
        year = int(m_slash.group(3))
        if year < 100:
            year += 2000
    else:
        m_iso = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})$", s)
        if m_iso:
            year = int(m_iso.group(1))
            month = int(m_iso.group(2))
            day = int(m_iso.group(3))

    if day and month and year:
        try:
            d = datetime.date(year, month, day)
            return f"{ville_clean}, {JOURS_FR[d.weekday()]} {d.day} {MOIS_FR[d.month - 1]} {d.year}"
        except ValueError:
            pass

    return f"{ville_clean}, {s}"


def parse_price(val: str) -> float:
    if not val:
        return 0.0
    clean = str(val).replace("€", "").replace("EUR", "").replace(" ", "").replace(",", ".")
    try:
        return float(clean)
    except ValueError:
        return 0.0


def format_euro_french(val: float) -> str:
    parts = f"{val:.2f}".split(".")
    integer_part = f"{int(parts[0]):,}".replace(",", " ")
    return f"{integer_part},{parts[1]}"


def format_euro_dot(val: float) -> str:
    parts = f"{val:.2f}".split(".")
    integer_part = f"{int(parts[0]):,}".replace(",", " ")
    return f"{integer_part}.{parts[1]}"


@dataclass
class FredItemData:
    code: str = "0B0006-6B0275"
    quantite: str = "1"
    designation: str = "BRACELET FORCE 10 GRAND MODÈLE OR JAUNE\nAJUSTABLE\nFRED PARIS\nRéférence: 6B0146\nGravure: 1012846"
    prix_ttc: str = "3 250.00"
    total: str = "3 250.00"


@dataclass
class Doc:
    civilite: str = ""
    prenom: str = ""
    nom: str = ""
    adresse: str = ""
    cp: str = ""
    ville: str = ""
    pays: str = ""
    client_tel: str = ""
    client_code: str = ""
    date_facture: str = "02/09/2023"
    date_lieu: str = "Neuilly Sur Marne, Samedi 2 Septembre 2023"
    num_facture: str = "8259"
    store_name: str = "PRINTEMPS PARLY 2"
    store_code: str = "5921489590020"
    mode_paiement: str = "Carte Bleue (Eu)"
    payment_label: str = "Carte Bleue (Eu)"
    total_ttc: str = "3 250.00"
    hors_taxes: str = "2 708,33"
    base_ht: str = "2 708,33"
    tva_20: str = "541,67"
    net_a_payer: str = "3 250.00"
    items: List[FredItemData] = field(default_factory=list)
    visible: dict = field(default_factory=dict)


def from_payload(d: dict) -> Doc:
    d = d or {}
    raw_items = d.get("items")
    items: List[FredItemData] = []
    items_total = 0.0

    if isinstance(raw_items, list) and raw_items:
        for it in raw_items:
            if not isinstance(it, dict):
                continue
            code = str(it.get("code") or it.get("ref") or "").strip()
            desc = str(it.get("designation") or it.get("desc") or "").strip()
            qty = str(it.get("quantite") or it.get("qte") or it.get("qty") or "1").strip()
            unit_price = str(it.get("prix_ttc") or it.get("unit_price") or "0.00").strip()
            tot = str(it.get("total") or it.get("montant") or unit_price).strip()

            unit_float = parse_price(unit_price)
            try:
                q_val = float(qty)
            except ValueError:
                q_val = 1.0

            if unit_float > 0 and (not tot or tot == "0.00"):
                line_tot = unit_float * q_val
                tot = format_euro_dot(line_tot)
            else:
                line_tot = parse_price(tot)

            items_total += line_tot

            items.append(FredItemData(
                code=code or "0B0006-6B0275",
                quantite=qty or "1",
                designation=desc or "BRACELET FORCE 10 GRAND MODÈLE OR JAUNE",
                prix_ttc=unit_price or "3 250.00",
                total=tot or "3 250.00"
            ))
    else:
        items.append(FredItemData())
        items_total = 3250.0

    raw_total_str = str(d.get("total_ttc") or d.get("total") or "").strip()
    total_val = parse_price(raw_total_str) if raw_total_str else items_total
    if total_val <= 0:
        total_val = items_total if items_total > 0 else 3250.0

    ht_val = round(total_val / 1.20, 2)
    tva_val = round(total_val - ht_val, 2)

    total_dot = format_euro_dot(total_val)
    ht_french = format_euro_french(ht_val)
    tva_french = format_euro_french(tva_val)

    df = str(d.get("date_facture") or "02/09/2023").strip()
    ville = str(d.get("ville_emission") or d.get("ville") or "Neuilly Sur Marne").strip()
    raw_dl = str(d.get("date_lieu") or "").strip()
    if raw_dl and not d.get("date_facture") and not d.get("ville_emission"):
        date_lieu_str = raw_dl
    else:
        date_lieu_str = format_fred_date_lieu(df, ville)

    return Doc(
        civilite=str(d.get("civilite") or "").strip(),
        prenom=str(d.get("prenom") or "").strip(),
        nom=str(d.get("nom") or "").strip(),
        adresse=str(d.get("adresse") or "").strip(),
        cp=str(d.get("cp") or "").strip(),
        ville=str(d.get("ville") or "").strip(),
        pays=str(d.get("pays") or "").strip(),
        client_tel=str(d.get("client_tel") or "").strip(),
        client_code=str(d.get("client_code") or "").strip(),
        date_facture=df,
        date_lieu=date_lieu_str,
        num_facture=str(d.get("num_facture") or d.get("facture_num") or "8259").strip(),
        store_name=str(d.get("store_name") or "PRINTEMPS PARLY 2").strip(),
        store_code=str(d.get("store_code") or "5921489590020").strip(),
        mode_paiement=str(d.get("mode_paiement") or "Carte Bleue (Eu)").strip(),
        payment_label=str(d.get("payment_label") or d.get("mode_paiement") or "Carte Bleue (Eu)").strip(),
        total_ttc=total_dot,
        hors_taxes=ht_french,
        base_ht=ht_french,
        tva_20=tva_french,
        net_a_payer=total_dot,
        items=items,
        visible=d.get("visible") if isinstance(d.get("visible"), dict) else {}
    )
