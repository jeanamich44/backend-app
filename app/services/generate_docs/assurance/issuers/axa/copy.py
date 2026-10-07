from datetime import datetime, timedelta

# ----------------------------------------------------------------------


def dynamic_date(d=None) -> datetime:
    return (d or datetime.now()) - timedelta(days=1)


def default_edition_date(d=None) -> str:
    dt = dynamic_date(d)
    return f"A Rueil-Malmaison, le {dt.strftime('%d/%m/%Y')}"


def default_info_effet(d=None) -> str:
    dt = dynamic_date(d)
    return f"{dt.strftime('%d/%m/%Y')} - 00:00"


def default_date_effet(d=None) -> str:
    dt = dynamic_date(d)
    return dt.strftime('%d/%m/%Y')


def default_date_delivrance(d=None) -> str:
    dt = dynamic_date(d)
    return dt.strftime('%d/%m/%Y')


CIVILITE = "MONSIEUR"
NOM = "MARTIN"
PRENOM = "LUCAS"
ADRESSE = "12 RUE DES FLEURS"
CP = "75011"
VILLE = "PARIS"

DESTINATAIRE_L1 = "MONSIEUR MARTIN LUCAS"
DESTINATAIRE_L2 = "12 RUE DES FLEURS"
DESTINATAIRE_L3 = "75011 PARIS"
EDITION_DATE = default_edition_date()

RAPPEL_TITLE = "Rappel : La carte verte n'existe plus depuis le 01/04/2024 !"
RAPPEL_L1 = "Depuis le 1er avril 2024, la loi a changé par l'Article de loi à intégrer (Article R.211-14-0 du code des assurances) : la carte verte"
RAPPEL_L2 = "n'est plus nécessaire pour prouver que vous êtes assuré. Maintenant, la preuve de votre assurance se fait par votre plaque"
RAPPEL_L3 = "d'immatriculation qui est enregistrée dans le Fichier des Véhicules Assurés (FVA)."

MEMO_TITLE = "Mémo Véhicule Assuré : "
MEMO_CONSERVER = "À CONSERVER"

NOTICE_L1 = "Nous vous recommandons de conserver ce document avec vous lors de vos déplacements, que ce soit en format papier ou électroniquement sur"
NOTICE_L2 = "votre téléphone."

PRESOMPTION_SOULIGNE = "Ce document constitue une présomption d’assurance pendant les 15 jours suivant la date de prise d’effet du contrat."
PRESOMPTION_VALABLE = "Ce document est valable pendant toute la durée de votre contrat d’assurance automobile. Il engage votre assureur uniquement dans les termes et limites précisés par les garanties et conditions du contrat d'assurance auquel il se réfère et sous réserve que le paiement effectif des primes ait bien été honoré sur la période."
OBLIGATION_FVA_L1 = "Tout véhicule terrestre à moteur est soumis à l'obligation d'assurance en responsabilité civile. Vous pouvez vérifier la situation de votre véhicule à tout moment en consultant le Fichier des"
OBLIGATION_FVA_L2 = "Véhicules Assurés (www.fva-assurance.fr) ou le serveur vocal au 01 83 64 32 22 (coût d'un appel local). L'inscription au FVA suffit pour circuler en France et dans l'Union Européenne."
POLITESSE = "Nous vous en souhaitons bonne réception et vous prions de croire, en nos sentiments dévoués."

VEHICULE_TITLE = "Votre Véhicule Assuré"
INFO_TITLE = "Vos informations contractuelles : "
INFO_CLIENT = "A084RZ"
INFO_CONTRAT = "D443 - 4180352981 - 4180352981   367304284920"
INFO_EFFET = default_info_effet()

NUM_CLIENT = "A084RZ"
NUM_CONTRAT = "D443 - 4180352981 - 4180352981   367304284920"

VEHICULE_SUBTITLE = "Le véhicule assuré : "
VEHICULE_MARQUE = "BMW X3"
VEHICULE_IMMAT = "FA-120-GM"

IMMATRICULATION = "FA-120-GM"
VEHICULE_MARQUE_MODELE = "BMW X3"

REMORQUE_TITLE = "Extension sur remorque :"
REMORQUE_L1 = "Votre remorque est automatiquement garantie pour la Responsabilité Civile (voir conditions et limites dans vos Conditions Générales)."
REMORQUE_L2 = "Votre remorque doit avoir la même immatriculation que le véhicule assuré au titre de ce contrat."

ASSUREUR_TITLE = "Votre assureur :"
ASSUREUR_NOM = "AXA FRANCE IARD"
ASSUREUR_ADRESSE = "313 Terrasses de l Arche 92000 Nanterre"

COUVERTURE_L1 = "La couverture géographique de votre contrat d'assurance est présente dans vos Conditions générales. Avant tout déplacement à l'étranger, veuillez vérifier que la liste des pays n'a pas fait l'objet"
COUVERTURE_L2 = "d'évolution."

NUMEROS_TITLE = "Les numéros utiles"
NUMEROS_SUBTITLE = "A tout moment, les numéros suivants peuvent vous être utiles. Nous vous conseillons donc de les inscrire dans les contacts de votre téléphone portable."

SINISTRE_HEADER = "En cas de sinistre : "
SINISTRE_INTRO = "Si vous souhaitez déclarer un sinistre, vous pouvez contacter : "
SINISTRE_SERVICE = "LSA Gestion - Service Sinistre"
SINISTRE_MAIL_LABEL = "Par mail : "
SINISTRE_MAIL_VAL = "sinistres@lsa-courtage.com"
SINISTRE_TEL_LABEL = "Par Téléphone : 01.41.03.31.08"
SINISTRE_HORAIRES = "Notre Service Sinistres est ouvert du lundi au vendredi de 9h-12h / 14h-18h (17h le vendredi)"

TEL_SINISTRE = "01.41.03.31.08"
MAIL_SINISTRE = "sinistres@lsa-courtage.com"

ASSISTANCE_HEADER = "Pour contacter l'assistance : "
ASSISTANCE_INTRO = "Vous bénéficiez de la garantie assistance. Pour toute demande d'intervention, contactez :"
ASSISTANCE_SERVICE = "MUTUAIDE ASSISTANCE"
ASSISTANCE_FRANCE = "Depuis la France : 01.45.16.65.55"
ASSISTANCE_ETRANGER = "Depuis l'étranger : (33).1.45.16.65.55"

TEL_ASSISTANCE_FRANCE = "01.45.16.65.55"
TEL_ASSISTANCE_ETRANGER = "(33).1.45.16.65.55"

QUESTIONS_TEXT = "Vous avez une question sur votre contrat ? Vous souhaitez déclarer un changement de situation ? N'hésitez pas à contacter votre conseiller au numéro suivant : 01.41.03.31.00."

RENVOI_L1 = "* Pour retrouver l'exhaustivité de vos garanties, référez-vous à vos Conditions Particulières. Les limites et les conditions de vos garanties sont décrites dans vos Conditions Générales présentes ici : "
RENVOI_L2 = "https://ressources.lsa-courtage.com/cg/535_DIPA_CG_2022.pdf"

LEGAL_L1 = "Contrat distribué et géré par LSA COURTAGE, SAS au capital de 224.888,50 €, Courtier en assurance inscrit à l’ORIAS sous le n° 07 001 857 - RCS Nanterre n° 702 053 000 - 18 rue des deux gares 92500 Rueil-Malmaison. Le contrat est assuré"
LEGAL_L2 = "par AXA France IARD, SA au capital de 214 799 030 € - 722 057 460 RCS Nanterre ; et AXA Assurances IARD Mutuelle, société d’assurance mutuelle, identifiée sous le numéro SIREN 775 699 309, ayant leur siège social 313, Terrasses de l’Arche"
LEGAL_L3 = "à Nanterre (92000). Le contrat d’assurance est souscrit en coassurance entre AXA France IARD et AXA Assurances IARD Mutuelle, qui seront solidaires entre elles. Entreprises régies par le Code des assurances. La garantie assistance est assurée"
LEGAL_L4 = "par Mutuaide Assistance - S.A. au capital de 12 558 240 € - 383 974 086 RCS Créteil - TVA intracommunautaire n° FR 31 383 974 086 - Siège social : 126, rue de la Piazza - 93196 Noisy le Grand CEDEX . Entreprise régie par le Code des assurances."
