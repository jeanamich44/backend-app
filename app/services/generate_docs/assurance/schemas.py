from typing import Optional
from pydantic import BaseModel, ConfigDict


class AssuranceGenerateRequest(BaseModel):
    model_config = ConfigDict(extra="allow")
    num_client: Optional[str] = None
    num_contrat: Optional[str] = None
    num_orias: Optional[str] = None
    titulaire: Optional[str] = None
    civilite: Optional[str] = None
    nom: Optional[str] = None
    prenom: Optional[str] = None
    adresse: Optional[str] = None
    cp: Optional[str] = None
    ville: Optional[str] = None
    cp_ville: Optional[str] = None
    pays: Optional[str] = None
    date_delivrance: Optional[str] = None
    date_effet: Optional[str] = None
    date_effet_jour: Optional[str] = None
    date_effet_mois: Optional[str] = None
    date_effet_annee: Optional[str] = None
    immatriculation: Optional[str] = None
    vehicule_marque_modele: Optional[str] = None
    courtier: Optional[str] = None
    destinataire_l1: Optional[str] = None
    destinataire_l2: Optional[str] = None
    destinataire_l3: Optional[str] = None
    edition_date: Optional[str] = None
    info_client: Optional[str] = None
    info_contrat: Optional[str] = None
    info_effet: Optional[str] = None
    vehicule_marque: Optional[str] = None
    vehicule_immat: Optional[str] = None
    assureur_nom: Optional[str] = None
    assureur_adresse: Optional[str] = None
    visible: Optional[dict] = None
    header: Optional[bool] = None
    header_logo: Optional[bool] = None
    header_identity: Optional[bool] = None
    header_banner: Optional[bool] = None
    middle: Optional[bool] = None
    footer: Optional[bool] = None


AssuranceMaxanceGenerateRequest = AssuranceGenerateRequest
AssuranceAxaGenerateRequest = AssuranceGenerateRequest

