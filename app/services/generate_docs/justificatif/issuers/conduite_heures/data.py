"""Applique un dict éditeur → Doc."""

from dataclasses import dataclass, field

from . import copy as texts
from . import layout, rules


@dataclass
class Rdv:
    jour: str = ""
    date: str = ""
    debut: str = ""
    fin: str = ""
    activite: str = ""
    commentaire: str = ""


_RDV_KEYS = ("jour", "date", "debut", "fin", "activite", "commentaire")


def _default_rdvs() -> list[Rdv]:
    return [
        Rdv(texts.RDV1_JOUR, texts.RDV1_DATE, texts.RDV1_DEBUT, texts.RDV1_FIN, texts.RDV1_ACTIVITE, texts.RDV1_COMMENT),
        Rdv(texts.RDV2_JOUR, texts.RDV2_DATE, texts.RDV2_DEBUT, texts.RDV2_FIN, texts.RDV2_ACTIVITE, texts.RDV2_COMMENT),
        Rdv(texts.RDV3_JOUR, texts.RDV3_DATE, texts.RDV3_DEBUT, texts.RDV3_FIN, texts.RDV3_ACTIVITE, texts.RDV3_COMMENT),
    ]


def _rdv_from_dict(item: dict) -> Rdv:
    return Rdv(
        jour=item.get("jour") or "",
        date=item.get("date") or "",
        debut=item.get("debut") or "",
        fin=item.get("fin") or "",
        activite=item.get("activite") or "",
        commentaire=item.get("commentaire") or "",
    )


def _rdvs_from_numbered(data: dict) -> list[Rdv] | None:
    rows: list[Rdv] = []
    found = False
    for i in range(layout.MAX_ROWS):
        n = i + 1
        keys = tuple(f"rdv{n}_{k}" for k in _RDV_KEYS)
        if not any(k in data for k in keys):
            if found:
                break
            continue
        found = True
        rows.append(Rdv(
            jour=data.get(f"rdv{n}_jour") or "",
            date=data.get(f"rdv{n}_date") or "",
            debut=data.get(f"rdv{n}_debut") or "",
            fin=data.get(f"rdv{n}_fin") or "",
            activite=data.get(f"rdv{n}_activite") or "",
            commentaire=data.get(f"rdv{n}_commentaire") or "",
        ))
    return rows if found else None


def _rdvs_from_payload(data: dict) -> list[Rdv]:
    raw = data.get("rdvs")
    if isinstance(raw, list):
        rows = []
        for item in raw[: layout.MAX_ROWS]:
            if isinstance(item, dict):
                rows.append(_rdv_from_dict(item))
        return rows
    numbered = _rdvs_from_numbered(data)
    if numbered is not None:
        return numbered
    return _default_rdvs()


@dataclass
class Card:
    eleve: str = texts.ELEVE
    edition: str = field(default_factory=lambda: texts.EDITION)
    rdvs: list = field(default_factory=_default_rdvs)


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
    vis.header = rules.flag(data, "header")
    vis.header_logo = rules.flag(data, "header_logo")
    vis.header_identity = rules.flag(data, "header_identity")
    vis.header_banner = rules.flag(data, "header_banner")
    vis.middle = rules.flag(data, "middle")
    vis.footer = rules.flag(data, "footer")
    if "eleve" in data:
        doc.card.eleve = data["eleve"]
    if "edition" in data:
        doc.card.edition = data["edition"]
    doc.card.rdvs = _rdvs_from_payload(data)
    return rules.apply_doc(doc)
