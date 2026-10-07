"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import layout, rules


@dataclass
class Item:
    sku: str = texts.SKU
    taille: str = texts.TAILLE
    nom: str = texts.PRODUIT
    qte: str = texts.QTE
    pu_ht: str = texts.PU_HT
    pu_ttc: str = texts.PU_TTC


def _default_items() -> list[Item]:
    return [Item()]


def _item_from_dict(item: dict) -> Item:
    return Item(
        sku=item.get("sku") or "",
        taille=item.get("taille") or "",
        nom=item.get("nom") or "",
        qte=item.get("qte") or "",
        pu_ht=item.get("pu_ht") or "",
        pu_ttc=item.get("pu_ttc") or "",
    )


def _items_from_payload(data: dict) -> list[Item]:
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
    livraison_adresse: str = texts.ADRESSE
    livraison_cp_ville: str = texts.CP_VILLE
    livraison_pays: str = texts.PAYS
    num_commande: str = texts.NUM_COMMANDE
    num_facture: str = texts.NUM_FACTURE
    date_facture: str = field(default_factory=lambda: texts.DATE_FACTURE)
    date_livraison: str = field(default_factory=lambda: texts.DATE_LIVRAISON)
    total: str = texts.TOTAL
    items: list = field(default_factory=_default_items)


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_title: bool = True
    header_service: bool = True
    header_addresses: bool = True
    header_refs: bool = True
    middle: bool = True
    middle_columns: bool = True
    middle_rows: bool = True
    middle_totals: bool = True
    footer: bool = True
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
    vis.header_logo = rules.flag(data, "header_logo")
    vis.header_title = rules.flag(data, "header_title")
    vis.header_service = rules.flag(data, "header_service")
    vis.header_addresses = rules.flag(data, "header_addresses")
    vis.header_refs = rules.flag(data, "header_refs")
    vis.middle = rules.flag(data, "middle")
    vis.middle_columns = rules.flag(data, "middle_columns")
    vis.middle_rows = rules.flag(data, "middle_rows")
    vis.middle_totals = rules.flag(data, "middle_totals")
    vis.footer = rules.flag(data, "footer")
    vis.footer_line = rules.flag(data, "footer_line")
    vis.footer_legal = rules.flag(data, "footer_legal")
    for key in (
        "nom", "adresse", "cp_ville", "pays",
        "livraison_nom", "livraison_adresse", "livraison_cp_ville", "livraison_pays",
        "num_commande", "num_facture", "date_facture", "date_livraison",
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
    l_nom = str(data.get("livraison_nom") or "").strip()
    l_prenom = str(data.get("livraison_prenom") or "").strip()
    if l_nom and l_prenom and l_prenom not in l_nom:
        doc.card.livraison_nom = f"{l_nom} {l_prenom}"
    elif l_nom:
        doc.card.livraison_nom = l_nom
    elif l_prenom:
        doc.card.livraison_nom = l_prenom
    if "items" in data:
        doc.card.items = _items_from_payload(data)
    return rules.apply_doc(doc)
