from datetime import datetime

CIVILITY = "M "
NOM = "Martin"
PRENOM = "Lucas"
CLIENT_NOM = "MARTIN LUCAS"
ADRESSE = "12 Rue des Fleurs"
CP_VILLE = "75011 PARIS"

NUM_FACTURE = "535006482817"
NUM_CLIENT = "319375842"
NUM_CONTRAT = "525866248"
LIEU_PCE = "1GHE*FD 48"
LIEU_BAT = "BAT A 1ET"

TITLE = "VOTRE FACTURE DE SOUSCRIPTION"
SUBTITLE = (
    "Votre facture de souscription est émise suite à un emménagement dans un nouveau logement ou un changement",
    "de Fournisseur.",
)
CLIENT_LABEL = "Référence client :"
CONTRAT_LABEL = "Numéro Compte de Contrat :"
LIEU_LABEL = "Lieu de consommation :"
DETAIL = "Détail de votre contrat en p.2"

CHEQUE_LABEL = "        Chèque Énergie : "
CHEQUE_BODY = "Enregistrez votre Chèque Énergie sur chequeenergie.gouv.fr"
CHEQUE_NOTE = (
    "Ou envoyez le à ENGIE TSA 10016  78924 YVELINES CEDEX 9 "
    "(référence client au dos du chèque)"
)

CORRESPOND_TITLE = "A quoi correspond cette facture ?"
CORRESPOND_BODY = (
    "Pour votre emménagement, elle comprend le paiement anticipé de deux mois d'abonnement maximum et les frais",
    "de mise en service facturés pour le compte du ou des Distributeur(s).",
)

LEGAL = (
    "ENGIE - SA au capital de 2 435 285 011 € - RCS Nanterre 542 107 651 - "
    "NI TVA FR 13 542 107 651 - 1 place Samuel de Champlain - 92400 COURBEVOIE"
)

CONTACTS_TITLE = "Vos Contacts Utiles"
CONTACTS_SERVICE = "Votre Service Clients Engie"
CONTACTS_WEB = "Accédez à votre espace client 24h/24 - 7j/7 :"
CONTACTS_URL = " particuliers.engie.fr"
CONTACTS_APP = "Accédez depuis votre application mobile"
CONTACTS_HOURS = "Du lundi au samedi : 8H-20H"
CONTACTS_PHONE = "0 969 324 324"
CONTACTS_FREE = "APPEL NON SURTAXÉ"
CONTACTS_MAIL_NAME = "ENGIE,"
CONTACTS_MAIL_ADDR = " TSA 87494, 76934 ROUEN CEDEX 09"
CONTACTS_URGENCE = "Urgence Dépannage 24h/24"
CONTACTS_GRDF = "Urgence sécurité Gaz GRDF"
CONTACTS_GRDF_PHONE = "0 800 473 333"
CONTACTS_ENEDIS = "Dépannage Electricité Enedis"
CONTACTS_ENEDIS_PHONE = "0 972 675 094"

ECONO_HEAD_1 = "Faites des économies d'énergie"
ECONO_HEAD_2 = "en maîtrisant votre consommation"
ECONO_CONSO_1 = "Suivez votre consommation au plus près sur votre"
ECONO_CONSO_2 = "Espace Client avec "
ECONO_CONSO_BOLD = "Ma conso"
ECONO_CONSO_NOTE = "(inclus dans votre offre)"
ECONO_THERMO_1 = "Pour réduire votre consommation de chauffage de 5% à"
ECONO_THERMO_2 = "15%, vous pouvez opter pour un thermostat d"
ECONO_THERMO_APOS = "’"
ECONO_THERMO_3 = "ambiance."
ECONO_LINE_BOLD = "Avec la Facture en Ligne,"
ECONO_LINE_1 = " vos factures sont disponibles 5 ans sur"
ECONO_LINE_2 = "votre Espace Client : vous pouvez les consulter et les imprimer"
ECONO_LINE_3 = "comme justificatif de domicile."

MONTANT_GAZ = "46,20"
MONTANT_PREST = "21,50"
TOTAL_TTC = "67,70"
MONTANT_HT = "61,55"
MONTANT_TVA = "6,15"
COMPTE = "20041000014763925L0XXXX."

GAZ_LABEL = "Gaz naturel"
PREST_LABEL = "Prestations"
PLUS = "+"
EQUAL = "="
TTC_LABEL = "Facture TTC"
TOTAL_LABEL = "Montant Total TTC "
NEXT_LABEL = "Prochaine facture"
TELE_LABEL = "Télé-relevé Gaz"
DETAIL_P2 = "(Détail p.2)"
PAY_TITLE = "VOTRE MODE DE PAIEMENT"
PAY_L1 = "Conformément à votre demande, le"
PAY_L2 = "montant de cette facture sera prélevé"
PAY_L3 = "sur le compte"
PAY_L5 = "Retrouvez vos coordonnées"
PAY_L6 = "bancaires p.3."
MONTHS_FR = (
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre",
)


def slash_date_yy(d=None) -> str:
    d = d or datetime.now()
    return f"{d:%d/%m/%y}"
