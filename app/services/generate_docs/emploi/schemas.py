from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# ----------------------------------------------------------------------


class FicheDePaieGenerateRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    duree_mois: int = Field(1, ge=1, le=24)
    mois_debut: Optional[int] = Field(None, ge=1, le=12)
    annee_debut: Optional[int] = Field(None, ge=1900, le=2100)
    mode: Optional[str] = "facile"

    raison_sociale: Optional[str] = None
    adresse: Optional[str] = None
    code_postal: Optional[str] = None
    ville: Optional[str] = None
    siret: Optional[str] = None
    code_naf: Optional[str] = None
    etablissement: Optional[str] = None
    convention_collective: Optional[str] = None
    convention_collective_court: Optional[str] = None

    civilite: Optional[str] = "M."
    nom: Optional[str] = None
    prenom: Optional[str] = None
    nom_complet: Optional[str] = None
    salarie_adresse: Optional[str] = None
    salarie_cp: Optional[str] = None
    salarie_ville: Optional[str] = None
    nir: Optional[str] = None
    matricule: Optional[str] = None
    emploi: Optional[str] = None
    qualification: Optional[str] = None
    echelon: Optional[str] = None
    coefficient: Optional[str] = None
    date_anciennete: Optional[str] = None

    net_a_payer_cible: Optional[str] = None
    salaire_base: Optional[str] = None
    heures_mensuelles: Optional[str] = None
    prime_habillage: Optional[str] = None
    frais_professionnels: Optional[str] = None
    mutuelle_salarie: Optional[str] = None
    mutuelle_patronale: Optional[str] = None
    allegement_cotisations: Optional[str] = None
    taux_pas: Optional[str] = None

    cp_n1_du: Optional[float] = None
    cp_n1_pris: Optional[float] = None
    cp_n1_reste: Optional[float] = None
    cp_n_du: Optional[float] = None
    cp_n_pris: Optional[float] = None
    cp_n_reste: Optional[float] = None
    repos_compensateur_du: Optional[float] = None
    repos_compensateur_pris: Optional[float] = None
    repos_compensateur_reste: Optional[float] = None

    date_debut: Optional[str] = None
    date_fin: Optional[str] = None
    date_paiement: Optional[str] = None
    mode_paiement: Optional[str] = None
    plafond_mensuel_ss: Optional[float] = None

    header: Optional[bool] = True
    header_employeur: Optional[bool] = True
    header_titre: Optional[bool] = True
    header_periode: Optional[bool] = True
    header_salarie: Optional[bool] = True
    header_convention: Optional[bool] = True
    middle: Optional[bool] = True
    middle_tableau_cotisations: Optional[bool] = True
    middle_net_avant_impot: Optional[bool] = True
    middle_impot_source: Optional[bool] = True
    footer: Optional[bool] = True
    footer_conges: Optional[bool] = True
    footer_cumuls: Optional[bool] = True
    footer_recapitulatif: Optional[bool] = True
    footer_mentions: Optional[bool] = True
