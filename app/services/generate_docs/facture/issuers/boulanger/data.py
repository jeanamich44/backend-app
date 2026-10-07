from dataclasses import dataclass, field
from . import copy

# ----------------------------------------------------------------------

@dataclass
class Article:
    nom: str = copy.EL_ARTICLE_1_NOM
    code: str = copy.EL_ARTICLE_1_CODE
    qte: str = copy.EL_ARTICLE_1_QTE
    pu_ttc: str = copy.EL_ARTICLE_1_PU_TTC
    tva_taux: str = copy.EL_ARTICLE_1_TVA_TAUX
    total_ttc: str = copy.EL_ARTICLE_1_TOTAL_TTC
    ecopart: str = copy.EL_ARTICLE_1_ECOPART
    garantie_non_retenue: str = copy.EL_ARTICLE_1_GARANTIE_NON_RETENUE
    garantie_reparation: str = copy.EL_ARTICLE_1_GARANTIE_REPARATION
    dispo_pieces_label: str = copy.EL_ARTICLE_1_DISPO_PIECES_LABEL
    dispo_pieces: str = copy.EL_ARTICLE_1_DISPO_PIECES
    vendeur: str = ""

# ----------------------------------------------------------------------

def default_items(mode: str = copy.MODE_EN_LIGNE) -> list[Article]:
    if mode == copy.MODE_MAGASIN:
        a1 = Article(
            nom=copy.MAG_ARTICLE_1_NOM,
            code=copy.MAG_ARTICLE_1_CODE,
            qte=copy.MAG_ARTICLE_1_QTE,
            pu_ttc=copy.MAG_ARTICLE_1_PU_TTC,
            tva_taux=copy.MAG_ARTICLE_1_TVA_TAUX,
            total_ttc=copy.MAG_ARTICLE_1_TOTAL_TTC,
            ecopart=copy.MAG_ARTICLE_1_ECOPART,
            garantie_non_retenue=copy.MAG_ARTICLE_1_GARANTIE_NON_RETENUE,
            garantie_reparation=copy.MAG_ARTICLE_1_GARANTIE_REPARATION,
            dispo_pieces_label=copy.MAG_ARTICLE_1_DISPO_PIECES_LABEL,
            dispo_pieces=copy.MAG_ARTICLE_1_DISPO_PIECES,
        )
    else:
        a1 = Article(
            nom=copy.EL_ARTICLE_1_NOM,
            code=copy.EL_ARTICLE_1_CODE,
            qte=copy.EL_ARTICLE_1_QTE,
            pu_ttc=copy.EL_ARTICLE_1_PU_TTC,
            tva_taux=copy.EL_ARTICLE_1_TVA_TAUX,
            total_ttc=copy.EL_ARTICLE_1_TOTAL_TTC,
            ecopart=copy.EL_ARTICLE_1_ECOPART,
            garantie_non_retenue=copy.EL_ARTICLE_1_GARANTIE_NON_RETENUE,
            garantie_reparation=copy.EL_ARTICLE_1_GARANTIE_REPARATION,
            dispo_pieces_label=copy.EL_ARTICLE_1_DISPO_PIECES_LABEL,
            dispo_pieces=copy.EL_ARTICLE_1_DISPO_PIECES,
        )
    return [a1]

# ----------------------------------------------------------------------

def _item_from_dict(d: dict, fallback: Article | None = None) -> Article:
    fb = fallback or Article()
    return Article(
        nom=str(d.get("nom", fb.nom)),
        code=str(d.get("code", fb.code)),
        qte=str(d.get("qte", fb.qte)),
        pu_ttc=str(d.get("pu_ttc", fb.pu_ttc)),
        tva_taux=str(d.get("tva_taux", fb.tva_taux)),
        total_ttc=str(d.get("total_ttc", fb.total_ttc)),
        ecopart=str(d.get("ecopart", fb.ecopart)),
        garantie_non_retenue=str(d.get("garantie_non_retenue", fb.garantie_non_retenue)),
        garantie_reparation=str(d.get("garantie_reparation", fb.garantie_reparation)),
        dispo_pieces_label=str(d.get("dispo_pieces_label", fb.dispo_pieces_label)),
        dispo_pieces=str(d.get("dispo_pieces", fb.dispo_pieces)),
        vendeur=str(d.get("vendeur", fb.vendeur)),
    )

# ----------------------------------------------------------------------

@dataclass
class DocCard:
    mode: str = copy.MODE_EN_LIGNE
    seller_type: str = copy.SELLER_BOULANGER

    doc_type: str = copy.DOC_TYPE
    facture_num: str = copy.EL_FACTURE_NUM
    facture_date: str = copy.EL_FACTURE_DATE
    facture_time: str = copy.EL_FACTURE_TIME
    facture_page: str = copy.FACTURE_PAGE

    store_nom: str = copy.EL_STORE_NOM
    store_rue1: str = copy.EL_STORE_RUE1
    store_rue2: str = copy.EL_STORE_RUE2
    store_lieu: str = ""
    store_cp_ville: str = copy.EL_STORE_CP_VILLE
    store_siret: str = copy.EL_STORE_SIRET
    store_tel: str = copy.EL_STORE_TEL

    seller_name: str = copy.TIERS_VENDEUR_NOM
    seller_rue: str = copy.TIERS_VENDEUR_RUE
    seller_cp_ville: str = copy.TIERS_VENDEUR_CP_VILLE
    seller_siret: str = copy.TIERS_VENDEUR_SIRET
    seller_tva: str = copy.TIERS_VENDEUR_TVA
    seller_capital: str = copy.TIERS_VENDEUR_CAPITAL
    seller_rcs: str = copy.TIERS_VENDEUR_RCS

    client_nom: str = copy.EL_CLIENT_NOM
    client_rue: str = copy.EL_CLIENT_RUE
    client_cp_ville: str = copy.EL_CLIENT_CP_VILLE
    client_tel: str = ""
    client_num: str = copy.EL_CLIENT_NUM

    barcode_val: str = copy.EL_BARCODE_VAL

    table_header_text: str = copy.TABLE_HEADER
    items: list[Article] = field(default_factory=default_items)

    extra_line_nom: str = copy.EL_EXTRA_NOM
    extra_line_code: str = copy.EL_EXTRA_CODE
    extra_line_qte: str = copy.EL_EXTRA_QTE
    extra_line_pu_ttc: str = copy.EL_EXTRA_PU_TTC
    extra_line_tva: str = copy.EL_EXTRA_TVA_TAUX
    extra_line_total: str = copy.EL_EXTRA_TOTAL_TTC

    club_nom: str = copy.CLUB_NOM
    club_code: str = copy.CLUB_CODE
    club_qte: str = copy.CLUB_QTE
    club_pu_ttc: str = copy.CLUB_PU_TTC
    club_tva_taux: str = copy.CLUB_TVA_TAUX
    club_total_ttc: str = copy.CLUB_TOTAL_TTC

    total_ht: str = copy.EL_TOTAL_HT
    total_ttc: str = copy.EL_TOTAL_TTC
    dont_tva: str = copy.EL_DONT_TVA
    dont_tva_taux: str = copy.EL_DONT_TVA_TAUX
    dont_ecopart: str = copy.EL_DONT_ECOPART

    reglement_mode: str = copy.EL_REGLEMENT_MODE
    reglement_montant: str = copy.EL_REGLEMENT_MONTANT

    notice_cumul: str = copy.EL_NOTICE_CUMUL
    notice_merci: str = copy.NOTICE_MERCI
    notice_garantie_1: str = copy.NOTICE_GARANTIE_L1
    notice_garantie_2: str = copy.NOTICE_GARANTIE_L2
    notice_garantie_3: str = copy.NOTICE_GARANTIE_L3

    conditions_type: str = "none"
    usage_pro: str = "NON"
    livraison: str = "NON"
    mise_en_service: str = "NON"

    company_nom: str = copy.COMPANY_NOM
    company_capital: str = copy.COMPANY_CAPITAL
    company_rue: str = copy.COMPANY_RUE
    company_rcs: str = copy.COMPANY_RCS
    company_cp_ville: str = copy.COMPANY_CP_VILLE
    company_tva: str = copy.COMPANY_TVA
    company_ape: str = copy.COMPANY_APE

# ----------------------------------------------------------------------

@dataclass
class DocVisible:
    header: bool = True
    header_lateral: bool = True
    header_lateral_logo: bool = True
    header_lateral_barcode: bool = True
    header_lateral_sidebar: bool = True
    header_title: bool = True
    header_addresses: bool = True
    header_store: bool = True
    header_client: bool = True

    middle: bool = True
    middle_table_header: bool = True
    middle_articles: bool = True
    middle_club: bool = True
    middle_totals: bool = True
    middle_payment: bool = True
    middle_notice: bool = True

    footer: bool = True
    footer_conditions: bool = True
    footer_company: bool = True
    footer_legal: bool = True

    @property
    def lateral(self) -> bool:
        return self.header_lateral

    @lateral.setter
    def lateral(self, val: bool):
        self.header_lateral = val

    @property
    def lateral_logo(self) -> bool:
        return self.header_lateral_logo

    @lateral_logo.setter
    def lateral_logo(self, val: bool):
        self.header_lateral_logo = val

    @property
    def lateral_barcode(self) -> bool:
        return self.header_lateral_barcode

    @lateral_barcode.setter
    def lateral_barcode(self, val: bool):
        self.header_lateral_barcode = val

    @property
    def lateral_sidebar(self) -> bool:
        return self.header_lateral_sidebar

    @lateral_sidebar.setter
    def lateral_sidebar(self, val: bool):
        self.header_lateral_sidebar = val

# ----------------------------------------------------------------------

@dataclass
class FactureBoulanger:
    card: DocCard = field(default_factory=DocCard)
    visible: DocVisible = field(default_factory=DocVisible)

Doc = FactureBoulanger

# ----------------------------------------------------------------------

def from_payload(payload: dict | None = None) -> FactureBoulanger:
    doc = FactureBoulanger()
    if not payload:
        return doc

    mode = str(payload.get("mode", doc.card.mode))
    doc.card.mode = mode
    seller_type = str(payload.get("seller_type", doc.card.seller_type))
    doc.card.seller_type = seller_type

    if mode == copy.MODE_MAGASIN:
        doc.card.facture_num = copy.MAG_FACTURE_NUM
        doc.card.facture_date = copy.MAG_FACTURE_DATE
        doc.card.facture_time = copy.MAG_FACTURE_TIME
        doc.card.barcode_val = copy.MAG_BARCODE_VAL
        doc.card.store_nom = copy.MAG_STORE_NOM
        doc.card.store_rue1 = copy.MAG_STORE_RUE1
        doc.card.store_rue2 = copy.MAG_STORE_RUE2
        doc.card.store_lieu = copy.MAG_STORE_LIEU
        doc.card.store_cp_ville = copy.MAG_STORE_CP_VILLE
        doc.card.store_siret = copy.MAG_STORE_SIRET
        doc.card.client_nom = copy.MAG_CLIENT_NOM
        doc.card.client_rue = copy.MAG_CLIENT_RUE
        doc.card.client_cp_ville = copy.MAG_CLIENT_CP_VILLE
        doc.card.client_num = copy.MAG_CLIENT_NUM
        doc.card.extra_line_nom = copy.MAG_EXTRA_NOM
        doc.card.extra_line_code = copy.MAG_EXTRA_CODE
        doc.card.extra_line_qte = copy.MAG_EXTRA_QTE
        doc.card.extra_line_pu_ttc = copy.MAG_EXTRA_PU_TTC
        doc.card.extra_line_tva = copy.MAG_EXTRA_TVA_TAUX
        doc.card.extra_line_total = copy.MAG_EXTRA_TOTAL_TTC
        doc.card.total_ht = copy.MAG_TOTAL_HT
        doc.card.total_ttc = copy.MAG_TOTAL_TTC
        doc.card.dont_tva = copy.MAG_DONT_TVA
        doc.card.dont_tva_taux = copy.MAG_DONT_TVA_TAUX
        doc.card.dont_ecopart = copy.MAG_DONT_ECOPART
        doc.card.reglement_montant = copy.MAG_REGLEMENT_MONTANT
        doc.card.conditions_type = "internet"
        doc.card.notice_cumul = ""
        doc.card.items = default_items(copy.MODE_MAGASIN)
        doc.visible.middle_club = True
        doc.card.extra_line_nom = ""

    for fld in (
        "header", "header_lateral", "header_lateral_logo", "header_lateral_barcode", "header_lateral_sidebar",
        "header_title", "header_addresses", "header_store", "header_client",
        "middle", "middle_table_header", "middle_articles", "middle_club", "middle_totals", "middle_payment", "middle_notice",
        "footer", "footer_conditions", "footer_company", "footer_legal",
        "lateral", "lateral_logo", "lateral_barcode", "lateral_sidebar",
    ):
        if fld in payload:
            setattr(doc.visible, fld, bool(payload[fld]))

    if "lateral" in payload:
        doc.visible.header_lateral = bool(payload["lateral"])
    if "lateral_logo" in payload:
        doc.visible.header_lateral_logo = bool(payload["lateral_logo"])
    if "lateral_barcode" in payload:
        doc.visible.header_lateral_barcode = bool(payload["lateral_barcode"])
    if "lateral_sidebar" in payload:
        doc.visible.header_lateral_sidebar = bool(payload["lateral_sidebar"])

    for fld in (
        "mode", "seller_type", "doc_type", "facture_num", "facture_date", "facture_time", "facture_page",
        "store_nom", "store_rue1", "store_rue2", "store_lieu", "store_cp_ville", "store_siret", "store_tel",
        "seller_name", "seller_rue", "seller_cp_ville", "seller_siret", "seller_tva", "seller_capital", "seller_rcs",
        "client_nom", "client_rue", "client_cp_ville", "client_tel", "client_num",
        "barcode_val", "table_header_text",
        "extra_line_nom", "extra_line_code", "extra_line_qte", "extra_line_pu_ttc", "extra_line_tva", "extra_line_total",
        "club_nom", "club_code", "club_qte", "club_pu_ttc", "club_tva_taux", "club_total_ttc",
        "total_ht", "total_ttc", "dont_tva", "dont_tva_taux", "dont_ecopart",
        "reglement_mode", "reglement_montant",
        "notice_cumul", "notice_merci", "notice_garantie_1", "notice_garantie_2", "notice_garantie_3",
        "conditions_type", "usage_pro", "livraison", "mise_en_service",
        "company_nom", "company_capital", "company_rue", "company_rcs", "company_cp_ville", "company_tva", "company_ape",
    ):
        if fld in payload and payload[fld] is not None:
            setattr(doc.card, fld, str(payload[fld]))

    if "items" in payload and isinstance(payload["items"], list):
        items_list = []
        defs = default_items(mode)
        for idx, itm in enumerate(payload["items"][:3]):
            if isinstance(itm, dict):
                fb = defs[idx] if idx < len(defs) else Article(
                    nom=getattr(copy, f"ARTICLE_{idx+1}_NOM", ""),
                    code=getattr(copy, f"ARTICLE_{idx+1}_CODE", ""),
                    qte=getattr(copy, f"ARTICLE_{idx+1}_QTE", "1"),
                    pu_ttc=getattr(copy, f"ARTICLE_{idx+1}_PU_TTC", ""),
                    tva_taux=getattr(copy, f"ARTICLE_{idx+1}_TVA_TAUX", "20,00"),
                    total_ttc=getattr(copy, f"ARTICLE_{idx+1}_TOTAL_TTC", ""),
                    ecopart=getattr(copy, f"ARTICLE_{idx+1}_ECOPART", ""),
                    garantie_non_retenue=getattr(copy, f"ARTICLE_{idx+1}_GARANTIE_NON_RETENUE", ""),
                    garantie_reparation=getattr(copy, f"ARTICLE_{idx+1}_GARANTIE_REPARATION", ""),
                    dispo_pieces_label=getattr(copy, f"ARTICLE_{idx+1}_DISPO_PIECES_LABEL", ""),
                    dispo_pieces=getattr(copy, f"ARTICLE_{idx+1}_DISPO_PIECES", ""),
                )
                items_list.append(_item_from_dict(itm, fb))
        if items_list:
            doc.card.items = items_list
    else:
        flat_items = []
        for i in (1, 2, 3):
            prefix = f"article_{i}_"
            if any(f"{prefix}{k}" in payload for k in ("nom", "code", "pu_ttc", "total_ttc")):
                item_dict = {
                    k: payload[f"{prefix}{k}"]
                    for k in (
                        "nom", "code", "qte", "pu_ttc", "tva_taux", "total_ttc",
                        "ecopart", "garantie_non_retenue", "garantie_reparation",
                        "dispo_pieces_label", "dispo_pieces", "vendeur"
                    )
                    if f"{prefix}{k}" in payload
                }
                fb = Article(
                    nom=getattr(copy, f"ARTICLE_{i}_NOM", ""),
                    code=getattr(copy, f"ARTICLE_{i}_CODE", ""),
                    qte=getattr(copy, f"ARTICLE_{i}_QTE", "1"),
                    pu_ttc=getattr(copy, f"ARTICLE_{i}_PU_TTC", ""),
                    tva_taux=getattr(copy, f"ARTICLE_{i}_TVA_TAUX", "20,00"),
                    total_ttc=getattr(copy, f"ARTICLE_{i}_TOTAL_TTC", ""),
                    ecopart=getattr(copy, f"ARTICLE_{i}_ECOPART", ""),
                    garantie_non_retenue=getattr(copy, f"ARTICLE_{i}_GARANTIE_NON_RETENUE", ""),
                    garantie_reparation=getattr(copy, f"ARTICLE_{i}_GARANTIE_REPARATION", ""),
                    dispo_pieces_label=getattr(copy, f"ARTICLE_{i}_DISPO_PIECES_LABEL", ""),
                    dispo_pieces=getattr(copy, f"ARTICLE_{i}_DISPO_PIECES", ""),
                )
                flat_items.append(_item_from_dict(item_dict, fb))
        if flat_items:
            doc.card.items = flat_items

    return doc
