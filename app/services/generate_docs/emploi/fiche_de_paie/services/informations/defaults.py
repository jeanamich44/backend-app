import calendar
from datetime import datetime

# ----------------------------------------------------------------------

PMSS_PALIERS = {
    "2020-01-01": 3428.00,
    "2021-01-01": 3428.00,
    "2022-01-01": 3428.00,
    "2023-01-01": 3666.00,
    "2024-01-01": 3864.00,
    "2025-01-01": 3925.00,
    "2026-01-01": 4005.00,
}

TAUX_VIEILLESSE_DEPLAFONNEE_PATRONALE_PALIERS = {
    "2020-01-01": 0.0190,
    "2024-01-01": 0.0202,
    "2026-01-01": 0.0211,
}

TAUX_AGIRC_T1_SALARIALE_PALIERS = {
    "2018-01-01": 0.0390,
    "2019-01-01": 0.0401,
}

TAUX_AGIRC_T1_PATRONALE_PALIERS = {
    "2018-01-01": 0.0585,
    "2019-01-01": 0.0601,
}

# ----------------------------------------------------------------------


def extract_date_iso(params: dict | None = None) -> str:
    p = params or {}
    for k in ("date_debut", "date_fin", "date_paiement"):
        val = p.get(k)
        if val and isinstance(val, str):
            clean = val.replace("le ", "").strip()
            parts = clean.split("/")
            if len(parts) == 3:
                try:
                    d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
                    if 1900 <= y <= 2100 and 1 <= m <= 12 and 1 <= d <= 31:
                        return f"{y:04d}-{m:02d}-{d:02d}"
                except (ValueError, TypeError):
                    pass
    for k_y in ("annee", "annee_debut", "start_year"):
        if k_y in p and p[k_y]:
            try:
                y = int(p[k_y])
                m = 1
                for k_m in ("mois", "mois_debut", "start_month"):
                    if k_m in p and p[k_m]:
                        try:
                            m = int(p[k_m])
                            break
                        except (ValueError, TypeError):
                            pass
                return f"{y:04d}-{m:02d}-01"
            except (ValueError, TypeError):
                pass
    today = datetime.now()
    return f"{today.year:04d}-{today.month:02d}-01"


def resolve_palier(paliers: dict[str, float], date_iso: str) -> float:
    selected = None
    for k in sorted(paliers.keys()):
        if date_iso >= k:
            selected = paliers[k]
        elif selected is None:
            selected = paliers[k]
            break
    if selected is None:
        first_key = sorted(paliers.keys())[0]
        selected = paliers[first_key]
    return selected


def get_pmss_for_date(params_or_date: dict | str | None = None) -> float:
    if isinstance(params_or_date, str):
        date_iso = extract_date_iso({"date_debut": params_or_date})
    elif isinstance(params_or_date, dict):
        date_iso = extract_date_iso(params_or_date)
    else:
        date_iso = extract_date_iso({})
    return resolve_palier(PMSS_PALIERS, date_iso)


def get_taux_vieillesse_deplafonnée_patronale_for_date(params_or_date: dict | str | None = None) -> float:
    if isinstance(params_or_date, str):
        date_iso = extract_date_iso({"date_debut": params_or_date})
    elif isinstance(params_or_date, dict):
        date_iso = extract_date_iso(params_or_date)
    else:
        date_iso = extract_date_iso({})
    return resolve_palier(TAUX_VIEILLESSE_DEPLAFONNEE_PATRONALE_PALIERS, date_iso)


def get_taux_agirc_t1_salariale_for_date(params_or_date: dict | str | None = None) -> float:
    if isinstance(params_or_date, str):
        date_iso = extract_date_iso({"date_debut": params_or_date})
    elif isinstance(params_or_date, dict):
        date_iso = extract_date_iso(params_or_date)
    else:
        date_iso = extract_date_iso({})
    return resolve_palier(TAUX_AGIRC_T1_SALARIALE_PALIERS, date_iso)


def get_taux_agirc_t1_patronale_for_date(params_or_date: dict | str | None = None) -> float:
    if isinstance(params_or_date, str):
        date_iso = extract_date_iso({"date_debut": params_or_date})
    elif isinstance(params_or_date, dict):
        date_iso = extract_date_iso(params_or_date)
    else:
        date_iso = extract_date_iso({})
    return resolve_palier(TAUX_AGIRC_T1_PATRONALE_PALIERS, date_iso)

# ----------------------------------------------------------------------


def get_previous_month_dates(ref_date: datetime | None = None) -> dict:
    today = ref_date or datetime.now()
    year = today.year
    month = today.month - 1
    if month == 0:
        month = 12
        year -= 1

    _, last_day = calendar.monthrange(year, month)

    date_debut_str = f"01/{month:02d}/{year}"
    date_fin_str = f"{last_day:02d}/{month:02d}/{year}"
    periode_str = f"du {date_debut_str} au {date_fin_str}"
    date_paiement_str = f"le {date_fin_str}"

    return {
        "mois": month,
        "annee": year,
        "nb_jours": last_day,
        "date_debut": date_debut_str,
        "date_fin": date_fin_str,
        "periode_libelle": periode_str,
        "date_paiement": date_paiement_str,
    }


def get_default_table(ref_date: datetime | None = None) -> dict:
    dates = get_previous_month_dates(ref_date)
    d_iso = f"{dates['annee']:04d}-{dates['mois']:02d}-01"
    pmss_default = resolve_palier(PMSS_PALIERS, d_iso)
    taux_ret_deplaf_default = resolve_palier(TAUX_VIEILLESSE_DEPLAFONNEE_PATRONALE_PALIERS, d_iso)
    taux_agirc_sal_default = resolve_palier(TAUX_AGIRC_T1_SALARIALE_PALIERS, d_iso)
    taux_agirc_pat_default = resolve_palier(TAUX_AGIRC_T1_PATRONALE_PALIERS, d_iso)

    return {
        "employeur": {
            "raison_sociale": "GROUPE EUROPE HANDLING",
            "adresse": "3 RUE DU REMBLAI",
            "code_postal": "93290",
            "ville": "TREMBLAY-EN-FRANCE",
            "siret": "40114427400040",
            "siren": "401144274",
            "code_naf": "5223Z",
            "etablissement": "Siège social",
            "convention_collective": "Convention collective nationale du personnel au sol des entreprises de transport aérien",
            "convention_collective_court": "PERSONNEL AU SOL DU TRANSPORT AERIEN",
            "convention_idcc": "0275",
        },
        "salarie": {
            "civilite": "M.",
            "nom": "MARTIN",
            "prenom": "Lucas",
            "nom_complet": "MARTIN LUCAS",
            "adresse": "12 RUE DES FLEURS",
            "code_postal": "75011",
            "ville": "PARIS",
            "nir": "1950475111001",
            "matricule": "05984",
            "emploi": "SUPERVISEUR COMMERCIAL",
            "qualification": "EMPLOYE",
            "echelon": "2",
            "coefficient": "215",
            "date_anciennete": "18 mars 2023",
        },
        "periode": {
            "date_debut": dates["date_debut"],
            "date_fin": dates["date_fin"],
            "periode_libelle": dates["periode_libelle"],
            "date_paiement": dates["date_paiement"],
            "mode_paiement": "Virement",
            "plafond_mensuel_ss": pmss_default,
        },
        "remuneration": {
            "net_a_payer_cible": 2460.00,
            "heures_mensuelles": 151.67,
            "prime_habillage": 210.42,
            "frais_professionnels": 94.00,
            "taux_pas": 5.00,
            "mutuelle_salarie": 33.59,
            "mutuelle_patronale": 64.45,
            "allegement_cotisations": 63.15,
            "taux_cotisations": {
                "maladie_ss_patronale": 0.1300,
                "accident_travail_patronale": 0.0100,
                "retraite_plafonnee_salariale": 0.0690,
                "retraite_plafonnee_patronale": 0.0855,
                "retraite_deplafonnee_salariale": 0.0040,
                "retraite_deplafonnee_patronale": taux_ret_deplaf_default,
                "agirc_t1_salariale": taux_agirc_sal_default,
                "agirc_t1_patronale": taux_agirc_pat_default,
                "famille_patronale": 0.0345,
                "chomage_patronale": 0.0420,
                "autres_contributions_patronale": 0.0550,
                "csg_deductible_salariale": 0.0680,
                "csg_crds_nondeductible_salariale": 0.0290,
                "assiette_csg_taux": 0.9825,
            },
        },
        "conges": {
            "cp_n1_du": 30.00,
            "cp_n1_pris": 5.00,
            "cp_n1_reste": 25.00,
            "cp_n_du": 10.00,
            "cp_n_pris": 0.00,
            "cp_n_reste": 10.00,
            "repos_compensateur_du": 0.00,
            "repos_compensateur_pris": 0.00,
            "repos_compensateur_reste": 0.00,
        },
        "mentions": {
            "conservation": "Dans votre intérêt, conservez ce bulletin sans limitation de durée.",
            "service_public": "Pour la définition des termes employés, se reporter au site internet servicepublic.fr rubrique cotisations sociales",
            "copyright": "©Sage",
        },
    }


DEFAULTS_TABLE = get_default_table()
