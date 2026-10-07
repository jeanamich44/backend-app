from datetime import datetime

# ----------------------------------------------------------------------

MODE_EN_LIGNE = "en_ligne"
MODE_MAGASIN = "magasin"

SELLER_BOULANGER = "boulanger"
SELLER_TIERS = "tiers"

# ----------------------------------------------------------------------

NOM = "Martin"
PRENOM = "Lucas"
CLIENT_NOM = "Martin Lucas"
ADRESSE = "12 Rue des Fleurs"
CP = "75011"
VILLE = "Paris"
CP_VILLE = "75011 Paris"
CLIENT_NUM = "29468065"
CLIENT_TEL = "06 12 34 56 78"

# ----------------------------------------------------------------------

def slash_date(d=None) -> str:
    d = d or datetime.now()
    return f"{d:%d/%m/%Y}"

# ----------------------------------------------------------------------

DOC_TYPE = "FACTURE"
FACTURE_PAGE = "1/1"

TABLE_HEADER = "REFERENCE DE L'ACHAT                      CODE     Qt\xe9  P.U.TTC  T.TVA TOTAL TTC"

# ----------------------------------------------------------------------

EL_FACTURE_NUM = "F905 FQ09058-23/002"
EL_FACTURE_DATE = "19.12.2023"
EL_FACTURE_TIME = "19:23"
EL_BARCODE_VAL = "F905FQ09058"

EL_STORE_NOM = "BOULANGER WWW.BOULANGER.COM"
EL_STORE_RUE1 = "CRT - BP137"
EL_STORE_RUE2 = "AV DE LA MOTTE"
EL_STORE_CP_VILLE = "59810 LESQUIN"
EL_STORE_SIRET = "34738457002017"
EL_STORE_TEL = "03 86 42 53 08"

EL_CLIENT_NOM = CLIENT_NOM
EL_CLIENT_RUE = ADRESSE
EL_CLIENT_CP_VILLE = CP_VILLE
EL_CLIENT_NUM = CLIENT_NUM

EL_ARTICLE_1_NOM = "PACK ADEQWAT Powerbank + Chargeur + C"
EL_ARTICLE_1_CODE = "0008010892"
EL_ARTICLE_1_QTE = "1"
EL_ARTICLE_1_PU_TTC = "49,97"
EL_ARTICLE_1_TVA_TAUX = "20,00"
EL_ARTICLE_1_TOTAL_TTC = "49,97"
EL_ARTICLE_1_ECOPART = "0,02"
EL_ARTICLE_1_GARANTIE_NON_RETENUE = ""
EL_ARTICLE_1_GARANTIE_REPARATION = "Garantie R\xe9paration jusqu'au 19.12.2025"
EL_ARTICLE_1_DISPO_PIECES_LABEL = "Disponibilit\xe9 des pi\xe8ces d\xe9tach\xe9es (donn\xe9e fournisseur) :"
EL_ARTICLE_1_DISPO_PIECES = "Pas de pi\xe8ce disponible"

EL_EXTRA_NOM = "BOULANGER FRAIS DE PORT"
EL_EXTRA_CODE = "0001037258"
EL_EXTRA_QTE = "1"
EL_EXTRA_PU_TTC = "3,99"
EL_EXTRA_TVA_TAUX = "20,00"
EL_EXTRA_TOTAL_TTC = "3,99"

EL_TOTAL_HT = "44,99"
EL_TOTAL_TTC = "53,98"
EL_DONT_TVA = "9,00"
EL_DONT_TVA_TAUX = "20,00"
EL_DONT_ECOPART = "0,02"

EL_REGLEMENT_MODE = "Carte Bancaire"
EL_REGLEMENT_MONTANT = "53,98"

EL_NOTICE_CUMUL = "Consultez votre cumul d'Euros sur www.boulanger.com"

# ----------------------------------------------------------------------

MAG_FACTURE_NUM = "F905 DR10494-23/003"
MAG_FACTURE_DATE = "27.04.2023"
MAG_FACTURE_TIME = "14:39"
MAG_BARCODE_VAL = "F905DR10494"

MAG_STORE_NOM = "BOULANGER CAMBRAI"
MAG_STORE_RUE1 = "CENTRE COMMERCIAL CORA"
MAG_STORE_RUE2 = "ZAC CAMBRAI SUD"
MAG_STORE_LIEU = "R.N. 44"
MAG_STORE_CP_VILLE = "59400 CAMBRAI"
MAG_STORE_SIRET = "34738457001167"

MAG_CLIENT_NOM = CLIENT_NOM
MAG_CLIENT_RUE = ADRESSE
MAG_CLIENT_CP_VILLE = CP_VILLE
MAG_CLIENT_NUM = CLIENT_NUM

MAG_ARTICLE_1_NOM = "Enceinte SONOS Era 300 EU Noir"
MAG_ARTICLE_1_CODE = "0001188819"
MAG_ARTICLE_1_QTE = "1"
MAG_ARTICLE_1_PU_TTC = "499,49"
MAG_ARTICLE_1_TVA_TAUX = "20,00"
MAG_ARTICLE_1_TOTAL_TTC = "499,49"
MAG_ARTICLE_1_ECOPART = "0,50"
MAG_ARTICLE_1_GARANTIE_NON_RETENUE = "Extension de garantie non retenue"
MAG_ARTICLE_1_GARANTIE_REPARATION = "Garantie R\xe9paration jusqu'au 27.04.2025"
MAG_ARTICLE_1_DISPO_PIECES_LABEL = "Disponibilit\xe9 des pi\xe8ces d\xe9tach\xe9es (donn\xe9e fournisseur) :"
MAG_ARTICLE_1_DISPO_PIECES = "Pas de pi\xe8ce disponible"

MAG_EXTRA_NOM = ""
MAG_EXTRA_CODE = ""
MAG_EXTRA_QTE = ""
MAG_EXTRA_PU_TTC = ""
MAG_EXTRA_TVA_TAUX = ""
MAG_EXTRA_TOTAL_TTC = ""

CLUB_NOM = "Le Club"
CLUB_CODE = "0001185162"
CLUB_QTE = "1"
CLUB_PU_TTC = "0,00"
CLUB_TVA_TAUX = "20,00"
CLUB_TOTAL_TTC = "0,00"

MAG_TOTAL_HT = "416,66"
MAG_TOTAL_TTC = "499,99"
MAG_DONT_TVA = "83,33"
MAG_DONT_TVA_TAUX = "20,00"
MAG_DONT_ECOPART = "0,50"

MAG_REGLEMENT_MODE = "Carte Bancaire"
MAG_REGLEMENT_MONTANT = "499,99"

MAG_CONDITIONS_LINES = (
    "Les conditions de vente internet accept\xe9es lors de votre commande sur notre site",
    "www.boulanger.com, sont les seules applicables \xe0 votre(s) achat(s) \xe0 l'exclusion",
    "de toutes autres, notamment celles au verso du pr\xe9sent document.",
)

# ----------------------------------------------------------------------

NOTICE_MERCI = "Merci de votre visite"
NOTICE_GARANTIE_L1 = "Garantie l\xe9gale de conformit\xe9 : 2 ans"
NOTICE_GARANTIE_L2 = "minimum \xe0 compter de la d\xe9livrance du"
NOTICE_GARANTIE_L3 = "produit"

# ----------------------------------------------------------------------

COMPANY_NOM = "Boulanger SA"
COMPANY_CAPITAL = "Au capital de 40 611 564 EUR"
COMPANY_RUE = "Avenue de la Motte"
COMPANY_RCS = "RCS LILLE B 347 384 570"
COMPANY_CP_VILLE = "59810 Lesquin"
COMPANY_TVA = "TVA I.C. FR 78 347 384 570"
COMPANY_APE = "APE 4754Z"

# ----------------------------------------------------------------------

TIERS_VENDEUR_NOM = "TECH STORE FRANCE"
TIERS_VENDEUR_RUE = "12 RUE DE LA PAIX"
TIERS_VENDEUR_CP_VILLE = "75002 PARIS"
TIERS_VENDEUR_SIRET = "82012345600012"
TIERS_VENDEUR_TVA = "FR 12 820123456"
TIERS_VENDEUR_CAPITAL = "50 000 EUR"
TIERS_VENDEUR_RCS = "RCS PARIS B 820 123 456"

# ----------------------------------------------------------------------

ARTICLE_2_NOM = "C\xe2ble USB-C Adeqwat 1m Noir"
ARTICLE_2_CODE = "0008012345"
ARTICLE_2_QTE = "1"
ARTICLE_2_PU_TTC = "14,99"
ARTICLE_2_TVA_TAUX = "20,00"
ARTICLE_2_TOTAL_TTC = "14,99"
ARTICLE_2_ECOPART = "0,02"
ARTICLE_2_GARANTIE_NON_RETENUE = ""
ARTICLE_2_GARANTIE_REPARATION = ""
ARTICLE_2_DISPO_PIECES_LABEL = "Disponibilit\xe9 des pi\xe8ces d\xe9tach\xe9es (donn\xe9e fournisseur) :"
ARTICLE_2_DISPO_PIECES = "Non communiqu\xe9e"

ARTICLE_3_NOM = "Chargeur Secteur Rapide 30W Adeqwat"
ARTICLE_3_CODE = "0008019876"
ARTICLE_3_QTE = "1"
ARTICLE_3_PU_TTC = "24,99"
ARTICLE_3_TVA_TAUX = "20,00"
ARTICLE_3_TOTAL_TTC = "24,99"
ARTICLE_3_ECOPART = "0,02"
ARTICLE_3_GARANTIE_NON_RETENUE = ""
ARTICLE_3_GARANTIE_REPARATION = ""
ARTICLE_3_DISPO_PIECES_LABEL = "Disponibilit\xe9 des pi\xe8ces d\xe9tach\xe9es (donn\xe9e fournisseur) :"
ARTICLE_3_DISPO_PIECES = "Pas de pi\xe8ce disponible"
