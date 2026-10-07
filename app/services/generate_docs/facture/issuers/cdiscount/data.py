"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import layout, rules


@dataclass
class Item:
    desc: str = texts.DESC
    qte: str = texts.QTE
    montant: str = texts.MONTANT


def _default_items() -> list:
    return [Item()]


def _item_from_dict(item: dict) -> Item:
    return Item(
        desc=item.get("desc") or "",
        qte=item.get("qte") or "",
        montant=item.get("montant") or "",
    )


def _items_from_payload(data: dict) -> list:
    raw = data.get("items")
    if isinstance(raw, list) and raw:
        rows = []
        for item in raw[: layout.MAX_ROWS]:
            if isinstance(item, dict):
                rows.append(_item_from_dict(item))
        if rows:
            return rows
    return [Item(
        desc=data.get("desc") if "desc" in data else texts.DESC,
        qte=data.get("qte") if "qte" in data else texts.QTE,
        montant=data.get("montant") if "montant" in data else texts.MONTANT,
    )]


@dataclass
class Card:
    nom: str = texts.CLIENT_NOM
    adresse: str = texts.ADRESSE
    cp_ville: str = texts.CP_VILLE
    livraison_nom: str = texts.CLIENT_NOM
    livraison_adresse: str = texts.ADRESSE
    livraison_cp_ville: str = texts.CP_VILLE
    num_commande: str = texts.NUM_COMMANDE
    date_commande: str = field(default_factory=texts.slash_date)
    payment: str = texts.PAYMENT
    port: str = texts.PORT_AMT
    vendeur: str = texts.VENDEUR
    immat: str = texts.IMMAT
    total: str = texts.MONTANT
    sold_by_cdiscount: bool = True
    items: list = field(default_factory=_default_items)


@dataclass
class Visible:
    header: bool = True
    header_banner: bool = True
    header_logo: bool = True
    header_title: bool = True
    header_order: bool = True
    header_addresses: bool = True
    middle: bool = True
    middle_heading: bool = True
    middle_columns: bool = True
    middle_rows: bool = True
    middle_totals: bool = True
    middle_vendor: bool = True
    footer: bool = True
    footer_note: bool = False
    footer_cgu: bool = True
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
    vis.header_order = rules.flag(data, "header_order")
    vis.header_addresses = rules.flag(data, "header_addresses")
    vis.middle = rules.flag(data, "middle")
    vis.middle_heading = rules.flag(data, "middle_heading")
    vis.middle_columns = rules.flag(data, "middle_columns")
    vis.middle_rows = rules.flag(data, "middle_rows")
    vis.middle_totals = rules.flag(data, "middle_totals")
    vis.middle_vendor = rules.flag(data, "middle_vendor")
    vis.footer = rules.flag(data, "footer")
    vis.footer_cgu = rules.flag(data, "footer_cgu")
    vis.footer_legal = rules.flag(data, "footer_legal")
    for key in (
        "nom", "adresse", "cp_ville",
        "livraison_nom", "livraison_adresse", "livraison_cp_ville",
        "num_commande", "date_commande",
        "payment", "port", "vendeur", "immat", "total",
    ):
        if key in data:
            setattr(doc.card, key, data[key])
    if "sold_by_cdiscount" in data:
        doc.card.sold_by_cdiscount = rules.as_bool(data["sold_by_cdiscount"], True)
    elif "vendeur" in data and str(data["vendeur"]).strip().upper() not in ("", "CDISCOUNT"):
        doc.card.sold_by_cdiscount = False
    if "num_facture" in data and "num_commande" not in data:
        doc.card.num_commande = str(data["num_facture"]).strip()
    if doc.card.sold_by_cdiscount:
        if not doc.card.vendeur or doc.card.vendeur == texts.VENDEUR_MKP:
            doc.card.vendeur = texts.VENDEUR_CDISCOUNT
        if not doc.card.immat or doc.card.immat == texts.IMMAT_MKP:
            doc.card.immat = texts.IMMAT_CDISCOUNT
        vis.footer_note = rules.flag(data, "footer_note", False)
    else:
        if not doc.card.vendeur or doc.card.vendeur == texts.VENDEUR_CDISCOUNT:
            doc.card.vendeur = texts.VENDEUR_MKP
        if not doc.card.immat or doc.card.immat == texts.IMMAT_CDISCOUNT:
            doc.card.immat = texts.IMMAT_MKP
        vis.footer_note = rules.flag(data, "footer_note", True)
    nom_val = str(data.get("nom") or "").strip()
    prenom_val = str(data.get("prenom") or "").strip()
    if nom_val and prenom_val and prenom_val not in nom_val:
        doc.card.nom = f"{nom_val} {prenom_val}"
    elif nom_val:
        doc.card.nom = nom_val
    elif prenom_val:
        doc.card.nom = prenom_val
    l_nom = str(data.get("livraison_nom") or "").strip()
    l_prenom = str(data.get("livraison_prenom") or "").strip()
    if l_nom and l_prenom and l_prenom not in l_nom:
        doc.card.livraison_nom = f"{l_nom} {l_prenom}"
    elif l_nom:
        doc.card.livraison_nom = l_nom
    elif l_prenom:
        doc.card.livraison_nom = l_prenom
    doc.card.items = _items_from_payload(data)
    return rules.apply_doc(doc)
