from .. import copy, layout, paint

# ----------------------------------------------------------------------

def is_visible(doc) -> bool:
    if not getattr(doc.visible, "header", True):
        return False
    return bool(getattr(doc.visible, "header_addresses", True))

# ----------------------------------------------------------------------

def get_lines(doc) -> list[str]:
    if not is_visible(doc):
        return []

    card = doc.card
    mode = getattr(card, "mode", copy.MODE_EN_LIGNE)
    seller_type = getattr(card, "seller_type", copy.SELLER_BOULANGER)

    c_nom = getattr(card, "client_nom", "")
    c_rue = getattr(card, "client_rue", "")
    c_cp = getattr(card, "client_cp_ville", "")
    c_tel = getattr(card, "client_tel", "")
    c_num = getattr(card, "client_num", "")

    show_store = bool(getattr(doc.visible, "header_store", True))
    show_client = bool(getattr(doc.visible, "header_client", True))

    if not show_client:
        c_nom = c_rue = c_cp = c_tel = c_num = ""

    lines = []

    if mode == copy.MODE_MAGASIN:
        if seller_type == copy.SELLER_TIERS:
            s_l1 = getattr(card, "seller_name", copy.TIERS_VENDEUR_NOM) if show_store else ""
            s_l2 = "Vendeur partenaire Boulanger" if show_store else ""
            s_l3 = getattr(card, "seller_rue", copy.TIERS_VENDEUR_RUE) if show_store else ""
            s_l4 = getattr(card, "seller_cp_ville", copy.TIERS_VENDEUR_CP_VILLE) if show_store else ""
            s_l5 = ""
            siretr = getattr(card, "seller_siret", copy.TIERS_VENDEUR_SIRET)
            s_l6 = f"SIRET {siretr}" if (show_store and siretr) else ""
        else:
            s_l1 = getattr(card, "store_nom", copy.MAG_STORE_NOM) if show_store else ""
            s_l2 = getattr(card, "store_rue1", copy.MAG_STORE_RUE1) if show_store else ""
            s_l3 = getattr(card, "store_rue2", copy.MAG_STORE_RUE2) if show_store else ""
            s_l4 = getattr(card, "store_lieu", copy.MAG_STORE_LIEU) if show_store else ""
            s_l5 = getattr(card, "store_cp_ville", copy.MAG_STORE_CP_VILLE) if show_store else ""
            siretr = getattr(card, "store_siret", copy.MAG_STORE_SIRET)
            s_l6 = f"SIRET {siretr}" if (show_store and siretr and not str(siretr).startswith("SIRET")) else (str(siretr) if show_store else "")

        c_num_str = f"N\xb0 client: {c_num}" if c_num else ""
        pairs = [
            (s_l1, c_nom),
            (s_l2, c_rue),
            (s_l3, c_cp),
            (s_l4, ""),
            (s_l5, ""),
            (s_l6, c_num_str),
        ]
        for s_part, c_part in pairs:
            if c_part:
                line_str = f"{' ' * 37}{s_part:<40}{c_part}"
            elif s_part:
                line_str = f"{' ' * 37}{s_part}"
            else:
                line_str = ""
            lines.append(paint.escape_pdf(line_str))

    else:
        if seller_type == copy.SELLER_TIERS:
            s_l1 = getattr(card, "seller_name", copy.TIERS_VENDEUR_NOM) if show_store else ""
            s_l2 = "Vendeur partenaire Boulanger" if show_store else ""
            s_l3 = getattr(card, "seller_rue", copy.TIERS_VENDEUR_RUE) if show_store else ""
            s_l4 = getattr(card, "seller_cp_ville", copy.TIERS_VENDEUR_CP_VILLE) if show_store else ""
            siretr = getattr(card, "seller_siret", copy.TIERS_VENDEUR_SIRET)
            s_l5 = f"SIRET {siretr}" if (show_store and siretr) else ""
        else:
            s_l1 = getattr(card, "store_nom", copy.EL_STORE_NOM) if show_store else ""
            s_l2 = getattr(card, "store_rue1", copy.EL_STORE_RUE1) if show_store else ""
            s_l3 = getattr(card, "store_rue2", copy.EL_STORE_RUE2) if show_store else ""
            s_l4 = getattr(card, "store_cp_ville", copy.EL_STORE_CP_VILLE) if show_store else ""
            siretr = getattr(card, "store_siret", copy.EL_STORE_SIRET)
            s_l5 = f"SIRET {siretr}" if (show_store and siretr and not str(siretr).startswith("SIRET")) else (str(siretr) if show_store else "")

        c_tel_val = c_tel or getattr(card, "store_tel", copy.EL_STORE_TEL)
        pairs = [
            (s_l1, c_nom),
            (s_l2, c_rue),
            (s_l3, c_cp),
            (s_l4, ""),
            (s_l5, c_tel_val),
        ]
        for s_part, c_part in pairs:
            if c_part:
                line_str = f"{' ' * 37}{s_part:<40}{c_part}"
            elif s_part:
                line_str = f"{' ' * 37}{s_part}"
            else:
                line_str = ""
            lines.append(paint.escape_pdf(line_str))

        c_num_line = f"{' ' * 77}N\xb0 client: {c_num}" if c_num else ""
        lines.append(f"() '({paint.escape_pdf(c_num_line)}) '")

    return lines

# ----------------------------------------------------------------------

def draw(c, doc):
    pass
