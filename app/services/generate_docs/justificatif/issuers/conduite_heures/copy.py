from app.services.generate_docs.common import example_dates as _dates

TITLE = "Liste des rendez-vous"
NOTICE = "Tout rendez-vous non annulé 48  (ouvrés) à l'avance sera dû."
EDITION_PREFIX = "Edition du : "

ELEVE = "Martin LUCAS [1001]"
NOM = "MARTIN"
PRENOM = "LUCAS"
NUM_ELEVE = "1001"
_JOUR_EXPAND = {
    "Lun.": "Lundi",
    "Mar.": "Mardi",
    "Mer.": "Mercredi",
    "Jeu.": "Jeudi",
    "Ven.": "Vendredi",
    "Sam.": "Samedi",
    "Dim.": "Dimanche",
}

HEAD_DATE = "Date"
HEAD_START = "Début"
HEAD_END = "Fin"
HEAD_ACT = "Activité"
HEAD_COM = "Commentaire(s)"

RDV1_ACTIVITE = "LECON PLATEAU"
RDV1_COMMENT = ""
RDV2_ACTIVITE = "LECON PLATEAU"
RDV2_COMMENT = ""
RDV3_ACTIVITE = "LECON PLATEAU"
RDV3_COMMENT = ""

_RDV_ATTR = {
    "JOUR": "jour",
    "DATE": "date",
    "DEBUT": "debut",
    "FIN": "fin",
}


def _get_default_rdvs() -> list[dict]:
    lessons = _dates.conduite_lessons()
    return [
        {
            **item,
            "jour": _JOUR_EXPAND.get(item["jour"], item["jour"]),
        }
        for item in lessons
    ]


def __getattr__(name: str):
    if name == "EDITION":
        return _dates.conduite_edition()
    if name == "EDITION_DATE":
        return _dates.ca_edition()
    if name == "EDITION_TIME":
        return _dates.now().strftime("%H:%M")
    if name == "DEFAULT_RDVS":
        return _get_default_rdvs()
    if name.startswith("RDV") and "_" in name:
        index = int(name[3]) - 1
        suffix = name.split("_", 1)[1]
        key = _RDV_ATTR.get(suffix)
        if key:
            return _dates.conduite_lessons()[index][key]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

SCHOOL = "CFRVITRY 2"
LEGAL_1 = (
    "SASU Centre de formation routiere vitry 2 - Siret 95141910000015 - "
    "NAF 8553Z - TVA FR11951419100- Agrément n° E2309400140 - RCS creteil 95141910000015 "
)
LEGAL_2 = "Médiateur : Société Mediation Professionnelle - 24 Rue Albert De Mun "
LEGAL_3 = "30000 Bordeaux "
