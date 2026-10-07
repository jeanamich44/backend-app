from dataclasses import dataclass, field

from . import rules
from .services.calculs import calculate_payroll
from .services.informations import DEFAULTS_TABLE, get_default_table, get_pmss_for_date

# ----------------------------------------------------------------------


@dataclass
class EmployeurData:
    raison_sociale: str = DEFAULTS_TABLE["employeur"]["raison_sociale"]
    adresse: str = DEFAULTS_TABLE["employeur"]["adresse"]
    code_postal: str = DEFAULTS_TABLE["employeur"]["code_postal"]
    ville: str = DEFAULTS_TABLE["employeur"]["ville"]
    siret: str = DEFAULTS_TABLE["employeur"]["siret"]
    siren: str = DEFAULTS_TABLE["employeur"]["siren"]
    code_naf: str = DEFAULTS_TABLE["employeur"]["code_naf"]
    etablissement: str = DEFAULTS_TABLE["employeur"]["etablissement"]
    convention_collective: str = DEFAULTS_TABLE["employeur"]["convention_collective"]
    convention_collective_court: str = DEFAULTS_TABLE["employeur"]["convention_collective_court"]
    convention_idcc: str = DEFAULTS_TABLE["employeur"]["convention_idcc"]


@dataclass
class SalarieData:
    civilite: str = DEFAULTS_TABLE["salarie"]["civilite"]
    nom: str = DEFAULTS_TABLE["salarie"]["nom"]
    prenom: str = DEFAULTS_TABLE["salarie"]["prenom"]
    nom_complet: str = DEFAULTS_TABLE["salarie"]["nom_complet"]
    adresse: str = DEFAULTS_TABLE["salarie"]["adresse"]
    code_postal: str = DEFAULTS_TABLE["salarie"]["code_postal"]
    ville: str = DEFAULTS_TABLE["salarie"]["ville"]
    nir: str = DEFAULTS_TABLE["salarie"]["nir"]
    matricule: str = DEFAULTS_TABLE["salarie"]["matricule"]
    emploi: str = DEFAULTS_TABLE["salarie"]["emploi"]
    qualification: str = DEFAULTS_TABLE["salarie"]["qualification"]
    echelon: str = DEFAULTS_TABLE["salarie"]["echelon"]
    coefficient: str = DEFAULTS_TABLE["salarie"]["coefficient"]
    date_anciennete: str = DEFAULTS_TABLE["salarie"]["date_anciennete"]


@dataclass
class PeriodeData:
    date_debut: str = DEFAULTS_TABLE["periode"]["date_debut"]
    date_fin: str = DEFAULTS_TABLE["periode"]["date_fin"]
    periode_libelle: str = DEFAULTS_TABLE["periode"]["periode_libelle"]
    date_paiement: str = DEFAULTS_TABLE["periode"]["date_paiement"]
    mode_paiement: str = DEFAULTS_TABLE["periode"]["mode_paiement"]
    plafond_mensuel_ss: float = DEFAULTS_TABLE["periode"]["plafond_mensuel_ss"]


@dataclass
class CongesData:
    cp_n1_du: float = DEFAULTS_TABLE["conges"]["cp_n1_du"]
    cp_n1_pris: float = DEFAULTS_TABLE["conges"]["cp_n1_pris"]
    cp_n1_reste: float = DEFAULTS_TABLE["conges"]["cp_n1_reste"]
    cp_n_du: float = DEFAULTS_TABLE["conges"]["cp_n_du"]
    cp_n_pris: float = DEFAULTS_TABLE["conges"]["cp_n_pris"]
    cp_n_reste: float = DEFAULTS_TABLE["conges"]["cp_n_reste"]
    repos_compensateur_du: float = DEFAULTS_TABLE["conges"]["repos_compensateur_du"]
    repos_compensateur_pris: float = DEFAULTS_TABLE["conges"]["repos_compensateur_pris"]
    repos_compensateur_reste: float = DEFAULTS_TABLE["conges"]["repos_compensateur_reste"]


@dataclass
class VisibleData:
    header: bool = True
    header_employeur: bool = True
    header_titre: bool = True
    header_periode: bool = True
    header_salarie: bool = True
    header_convention: bool = True

    middle: bool = True
    middle_tableau_cotisations: bool = True
    middle_net_avant_impot: bool = True
    middle_impot_source: bool = True

    footer: bool = True
    footer_conges: bool = True
    footer_cumuls: bool = True
    footer_recapitulatif: bool = True
    footer_mentions: bool = True


@dataclass
class Doc:
    employeur: EmployeurData = field(default_factory=EmployeurData)
    salarie: SalarieData = field(default_factory=SalarieData)
    periode: PeriodeData = field(default_factory=PeriodeData)
    conges: CongesData = field(default_factory=CongesData)
    calculs: dict = field(default_factory=calculate_payroll)
    visible: VisibleData = field(default_factory=VisibleData)


def from_payload(payload: dict | None = None) -> Doc:
    p = rules.apply_payload(payload)
    doc = Doc()
    if not payload:
        return rules.apply_doc(doc)

    for f in (
        "header", "header_employeur", "header_titre", "header_periode", "header_salarie", "header_convention",
        "middle", "middle_tableau_cotisations", "middle_net_avant_impot", "middle_impot_source",
        "footer", "footer_conges", "footer_cumuls", "footer_recapitulatif", "footer_mentions",
    ):
        if f in p:
            setattr(doc.visible, f, bool(p[f]))

    for field_name in ("raison_sociale", "adresse", "code_postal", "ville", "siret", "code_naf", "etablissement", "convention_collective", "convention_collective_court", "convention_idcc"):
        if field_name in p:
            setattr(doc.employeur, field_name, p[field_name])

    for field_name in ("civilite", "nom", "prenom", "nom_complet", "nir", "matricule", "emploi", "qualification", "echelon", "coefficient", "date_anciennete"):
        if field_name in p:
            setattr(doc.salarie, field_name, p[field_name])
    if "salarie_adresse" in p:
        doc.salarie.adresse = p["salarie_adresse"]
    elif "adresse_salarie" in p:
        doc.salarie.adresse = p["adresse_salarie"]
    if "salarie_cp" in p:
        doc.salarie.code_postal = p["salarie_cp"]
    if "salarie_ville" in p:
        doc.salarie.ville = p["salarie_ville"]
    if ("nom" in p or "prenom" in p) and "nom_complet" not in p:
        doc.salarie.nom_complet = f"{doc.salarie.nom} {doc.salarie.prenom}".strip().upper()

    for field_name in ("date_debut", "date_fin", "date_paiement", "mode_paiement"):
        if field_name in p:
            setattr(doc.periode, field_name, p[field_name])
    if "plafond_mensuel_ss" in p and p["plafond_mensuel_ss"] not in (None, ""):
        try:
            val_p = float(str(p["plafond_mensuel_ss"]).replace(",", "."))
            exp_p = get_pmss_for_date(p)
            if val_p not in (3428.00, 3666.00, 3864.00, 3925.00, 4005.00) or val_p == exp_p:
                doc.periode.plafond_mensuel_ss = val_p
            else:
                doc.periode.plafond_mensuel_ss = exp_p
        except (ValueError, TypeError):
            doc.periode.plafond_mensuel_ss = get_pmss_for_date(p)
    else:
        doc.periode.plafond_mensuel_ss = get_pmss_for_date(p)
    p["plafond_mensuel_ss"] = doc.periode.plafond_mensuel_ss
    if "date_debut" in p and "date_fin" in p:
        doc.periode.periode_libelle = f"du {doc.periode.date_debut} au {doc.periode.date_fin}"

    for field_name in ("cp_n1_du", "cp_n1_pris", "cp_n1_reste", "cp_n_du", "cp_n_pris", "cp_n_reste", "repos_compensateur_du", "repos_compensateur_pris", "repos_compensateur_reste"):
        if field_name in p:
            try:
                setattr(doc.conges, field_name, float(str(p[field_name]).replace(",", ".")))
            except (ValueError, TypeError):
                pass

    doc.calculs = calculate_payroll(p)
    return rules.apply_doc(doc)
