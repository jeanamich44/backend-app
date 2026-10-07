"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import rules


@dataclass
class Card:
    num_client: str = texts.NUM_CLIENT
    num_contrat: str = texts.NUM_CONTRAT
    num_orias: str = texts.NUM_ORIAS
    courtier: str = texts.COURTIER
    titulaire: str = texts.TITULAIRE
    adresse: str = texts.ADRESSE
    cp_ville: str = texts.CP_VILLE
    pays: str = texts.PAYS
    date_delivrance: str = field(default_factory=lambda: texts.DATE_DELIVRANCE)
    date_effet_jour: str = field(default_factory=lambda: texts.DATE_EFFET_JOUR)
    date_effet_mois: str = field(default_factory=lambda: texts.DATE_EFFET_MOIS)
    date_effet_annee: str = field(default_factory=lambda: texts.DATE_EFFET_ANNEE)
    immatriculation: str = texts.IMMATRICULATION
    vehicule: str = texts.VEHICULE


@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_identity: bool = True
    header_banner: bool = True
    middle: bool = True
    footer: bool = True


@dataclass
class Doc:
    card: Card = field(default_factory=Card)
    visible: Visible = field(default_factory=Visible)


def from_payload(data: dict | None) -> Doc:
    data = rules.apply_payload(data)
    doc = Doc()
    vis = doc.visible
    vis_dict = data.get("visible") if isinstance(data.get("visible"), dict) else {}
    for k in ("header", "header_logo", "header_identity", "header_banner", "middle", "footer"):
        if k in data:
            setattr(vis, k, rules.flag(data, k))
        elif k in vis_dict:
            setattr(vis, k, rules.flag(vis_dict, k))
    mapping = (
        ("num_client", "num_client"),
        ("num_contrat", "num_contrat"),
        ("num_orias", "num_orias"),
        ("courtier", "courtier"),
        ("titulaire", "titulaire"),
        ("adresse", "adresse"),
        ("cp_ville", "cp_ville"),
        ("pays", "pays"),
        ("date_delivrance", "date_delivrance"),
        ("date_effet_jour", "date_effet_jour"),
        ("date_effet_mois", "date_effet_mois"),
        ("date_effet_annee", "date_effet_annee"),
        ("immatriculation", "immatriculation"),
        ("vehicule", "vehicule"),
    )
    for key, attr in mapping:
        if key in data:
            setattr(doc.card, attr, data[key])
    if "vehicule" not in data and isinstance(data.get("vehicule_marque_modele"), str):
        doc.card.vehicule = data["vehicule_marque_modele"]
    return rules.apply_doc(doc)
