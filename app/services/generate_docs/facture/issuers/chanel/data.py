from dataclasses import dataclass, field
import re
from . import copy

# ----------------------------------------------------------------------

MONTHS_FR = {
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4,
    "mai": 5, "juin": 6, "juillet": 7, "août": 8, "aout": 8,
    "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12,
    "janv": 1, "févr": 2, "fevr": 2, "avr": 4, "juil": 7, "sept": 9, "oct": 10, "nov": 11, "déc": 12, "dec": 12
}

# ----------------------------------------------------------------------

def _format_chanel_date(date_val: str, time_val: str = "") -> str:
    raw_date = str(date_val or "").strip()
    raw_time = str(time_val or "").strip()

    clean_date = ""
    if raw_date:
        slash_match = re.match(r"^(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})$", raw_date)
        iso_match = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})$", raw_date)
        text_match = re.match(r"^(\d{1,2})\s+([a-zA-ZÀ-ÿ.]+)\s+(\d{4})$", raw_date)

        if slash_match:
            d, m, y = int(slash_match.group(1)), int(slash_match.group(2)), int(slash_match.group(3))
            if y < 100:
                y += 2000
            clean_date = f"{d:02d}/{m:02d}/{y}"
        elif iso_match:
            y, m, d = int(iso_match.group(1)), int(iso_match.group(2)), int(iso_match.group(3))
            clean_date = f"{d:02d}/{m:02d}/{y}"
        elif text_match:
            d = int(text_match.group(1))
            m_str = text_match.group(2).rstrip(".").lower()
            y = int(text_match.group(3))
            m = MONTHS_FR.get(m_str, 9)
            clean_date = f"{d:02d}/{m:02d}/{y}"
        else:
            clean_date = raw_date

    clean_time = ""
    if raw_time:
        t = raw_time.split()[0]
        if len(t) >= 5 and t[2] == ":":
            clean_time = t[:5]
        else:
            clean_time = t

    if " " in clean_date and len(clean_date.split()) == 2 and not clean_time:
        return clean_date
    if clean_date and clean_time:
        return f"{clean_date} {clean_time}"
    if clean_date:
        return f"{clean_date} 14:34"
    if clean_time:
        return f"05/09/2023 {clean_time}"
    return copy.DATE_STR

# ----------------------------------------------------------------------

def _clean_client_name(d: dict) -> str:
    civilite = str(d.get("civilite", "")).strip()
    prenom = str(d.get("prenom", "")).strip()
    nom = str(d.get("nom", "")).strip()

    if civilite or prenom or nom:
        clean_nom = nom
        if prenom and prenom.lower() in nom.lower():
            clean_nom = nom
        elif prenom and nom:
            clean_nom = f"{nom} {prenom}"
        elif prenom:
            clean_nom = prenom

        if civilite and civilite.lower() not in clean_nom.lower():
            return f"{civilite} {clean_nom}".strip()
        return clean_nom.strip()
    if "client_name" in d and isinstance(d["client_name"], str) and d["client_name"].strip():
        return d["client_name"].strip()
    if "client_nom" in d and isinstance(d["client_nom"], str) and d["client_nom"].strip():
        return d["client_nom"].strip()
    return copy.CLIENT_NAME

# ----------------------------------------------------------------------

def _clean_client_addresses(d: dict) -> tuple[str, str, str]:
    addr_1 = str(d.get("adresse", d.get("client_adresse", d.get("client_rue", d.get("client_address_1", copy.CLIENT_ADDRESS_1))))).strip()
    cp = str(d.get("cp", d.get("client_cp", ""))).strip()
    ville = str(d.get("ville", d.get("client_ville", ""))).strip()
    if cp or ville:
        addr_2 = f"{cp} {ville}".strip()
    else:
        addr_2 = str(d.get("client_address_2", copy.CLIENT_ADDRESS_2)).strip()
    addr_3 = str(d.get("pays", d.get("client_pays", d.get("client_address_3", copy.CLIENT_ADDRESS_3)))).strip()
    return addr_1.upper(), addr_2.upper(), addr_3.upper()

# ----------------------------------------------------------------------

def _clean_accueil(d: dict) -> str:
    conseiller = str(d.get("conseiller", d.get("vendeur", d.get("accueil_text", copy.ACCUEIL_TEXT)))).strip()
    if conseiller and not conseiller.lower().startswith("vous avez été accueilli"):
        return f"Vous avez été accueilli par {conseiller}"
    return conseiller or copy.ACCUEIL_TEXT

# ----------------------------------------------------------------------

def _to_float(val: str, default: float = 0.0) -> float:
    try:
        clean = re.sub(r"[^\d.,]", "", str(val)).replace(",", ".")
        return float(clean)
    except Exception:
        return default

# ----------------------------------------------------------------------

@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_contact: bool = True
    header_client: bool = True
    header_meta: bool = True
    middle: bool = True
    middle_accueil: bool = True
    middle_table: bool = True
    middle_totaux: bool = True
    middle_paiement: bool = True
    footer: bool = False

# ----------------------------------------------------------------------

@dataclass
class Header:
    store_line_1: str = copy.STORE_LINE_1
    store_line_2: str = copy.STORE_LINE_2
    client_code: str = copy.CLIENT_CODE
    client_name: str = copy.CLIENT_NAME
    client_address_1: str = copy.CLIENT_ADDRESS_1
    client_address_2: str = copy.CLIENT_ADDRESS_2
    client_address_3: str = copy.CLIENT_ADDRESS_3
    date_str: str = copy.DATE_STR
    facture_num: str = copy.FACTURE_NUM
    caisse_num: str = copy.CAISSE_NUM
    folio_num: str = copy.FOLIO_NUM

# ----------------------------------------------------------------------

@dataclass
class Item:
    desc: str = copy.ARTICLE_DESC
    ref: str = copy.ARTICLE_REF
    qty: str = copy.ARTICLE_QTE
    unit_price: str = copy.ARTICLE_PU
    total: str = copy.ARTICLE_MONTANT

# ----------------------------------------------------------------------

@dataclass
class Middle:
    accueil_text: str = copy.ACCUEIL_TEXT
    col_ref_title: str = copy.COL_REF_TITLE
    col_qte_title: str = copy.COL_QTE_TITLE
    col_pu_title: str = copy.COL_PU_TITLE
    col_montant_title: str = copy.COL_MONTANT_TITLE
    items: list[Item] = field(default_factory=lambda: [Item()])
    articles_count: str = copy.ARTICLES_COUNT
    total_ht: str = copy.TOTAL_HT
    total_tva: str = copy.TOTAL_TVA
    total_ttc: str = copy.TOTAL_TTC
    paiement: str = copy.PAIEMENT

    @property
    def article_desc(self) -> str:
        return self.items[0].desc if self.items else copy.ARTICLE_DESC

    @property
    def article_ref(self) -> str:
        return self.items[0].ref if self.items else copy.ARTICLE_REF

    @property
    def article_qte(self) -> str:
        return self.items[0].qty if self.items else copy.ARTICLE_QTE

    @property
    def article_pu(self) -> str:
        return self.items[0].unit_price if self.items else copy.ARTICLE_PU

    @property
    def article_montant(self) -> str:
        return self.items[0].total if self.items else copy.ARTICLE_MONTANT

# ----------------------------------------------------------------------

@dataclass
class Footer:
    pass

# ----------------------------------------------------------------------

@dataclass
class FactureChannel:
    visible: Visible = field(default_factory=Visible)
    header: Header = field(default_factory=Header)
    middle: Middle = field(default_factory=Middle)
    footer: Footer = field(default_factory=Footer)

# ----------------------------------------------------------------------

Doc = FactureChannel

# ----------------------------------------------------------------------

def _items_from_payload(d: dict) -> list[Item]:
    raw = d.get("items")
    if isinstance(raw, list) and len(raw) > 0:
        res = []
        for it in raw[:3]:
            if isinstance(it, dict):
                desc = str(it.get("desc", it.get("article_desc", it.get("designation", it.get("nom", copy.ARTICLE_DESC)))))
                ref = str(it.get("ref", it.get("article_ref", copy.ARTICLE_REF)))
                qty = str(it.get("qty", it.get("article_qte", it.get("qte", copy.ARTICLE_QTE))))
                unit = str(it.get("unit_price", it.get("prix", it.get("article_pu", copy.ARTICLE_PU))))
                tot = str(it.get("total", it.get("montant", it.get("article_montant", copy.ARTICLE_MONTANT))))
                res.append(Item(desc=desc, ref=ref, qty=qty, unit_price=unit, total=tot))
        if res:
            return res
    return [
        Item(
            desc=str(d.get("article_desc", copy.ARTICLE_DESC)),
            ref=str(d.get("article_ref", copy.ARTICLE_REF)),
            qty=str(d.get("article_qte", copy.ARTICLE_QTY if hasattr(copy, "ARTICLE_QTY") else copy.ARTICLE_QTE)),
            unit_price=str(d.get("article_pu", copy.ARTICLE_PU)),
            total=str(d.get("article_montant", copy.ARTICLE_MONTANT)),
        )
    ]

# ----------------------------------------------------------------------

def from_payload(d: dict | None = None) -> FactureChannel:
    d = d or {}
    vis = Visible(
        header=bool(d.get("header", True)),
        header_logo=bool(d.get("header_logo", True)),
        header_contact=bool(d.get("header_contact", True)),
        header_client=bool(d.get("header_client", True)),
        header_meta=bool(d.get("header_meta", True)),
        middle=bool(d.get("middle", True)),
        middle_accueil=bool(d.get("middle_accueil", True)),
        middle_table=bool(d.get("middle_table", True)),
        middle_totaux=bool(d.get("middle_totaux", True)),
        middle_paiement=bool(d.get("middle_paiement", True)),
        footer=bool(d.get("footer", False)),
    )

    addr_1, addr_2, addr_3 = _clean_client_addresses(d)
    date_val = str(d.get("date_vente", d.get("date_facture", d.get("date", d.get("date_str", ""))))).strip()
    time_val = str(d.get("heure_vente", d.get("heure_facture", d.get("heure", "")))).strip()

    hdr = Header(
        store_line_1=str(d.get("store_line_1", copy.STORE_LINE_1)),
        store_line_2=str(d.get("store_line_2", copy.STORE_LINE_2)),
        client_code=str(d.get("client_code", copy.CLIENT_CODE)),
        client_name=_clean_client_name(d),
        client_address_1=addr_1,
        client_address_2=addr_2,
        client_address_3=addr_3,
        date_str=_format_chanel_date(date_val, time_val),
        facture_num=str(d.get("facture_num", copy.FACTURE_NUM)),
        caisse_num=str(d.get("caisse_num", copy.CAISSE_NUM)),
        folio_num=str(d.get("folio_num", copy.FOLIO_NUM)),
    )

    items = _items_from_payload(d)

    total_ttc_val = 0.0
    total_qty = 0
    for it in items:
        total_ttc_val += _to_float(it.total)
        total_qty += int(_to_float(it.qty, 1.0))

    user_ttc = _to_float(d.get("total_ttc", d.get("total", 0.0)))
    if user_ttc > 0:
        total_ttc_val = user_ttc

    if total_ttc_val <= 0:
        total_ttc_val = 132.0
    if total_qty <= 0:
        total_qty = 1

    total_ht_val = total_ttc_val / 1.2
    total_tva_val = total_ttc_val - total_ht_val

    user_ht = _to_float(d.get("total_ht", 0.0))
    if user_ht > 0:
        total_ht_val = user_ht

    user_tva = _to_float(d.get("total_tva", 0.0))
    if user_tva > 0:
        total_tva_val = user_tva

    raw_ht = str(d.get("total_ht", "")).strip()
    if raw_ht and raw_ht.upper().startswith("TOTAL HT"):
        def_ht = raw_ht
    else:
        def_ht = f"Total HT : {total_ht_val:.2f} EUR".replace(".", ",")

    raw_tva = str(d.get("total_tva", "")).strip()
    if raw_tva and raw_tva.upper().startswith("TVA"):
        def_tva = raw_tva
    else:
        def_tva = f"TVA 20,00% : {total_tva_val:.2f} EUR".replace(".", ",")

    raw_ttc = str(d.get("total_ttc", d.get("total", ""))).strip()
    if raw_ttc and raw_ttc.upper().startswith("TOTAL TTC"):
        def_ttc = raw_ttc
    else:
        def_ttc = f"Total TTC : {total_ttc_val:.2f} EUR".replace(".", ",")

    def_count = f"{total_qty} article{'s' if total_qty > 1 else ''} vendu{'s' if total_qty > 1 else ''}"

    mode_pay = str(d.get("mode_paiement", "")).strip() or "ESPECES EUROS"
    raw_pay = str(d.get("paiement", "")).strip()
    if raw_pay and any(c.isdigit() for c in raw_pay) and any(kw in raw_pay.upper() for kw in ("ESPECES", "CARTE", "VISA", "MASTERCARD", "AMERICAN")):
        pay_str = raw_pay
    else:
        pay_str = f"{mode_pay.upper()} {total_ttc_val:.2f} EUR".replace(".", ",")

    mid = Middle(
        accueil_text=_clean_accueil(d),
        col_ref_title=str(d.get("col_ref_title", copy.COL_REF_TITLE)),
        col_qte_title=str(d.get("col_qte_title", copy.COL_QTE_TITLE)),
        col_pu_title=str(d.get("col_pu_title", copy.COL_PU_TITLE)),
        col_montant_title=str(d.get("col_montant_title", copy.COL_MONTANT_TITLE)),
        items=items,
        articles_count=def_count if not str(d.get("articles_count", "")).strip() or "article" in str(d.get("articles_count", "")) else f"{d.get('articles_count')} article{'s' if _to_float(d.get('articles_count', 1)) > 1 else ''} vendu{'s' if _to_float(d.get('articles_count', 1)) > 1 else ''}",
        total_ht=def_ht,
        total_tva=def_tva,
        total_ttc=def_ttc,
        paiement=pay_str,
    )
    return FactureChannel(visible=vis, header=hdr, middle=mid, footer=Footer())
