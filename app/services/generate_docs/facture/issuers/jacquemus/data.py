from dataclasses import dataclass, field
import re
from . import copy as texts
from . import layout

# ----------------------------------------------------------------------

MONTH_MAP = {
    "janvier": "janv.", "février": "févr.", "fevrier": "févr.",
    "mars": "mars", "avril": "avr.", "mai": "mai",
    "juin": "juin", "juillet": "juil.", "août": "août", "aout": "août",
    "septembre": "sept.", "octobre": "oct.", "novembre": "nov.",
    "décembre": "déc.", "decembre": "déc.",
    "janv": "janv.", "févr": "févr.", "fevr": "févr.", "fév": "févr.", "fev": "févr.",
    "avr": "avr.", "juil": "juil.", "sept": "sept.", "sep": "sept.",
    "oct": "oct.", "nov": "nov.", "déc": "déc.", "dec": "déc.",
}

# ----------------------------------------------------------------------

def normalize_jacquemus_date(date_str: str) -> str:
    if not date_str:
        return ""
    s = str(date_str).strip()
    slash_match = re.search(r"\b(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})\b", s)
    if slash_match:
        day = int(slash_match.group(1))
        month = int(slash_match.group(2))
        year = int(slash_match.group(3))
        if year < 100:
            year += 2000
        fr_short = {1: "janv.", 2: "févr.", 3: "mars", 4: "avr.", 5: "mai", 6: "juin", 7: "juil.", 8: "août", 9: "sept.", 10: "oct.", 11: "nov.", 12: "déc."}
        if 1 <= month <= 12:
            s = s[:slash_match.start()] + f"{day} {fr_short[month]} {year}" + s[slash_match.end():]
    pat = r"\b(janvier|février|fevrier|mars|avril|mai|juin|juillet|août|aout|septembre|octobre|novembre|décembre|janv|févr|fevr|fév|fev|avr|juil|sept|sep|oct|nov|déc|dec)\b\.?"
    def _rep(m):
        raw = m.group(1).lower()
        return MONTH_MAP.get(raw, m.group(0))
    s = re.sub(pat, _rep, s, flags=re.IGNORECASE)
    s = re.sub(r"(\d{1,2}:\d{2}):\d{2}", r"\1", s)
    s = re.sub(r"\s*(?:UTC(?:\+\d+)?|GMT)", "", s, flags=re.IGNORECASE).strip()
    return s

# ----------------------------------------------------------------------

def _format_jacquemus_date(date_val: str, time_val: str = "") -> str:
    raw = str(date_val or "").strip()
    raw_time = str(time_val or "").strip()
    if raw_time:
        raw_time = raw_time.split()[0]
        if len(raw_time) > 5 and raw_time[2] == ":":
            raw_time = raw_time[:5]
    if raw and raw_time and " à " not in raw:
        combined = f"{raw} à {raw_time}"
    elif raw:
        combined = raw
    elif raw_time:
        combined = raw_time
    else:
        return ""
    return normalize_jacquemus_date(combined)

# ----------------------------------------------------------------------

@dataclass
class Item:
    nom: str = texts.ITEM_DEFAULT_NOM
    ref: str = texts.ITEM_DEFAULT_REF
    couleur: str = texts.ITEM_DEFAULT_COULEUR
    taille: str = texts.ITEM_DEFAULT_TAILLE
    pays: str = texts.ITEM_DEFAULT_PAYS
    prix: str = texts.ITEM_DEFAULT_PRIX
    qte: str = texts.ITEM_DEFAULT_QTE
    sous_total: str = texts.ITEM_DEFAULT_PRIX

# ----------------------------------------------------------------------

@dataclass
class Header:
    contact_email: str = texts.CONTACT_EMAIL
    client_nom: str = texts.CLIENT_NOM
    client_rue: str = texts.CLIENT_RUE
    client_complement: str = texts.CLIENT_COMPLEMENT
    client_ville_cp: str = texts.CLIENT_VILLE_CP
    client_pays: str = texts.CLIENT_PAYS
    client_tel: str = texts.CLIENT_TEL
    label_commande: str = texts.LABEL_COMMANDE
    val_commande: str = texts.VAL_COMMANDE
    label_facture: str = texts.LABEL_FACTURE
    val_facture: str = texts.VAL_FACTURE
    label_date: str = texts.LABEL_DATE
    val_date: str = texts.VAL_DATE

# ----------------------------------------------------------------------

@dataclass
class Middle:
    label_payment: str = texts.LABEL_PAYMENT
    val_payment: str = texts.VAL_PAYMENT
    label_delivery: str = texts.LABEL_DELIVERY
    val_delivery: str = texts.VAL_DELIVERY
    col_produits: str = texts.COL_PRODUITS
    col_prix: str = texts.COL_PRIX
    col_qte: str = texts.COL_QTE
    col_sous_total: str = texts.COL_SOUS_TOTAL
    items: list[Item] = field(default_factory=lambda: [Item()])
    tot_sous_total: str = texts.VAL_TOT_SOUS_TOTAL
    tot_tva: str = texts.VAL_TOT_TVA
    tot_livraison: str = texts.VAL_TOT_LIVRAISON
    tot_total: str = texts.VAL_TOT_TOTAL

# ----------------------------------------------------------------------

@dataclass
class Footer:
    legal_lines: list[str] = field(default_factory=lambda: list(texts.LEGAL_LINES))
    notice_lines: list[str] = field(default_factory=lambda: list(texts.EXPORTER_LINES))

# ----------------------------------------------------------------------

@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_contact: bool = True
    header_client: bool = True
    header_meta: bool = True
    middle: bool = True
    middle_payment: bool = True
    middle_delivery: bool = True
    middle_table: bool = True
    middle_rows: bool = True
    middle_totals: bool = True
    footer: bool = True
    footer_legal: bool = True
    footer_notice: bool = True

# ----------------------------------------------------------------------

@dataclass
class Doc:
    header: Header = field(default_factory=Header)
    middle: Middle = field(default_factory=Middle)
    footer: Footer = field(default_factory=Footer)
    visible: Visible = field(default_factory=Visible)

# ----------------------------------------------------------------------

def _as_bool(val, default: bool = True) -> bool:
    if val is None:
        return default
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        return val.strip().lower() not in ("false", "0", "off", "no", "")
    return bool(val)

# ----------------------------------------------------------------------

def from_payload(payload: dict | None = None) -> Doc:
    doc = Doc()
    if not payload:
        return doc
    data = dict(payload)
    if isinstance(data.get("visible"), dict):
        data.update(data["visible"])

    if "header" in data:
        doc.visible.header = _as_bool(data["header"])
    if "header_logo" in data:
        doc.visible.header_logo = _as_bool(data["header_logo"])
    if "header_contact" in data:
        doc.visible.header_contact = _as_bool(data["header_contact"])
    if "header_client" in data:
        doc.visible.header_client = _as_bool(data["header_client"])
    if "header_meta" in data:
        doc.visible.header_meta = _as_bool(data["header_meta"])

    if "middle" in data:
        doc.visible.middle = _as_bool(data["middle"])
    if "middle_payment" in data:
        doc.visible.middle_payment = _as_bool(data["middle_payment"])
    if "middle_delivery" in data:
        doc.visible.middle_delivery = _as_bool(data["middle_delivery"])
    if "middle_table" in data:
        doc.visible.middle_table = _as_bool(data["middle_table"])
    if "middle_rows" in data:
        doc.visible.middle_rows = _as_bool(data["middle_rows"])
    if "middle_totals" in data:
        doc.visible.middle_totals = _as_bool(data["middle_totals"])

    if "footer" in data:
        doc.visible.footer = _as_bool(data["footer"])
    if "footer_legal" in data:
        doc.visible.footer_legal = _as_bool(data["footer_legal"])
    if "footer_notice" in data:
        doc.visible.footer_notice = _as_bool(data["footer_notice"])

    if "header_contact_email" in data and isinstance(data["header_contact_email"], str):
        doc.header.contact_email = data["header_contact_email"]
    elif "contact_email" in data and isinstance(data["contact_email"], str):
        doc.header.contact_email = data["contact_email"]

    prenom = str(data.get("prenom", "")).strip()
    nom = str(data.get("nom", "")).strip()
    if prenom and nom:
        doc.header.client_nom = nom if prenom.lower() in nom.lower() else f"{nom} {prenom}".strip()
    elif nom:
        doc.header.client_nom = nom
    elif prenom:
        doc.header.client_nom = prenom
    elif "client_nom" in data and isinstance(data["client_nom"], str):
        doc.header.client_nom = data["client_nom"]
    elif "nom" in data and isinstance(data["nom"], str):
        doc.header.client_nom = data["nom"]

    if "client_rue" in data and isinstance(data["client_rue"], str):
        doc.header.client_rue = data["client_rue"]
    elif "client_adresse" in data and isinstance(data["client_adresse"], str):
        doc.header.client_rue = data["client_adresse"]
    elif "adresse" in data and isinstance(data["adresse"], str):
        doc.header.client_rue = data["adresse"]

    if "client_complement" in data and isinstance(data["client_complement"], str):
        doc.header.client_complement = data["client_complement"]
    elif "client_adresse2" in data and isinstance(data["client_adresse2"], str):
        doc.header.client_complement = data["client_adresse2"]
    elif "adresse2" in data and isinstance(data["adresse2"], str):
        doc.header.client_complement = data["adresse2"]
    elif "complement" in data and isinstance(data["complement"], str):
        doc.header.client_complement = data["complement"]

    if "client_ville_cp" in data and isinstance(data["client_ville_cp"], str):
        doc.header.client_ville_cp = data["client_ville_cp"]
    elif "ville_cp" in data and isinstance(data["ville_cp"], str):
        doc.header.client_ville_cp = data["ville_cp"]
    elif "ville" in data or "cp" in data:
        v = str(data.get("ville", "")).strip()
        c = str(data.get("cp", "")).strip()
        doc.header.client_ville_cp = f"{c} {v}".strip()

    if "client_pays" in data and isinstance(data["client_pays"], str):
        doc.header.client_pays = data["client_pays"]
    elif "pays" in data and isinstance(data["pays"], str):
        doc.header.client_pays = data["pays"]

    if "client_tel" in data and isinstance(data["client_tel"], str):
        doc.header.client_tel = data["client_tel"]
    elif "client_telephone" in data and isinstance(data["client_telephone"], str):
        doc.header.client_tel = data["client_telephone"]
    elif "telephone" in data and isinstance(data["telephone"], str):
        doc.header.client_tel = data["telephone"]
    elif "tel" in data and isinstance(data["tel"], str):
        doc.header.client_tel = data["tel"]

    if "header_client_lines" in data:
        raw_lines = data["header_client_lines"]
        if isinstance(raw_lines, str):
            lines = [l for l in raw_lines.splitlines() if l.strip()]
        elif isinstance(raw_lines, (list, tuple)):
            lines = [str(l) for l in raw_lines if str(l).strip()]
        else:
            lines = []
        if len(lines) > 0: doc.header.client_nom = lines[0]
        if len(lines) > 1: doc.header.client_rue = lines[1]
        if len(lines) > 2: doc.header.client_complement = lines[2]
        if len(lines) > 3: doc.header.client_ville_cp = lines[3]
        if len(lines) > 4: doc.header.client_pays = lines[4]
        if len(lines) > 5: doc.header.client_tel = lines[5]

    if "val_commande" in data and isinstance(data["val_commande"], str):
        doc.header.val_commande = data["val_commande"]
    elif "header_val_commande" in data and isinstance(data["header_val_commande"], str):
        doc.header.val_commande = data["header_val_commande"]

    if "val_facture" in data and isinstance(data["val_facture"], str):
        doc.header.val_facture = data["val_facture"]
    elif "header_val_facture" in data and isinstance(data["header_val_facture"], str):
        doc.header.val_facture = data["header_val_facture"]

    date_cmd = str(data.get("date_commande", data.get("date", ""))).strip()
    heure_cmd = str(data.get("heure_commande", data.get("heure", ""))).strip()
    if date_cmd or heure_cmd:
        doc.header.val_date = _format_jacquemus_date(date_cmd, heure_cmd)
    elif "val_date" in data and isinstance(data["val_date"], str):
        doc.header.val_date = _format_jacquemus_date(data["val_date"])
    elif "header_val_date" in data and isinstance(data["header_val_date"], str):
        doc.header.val_date = _format_jacquemus_date(data["header_val_date"])

    if "val_payment" in data and isinstance(data["val_payment"], str):
        doc.middle.val_payment = data["val_payment"]
    elif "payment_val" in data and isinstance(data["payment_val"], str):
        doc.middle.val_payment = data["payment_val"]

    if "val_delivery" in data and isinstance(data["val_delivery"], str):
        doc.middle.val_delivery = data["val_delivery"]
    elif "delivery_val" in data and isinstance(data["delivery_val"], str):
        doc.middle.val_delivery = data["delivery_val"]

    if "tot_sous_total" in data and isinstance(data["tot_sous_total"], str):
        doc.middle.tot_sous_total = data["tot_sous_total"]
    if "tot_tva" in data and isinstance(data["tot_tva"], str):
        doc.middle.tot_tva = data["tot_tva"]
    if "tot_livraison" in data and isinstance(data["tot_livraison"], str):
        doc.middle.tot_livraison = data["tot_livraison"]
    if "tot_total" in data and isinstance(data["tot_total"], str):
        doc.middle.tot_total = data["tot_total"]

    if "items" in data and isinstance(data["items"], list):
        items = []
        for it in data["items"][:layout.MAX_ROWS]:
            if isinstance(it, dict):
                nom = it.get("nom") or it.get("designation") or texts.ITEM_DEFAULT_NOM
                ref = it.get("ref") or it.get("code") or texts.ITEM_DEFAULT_REF
                couleur = it.get("couleur") or texts.ITEM_DEFAULT_COULEUR
                taille = it.get("taille") or texts.ITEM_DEFAULT_TAILLE
                pays = it.get("pays") or texts.ITEM_DEFAULT_PAYS
                prix = it.get("prix") or it.get("prix_ttc") or it.get("pu_ttc") or texts.ITEM_DEFAULT_PRIX
                qte = str(it.get("qte") or it.get("quantite") or texts.ITEM_DEFAULT_QTE)
                sous_total = it.get("sous_total") or prix
                items.append(Item(
                    nom=nom,
                    ref=ref,
                    couleur=couleur,
                    taille=taille,
                    pays=pays,
                    prix=prix,
                    qte=qte,
                    sous_total=sous_total,
                ))
        if items:
            doc.middle.items = items

    if "footer_legal_lines" in data:
        raw = data["footer_legal_lines"]
        if isinstance(raw, str):
            doc.footer.legal_lines = [l for l in raw.splitlines() if l.strip()]
        elif isinstance(raw, (list, tuple)):
            doc.footer.legal_lines = [str(l) for l in raw if str(l).strip()]
    elif "legal_lines" in data:
        raw = data["legal_lines"]
        if isinstance(raw, str):
            doc.footer.legal_lines = [l for l in raw.splitlines() if l.strip()]
        elif isinstance(raw, (list, tuple)):
            doc.footer.legal_lines = [str(l) for l in raw if str(l).strip()]

    if "footer_notice_lines" in data:
        raw = data["footer_notice_lines"]
        if isinstance(raw, str):
            doc.footer.notice_lines = [l for l in raw.splitlines() if l.strip()]
        elif isinstance(raw, (list, tuple)):
            doc.footer.notice_lines = [str(l) for l in raw if str(l).strip()]
    elif "notice_lines" in data:
        raw = data["notice_lines"]
        if isinstance(raw, str):
            doc.footer.notice_lines = [l for l in raw.splitlines() if l.strip()]
        elif isinstance(raw, (list, tuple)):
            doc.footer.notice_lines = [str(l) for l in raw if str(l).strip()]

    return doc
