import random
import re

from app.services.generate_docs.releve import generate_transactions as gt

# ==========================================
# 1. CONSTANTES & TABLES DE RÉFÉRENCE
# ==========================================

VALID_DURATIONS = {
    1: "Mois Unique",
    3: "Trimestre (3 mois)",
    6: "Semestre (6 mois)",
    12: "Année complète (12 mois)"
}

MODES = ["facile", "personnalise"]

CITIES_DATA = [
    ("PARIS", "75001"), ("MARSEILLE", "13001"), ("LYON", "69001"), ("TOULOUSE", "31000"),
    ("NICE", "06000"), ("NANTES", "44000"), ("MONTPELLIER", "34000"), ("STRASBOURG", "67000"),
    ("BORDEAUX", "33000"), ("LILLE", "59000"), ("RENNES", "35000"), ("REIMS", "51100"),
    ("SAINT-ETIENNE", "42000"), ("TOULON", "83000"), ("GRENOBLE", "38000"), ("DIJON", "21000"),
    ("ANGERS", "49000"), ("NIMES", "30000"), ("VILLEURBANNE", "69100"), ("LE MANS", "72000"),
    ("AIX-EN-PROVENCE", "13100"), ("CLERMONT-FERRAND", "63000"), ("BREST", "29200"), ("TOURS", "37000"),
    ("AMIENS", "80000"), ("LIMOGES", "87000"), ("ANNECY", "74000"), ("PERPIGNAN", "66000"),
    ("BOULOGNE-BILLANCOURT", "92100"), ("METZ", "57000"), ("BESANCON", "25000"), ("ORLEANS", "45000"),
    ("SAINT-DENIS", "93200"), ("ROUEN", "76000"), ("ARGENTEUIL", "95100"), ("MULHOUSE", "68100"),
    ("CAEN", "14000"), ("NANCY", "54000"), ("ROUBAIX", "59100"), ("TOURCOING", "59200"),
    ("NANTERRE", "92000"), ("AVIGNON", "84000"), ("VITRY-SUR-SEINE", "94400"), ("CRETEIL", "94000"),
    ("DUNKERQUE", "59140"), ("POITIERS", "86000"), ("ASNIERES-SUR-SEINE", "92600"), ("VERSAILLES", "78000")
]

NOMS_FAMILLE = [
    "MARTIN", "BERNARD", "THOMAS", "PETIT", "ROBERT", "RICHARD", "DURAND", "DUBOIS", "MOREAU", "LAURENT",
    "SIMON", "MICHEL", "LEFEBVRE", "LEROY", "ROUX", "DAVID", "BERTRAND", "MOREL", "FOURNIER", "GIRARD",
    "BONNET", "DUPONT", "LAMBERT", "FONTAINE", "ROUSSEAU", "VINCENT", "MULLER", "LEFEVRE", "FAURE", "ANDRE",
    "MERCIER", "BLANC", "GUERIN", "BOYER", "GARNIER", "CHEVALIER", "FRANCOIS", "LEGRAND", "GAUTHIER", "GARCIA"
]

RUES_EXEMPLES = [
    "12 RUE DE LA PAIX", "45 AVENUE DE LA REPUBLIQUE", "8 BOULEVARD VOLTAIRE", "23 RUE VICTOR HUGO",
    "17 AVENUE JEAN JAURES", "6 RUE DU MOULIN", "31 RUE NATIONALE", "14 BOULEVARD PASTEUR",
    "9 AVENUE FOCH", "52 RUE DE PARIS", "3 IMPASSE DES FLEURS", "74 RUE DU COMMERCE"
]

ENTREPRISES_PRIVEES = [
    "CAPGEMINI TECHNOLOGY SERVICES", "GROUPE RENAULT SAS", "SOCIETE GENERALE SA", "THALES SIX GTS FRANCE SAS",
    "DASSAULT AVIATION SA", "AIRBUS COMMERCIAL AIRCRAFT", "SCHNEIDER ELECTRIC FRANCE", "SAFRAN AIRCRAFT ENGINES",
    "ORANGE SA DIRECTION REGIONALE", "SANOFI WINTHROP INDUSTRIE", "ENGIE SOLUTIONS FRANCE", "MICHELIN PNEUMATIQUES"
]

# ==========================================
# 2. UTILITAIRES DE CONTINUITÉ TEMPORELLE
# ==========================================

def get_month_sequence(start_month, start_year, count):
    sequence = []
    curr_m = int(start_month)
    curr_y = int(start_year)
    for _ in range(count):
        sequence.append((curr_m, curr_y))
        curr_m += 1
        if curr_m > 12:
            curr_m = 1
            curr_y += 1
    return sequence

def generate_random_account_number():
    chiffres = "".join(random.choices("0123456789", k=7))
    lettre = random.choice(["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"])
    cle = "".join(random.choices("0123456789", k=3))
    return f"{chiffres} {lettre} {cle}"

def generate_random_iban(account_num_str):
    clean_no = str(account_num_str).replace(" ", "")
    cle_iban = "".join(random.choices("0123456789", k=2))
    return f"FR{cle_iban} 2004 1010 05{clean_no[:8]} {clean_no[8:]}65"

def format_currency_french(val):
    return f"{val:,.2f}".replace(",", " ").replace(".", ",")

def parse_currency_french(val_str):
    if val_str is None:
        return 0.0
    s = str(val_str).replace("€", "").replace("¤", "").replace("+", "").replace(" ", "").replace(",", ".")
    try:
        return float(s)
    except Exception:
        return 0.0

# ==========================================
# 3. CONSTRUCTEURS DE PROFILS (LES 4 MODES)
# ==========================================

def build_mode_facile(user_params):
    profil = user_params.get("profil", "normal")
    nom_part = (user_params.get("nom") or "").strip()
    prenom_part = (user_params.get("prenom") or "").strip()
    if nom_part or prenom_part:
        nom_input = f"{nom_part} {prenom_part}".strip()
    else:
        nom_input = (user_params.get("nom_prenom") or user_params.get("titulaire_nom_complet") or user_params.get("titulaire_nom") or user_params.get("nom_complet") or "").strip()
        if nom_input:
            parts = nom_input.split(None, 1)
            nom_part = parts[0]
            prenom_part = parts[1] if len(parts) > 1 else ""
    civ_input = (user_params.get("civilite") or "M.").strip()
    
    if nom_input:
        civ_pattern = r"^(?:M\.|MR\.|MR|MME\.|MME|MLLE\.|MLLE|MONSIEUR|MADAME|MADEMOISELLE)\s+"
        cleaned_nom = nom_input
        detected_civ = None
        while True:
            m_civ = re.match(civ_pattern, cleaned_nom, flags=re.IGNORECASE)
            if m_civ:
                detected_civ = m_civ.group(0).strip()
                cleaned_nom = cleaned_nom[m_civ.end():].strip()
            else:
                break
                
        chosen_civ = (civ_input or detected_civ or "M.").strip()
        civ_u = chosen_civ.upper().replace(".", "")
        if civ_u in ["MR", "MONSIEUR", "M"]:
            norm_civ = "M."
        elif civ_u in ["MME", "MADAME"]:
            norm_civ = "Mme"
        elif civ_u in ["MLLE", "MADEMOISELLE"]:
            norm_civ = "Mlle"
        else:
            norm_civ = chosen_civ
            
        if not cleaned_nom:
            cleaned_nom = "DUPONT JEAN"
            
        nom_complet = f"{norm_civ} {cleaned_nom}".strip()
    else:
        sexe = random.choice(["MR", "MME"])
        norm_civ = "M." if sexe == "MR" else "Mme"
        nom_complet = f"{norm_civ} {random.choice(NOMS_FAMILLE)} {random.choice(gt.PRENOMS_VIREMENT).upper()}"
        
    sexe = "F" if any(k in nom_complet.upper() for k in ["MME", "MADAME", "MLLE"]) else "M"
    
    ville_input = user_params.get("ville") or user_params.get("titulaire_ville")
    cp_input = user_params.get("cp") or user_params.get("titulaire_cp")
    if ville_input:
        matched_city = next((c for c in CITIES_DATA if c[0].upper() == ville_input.upper()), None)
        if matched_city:
            city = matched_city[0]
            cp = cp_input or matched_city[1]
        else:
            city = ville_input.upper()
            cp = cp_input or "75000"
    else:
        city, cp = random.choice(CITIES_DATA)
        
    adresse = user_params.get("adresse", random.choice(RUES_EXEMPLES))
    card_number = user_params.get("card_number", str(random.randint(100, 999)))
    account_num = user_params.get("account_num") or user_params.get("numero_compte") or generate_random_account_number()
    identifiant = user_params.get("identifiant", "".join(random.choices("0123456789", k=10)))
    iban = user_params.get("iban", generate_random_iban(account_num))
    
    wealth_profile = user_params.get("wealth_profile", "moyen")
    if profil in ["chomage", "etudiant"]:
        wealth_profile = "pauvre"
    elif profil == "investisseur":
        wealth_profile = "riche"
        
    age_profile = "jeune" if profil == "etudiant" else ("senior" if profil == "retraite" else "adulte")
    
    solde_initial = user_params.get("solde_initial")
    if solde_initial is None:
        if wealth_profile == "riche":
            solde_initial = round(random.uniform(5500.0, 14000.0), 2)
        elif wealth_profile == "pauvre":
            solde_initial = round(random.uniform(250.0, 950.0), 2)
        else:
            solde_initial = round(random.uniform(1800.0, 4200.0), 2)
    else:
        solde_initial = parse_currency_french(solde_initial)
        
    nb_tx_moyen = max(18, int(user_params.get("nb_transactions") or user_params.get("nb_transactions_moyen") or random.randint(18, 30)))
    
    return {
        "mode": "facile",
        "profil": profil,
        "wealth_profile": wealth_profile,
        "age_profile": age_profile,
        "nom": nom_part,
        "prenom": prenom_part,
        "nom_prenom": cleaned_nom,
        "titulaire_nom": nom_complet,
        "titulaire_nom_complet": nom_complet,
        "titulaire_sexe": sexe,
        "titulaire_adresse": adresse,
        "complement_adresse": user_params.get("complement_adresse", ""),
        "titulaire_cp": cp,
        "titulaire_ville": city,
        "centre_financier": user_params.get("centre_financier", "PARIS CENTRE FINANCIER"),
        "identifiant": identifiant,
        "card_number": card_number,
        "account_num": account_num,
        "numero_compte": account_num,
        "cle_compte": user_params.get("cle_compte", "57"),
        "iban": iban,
        "bic": user_params.get("bic", "PSSTFRPPPAR"),
        "decouvert_autorise": user_params.get("decouvert_autorise", "300,00"),
        "solde_initial": solde_initial,
        "nb_transactions": nb_tx_moyen,
        "has_epargne": bool(user_params.get("has_epargne", user_params.get("include_epargne", False))),
        "include_epargne": bool(user_params.get("has_epargne", user_params.get("include_epargne", False))),
        "afficher_ccp": user_params.get("afficher_ccp", True),
        "livret_a_nom": user_params.get("livret_a_nom", user_params.get("epargne_nom", "Livret A")),
        "livret_a_numero": user_params.get("livret_a_numero", user_params.get("epargne_numero", "210 5436798 J")),
        "livret_a_iban": user_params.get("livret_a_iban", user_params.get("epargne_iban", "FR76 1001 1000 2021 0543 6798 J51")),
        "livret_a_bic": user_params.get("livret_a_bic", user_params.get("epargne_bic", "PSSTFRPPCNE")),
        "livret_a_taux": user_params.get("livret_a_taux", user_params.get("epargne_taux", "3,00")),
        "solde_livret_a_initial": parse_currency_french(user_params.get("solde_livret_a_initial", user_params.get("epargne_solde_initial", 5000.0))),
        "livret_a_nb_transactions": int(user_params.get("livret_a_nb_transactions", user_params.get("epargne_nb_tx", 2))),
        "epargne_comptes": user_params.get("epargne_comptes"),
        "auto_fill_info_block": user_params.get("auto_fill_info_block", True),
        "annexe_info_type": user_params.get("annexe_info_type", "auto"),
        "annexe_info_custom_text": user_params.get("annexe_info_custom_text", ""),
        "show_annexe_carbone": user_params.get("show_annexe_carbone", True),
        "target_solde_final": user_params.get("target_solde_final"),
        "custom_transactions": user_params.get("custom_transactions", [])
    }

def build_mode_personnalise(user_params):
    base_cfg = build_mode_facile(user_params)
    base_cfg["mode"] = "personnalise"
    
    base_cfg["decouvert_autorise"] = user_params.get("decouvert_autorise", "300,00" if base_cfg["profil"] != "etudiant" else "100,00")
    base_cfg["prelevements_selectionnes"] = user_params.get("prelevements_selectionnes", ["EDF", "ORANGE", "GMF", "MUTUELLE"])
    base_cfg["auto_fill_info_block"] = user_params.get("auto_fill_info_block", True)
    
    base_cfg["custom_supermarche"] = user_params.get("custom_supermarche")
    base_cfg["custom_carburant"] = user_params.get("custom_carburant")
    base_cfg["custom_resto"] = user_params.get("custom_resto")
    base_cfg["custom_shopping"] = user_params.get("custom_shopping")
    base_cfg["custom_loisirs"] = user_params.get("custom_loisirs")
    base_cfg["custom_online"] = user_params.get("custom_online")
    
    base_cfg["custom_salaire_montant"] = user_params.get("custom_salaire_montant") or user_params.get("salaire_net")
    base_cfg["custom_employeur_nom"] = user_params.get("custom_employeur_nom") or user_params.get("employeur_nom")
    base_cfg["custom_salaire_jour"] = user_params.get("custom_salaire_jour") or user_params.get("jour_salaire")
    base_cfg["custom_loyer_montant"] = user_params.get("custom_loyer_montant") or user_params.get("loyer_montant")
    base_cfg["custom_loyer_bailleur"] = user_params.get("custom_loyer_bailleur") or user_params.get("loyer_bailleur")
    base_cfg["annexe_info_type"] = user_params.get("annexe_info_type", "auto")
    base_cfg["annexe_info_custom_text"] = user_params.get("annexe_info_custom_text", "")
    base_cfg["show_annexe_carbone"] = user_params.get("show_annexe_carbone", True)
    base_cfg["target_deltas_sequence"] = user_params.get("target_deltas_sequence")
    base_cfg["target_solde_final"] = user_params.get("target_solde_final", base_cfg.get("target_solde_final"))
    base_cfg["has_epargne"] = bool(user_params.get("has_epargne", user_params.get("include_epargne", False)))
    base_cfg["include_epargne"] = bool(user_params.get("has_epargne", user_params.get("include_epargne", False)))
    base_cfg["custom_transactions"] = user_params.get("custom_transactions", base_cfg.get("custom_transactions", []))
    
    return base_cfg

def generate_multi_releves(config, start_month, start_year, duration_months=3):
    try:
        duration_months = max(1, min(24, int(duration_months)))
    except Exception:
        duration_months = 3
        
    mode = config.get("mode", "facile")
    if mode == "personnalise":
        runtime_cfg = build_mode_personnalise(config)
    else:
        runtime_cfg = build_mode_facile(config)
        
    months_seq = get_month_sequence(start_month, start_year, duration_months)
    runtime_cfg["bank_type"] = config.get("bank_type", "lbp")
    raw_start_num = config.get("start_num_releve") or config.get("numero_releve_debut")
    try:
        start_num_releve = int(raw_start_num) if raw_start_num is not None and str(raw_start_num).strip() else int(start_month if start_month else 1)
    except Exception:
        start_num_releve = int(start_month if start_month else 1)
    
    current_ccp_solde = runtime_cfg["solde_initial"]
    current_epargne_solde = runtime_cfg.get("solde_livret_a_initial", 3500.0)
    
    prof = runtime_cfg["profil"]
    w = runtime_cfg["wealth_profile"]
    
    nom_emp_req = runtime_cfg.get("custom_employeur_nom") or config.get("custom_employeur_nom") or config.get("employeur_nom")
    sal_net_req = runtime_cfg.get("custom_salaire_montant") or config.get("custom_salaire_montant") or config.get("salaire_net")
    jour_sal_req = runtime_cfg.get("custom_salaire_jour") or config.get("custom_salaire_jour") or config.get("jour_salaire")
    
    if nom_emp_req or sal_net_req or prof in ["normal", "locataire", "famille", "demandeur_credit"]:
        nom_emp = nom_emp_req or random.choice([
            "ORANGE SA", "CAPGEMINI TECHNOLOGY SERVICES", "GROUPE RENAULT SAS",
            "SOCIETE GENERALE SA", "THALES SIX GTS FRANCE SAS", "DASSAULT AVIATION SA",
            "AIRBUS COMMERCIAL AIRCRAFT", "SANOFI WINTHROP INDUSTRIE", "ENGIE SOLUTIONS FRANCE"
        ])
        mat = str(random.randint(100000, 999999))
        is_exact = bool(sal_net_req is not None)
        if sal_net_req:
            base_sal = sal_net_req
        elif w == "riche":
            base_sal = round(random.uniform(4800.0, 7500.0), 2)
        elif w == "pauvre":
            base_sal = round(random.uniform(1450.0, 1750.0), 2)
        else:
            base_sal = round(random.uniform(2250.0, 3100.0), 2)
            
        base_sal = parse_currency_french(base_sal) if isinstance(base_sal, str) else float(base_sal)
            
        pay_day = int(jour_sal_req or random.choice([27, 28, 29, 30]))
        ref_prefix = "TRF" + "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
        ref_num = "".join(random.choices("0123456789", k=16))
        
        emp_context = {
            "nom": nom_emp,
            "matricule": mat,
            "base_amount": float(base_sal),
            "day": pay_day,
            "ref_prefix": ref_prefix,
            "ref_num": ref_num,
            "is_exact": is_exact
        }
    else:
        emp_context = None

    user_prelevs = runtime_cfg.get("prelevements_selectionnes")
    if user_prelevs and len(user_prelevs) > 0:
        persistent_prelevs = user_prelevs
    elif prof == "locataire":
        persistent_prelevs = ["FREE_MOBILE", "ORANGE", "FITNESS_PARK"]
    elif prof == "demandeur_credit":
        persistent_prelevs = ["EDF", "ORANGE", "MUTUELLE"]
    elif prof == "investisseur":
        persistent_prelevs = ["SYNDIC_FONCIA", "EDF", "MUTUELLE"]
    elif prof == "fonctionnaire":
        persistent_prelevs = ["MGEN", "CASDEN", "EDF"]
    elif prof == "famille":
        persistent_prelevs = ["MAIRIE_SCOLAIRE", "EDF", "MUTUELLE"]
    elif prof == "retraite":
        persistent_prelevs = ["EDF", "MUTUELLE", "ORANGE"]
    elif prof == "artisan":
        persistent_prelevs = ["PRO_BTP", "TOTAL_FLEET", "MUTUELLE"]
    elif prof == "etudiant":
        persistent_prelevs = ["FREE_MOBILE", "SPOTIFY", "FITNESS_PARK"]
    else:
        persistent_prelevs = ["EDF", "FREE_MOBILE", "MUTUELLE"]

    loyer_ctx = None
    custom_loyer_amt = runtime_cfg.get("custom_loyer_montant") or config.get("custom_loyer_montant") or config.get("loyer_montant")
    if custom_loyer_amt:
        loyer_ctx = {
            "montant": parse_currency_french(custom_loyer_amt),
            "bailleur": runtime_cfg.get("custom_loyer_bailleur") or config.get("custom_loyer_bailleur") or config.get("loyer_bailleur") or "BAILLEUR IMMOBILIER"
        }

    target_sf = runtime_cfg.get("target_solde_final")
    if target_sf is not None and str(target_sf).strip():
        target_sf_float = parse_currency_french(target_sf) if isinstance(target_sf, str) else float(target_sf)
    else:
        target_sf_float = None

    custom_contacts = runtime_cfg.get("contacts_virements")
    if custom_contacts and isinstance(custom_contacts, str) and len(custom_contacts.strip()) > 0:
        cleaned_contacts = [c.strip().capitalize() for c in custom_contacts.replace(";", ",").split(",") if c.strip()]
        if cleaned_contacts:
            persistent_contacts_emis = cleaned_contacts
            persistent_contacts_recu = cleaned_contacts
        else:
            persistent_contacts_emis = random.sample(gt.PRENOMS_VIREMENT, min(4, len(gt.PRENOMS_VIREMENT)))
            persistent_contacts_recu = random.sample(gt.PRENOMS_VIREMENT, min(3, len(gt.PRENOMS_VIREMENT)))
    else:
        persistent_contacts_emis = random.sample(gt.PRENOMS_VIREMENT, min(4, len(gt.PRENOMS_VIREMENT)))
        persistent_contacts_recu = random.sample(gt.PRENOMS_VIREMENT, min(3, len(gt.PRENOMS_VIREMENT)))
    has_master_epargne = bool(runtime_cfg.get("has_epargne") or runtime_cfg.get("include_epargne"))
    active_epargne_configs = []
    if has_master_epargne:
        custom_ep_list = runtime_cfg.get("epargne_comptes")
        if custom_ep_list and isinstance(custom_ep_list, list) and len(custom_ep_list) > 0:
            for ep in custom_ep_list:
                if ep.get("enabled", True):
                    init_s = parse_currency_french(ep.get("solde_initial", 5000.0))
                    active_epargne_configs.append({
                        "nom": ep.get("nom") or ep.get("name") or "Livret A",
                        "numero": ep.get("numero") or ep.get("num") or "210 5436798 J",
                        "iban": ep.get("iban", "FR76 1001 1000 2021 0543 6798 J51"),
                        "bic": ep.get("bic", "PSSTFRPPCNE"),
                        "taux": ep.get("taux", "3,00"),
                        "nb_transactions": int(ep.get("nb_transactions", 2)),
                        "current_solde": init_s
                    })
        else:
            active_epargne_configs.append({
                "nom": runtime_cfg.get("livret_a_nom", "Livret A"),
                "numero": runtime_cfg.get("livret_a_numero", "210 5436798 J"),
                "iban": runtime_cfg.get("livret_a_iban", "FR76 1001 1000 2021 0543 6798 J51"),
                "bic": runtime_cfg.get("livret_a_bic", "PSSTFRPPCNE"),
                "taux": runtime_cfg.get("livret_a_taux", "3,00"),
                "nb_transactions": int(runtime_cfg.get("livret_a_nb_transactions", 2)),
                "current_solde": parse_currency_french(runtime_cfg.get("solde_livret_a_initial", 5000.0))
            })
        
    has_epargne_active = bool(len(active_epargne_configs) > 0)

    all_releves_data = []
    
    for idx, (m, y) in enumerate(months_seq):
        mois_str = str(m).zfill(2)
        _, year_4 = gt.get_year_strings(y)
        max_days = gt.get_days_in_month(m, y)
        date_releve = f"{str(max_days).zfill(2)}/{mois_str}/{year_4}"
        date_ancien_solde = f"01/{mois_str}/{year_4}"
        num_releve_val = str(start_num_releve + idx)
        
        solde_ancien_formatted = format_currency_french(current_ccp_solde)
        
        deltas_seq = runtime_cfg.get("target_deltas_sequence")
        if deltas_seq and idx < len(deltas_seq):
            monthly_delta = float(deltas_seq[idx])
        elif target_sf_float is not None:
            remaining_months = len(months_seq) - idx
            if remaining_months <= 1:
                monthly_delta = round(target_sf_float - current_ccp_solde, 2)
            else:
                base_needed = (target_sf_float - current_ccp_solde) / remaining_months
                variance = round(random.uniform(-30.0, 30.0), 2)
                monthly_delta = round(base_needed + variance, 2)
        else:
            if runtime_cfg.get("dossier_type") == "credit_immo":
                monthly_delta = round(random.uniform(150.0, 650.0), 2)
            elif w == "riche":
                monthly_delta = round(random.uniform(-400.0, 1200.0), 2)
            elif w == "pauvre":
                monthly_delta = round(random.uniform(-150.0, 200.0), 2)
            else:
                monthly_delta = round(random.uniform(-250.0, 500.0), 2)
                
        nb_tx = max(18, int(runtime_cfg.get("nb_transactions", random.randint(18, 30))))
        
        txs_ccp = gt.generate_random_txs(
            num_tx=nb_tx,
            city=runtime_cfg["titulaire_ville"],
            month=m,
            year=y,
            is_epargne=False,
            profile=runtime_cfg["profil"],
            wealth_profile=runtime_cfg["wealth_profile"],
            age_profile=runtime_cfg["age_profile"],
            titulaire_nom=runtime_cfg["titulaire_nom"],
            card_number=runtime_cfg["card_number"],
            cp=runtime_cfg["titulaire_cp"],
            titulaire_sexe=runtime_cfg["titulaire_sexe"],
            dest_iban=None,
            target_delta=monthly_delta,
            solde_ancien=solde_ancien_formatted,
            bank_type=runtime_cfg.get("bank_type", "lbp"),
            allow_epargne=has_epargne_active,
            contacts_emis=persistent_contacts_emis,
            contacts_recu=persistent_contacts_recu
        )
        
        # Injection du salaire persistant pour remplacer le salaire aléatoire
        if emp_context:
            for t in txs_ccp:
                if 'SALAIRE' in str(t.get('lignes', '')).upper() or 'PAYE' in str(t.get('lignes', '')).upper():
                    pers_sal = gt.generate_salaire(m, y, wealth_profile=w, city=runtime_cfg["titulaire_ville"], custom_employeur=emp_context)
                    t['lignes'] = pers_sal['lignes']
                    t['date'] = pers_sal['date']
                    t['montant'] = pers_sal['montant']
                    t['amount'] = pers_sal['amount']
                    if emp_context.get("is_exact"):
                        t['is_protected'] = True
                    break
                    
        # Persistance stricte des prélèvements d'un mois sur l'autre
        current_prelevs = [t for t in txs_ccp if t.get('type') == 'PRELEVEMENT']
        if persistent_prelevs:
            for idx_p, p_type in enumerate(persistent_prelevs):
                if idx_p < len(current_prelevs):
                    p_tx = gt.generate_prelevement(p_type, m, year=y, wealth_profile=w)
                    current_prelevs[idx_p]['lignes'] = p_tx['lignes']
                    current_prelevs[idx_p]['date'] = p_tx['date']
                    current_prelevs[idx_p]['montant'] = p_tx['montant']
                    current_prelevs[idx_p]['amount'] = p_tx['amount']
                    
        txs_ccp = [t for t in txs_ccp if not any(k in str(t.get('lignes', '')).upper() for k in ['VERS COMPTE EPARGNE', 'VERS LIVRET', 'VERS PEL'])]
        
        comptes_epargne_output = []
        if active_epargne_configs:
            for ep_cfg in active_epargne_configs:
                ep_solde_ancien = format_currency_french(ep_cfg["current_solde"])
                txs_ep = []
                nb_vir_ep = ep_cfg["nb_transactions"]
                livret_nom_str = ep_cfg["nom"]
                
                if nb_vir_ep > 0:
                    delta_ep1 = round(random.uniform(50.0, 150.0), 2) if runtime_cfg["wealth_profile"] != "pauvre" else 20.0
                    txs_ccp.append({
                        "date": f"05/{mois_str}",
                        "lignes": [f"VIREMENT EMIS VERS {livret_nom_str.upper()}", f"EN DATE DU 05/{mois_str}"],
                        "montant": format_currency_french(delta_ep1),
                        "signe": "-",
                        "amount": delta_ep1,
                        "type": "VIREMENT EMIS",
                        "is_protected": True,
                        "is_mirror": True
                    })
                    txs_ep.append({
                        "date": f"05/{mois_str}",
                        "lignes": [f"VIREMENT VERS {livret_nom_str.upper()}", f"DE CCP {runtime_cfg['account_num']}"],
                        "montant": format_currency_french(delta_ep1),
                        "signe": "+",
                        "amount": delta_ep1,
                        "type": "VIREMENT",
                        "is_protected": True,
                        "is_mirror": True
                    })
                    ep_cfg["current_solde"] = round(ep_cfg["current_solde"] + delta_ep1, 2)
                    
                    if nb_vir_ep >= 2:
                        delta_ep2 = round(random.uniform(40.0, 100.0), 2) if runtime_cfg["wealth_profile"] != "pauvre" else 15.0
                        txs_ccp.append({
                            "date": f"20/{mois_str}",
                            "lignes": [f"VIREMENT EMIS VERS {livret_nom_str.upper()}", f"EN DATE DU 20/{mois_str}"],
                            "montant": format_currency_french(delta_ep2),
                            "signe": "-",
                            "amount": delta_ep2,
                            "type": "VIREMENT EMIS",
                            "is_protected": True,
                            "is_mirror": True
                        })
                        txs_ep.append({
                            "date": f"20/{mois_str}",
                            "lignes": [f"VIREMENT VERS {livret_nom_str.upper()}", f"DE CCP {runtime_cfg['account_num']}"],
                            "montant": format_currency_french(delta_ep2),
                            "signe": "+",
                            "amount": delta_ep2,
                            "type": "VIREMENT",
                            "is_protected": True,
                            "is_mirror": True
                        })
                        ep_cfg["current_solde"] = round(ep_cfg["current_solde"] + delta_ep2, 2)
                        
                if int(m) == 12:
                    taux_str = str(ep_cfg["taux"]).replace(",", ".")
                    try:
                        taux_f = float(taux_str)
                        if taux_f > 0.5:
                            taux_f /= 100.0
                    except Exception:
                        taux_f = 0.03
                    interets_annuels = round(max(0.50, ep_cfg["current_solde"] * taux_f), 2)
                    txs_ep.append({
                        "date": f"31/{mois_str}",
                        "lignes": [f"INTERETS ACQUIS AU 31/12/{year_4}"],
                        "montant": format_currency_french(interets_annuels),
                        "signe": "+",
                        "amount": interets_annuels,
                        "type": "INTERETS"
                    })
                    ep_cfg["current_solde"] = round(ep_cfg["current_solde"] + interets_annuels, 2)
                    
                txs_ep.sort(key=gt.get_tx_date_sort_key)
                comptes_epargne_output.append({
                    "type": "epargne",
                    "name": ep_cfg["nom"],
                    "num": ep_cfg["numero"],
                    "iban": ep_cfg["iban"],
                    "bic": ep_cfg["bic"],
                    "txs": txs_ep,
                    "solde_anc": ep_solde_ancien,
                    "solde_nouv": format_currency_french(ep_cfg["current_solde"]),
                    "solde": format_currency_french(ep_cfg["current_solde"])
                })

        if loyer_ctx:
            loyer_day = random.randint(1, 5)
            loyer_date = f"{str(loyer_day).zfill(2)}/{mois_str}"
            loyer_amt = loyer_ctx["montant"]
            loyer_bailleur = loyer_ctx["bailleur"]
            existing_loyer = next((t for t in txs_ccp if 'LOYER' in str(t.get('lignes', '')).upper() or 'BAILLEUR' in str(t.get('lignes', '')).upper()), None)
            loyer_tx = {
                "date": loyer_date,
                "lignes": [f"PRELEVEMENT DE {loyer_bailleur}", f"LOYER {mois_str}/{year_4}"],
                "montant": format_currency_french(loyer_amt),
                "signe": "-",
                "amount": loyer_amt,
                "type": "PRELEVEMENT",
                "is_protected": True
            }
            if existing_loyer:
                existing_loyer['lignes'] = loyer_tx['lignes']
                existing_loyer['date'] = loyer_tx['date']
                existing_loyer['montant'] = loyer_tx['montant']
                existing_loyer['amount'] = loyer_tx['amount']
            else:
                txs_ccp.append(loyer_tx)

        txs_ccp = gt.calibrate_transactions_to_delta(txs_ccp, monthly_delta, city=runtime_cfg["titulaire_ville"], month=str(m), year=str(y))
        
        custom_user_txs = runtime_cfg.get("custom_transactions") or []
        for ctx in custom_user_txs:
            if not ctx: 
                continue
            is_all = ctx.get("all_months") is True or str(ctx.get("all_months")).lower() in ("true", "all", "1")
            try:
                target_month = int(ctx.get("month", m))
            except Exception:
                target_month = m
                
            if is_all or target_month == m:
                raw_amt = ctx.get("montant") if ctx.get("montant") is not None else ctx.get("amount", 0)
                amt_float = parse_currency_french(raw_amt) if isinstance(raw_amt, str) else float(raw_amt)
                amt_float = abs(amt_float)
                sign = "+" if str(ctx.get("signe", "-")).strip() == "+" else "-"
                
                raw_date = str(ctx.get("date", "15")).strip()
                if "/" in raw_date:
                    day_part = raw_date.split("/")[0].strip()
                else:
                    day_part = raw_date.strip()
                if not day_part.isdigit():
                    day_part = "15"
                day_int = max(1, min(max_days, int(day_part)))
                date_val = f"{str(day_int).zfill(2)}/{mois_str}"
                
                lib = ctx.get("libelle") or ctx.get("label") or "OPERATION SUR MESURE"
                if isinstance(lib, list):
                    lignes_raw = [str(l).strip() for l in lib if str(l).strip()]
                else:
                    lignes_raw = [str(l).strip() for l in str(lib).split("\n") if str(l).strip()]
                if not lignes_raw:
                    lignes_raw = ["OPERATION SUR MESURE"]
                    
                tx_type = ctx.get("type") or ("VIREMENT" if sign == "+" else "ACHAT CB")
                
                new_custom_tx = {
                    "date": date_val,
                    "lignes": lignes_raw,
                    "montant": format_currency_french(amt_float),
                    "signe": sign,
                    "amount": amt_float,
                    "type": tx_type,
                    "is_protected": True
                }
                if sign == "+":
                    new_custom_tx["credit"] = format_currency_french(amt_float)
                    new_custom_tx["debit"] = None
                else:
                    new_custom_tx["debit"] = format_currency_french(amt_float)
                    new_custom_tx["credit"] = None
                    
                txs_ccp.append(new_custom_tx)

        injected = runtime_cfg.get("injected_transactions_per_month", {}).get(m)
        if injected:
            txs_ccp.extend(injected)
            
        if (target_sf_float is not None) or (deltas_seq and idx < len(deltas_seq)):
            txs_ccp = gt.calibrate_transactions_to_delta(
                txs_ccp,
                monthly_delta,
                city=runtime_cfg["titulaire_ville"],
                month=str(m),
                year=str(y),
                wealth_profile=runtime_cfg["wealth_profile"]
            )
            
        txs_ccp.sort(key=gt.get_tx_date_sort_key)
            
        final_delta = sum(gt.get_tx_delta(t) for t in txs_ccp)
        new_ccp_solde = round(current_ccp_solde + final_delta, 2)
        solde_nouveau_formatted = format_currency_french(new_ccp_solde)
        
        date_edition_val = runtime_cfg.get("date_edition_custom")
        if not date_edition_val:
            next_m = m + 1 if m < 12 else 1
            next_y = y if m < 12 else y + 1
            _, next_y4 = gt.get_year_strings(next_y)
            month_names_fr = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
            date_edition_val = f"03 {month_names_fr[next_m - 1]} {next_y4}"

        releve_data = {
            "num_releve": num_releve_val,
            "releve_mois": m,
            "releve_annee": y,
            "date_releve": date_releve,
            "date_ancien_solde": date_ancien_solde,
            "date_nouveau_solde": date_releve,
            "date_edition": date_edition_val,
            "nom": runtime_cfg.get("nom", ""),
            "prenom": runtime_cfg.get("prenom", ""),
            "nom_prenom": runtime_cfg.get("nom_prenom", ""),
            "titulaire_nom": runtime_cfg["titulaire_nom"],
            "titulaire_nom_complet": runtime_cfg.get("titulaire_nom_complet", runtime_cfg["titulaire_nom"]),
            "titulaire_adresse1": runtime_cfg.get("complement_adresse", ""),
            "titulaire_adresse2": runtime_cfg["titulaire_adresse"],
            "titulaire_cp": runtime_cfg["titulaire_cp"],
            "titulaire_ville": runtime_cfg["titulaire_ville"],
            "titulaire_cp_ville": f"{runtime_cfg['titulaire_cp']} {runtime_cfg['titulaire_ville']}".strip(),
            "centre_financier": runtime_cfg.get("centre_financier", "PARIS CENTRE FINANCIER"),
            "identifiant": runtime_cfg["identifiant"],
            "iban": runtime_cfg["iban"],
            "bic": runtime_cfg.get("bic", "PSSTFRPPPAR"),
            "card_number": runtime_cfg.get("card_number", "456"),
            "ccp_account_num": runtime_cfg["account_num"],
            "ccp_numero": runtime_cfg["account_num"],
            "ccp_iban": runtime_cfg["iban"],
            "ccp_bic": runtime_cfg.get("bic", "PSSTFRPPPAR"),
            "ccp_solde_ancien": solde_ancien_formatted,
            "ccp_solde": solde_nouveau_formatted,
            "ccp_decouvert_autorise": runtime_cfg.get("decouvert_autorise", "300,00"),
            "afficher_ccp": runtime_cfg.get("afficher_ccp", True),
            "afficher_livret_a": has_epargne_active,
            "afficher_epargne": has_epargne_active,
            "has_epargne": has_epargne_active,
            "show_situation_livret_a": has_epargne_active,
            "show_tx_livret_a": has_epargne_active,
            "show_tx_decouvert_ccp": True,
            "transactions_ccp": txs_ccp,
            "show_annexe_carbone": bool(runtime_cfg.get("show_annexe_carbone", True)),
            "auto_fill_info_block": runtime_cfg.get("annexe_info_type", "auto") == "auto",
            "annexe_info_type": runtime_cfg.get("annexe_info_type", "auto"),
            "annexe_info_custom_text": runtime_cfg.get("annexe_info_custom_text", ""),
            "comptes_epargne_list": comptes_epargne_output
        }
        
        if comptes_epargne_output:
            first_ep = comptes_epargne_output[0]
            releve_data["livret_a_nom"] = first_ep["name"]
            releve_data["livret_a_numero"] = first_ep["num"]
            releve_data["livret_a_iban"] = first_ep["iban"]
            releve_data["livret_a_bic"] = first_ep["bic"]
            releve_data["livret_a_solde_ancien"] = first_ep["solde_anc"]
            releve_data["livret_a_solde"] = first_ep["solde_nouv"]
            releve_data["transactions_livret_a"] = first_ep["txs"]
            
        all_releves_data.append(releve_data)
        current_ccp_solde = new_ccp_solde
        
    return all_releves_data

# ==========================================
