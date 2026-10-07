from dataclasses import dataclass, field

from . import copy as texts
from . import layout, rules


@dataclass
class Item:
    sku: str = texts.SKU
    desc: str = texts.DESC
    couleur: str = texts.COULEUR
    taille: str = texts.TAILLE
    qte: str = texts.QTE
    pu: str = texts.PU
    tva: str = texts.TVA


def _default_items() -> list:
    return [
        Item(),
        Item(
            sku=texts.SKU2,
            desc=texts.DESC2,
            couleur=texts.COULEUR,
            taille=texts.TAILLE,
            qte=texts.QTE,
            pu=texts.PU2,
            tva=texts.TVA,
        ),
    ]


def _item_from_dict(item: dict) -> Item:
    return Item(
        sku=item.get("sku") or "",
        desc=item.get("desc") or "",
        couleur=item.get("couleur") or "",
        taille=item.get("taille") or "",
        qte=item.get("qte") or "",
        pu=item.get("pu") or "",
        tva=item.get("tva") or "",
    )


def _items_from_payload(data: dict) -> list:
    raw = data.get("items")
    if not isinstance(raw, list):
        return _default_items()
    rows = []
    for item in raw[: layout.MAX_ROWS]:
        if isinstance(item, dict):
            rows.append(_item_from_dict(item))
    return rows


@dataclass
class Card:
    nom: str = texts.CLIENT_NOM
    adresse: str = texts.ADRESSE
    cp_ville: str = texts.CP_VILLE
    pays: str = texts.PAYS
    livraison_nom: str = texts.CLIENT_NOM
    livraison_extra: str = texts.LIVRAISON_EXTRA
    livraison_adresse: str = texts.ADRESSE
    livraison_cp_ville: str = texts.CP_VILLE
    livraison_pays: str = texts.PAYS
    livraison_mode: str = texts.LIVRAISON_CHRONO
    magasin_nom: str = texts.MAGASIN_NOM
    num_client: str = texts.NUM_CLIENT
    num_commande: str = texts.NUM_COMMANDE
    num_facture: str = texts.NUM_FACTURE
    date_commande: str = field(default_factory=texts.slash_date)
    date_facture: str = field(default_factory=texts.slash_date)
    payment: str = texts.PAYMENT
    remise: str = texts.REMISE
    port: str = texts.PORT
    total: str = "239,99"
    items: list = field(default_factory=_default_items)


@dataclass
class Visible:
    header: bool = True
    header_banner: bool = True
    header_logo: bool = True
    header_title: bool = True
    header_issuer: bool = True
    header_refs: bool = True
    header_addresses: bool = True
    middle: bool = True
    middle_columns: bool = True
    middle_rows: bool = True
    middle_totals: bool = True
    footer: bool = True
    footer_thanks: bool = True
    footer_line: bool = True
    footer_legal: bool = True


@dataclass
class Doc:
    card: Card = field(default_factory=Card)
    visible: Visible = field(default_factory=Visible)


def from_payload(data: dict | None) -> Doc:
    data = rules.apply_payload(data)
    doc = Doc()
    vis = doc.visible
    vis.header = rules.flag(data, "header")
    vis.header_banner = rules.flag(data, "header_banner")
    vis.header_logo = rules.flag(data, "header_logo")
    vis.header_title = rules.flag(data, "header_title")
    vis.header_issuer = rules.flag(data, "header_issuer")
    vis.header_refs = rules.flag(data, "header_refs")
    vis.header_addresses = rules.flag(data, "header_addresses")
    vis.middle = rules.flag(data, "middle")
    vis.middle_columns = rules.flag(data, "middle_columns")
    vis.middle_rows = rules.flag(data, "middle_rows")
    vis.middle_totals = rules.flag(data, "middle_totals")
    vis.footer = rules.flag(data, "footer")
    vis.footer_thanks = rules.flag(data, "footer_thanks")
    vis.footer_line = rules.flag(data, "footer_line")
    vis.footer_legal = rules.flag(data, "footer_legal")
    for key in (
        "nom", "adresse", "cp_ville", "pays",
        "livraison_nom", "livraison_extra", "livraison_adresse",
        "livraison_cp_ville", "livraison_pays",
        "livraison_mode", "magasin_nom",
        "num_client", "num_commande", "num_facture",
        "date_commande", "date_facture", "payment",
        "remise", "port", "total",
    ):
        if key in data:
            setattr(doc.card, key, data[key])
    nom_val = str(data.get("nom") or "").strip()
    prenom_val = str(data.get("prenom") or "").strip()
    if nom_val and prenom_val and prenom_val not in nom_val:
        doc.card.nom = f"{nom_val} {prenom_val}"
    elif nom_val:
        doc.card.nom = nom_val
    elif prenom_val:
        doc.card.nom = prenom_val
    cp_val = str(data.get("cp") or "").strip()
    ville_val = str(data.get("ville") or "").strip()
    if cp_val or ville_val:
        doc.card.cp_ville = f"{cp_val} {ville_val}".strip()
    l_nom = str(data.get("livraison_nom") or "").strip()
    l_prenom = str(data.get("livraison_prenom") or "").strip()
    if l_nom and l_prenom and l_prenom not in l_nom:
        doc.card.livraison_nom = f"{l_nom} {l_prenom}"
    elif l_nom:
        doc.card.livraison_nom = l_nom
    elif l_prenom:
        doc.card.livraison_nom = l_prenom
    l_cp = str(data.get("livraison_cp") or "").strip()
    l_ville = str(data.get("livraison_ville") or "").strip()
    if l_cp or l_ville:
        doc.card.livraison_cp_ville = f"{l_cp} {l_ville}".strip()
    if "items" in data:
        doc.card.items = _items_from_payload(data)
    _ht, _ttc, _rem, _port, due, _dont = rules.invoice_totals(doc.card)
    card_tot = str(data.get("total") or "").strip()
    if not card_tot:
        doc.card.total = rules.format_money(due)
    return rules.apply_doc(doc)
