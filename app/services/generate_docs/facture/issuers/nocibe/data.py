from dataclasses import dataclass, field
from . import copy, layout, rules

# ----------------------------------------------------------------------

@dataclass
class Item:
    ref: str = copy.ITEM_REF
    desc: str = copy.ITEM_DESC
    tva_rate: str = copy.ITEM_TVA_RATE
    qty: str = copy.ITEM_QTY
    unit_price: str = copy.ITEM_PRICE_BRUT
    remise: str = copy.ITEM_REMISE
    remise_code: str = copy.ITEM_REMISE_CODE
    net_ht: str = copy.ITEM_NET_HT

# ----------------------------------------------------------------------

def _default_items() -> list[Item]:
    return [Item()]

# ----------------------------------------------------------------------

def _item_from_dict(d: dict) -> Item:
    d = rules.clean_item(d)
    ref = d.get("ref") or copy.ITEM_REF.strip()
    desc = d.get("desc") or copy.ITEM_DESC
    tva_rate = d.get("tva_rate") or copy.ITEM_TVA_RATE
    qty = d.get("qty") or copy.ITEM_QTY
    unit_price = d.get("unit_price") or copy.ITEM_PRICE_BRUT
    remise = d.get("remise") or copy.ITEM_REMISE
    remise_code = d.get("remise_code") or copy.ITEM_REMISE_CODE
    net_ht = d.get("net_ht")
    if not net_ht:
        net_ht = rules.compute_item_net(d)

    return Item(
        ref=ref,
        desc=desc,
        tva_rate=tva_rate,
        qty=qty,
        unit_price=unit_price,
        remise=remise,
        remise_code=remise_code,
        net_ht=net_ht,
    )

# ----------------------------------------------------------------------

def _items_from_payload(data: dict) -> list[Item]:
    raw = data.get("items")
    if not isinstance(raw, list) or len(raw) == 0:
        return _default_items()
    result = []
    for entry in raw[: layout.MAX_ROWS]:
        if isinstance(entry, dict):
            result.append(_item_from_dict(entry))
        elif isinstance(entry, Item):
            result.append(entry)
    return result if result else _default_items()

# ----------------------------------------------------------------------

@dataclass
class Card:
    facture_num: str = copy.FACTURE_NUM
    date_emission: str = copy.DATE_EMISSION
    facturation_titre: str = copy.TITRE_FACTURATION
    client_nom: str = copy.CLIENT_NOM
    client_rue: str = copy.CLIENT_RUE
    client_ville: str = copy.CLIENT_VILLE
    client_pays: str = copy.CLIENT_PAYS
    livraison_titre: str = copy.TITRE_LIVRAISON
    livraison_nom: str = copy.LIVRAISON_NOM
    livraison_rue: str = copy.LIVRAISON_RUE
    livraison_ville: str = copy.LIVRAISON_VILLE
    livraison_pays: str = copy.LIVRAISON_PAYS
    commande_date: str = copy.COMMANDE_DATE
    commande_mode: str = copy.COMMANDE_MODE
    commande_expedition: str = copy.COMMANDE_EXPEDITION
    commande_etat: str = copy.COMMANDE_ETAT
    items: list[Item] = field(default_factory=_default_items)
    total_ht: str = copy.DEFAULT_TOTAL_HT
    total_tva: str = copy.DEFAULT_TOTAL_TVA
    total_ttc: str = copy.DEFAULT_TOTAL_TTC
    tva_rate_pct: str = "20.00 %"
    tva_base_ht: str = copy.DEFAULT_TOTAL_HT.replace(",", ".")
    tva_montant: str = copy.DEFAULT_TOTAL_TVA
    reglement_date: str = copy.DEFAULT_REGLEMENT_DATE
    reglement_mode: str = copy.DEFAULT_REGLEMENT_MODE
    reglement_montant: str = copy.DEFAULT_REGLEMENT_MONTANT

# ----------------------------------------------------------------------

@dataclass
class Visible:
    header: bool = True
    header_logo: bool = True
    header_titre: bool = True
    header_facturation: bool = True
    header_livraison: bool = True
    header_commande: bool = True
    middle: bool = True
    middle_table: bool = True
    middle_totals: bool = True
    middle_details: bool = True

# ----------------------------------------------------------------------

@dataclass
class FactureNocibe:
    card: Card = field(default_factory=Card)
    visible: Visible = field(default_factory=Visible)

# ----------------------------------------------------------------------

Doc = FactureNocibe

# ----------------------------------------------------------------------

def _format_facture_num(val) -> str:
    s = str(val or "").strip()
    if not s:
        return copy.FACTURE_NUM
    if not s.upper().startswith("FACTURE"):
        return f"FACTURE n°{s}"
    return s

# ----------------------------------------------------------------------

def _format_date_emission(val) -> str:
    s = str(val or "").strip()
    if not s:
        return copy.DATE_EMISSION
    if not s.lower().startswith("du"):
        return f"Du {s} "
    return s if s.endswith(" ") else f"{s} "

# ----------------------------------------------------------------------

def _format_commande_date(val) -> str:
    s = str(val or "").strip()
    if not s:
        return copy.COMMANDE_DATE
    if not s.lower().startswith("date de commande"):
        return f"Date de commande : {s} "
    return s if s.endswith(" ") else f"{s} "

# ----------------------------------------------------------------------

def _format_commande_mode(val) -> str:
    s = str(val or "").strip()
    if not s:
        return copy.COMMANDE_MODE
    if not s.lower().startswith("vous avez opté"):
        return f"Vous avez opté pour une livraison : {s}"
    return s

# ----------------------------------------------------------------------

def _format_commande_expedition(val) -> str:
    s = str(val or "").strip()
    if not s:
        return copy.COMMANDE_EXPEDITION
    if not s.lower().startswith("date d’") and not s.lower().startswith("date d'"):
        return f"Date d’épédition/retrait : {s} "
    return s if s.endswith(" ") else f"{s} "

# ----------------------------------------------------------------------

def from_payload(data: dict | None = None) -> FactureNocibe:
    raw_data = rules.as_dict(data)
    merged = dict(raw_data)
    if "card" in raw_data and isinstance(raw_data["card"], dict):
        for k, v in raw_data["card"].items():
            merged.setdefault(k, v)
    if "visible" in raw_data and isinstance(raw_data["visible"], dict):
        for k, v in raw_data["visible"].items():
            merged.setdefault(k, v)
    data = rules.apply_payload(merged)
    doc = FactureNocibe()

    doc.visible.header = rules.flag(data, "header", True)
    doc.visible.header_logo = rules.flag(data, "header_logo", True)
    doc.visible.header_titre = rules.flag(data, "header_titre", True)
    doc.visible.header_facturation = rules.flag(data, "header_facturation", True)
    doc.visible.header_livraison = rules.flag(data, "header_livraison", True)
    doc.visible.header_commande = rules.flag(data, "header_commande", True)
    doc.visible.middle = rules.flag(data, "middle", True)
    doc.visible.middle_table = rules.flag(data, "middle_table", True)
    doc.visible.middle_totals = rules.flag(data, "middle_totals", True)
    doc.visible.middle_details = rules.flag(data, "middle_details", True)

    c = doc.card
    c.facture_num = _format_facture_num(data.get("facture_num"))
    c.date_emission = _format_date_emission(data.get("date_emission"))
    c.facturation_titre = str(data.get("facturation_titre") or copy.TITRE_FACTURATION)

    nom = str(data.get("nom") or "").strip()
    prenom = str(data.get("prenom") or "").strip()
    if nom or prenom:
        c.client_nom = f"{nom} {prenom}".strip() + " "
    else:
        c.client_nom = str(data.get("client_nom") or copy.CLIENT_NOM)

    c.client_rue = str(data.get("adresse") or data.get("client_rue") or copy.CLIENT_RUE)

    cp = str(data.get("cp") or "").strip()
    ville = str(data.get("ville") or "").strip()
    if cp or ville:
        c.client_ville = f"{cp} {ville}".strip()
    else:
        c.client_ville = str(data.get("client_ville") or copy.CLIENT_VILLE)

    c.client_pays = str(data.get("pays") or data.get("client_pays") or copy.CLIENT_PAYS)
    c.livraison_titre = str(data.get("livraison_titre") or copy.TITRE_LIVRAISON)

    liv_nom = str(data.get("livraison_nom") or "").strip()
    liv_prenom = str(data.get("livraison_prenom") or "").strip()
    if liv_prenom:
        c.livraison_nom = f"{liv_nom} {liv_prenom}".strip() + " "
    elif liv_nom:
        c.livraison_nom = liv_nom if liv_nom.endswith(" ") else f"{liv_nom} "
    else:
        c.livraison_nom = str(copy.LIVRAISON_NOM)

    c.livraison_rue = str(data.get("livraison_adresse") or data.get("livraison_rue") or copy.LIVRAISON_RUE)

    liv_cp = str(data.get("livraison_cp") or "").strip()
    liv_ville = str(data.get("livraison_ville") or "").strip()
    if liv_cp or liv_ville:
        c.livraison_ville = f"{liv_cp} {liv_ville}".strip()
    else:
        c.livraison_ville = str(data.get("livraison_ville") or copy.LIVRAISON_VILLE)

    c.livraison_pays = str(data.get("livraison_pays") or copy.LIVRAISON_PAYS)
    c.commande_date = _format_commande_date(data.get("commande_date"))
    c.commande_mode = _format_commande_mode(data.get("commande_mode"))
    c.commande_expedition = _format_commande_expedition(data.get("commande_expedition"))
    c.commande_etat = str(data.get("commande_etat") or copy.COMMANDE_ETAT)

    c.items = _items_from_payload(data)

    tot_ht = data.get("total_ht")
    tot_tva = data.get("total_tva")
    tot_ttc = data.get("total_ttc")

    has_custom_ttc = tot_ttc is not None and str(tot_ttc).strip() != "" and str(tot_ttc).strip() != copy.DEFAULT_TOTAL_TTC
    has_custom_ht = tot_ht is not None and str(tot_ht).strip() != "" and str(tot_ht).strip() not in (copy.DEFAULT_TOTAL_HT, copy.DEFAULT_TOTAL_HT.replace(",", "."))

    if "items" in data and not has_custom_ttc and not has_custom_ht:
        totals = rules.compute_totals(c.items)
        c.total_ht = totals["total_ht"]
        c.total_tva = totals["total_tva"]
        c.total_ttc = totals["total_ttc"]
        c.tva_base_ht = totals["tva_base_ht"]
        c.tva_montant = totals["tva_montant"]
        c.reglement_montant = totals["reglement_montant"]
    elif has_custom_ttc and not has_custom_ht:
        ttc_val = rules.parse_money(tot_ttc)
        ht_val = round(ttc_val / 1.20, 2)
        tva_val = round(ttc_val - ht_val, 2)
        c.total_ttc = rules.format_money(ttc_val)
        c.total_ht = rules.format_money(ht_val).replace(".", ",")
        c.total_tva = rules.format_money(tva_val)
        c.tva_base_ht = rules.format_money(ht_val)
        c.tva_montant = rules.format_money(tva_val)
        c.reglement_montant = rules.format_money(ttc_val)
    else:
        c.total_ht = str(tot_ht if tot_ht is not None else copy.DEFAULT_TOTAL_HT)
        c.total_tva = str(tot_tva if tot_tva is not None else copy.DEFAULT_TOTAL_TVA)
        c.total_ttc = str(tot_ttc if tot_ttc is not None else copy.DEFAULT_TOTAL_TTC)
        c.tva_base_ht = str(data.get("tva_base_ht", c.total_ht.replace(",", ".")))
        c.tva_montant = str(data.get("tva_montant", c.total_tva))
        c.reglement_montant = str(data.get("reglement_montant", c.total_ttc))

    c.tva_rate_pct = str(data.get("tva_rate_pct", "20.00 %"))
    c.reglement_date = str(data.get("reglement_date", copy.DEFAULT_REGLEMENT_DATE))
    c.reglement_mode = str(data.get("reglement_mode", copy.DEFAULT_REGLEMENT_MODE))

    return rules.apply_doc(doc)
