from typing import Optional

from pydantic import BaseModel, ConfigDict


class ExtraAllow(BaseModel):
    model_config = ConfigDict(extra="allow")


class ConduiteRdv(ExtraAllow):
    jour: Optional[str] = None
    date: Optional[str] = None
    debut: Optional[str] = None
    fin: Optional[str] = None
    activite: Optional[str] = None
    commentaire: Optional[str] = None


class JustificatifConduiteHeuresRequest(ExtraAllow):
    nom: Optional[str] = "MARTIN"
    prenom: Optional[str] = "LUCAS"
    num_eleve: Optional[str] = "1001"
    eleve: Optional[str] = None
    edition_date: Optional[str] = None
    edition_time: Optional[str] = None
    edition: Optional[str] = None
    rdvs: Optional[list[ConduiteRdv]] = None


class JustificatifAttestationEdfRequest(ExtraAllow):
    civilite: Optional[str] = "Mr."
    nom: Optional[str] = "MARTIN"
    prenom: Optional[str] = "LUCAS"
    adresse: Optional[str] = "12 RUE DES FLEURS"
    ville: Optional[str] = "PARIS"
    cp: Optional[str] = "75011"
    num_client: Optional[str] = "6 013 159 667"
    num_compte: Optional[str] = "4 02 4 024 8 51 258"
    pdl: Optional[str] = "07334145884965"
    puissance: Optional[str] = "06"
    date: Optional[str] = None
    email: Optional[str] = "serviceclient@edf.fr"
    conseillere: Optional[str] = "Marie"
    footer_cachet: Optional[bool] = False


class JustificatifAttestationDirectEnergieRequest(ExtraAllow):
    civilite: Optional[str] = "M."
    nom: Optional[str] = "Martin"
    prenom: Optional[str] = "Lucas"
    adresse: Optional[str] = "12 Rue des Fleurs"
    cp: Optional[str] = "75011"
    ville: Optional[str] = "Paris"
    cp_ville: Optional[str] = None
    date: Optional[str] = None
    num_client: Optional[str] = "103866054"
    depuis: Optional[str] = "1 Janvier 2020"


class JustificatifGenerateRequest(ExtraAllow):
    pass


JUSTIFICATIF_MODELS = {
    "conduite_heures": JustificatifConduiteHeuresRequest,
    "attestation_edf": JustificatifAttestationEdfRequest,
    "attestation_direct_energie": JustificatifAttestationDirectEnergieRequest,
}


def dump_model(model: BaseModel) -> dict:
    if hasattr(model, "model_dump"):
        return model.model_dump(exclude_none=True)
    data = model.dict()
    return {key: value for key, value in data.items() if value is not None}


def parse_justificatif_payload(issuer: str, data: dict | None) -> dict:
    payload = {key: value for key, value in dict(data or {}).items() if value is not None}
    model_cls = JUSTIFICATIF_MODELS.get(issuer)
    if model_cls is None:
        return payload
    return dump_model(model_cls(**payload))
