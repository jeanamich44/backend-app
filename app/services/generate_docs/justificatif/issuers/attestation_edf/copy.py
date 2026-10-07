from app.services.generate_docs.common import example_dates as _dates

TITRE = "ATTESTATION TITULAIRE DE CONTRAT"
TITLE = TITRE

CIVILITE = "Mr."
NOM = "MARTIN"
PRENOM = "LUCAS"
NOM_COMPLET = "MARTIN LUCAS"
ADRESSE = "12 RUE DES FLEURS"
VILLE = "PARIS"
CP = "75011"
FOOTER_CACHET = False

NUM_CLIENT = "6 013 159 667"
NUM_COMPTE = "4 02 4 024 8 51 258"
PDL = "07334145884965"
PUISSANCE = "06"

CONSEILLERE = "Marie"
CONSEILLERE_LIBELLE = "Votre conseillère EDF"
CONSEILLERE_LABEL = CONSEILLERE_LIBELLE

CONTACT_TITRE = "NOUS CONTACTER"
CLIENT_SIDE_LIBELLE = "N° client :"
PAR_INTERNET = "Par Internet"
SITE = "edf.fr"
APP_MOBILE = "application mobile :"
APP_NOM = "EDF&MOI"
MAIL_LIBELLE = "mail :"
EMAIL = "serviceclient@edf.fr"
PAR_TELEPHONE = "Par téléphone"
HORAIRES = "Du lundi au samedi dès 8h et jusqu'à 20h"
NUM_COURT = "3004"
SERVICE_APPEL = "Service et appel gratuits"
SERVEUR_VOCAL = "Mon Compte sur Serveur Vocal"
NUM_VOCAL = "09 70 83 33 33"
PRIX_APPEL = "(Service gratuit + prix appel)"
PAR_COURRIER = "Par courrier"
COURRIER_L1 = "EDF SERVICE CLIENTS"
COURRIER_L2 = "TSA 21941"
COURRIER_L3 = "62978 ARRAS CEDEX 9"
CHEQUE_TITRE = "NOUS ENVOYER UN CHEQUE ENERGIE"
CHEQUE_COURRIER = "Par courrier"
CHEQUE_L1 = "EDF TSA 81401"
CHEQUE_L2 = "87014 LIMOGES Cedex 1"
LIEU_TITRE = "Lieu de consommation"
TITULAIRE_LIBELLE = "Titulaire du contrat"
CONTRAT_LIBELLE = "Votre contrat"
N_CLIENT_LIBELLE = "N° de client :"
N_COMPTE_LIBELLE = "N° de compte :"
COMPTE_HINT1 = "(numéro à transmettre pour le"
COMPTE_HINT2 = "règlement de vos factures)"
TARIF_BLEU = "Electricité « Tarif Bleu »"
PDL_LIBELLE = "• Point de livraison (PDL) :"
N_PDL = "N°"
PUISSANCE_LIBELLE = "• Puissance :"
UNITE_KVA = "KVA"
POUR_SERVIR = "Pour servir et valoir ce que de droit."

CACHET_L1 = "Cachet Électronique"
CACHET_L2 = "Visible d'authentification"
CACHET_L3 = "de ce document"

LEGAL = (
    "EDF-SA au capital de 1 943 859 339,50 euros - Siège social 22-30 avenue de "
    "Wagram 75008 Paris - R.C.S. Paris 552 081 317 - N° TVA FR 03 552 081 317"
)

MONTHS = (
    "", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre",
)


def today_date(d=None) -> str:
    return _dates.edf_attestation(d)


def date_line(ville: str, date: str) -> str:
    return f"A {ville}, le {date}"


def __getattr__(name: str):
    if name == "DATE":
        return _dates.edf_attestation()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
