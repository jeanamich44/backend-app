from app.services.generate_docs.common import example_dates as _dates

# ----------------------------------------------------------------------

LABEL_CLIENT = "Numéro client : "
LABEL_CONTRAT = "Numéro contrat :"
LABEL_COURTIER = "Courtier : "
LABEL_ORIAS = "N° ORIAS : "
LABEL_DATE = "Date de délivrance du document : "

COURTIER = "CARREZ CONSEIL ASSURANCES"
NUM_CLIENT = "TI0002738510"
NUM_CONTRAT = "MOT001224269"
NUM_ORIAS = "17009627"

CIVILITE = "M."
NOM = "MARTIN"
PRENOM = "LUCAS"
TITULAIRE = "M. MARTIN LUCAS"
ADRESSE = "12 RUE DES FLEURS"
CP = "75011"
VILLE = "PARIS"
CP_VILLE = "75011 PARIS"
PAYS = "FRANCE"


def __getattr__(name: str):
    if name == "DATE_DELIVRANCE":
        return _dates.maxance_delivrance()
    if name in {"DATE_EFFET_JOUR", "DATE_EFFET_MOIS", "DATE_EFFET_ANNEE"}:
        jour, mois, annee = _dates.maxance_effet()
        return {"DATE_EFFET_JOUR": jour, "DATE_EFFET_MOIS": mois, "DATE_EFFET_ANNEE": annee}[name]
    if name == "DATE_EFFET":
        jour, mois, annee = _dates.maxance_effet()
        return f"{jour}/{mois}/{annee}"
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


IMMATRICULATION = "AH-120-PO"
VEHICULE = "YAMAHA X-MAX (SCOOTER 125 CC)"
VEHICULE_MARQUE_MODELE = "YAMAHA X-MAX (SCOOTER 125 cc)"

TITLE = "MÉMO VÉHICULE ASSURÉ PROVISOIRE"
NOTICE_1 = (
    "Ce mémo constitue une présomption d’assurance pour les véhicules "
    "immatriculés pendant les 15 jours suivant la date de prise"
)
NOTICE_2 = (
    "d’effet de votre contrat d’assurance. Pour plus d’information sur le mémo, "
    "www.maxance.com"
)

SEC1 = "MÉMO VÉHICULE ASSURÉ"
SEC1_RIGHT = "IMIC - INTERNATIONAL MOTOR INSURANCE CARD"
SEC2 = "DATE D’EFFET"
SEC3 = "NUMÉRO DE CONTRAT"
SEC4 = "NUMÉRO D’IMMATRICULATION"
SEC5 = "MARQUE / MODÈLE - VÉHICULE / REMORQUE"
SEC6 = "BESOIN D’AIDE ?"
SEC7 = "VALIDITÉ TERRITORIALE"
SEC8 = "SIGNATURE DE L’ASSUREUR"
SEC9 = "CE MÉMO A ÉTÉ DÉLIVRÉ PAR maxance"
SEC9_RIGHT = "SOUS COUVERT DE"

NOTE_1 = (
    "À noter : les remorques jusqu’à 750 kg (PTAC) tractées par le véhicule "
    "assuré sont garanties en responsabilité civile dans la limite d’un poids "
    "total roulant autorisé de 3500 kg"
)
NOTE_2 = "(véhicule tracteur + remorque)"

JOUR = "JOUR : "
MOIS = "MOIS : "
ANNEE = "ANNEE : "

HELP_1 = "Bénéficiez de notre réseau de 5000 garages agréés."
HELP_2 = "Le bon réflexe pour faire réparer votre véhicule, en cas de sinistre garanti."
DECLARE_PREFIX = "Pour déclarer "
DECLARE_BOLD = "un sinistre"
DECLARE_SUFFIX = ","
CONTACT_MAXANCE = "contactez maxance"
ASSIST_PREFIX = "Pour toute demande "
ASSIST_BOLD = "d’assistance"
ASSIST_SUFFIX = ","
CONTACT_MONDIAL = "contactez Mondial Assistance France"

TERR_1 = "Nous vous rappelons que l’assurance Responsabilité Civile est obligatoire"
TERR_2 = "et la conduite sans assurance est un délit qui peut s’accompagner d’une"
TERR_3 = "amende. Vous avez la possibilité de vérifier si le véhicule immatriculé que"
TERR_4 = "vous conduisez est bien assuré : "
TERR_5_PREFIX = "• en consultant le site public FVA : "
TERR_5_BOLD = "www.fva-assurance.fr"
TERR_6_PREFIX = "• en appelant le serveur vocal :"
TERR_6_BOLD = " 01 83 64 32 22 (coût d’un appel local)"

PHONE_1 = " 01 49 15 33 00"
PHONE_2 = " 02 43 80 21 38"
FROM_ABROAD = "Depuis l’étranger :"
PHONE_INTL_1 = "(+33) 01 49 15 33 00"
PHONE_INTL_2 = "(33) 2 43 80 21 38"
SIGNATURE = "par délégation Claude Zaouati, Président."

LEGAL_LEFT = (
    "MAXANCE ASSURANCES - Siège social : 34 avenue Léon Gaumont, 93100 Montreuil - Tél :\n"
    "+33(0)1.49.15.33.00 - SAS au capital de 35 000 Euros - RCS de Bobigny - SIRET n°\n"
    "439 158 445 00023 - APE : 6622Z - Société de Courtage d'Assurances soumise à l'autorité de\n"
    "l'ACPR (Autorité de Contrôle Prudentiel et de Résolution) - www.acpr.banque-france.fr - ORIAS n°\n"
    "07 032 460 - www.orias.fr - N° TVA intracommunautaire FR07 439 158 445"
)
LEGAL_RIGHT = (
    "L'Équité, SA au capital de 26 469 320 euros - Entreprise régie par le Code des\n"
    "assurances - 572 084 697 RCS Paris - Siège Social : 2 rue Pillet-Will 75009 Paris -\n"
    "Société appartenant au Groupe Generali immatriculé sur le registre italien des groupes\n"
    "d'assurances sous le numéro 026."
)

FOOTER_ADDR_1 = "Maxance - Siège social : 6 rue Gracchus Babeuf, 93130 Noisy-le-Sec, France"
FOOTER_ADDR_2 = "Tél. +33 (0)1 49 15 33 00 - www.maxance.com"
FOOTER_LEGAL_1 = (
    "SASU au capital de 35.000,00 € – RCS de Bobigny – SIREN n° 439 158 445 – "
    "SIRET n° 439 158 445 00015 – APE : 6622Z – Société de Courtage d’assurances "
    "soumise à l’autorité de"
)
FOOTER_LEGAL_2 = (
    "l’ACPR (Autorité de Contrôle Prudentiel et de Résolution), 4 place de Budapest, "
    "CS 92459, 75436 Paris cedex 09, France – Tél. +33 (0)1 49 95 40 00 – "
    "www.acpr.banque-france.fr –"
)
FOOTER_LEGAL_3 = (
    "Inscription ORIAS n° 07 032 460 en catégorie Courtier d’Assurances (COA) – "
    "www.orias.fr"
)
PAGE = "1/1"
