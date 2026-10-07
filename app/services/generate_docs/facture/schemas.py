from typing import Optional

from pydantic import BaseModel, ConfigDict


class ExtraAllow(BaseModel):
    model_config = ConfigDict(extra="allow")


class AdidasItem(ExtraAllow):
    sku: Optional[str] = "AD1001"
    taille: Optional[str] = "42"
    nom: Optional[str] = "SUPERSTAR"
    qte: Optional[str] = "1"
    pu_ht: Optional[str] = "291,67"
    pu_ttc: Optional[str] = "350,00"


class FactureAdidasRequest(ExtraAllow):
    nom: Optional[str] = "Martin Lucas"
    adresse: Optional[str] = "12 Rue des Fleurs"
    cp_ville: Optional[str] = "75011 Paris"
    pays: Optional[str] = "FR"
    livraison_nom: Optional[str] = "Martin Lucas"
    livraison_adresse: Optional[str] = "12 Rue des Fleurs"
    livraison_cp_ville: Optional[str] = "75011 Paris"
    livraison_pays: Optional[str] = "FR"
    num_commande: Optional[str] = "AFR90132922"
    num_facture: Optional[str] = "FRADIN0007203672"
    date_facture: Optional[str] = None
    date_livraison: Optional[str] = None
    total: Optional[str] = "350,00"
    items: Optional[list[AdidasItem]] = None


class AmazonItem(ExtraAllow):
    nom: Optional[str] = "Casque audio sans fil Bluetooth, autonomie 30 h."
    note: Optional[str] = "Information indisponible sur les pièces détachées"
    qte: Optional[str] = "1"
    pu_ht: Optional[str] = "100,00"
    pu_ttc: Optional[str] = "120,00"
    asin: Optional[str] = "B0C3D81M43"


class FactureAmazonRequest(ExtraAllow):
    nom: Optional[str] = "Martin Lucas"
    adresse: Optional[str] = "12 Rue des Fleurs"
    cp_ville: Optional[str] = "PARIS, 75011"
    pays: Optional[str] = "FR"
    livraison_nom: Optional[str] = "Martin Lucas"
    livraison_adresse: Optional[str] = "12 Rue des Fleurs"
    livraison_cp_ville: Optional[str] = "Paris, 75011"
    livraison_pays: Optional[str] = "FR"
    seller_nom: Optional[str] = "Amazon EU S.à r.l., Succursale Française"
    seller_adresse: Optional[str] = "67 Boulevard du General Leclerc"
    seller_adresse2: Optional[str] = ""
    seller_cp_ville: Optional[str] = "Clichy 92110"
    seller_pays: Optional[str] = "France"
    seller_tva: Optional[str] = "LU19647148"
    payment_ref: Optional[str] = "2MVI3VL9HC4A0NEC"
    num_facture: Optional[str] = "DS-ASE-INV-FR-2022-172445727"
    date_facture: Optional[str] = None
    total: Optional[str] = "120,00 €"
    num_commande: Optional[str] = "403-2699905-9515527"
    date_commande: Optional[str] = None
    expedition_ht: Optional[str] = "0,00"
    expedition_ttc: Optional[str] = "0,00"
    remise_ht: Optional[str] = "0,00"
    remise_ttc: Optional[str] = "0,00"
    tva_rate: Optional[str] = "20 %"
    sold_by_amazon: Optional[bool] = True
    items: Optional[list[AmazonItem]] = None


class FnacItem(ExtraAllow):
    nom: Optional[str] = "Casque audio sans fil Bluetooth, autonomie 30 h."
    subtitle: Optional[str] = ""
    ean: Optional[str] = "3001100110011"
    reference: Optional[str] = "1001101"
    qte: Optional[str] = "1"
    pu_ht: Optional[str] = "100.00"
    pu_ttc: Optional[str] = "120.00"
    pu_brut_ht: Optional[str] = "100.00"
    remise_ht: Optional[str] = "20.00"
    serial: Optional[str] = ""
    distribution: Optional[str] = ""
    pieces: Optional[str] = ""
    garantie: Optional[str] = ""
    eco_ht: Optional[str] = "0.00"
    eco_ttc: Optional[str] = "0.00"


class FactureFnacRequest(ExtraAllow):
    livraison_email: Optional[str] = "martin.lucas@gmail.com"
    livraison_nom: Optional[str] = "Martin Lucas"
    livraison_adresse: Optional[str] = "12 Rue des Fleurs"
    livraison_cp_ville: Optional[str] = "75011 Paris"
    livraison_pays: Optional[str] = "France métropolitaine"
    facturation_email: Optional[str] = "martin.lucas@gmail.com"
    facturation_nom: Optional[str] = "Martin Lucas"
    facturation_adresse: Optional[str] = "12 Rue des Fleurs"
    facturation_cp_ville: Optional[str] = "75011 Paris"
    facturation_pays: Optional[str] = "France métropolitaine"
    store_nom: Optional[str] = "FNAC DIRECT"
    store_l1: Optional[str] = "ZONE LOGISTIQUE NORD"
    store_l2: Optional[str] = "91000 EVRY"
    store_l3: Optional[str] = "FRANCE"
    num_commande: Optional[str] = "BXU7ZFTY2SUE2"
    date_commande: Optional[str] = None
    num_facture: Optional[str] = "2027880107"
    date_facture: Optional[str] = None
    nref: Optional[str] = "2027880107 - MLUCAS -FND"
    matricule: Optional[str] = "7000575"
    payment_mode: Optional[str] = "Carte bancaire"
    echeance: Optional[str] = None
    tva_code: Optional[str] = "I"
    tva_rate: Optional[str] = "20.00"
    frais_ht: Optional[str] = "0.00"
    tva_frais: Optional[str] = "0.00"
    pays_expedition: Optional[str] = (
        "Pays d'expédition : FRANCE (Union Européenne) – "
        "Shipping country : FRANCE (European Union)"
    )
    en_ligne: Optional[bool] = True
    items: Optional[list[FnacItem]] = None


class NikeItem(ExtraAllow):
    sku: Optional[str] = "FB7921"
    desc: Optional[str] = (
        "Sweat à capuche et zip Nike\n"
        "Sportswear Tech Fleece Windrunner\n"
        "pour homme"
    )
    qte: Optional[str] = "1.00"
    brut: Optional[str] = "119,99"
    remise: Optional[str] = "60,00"
    tva: Optional[str] = "20"


class FactureNikeRequest(ExtraAllow):
    nom: Optional[str] = "Martin Lucas"
    adresse: Optional[str] = "12 Rue des Fleurs"
    cp_ville: Optional[str] = "75011 Paris"
    pays: Optional[str] = "FRANCE"
    livraison_adresse: Optional[str] = "12 RUE DES FLEURS"
    livraison_cp_ville: Optional[str] = "75011 PARIS"
    livraison_pays: Optional[str] = "FRANCE"
    num_commande: Optional[str] = "C01001100001"
    num_facture: Optional[str] = "FR10011001"
    date_facture: Optional[str] = None
    date_envoi: Optional[str] = None
    date_echeance: Optional[str] = None
    seller: Optional[str] = "NIKE Retail B.V.,65-67 avenue des Champs-Elysees, Paris, 75008, France"
    vat: Optional[str] = "VAT Reg. No:FR81405395518"
    payment: Optional[str] = "Carte de Crédit"
    total: Optional[str] = "219,98"
    items: Optional[list[NikeItem]] = None


class AmiItem(ExtraAllow):
    desc: Optional[str] = "Sweat capuche noir"
    qte: Optional[str] = "1"
    pu: Optional[str] = "80,00"


class FactureAmiRequest(ExtraAllow):
    nom: Optional[str] = "Martin"
    prenom: Optional[str] = "Lucas"
    adresse: Optional[str] = "Martin Lucas - 12 Rue des Fleurs"
    cp: Optional[str] = "75011"
    num_facture: Optional[str] = "67 459"
    date_facture: Optional[str] = None
    tva: Optional[str] = "20"
    total: Optional[str] = "96,00"
    items: Optional[list[AmiItem]] = None


class BurberryItem(ExtraAllow):
    sku: Optional[str] = "80089081003"
    barcode: Optional[str] = "5045556761666"
    desc: Optional[str] = "Cotton Pique Polo"
    desc2: Optional[str] = "Polo Shirt"
    taille: Optional[str] = "M"
    couleur: Optional[str] = "Noir"
    qte: Optional[str] = "1"
    prix: Optional[str] = "80.00"


class FactureBurberryRequest(ExtraAllow):
    nom: Optional[str] = "Martin Lucas"
    adresse: Optional[str] = "12 Rue des Fleurs"
    ville: Optional[str] = "Paris"
    cp: Optional[str] = "75011"
    pays: Optional[str] = "France"
    retrait_magasin: Optional[bool] = True
    num_commande: Optional[str] = "4845001"
    date_commande: Optional[str] = None
    date_expedition: Optional[str] = None
    payment_mode: Optional[str] = "MasterCard *************6357"
    total: Optional[str] = "80,00"
    items: Optional[list[BurberryItem]] = None


class CdiscountItem(ExtraAllow):
    desc: Optional[str] = "Casque sans fil Bluetooth à réduction de bruit"
    qte: Optional[str] = "1"
    montant: Optional[str] = "120,00"


class FactureCdiscountRequest(ExtraAllow):
    nom: Optional[str] = "Martin Lucas"
    adresse: Optional[str] = "12 Rue des Fleurs"
    cp_ville: Optional[str] = "75011 Paris"
    livraison_nom: Optional[str] = "Martin Lucas"
    livraison_adresse: Optional[str] = "12 Rue des Fleurs"
    livraison_cp_ville: Optional[str] = "75011 Paris"
    num_commande: Optional[str] = "240101X1001"
    date_commande: Optional[str] = None
    payment: Optional[str] = "Carte Bancaire"
    port: Optional[str] = "0,00"
    vendeur: Optional[str] = "CDISCOUNT"
    immat: Optional[str] = "RCS BORDEAUX 424 059 822"
    total: Optional[str] = "120,00"
    items: Optional[list[CdiscountItem]] = None


class DafyItem(ExtraAllow):
    sku: Optional[str] = "DF-1001"
    desc: Optional[str] = "Casque Intégral Moto Noir Mat"
    couleur: Optional[str] = "Noir"
    taille: Optional[str] = "L"
    qte: Optional[str] = "1"
    pu: Optional[str] = "199,99"
    tva: Optional[str] = "20.00"


class FactureDafyRequest(ExtraAllow):
    nom: Optional[str] = "Martin Lucas"
    adresse: Optional[str] = "12 Rue des Fleurs"
    cp_ville: Optional[str] = "75011 Paris"
    pays: Optional[str] = "FRANCE"
    livraison_nom: Optional[str] = "Martin Lucas"
    livraison_extra: Optional[str] = ""
    livraison_adresse: Optional[str] = "12 Rue des Fleurs"
    livraison_cp_ville: Optional[str] = "75011 Paris"
    livraison_pays: Optional[str] = "FRANCE"
    livraison_mode: Optional[str] = "CHRONOPOST DOMICILE"
    magasin_nom: Optional[str] = "DAFY MOTO PARIS"
    num_client: Optional[str] = "CLI-100110"
    num_commande: Optional[str] = "CMD-10011001"
    num_facture: Optional[str] = "FAC-10011001"
    date_commande: Optional[str] = None
    date_facture: Optional[str] = None
    payment: Optional[str] = "Carte Bancaire"
    remise: Optional[str] = "0,00"
    port: Optional[str] = "0,00"
    total: Optional[str] = "239,99"
    items: Optional[list[DafyItem]] = None


class DartyItem(ExtraAllow):
    sku: Optional[str] = "DAR-1001"
    desc: Optional[str] = "Téléviseur LED 4K Ultra HD"
    desc2: Optional[str] = "Garantie 2 ans incluse"
    qte: Optional[str] = "1"
    ht: Optional[str] = "399,00"
    tva: Optional[str] = "20,00"
    date_delivrance: Optional[str] = None


class FactureDartyRequest(ExtraAllow):
    nom: Optional[str] = "Martin Lucas"
    adresse: Optional[str] = "12 Rue des Fleurs"
    cp_ville: Optional[str] = "75011 Paris"
    pays: Optional[str] = "France"
    livraison_nom: Optional[str] = "Martin Lucas"
    livraison_adresse: Optional[str] = "12 Rue des Fleurs"
    livraison_cp_ville: Optional[str] = "75011 Paris"
    livraison_pays: Optional[str] = "France"
    num_commande: Optional[str] = "DAR-100110"
    date_commande: Optional[str] = None
    date_facture: Optional[str] = None
    payment: Optional[str] = "Carte Bancaire"
    total: Optional[str] = "478,80"
    items: Optional[list[DartyItem]] = None


class BoulangerItem(ExtraAllow):
    nom: Optional[str] = "PACK ADEQWAT Powerbank + Chargeur + C"
    code: Optional[str] = "0008010892"
    qte: Optional[str] = "1"
    pu_ttc: Optional[str] = "49,97"
    tva_taux: Optional[str] = "20,00"
    total_ttc: Optional[str] = "49,97"
    ecopart: Optional[str] = "0,02"
    garantie_non_retenue: Optional[str] = None
    garantie_reparation: Optional[str] = "Garantie Réparation jusqu'au 19.12.2025"
    dispo_pieces_label: Optional[str] = "Disponibilité des pièces détachées (donnée fournisseur) :"
    dispo_pieces: Optional[str] = "Pas de pièce disponible"
    vendeur: Optional[str] = None


class FactureBoulangerRequest(ExtraAllow):
    nom: Optional[str] = "Martin Lucas"
    adresse: Optional[str] = "12 Rue des Fleurs"
    cp_ville: Optional[str] = "75011 Paris"
    client_nom: Optional[str] = None
    client_rue: Optional[str] = None
    client_cp_ville: Optional[str] = None
    client_num: Optional[str] = "29468065"
    client_tel: Optional[str] = None
    mode: Optional[str] = "en_ligne"
    seller_type: Optional[str] = "boulanger"
    facture_num: Optional[str] = "F905 FQ09058-23/002"
    facture_date: Optional[str] = None
    facture_time: Optional[str] = "19:23"
    facture_page: Optional[str] = "1/1"
    barcode_val: Optional[str] = "0008010892"
    store_nom: Optional[str] = "BOULANGER WWW.BOULANGER.COM"
    store_rue1: Optional[str] = "CRT - BP137"
    store_rue2: Optional[str] = "AV DE LA MOTTE"
    store_lieu: Optional[str] = None
    store_cp_ville: Optional[str] = "59810 LESQUIN"
    store_siret: Optional[str] = "34738457002017"
    store_tel: Optional[str] = "03 86 42 53 08"
    seller_name: Optional[str] = None
    seller_rue: Optional[str] = None
    seller_cp_ville: Optional[str] = None
    seller_siret: Optional[str] = None
    seller_tva: Optional[str] = None
    seller_capital: Optional[str] = None
    seller_rcs: Optional[str] = None
    extra_line_nom: Optional[str] = "BOULANGER FRAIS DE PORT"
    extra_line_code: Optional[str] = "0001037258"
    extra_line_qte: Optional[str] = "1"
    extra_line_pu_ttc: Optional[str] = "3,99"
    extra_line_tva: Optional[str] = "20,00"
    extra_line_total: Optional[str] = "3,99"
    club_nom: Optional[str] = "Le Club"
    club_code: Optional[str] = "0001185162"
    club_qte: Optional[str] = "1"
    club_pu_ttc: Optional[str] = "0,00"
    club_tva_taux: Optional[str] = "20,00"
    club_total_ttc: Optional[str] = "0,00"
    total_ht: Optional[str] = "44,99"
    total_ttc: Optional[str] = "53,98"
    dont_tva: Optional[str] = "9,00"
    dont_tva_taux: Optional[str] = "20,00"
    dont_ecopart: Optional[str] = "0,02"
    reglement_mode: Optional[str] = "Règlements perçus"
    reglement_montant: Optional[str] = "53,98"
    items: Optional[list[BoulangerItem]] = None


class FactureGazRequest(ExtraAllow):
    nom: Optional[str] = "Martin Lucas"
    adresse: Optional[str] = "12 Rue des Fleurs"
    cp_ville: Optional[str] = "75011 Paris"
    date_facture: Optional[str] = None
    num_facture: Optional[str] = "100110010001"
    num_client: Optional[str] = "100110010"
    num_contrat: Optional[str] = "100110011"
    lieu_pce: Optional[str] = "1ML*100 11"
    lieu_bat: Optional[str] = "BAT A 1ET"
    montant_gaz: Optional[str] = "84,50"
    montant_prestations: Optional[str] = "15,50"
    montant_ht: Optional[str] = "83,33"
    montant_tva: Optional[str] = "16,67"
    compte: Optional[str] = "00010011001"


class LoroPianaItem(ExtraAllow):
    sku: Optional[str] = "LP-1001"
    desc: Optional[str] = "PULL EN CACHEMIRE COL ROND"
    qte: Optional[str] = "1"
    prix: Optional[str] = "1 250,00"


class FactureLoroPianaRequest(ExtraAllow):
    nom: Optional[str] = "Martin"
    prenom: Optional[str] = "Lucas"
    num_ticket: Optional[str] = "001001"
    ticket_caisse: Optional[str] = "CAISSE 01"
    date_ticket: Optional[str] = None
    caissier: Optional[str] = "Martin Lucas"
    payment: Optional[str] = "CB"
    monnaie: Optional[str] = "0,00"
    tva_rate: Optional[str] = "20,00"
    total: Optional[str] = "1 250,00"
    items: Optional[list[LoroPianaItem]] = None


class PackMotoItem(ExtraAllow):
    sku: Optional[str] = "PM-1001"
    desc: Optional[str] = "Gants Moto Cuir Renforcé Homme"
    qte: Optional[str] = "1"
    pu: Optional[str] = "79,90"
    tva: Optional[str] = "20.00"


class FacturePackMotoRequest(ExtraAllow):
    nom: Optional[str] = "Martin Lucas"
    adresse: Optional[str] = "12 Rue des Fleurs"
    cp_ville: Optional[str] = "75011 Paris"
    pays: Optional[str] = "France"
    livraison_nom: Optional[str] = "Martin Lucas"
    livraison_societe: Optional[str] = ""
    livraison_adresse: Optional[str] = "12 Rue des Fleurs"
    livraison_cp_ville: Optional[str] = "75011 Paris"
    livraison_pays: Optional[str] = "France"
    num_facture: Optional[str] = "FAC-2024-1001"
    date_facture: Optional[str] = None
    num_commande: Optional[str] = "CMD-2024-1001"
    date_commande: Optional[str] = None
    payment: Optional[str] = "Carte Bancaire"
    transporteur: Optional[str] = "Colissimo Domicile"
    frais: Optional[str] = "0.00"
    total: Optional[str] = "95,88"
    items: Optional[list[PackMotoItem]] = None


class DiorItem(ExtraAllow):
    ref: Optional[str] = "KC1322VNI"
    desc: Optional[str] = "S799 / T40 SNEAKERS TOILE ET VEAU"
    qty: Optional[str] = "1"
    unit_price: Optional[str] = "790,00"
    total: Optional[str] = "790,00"


class FactureDiorRequest(ExtraAllow):
    prenom: Optional[str] = "Lucas"
    nom: Optional[str] = "Martin"
    duplicata: Optional[str] = "DUPLICATA"
    contact_line_0: Optional[str] = "Christian Dior Couture Paris"
    contact_line_1: Optional[str] = "30 Avenue Montaigne"
    contact_line_2: Optional[str] = "FR 612 035 832"
    contact_line_3: Optional[str] = "75008 Paris"
    contact_line_4: Optional[str] = "Tél : 01 45 63 12 51"
    client_nom: Optional[str] = None
    client_email: Optional[str] = "martin.lucas@gmail.com"
    client_tel: Optional[str] = "0658692545"
    vente_title: Optional[str] = "VENTE"
    oper: Optional[str] = "Maria"
    trans: Optional[str] = "10738"
    store: Optional[str] = "FRpar01"
    store_num: Optional[str] = "3"
    date_vente: Optional[str] = None
    heure_vente: Optional[str] = None
    date_str: Optional[str] = None
    page_info: Optional[str] = "Page:  1 / 1"
    vendeur: Optional[str] = "Maria"
    count_label: Optional[str] = "1 produit(s)"
    total_facture: Optional[str] = "790,00"
    payment_method: Optional[str] = "Cash"
    payment_amount: Optional[str] = "800,00"
    rendu_amount: Optional[str] = "10,00"
    total_ht: Optional[str] = "658,33"
    tva_product: Optional[str] = "TVA FR Product"
    tva_rate: Optional[str] = "TVA 20%"
    tva_amount: Optional[str] = "131,67"
    total_ttc: Optional[str] = "790,00"
    code: Optional[str] = "1066000"
    items: Optional[list[DiorItem]] = None


class JacquemusItem(ExtraAllow):
    nom: Optional[str] = "Le pichoto"
    ref: Optional[str] = "213BA01-213"
    couleur: Optional[str] = "Noir"
    taille: Optional[str] = "Unique"
    pays: Optional[str] = "Italie"
    prix: Optional[str] = "€360.00"
    qte: Optional[str] = "1"
    sous_total: Optional[str] = "€360.00"


class FactureJacquemusRequest(ExtraAllow):
    prenom: Optional[str] = "Lucas"
    nom: Optional[str] = "Martin"
    contact_email: Optional[str] = "boutique@jacquemus.com"
    client_nom: Optional[str] = None
    adresse: Optional[str] = "12 Rue des Fleurs"
    client_rue: Optional[str] = "12 Rue des Fleurs"
    complement: Optional[str] = ""
    client_complement: Optional[str] = ""
    cp: Optional[str] = "75011"
    ville: Optional[str] = "Paris"
    client_ville_cp: Optional[str] = "75011 Paris"
    client_pays: Optional[str] = "France"
    client_tel: Optional[str] = "06 12 34 56 78"
    val_commande: Optional[str] = "20541994"
    val_facture: Optional[str] = "48949848"
    date_commande: Optional[str] = None
    heure_commande: Optional[str] = None
    val_date: Optional[str] = None
    val_payment: Optional[str] = "Paiement en 3 fois sans frais"
    val_delivery: Optional[str] = "United Parcel Service - UPS Standard"
    tot_sous_total: Optional[str] = "€300.00"
    tot_tva: Optional[str] = "€60.00"
    tot_livraison: Optional[str] = "GRATUIT"
    tot_total: Optional[str] = "€360.00"
    items: Optional[list[JacquemusItem]] = None


class ChanelItem(ExtraAllow):
    desc: Optional[str] = "Eau de parfum vaporisateur - 100ml"
    ref: Optional[str] = "107360"
    qty: Optional[str] = "1"
    unit_price: Optional[str] = "132,00"
    total: Optional[str] = "132,00"


class FactureChanelRequest(ExtraAllow):
    civilite: Optional[str] = "Monsieur"
    prenom: Optional[str] = "Lucas"
    nom: Optional[str] = "Martin"
    client_name: Optional[str] = None
    adresse: Optional[str] = "12 Rue des Fleurs"
    client_address_1: Optional[str] = None
    cp: Optional[str] = "75011"
    ville: Optional[str] = "Paris"
    client_address_2: Optional[str] = None
    pays: Optional[str] = "France"
    client_address_3: Optional[str] = None
    client_code: Optional[str] = "AA01454795"
    store_line_1: Optional[str] = "31 rue Cambon - 75001 PARIS"
    store_line_2: Optional[str] = "TEL : +33 (0) 1 44 50 66 00"
    date_vente: Optional[str] = None
    heure_vente: Optional[str] = None
    date_str: Optional[str] = None
    facture_num: Optional[str] = "735179"
    caisse_num: Optional[str] = "AA1/AA105"
    folio_num: Optional[str] = "1"
    conseiller: Optional[str] = "Amélie"
    accueil_text: Optional[str] = None
    items: Optional[list[ChanelItem]] = None
    articles_count: Optional[str] = None
    total_ht: Optional[str] = "110,00"
    total_tva: Optional[str] = "22,00"
    total_ttc: Optional[str] = "132,00"
    mode_paiement: Optional[str] = "ESPECES EUROS"
    paiement: Optional[str] = None


class FredItem(ExtraAllow):
    code: Optional[str] = "0B0006-6B0275"
    ref: Optional[str] = None
    quantite: Optional[str] = "1"
    qte: Optional[str] = "1"
    qty: Optional[str] = "1"
    designation: Optional[str] = "BRACELET FORCE 10 GRAND MODÈLE OR JAUNE\nAJUSTABLE\nFRED PARIS\nRéférence: 6B0146\nGravure: 1012846"
    desc: Optional[str] = None
    prix_ttc: Optional[str] = "3 250.00"
    unit_price: Optional[str] = None
    total: Optional[str] = None


class FactureFredRequest(ExtraAllow):
    civilite: Optional[str] = "Monsieur"
    prenom: Optional[str] = "David"
    nom: Optional[str] = "Kazarian"
    adresse: Optional[str] = "118 Avenue Molière"
    cp: Optional[str] = "1190"
    ville: Optional[str] = "Bruxelles"
    pays: Optional[str] = "Belgique"
    client_tel: Optional[str] = None
    client_code: Optional[str] = None
    ville_emission: Optional[str] = "Neuilly Sur Marne"
    date_facture: Optional[str] = None
    date_lieu: Optional[str] = None
    num_facture: Optional[str] = "8259"
    facture_num: Optional[str] = "8259"
    facture_titre: Optional[str] = None
    store_name: Optional[str] = "PRINTEMPS PARLY 2"
    store_code: Optional[str] = "5921489590020"
    mode_paiement: Optional[str] = "Carte Bleue (Eu)"
    payment_label: Optional[str] = "Carte Bleue (Eu)"
    total_ttc: Optional[str] = None
    items: Optional[list[FredItem]] = None


class NocibeItem(ExtraAllow):
    ref: Optional[str] = "222876"
    desc: Optional[str] = "Sauvage - Parfum pour homme - Notes santal & fève tonka - 100ml"
    tva_rate: Optional[str] = "20.00"
    qty: Optional[str] = "1"
    unit_price: Optional[str] = "91.25"
    remise: Optional[str] = "18.25"
    remise_code: Optional[str] = "98313 - 25% des 79€"
    net_ht: Optional[str] = "91.25"


class FactureNocibeRequest(ExtraAllow):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    adresse: Optional[str] = None
    cp: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    livraison_prenom: Optional[str] = None
    livraison_adresse: Optional[str] = None
    livraison_cp: Optional[str] = None
    facture_num: Optional[str] = "27414163"
    date_emission: Optional[str] = "23/08/2023"
    facturation_titre: Optional[str] = "ADRESSE DE FACTURATION"
    client_nom: Optional[str] = "Martin Lucas"
    client_rue: Optional[str] = "12 Rue des Fleurs"
    client_ville: Optional[str] = "75011 Paris"
    client_pays: Optional[str] = "FR"
    livraison_titre: Optional[str] = "ADRESSE DE LIVRAISON"
    livraison_nom: Optional[str] = "Martin Lucas"
    livraison_rue: Optional[str] = "12 Rue des Fleurs"
    livraison_ville: Optional[str] = "75011 Paris"
    livraison_pays: Optional[str] = "FR"
    commande_date: Optional[str] = "23/08/2023"
    commande_mode: Optional[str] = "Click & Collect"
    commande_expedition: Optional[str] = "23/08/2023"
    commande_etat: Optional[str] = "Préparation Totale"
    items: Optional[list[NocibeItem]] = None
    total_ht: Optional[str] = "91,25"
    total_tva: Optional[str] = "18.25"
    total_ttc: Optional[str] = "109.50"
    tva_rate_pct: Optional[str] = "20.00 %"
    tva_base_ht: Optional[str] = "91.25"
    tva_montant: Optional[str] = "18.25"
    reglement_date: Optional[str] = "23/08/2023"
    reglement_mode: Optional[str] = "Carte Bleue"
    reglement_montant: Optional[str] = "109.50"


class SfrItem(ExtraAllow):
    numero_ligne: Optional[str] = "06 12 34 56 78"
    description: Optional[str] = "Pénalités de retard pour échec de prélèvement: 7.5 €"
    date: Optional[str] = "2026-09-01"
    montant_ttc: Optional[str] = "7.5 €"


class FactureSfrRequest(ExtraAllow):
    nom: Optional[str] = "Martin"
    prenom: Optional[str] = "Lucas"
    adresse: Optional[str] = "12 Rue des Fleurs"
    cp: Optional[str] = "75011"
    ville: Optional[str] = "Paris"
    destinataire_nom: Optional[str] = "LUCAS MARTIN"
    destinataire_adresse: Optional[str] = "12 Rue des Fleurs"
    destinataire_cp_ville: Optional[str] = "75011 Paris"
    titulaire_ligne: Optional[str] = "LUCAS MARTIN"
    num_compte_client: Optional[str] = "2LH5L"
    date_facture: Optional[str] = "2026-09-01"
    num_facture: Optional[str] = "169793"
    montant_ht: Optional[str] = "6.25€"
    montant_tva: Optional[str] = "1.25€"
    taux_tva: Optional[str] = "20.0 %"
    total_ttc: Optional[str] = "7.5€"
    solde_ht: Optional[str] = "0€"
    solde_ttc: Optional[str] = "0€"
    net_a_payer_ht: Optional[str] = "6.25€"
    net_a_payer_ttc: Optional[str] = "7.5€"
    total_facture_ht: Optional[str] = "6.25"
    total_facture_ttc: Optional[str] = "7.5"
    mention_encaissement: Optional[str] = None
    footer_note: Optional[str] = None
    sepa_ligne1: Optional[str] = "Le prélèvement de votre facture se fera sur le compte no FPELFR21 FR76XXXXXXXXXXXXXXX5545 par l'ICS no xxx"
    sepa_ligne2: Optional[str] = "conformément à votre Mandat de prélèvement SEPA référencé 2LH5L-00000 le 2026-10-01."
    items: Optional[list[SfrItem]] = None


class FactureGenerateRequest(ExtraAllow):
    pass


FACTURE_MODELS = {
    "adidas": FactureAdidasRequest,
    "amazon": FactureAmazonRequest,
    "fnac": FactureFnacRequest,
    "nike": FactureNikeRequest,
    "ami": FactureAmiRequest,
    "burberry": FactureBurberryRequest,
    "cdiscount": FactureCdiscountRequest,
    "dafy": FactureDafyRequest,
    "darty": FactureDartyRequest,
    "boulanger": FactureBoulangerRequest,
    "gaz": FactureGazRequest,
    "engie": FactureGazRequest,
    "loro_piana": FactureLoroPianaRequest,
    "pack_moto": FacturePackMotoRequest,
    "dior": FactureDiorRequest,
    "jacquemus": FactureJacquemusRequest,
    "chanel": FactureChanelRequest,
    "channel": FactureChanelRequest,
    "fred": FactureFredRequest,
    "nocibe": FactureNocibeRequest,
    "sfr": FactureSfrRequest,
}


COUNTRY_NAME_TO_CODE = {
    "FRANCE": "FR",
    "BELGIQUE": "BE",
    "SUISSE": "CH",
    "LUXEMBOURG": "LU",
    "MONACO": "MC",
    "ANDORRE": "AD",
    "ALLEMAGNE": "DE",
    "ESPAGNE": "ES",
    "ITALIE": "IT",
    "ROYAUME-UNI": "GB",
    "ROYAUME UNI": "GB",
    "PORTUGAL": "PT",
    "PAYS-BAS": "NL",
    "PAYS BAS": "NL",
    "AUTRICHE": "AT",
    "IRLANDE": "IE",
    "POLOGNE": "PL",
    "SUEDE": "SE",
    "SUÈDE": "SE",
    "NORVEGE": "NO",
    "NORVÈGE": "NO",
    "DANEMARK": "DK",
    "FINLANDE": "FI",
    "GRECE": "GR",
    "GRÈCE": "GR",
    "REPUBLIQUE TCHEQUE": "CZ",
    "RÉPUBLIQUE TCHÈQUE": "CZ",
    "ROUMANIE": "RO",
    "HONGRIE": "HU",
    "SLOVAQUIE": "SK",
    "BULGARIE": "BG",
    "CROATIE": "HR",
    "SLOVENIE": "SI",
    "SLOVÉNIE": "SI",
    "ESTONIE": "EE",
    "LETTONIE": "LV",
    "LITUANIE": "LT",
    "CHYPRE": "CY",
    "MALTE": "MT",
    "ISLANDE": "IS",
    "ETATS-UNIS": "US",
    "ÉTATS-UNIS": "US",
    "CANADA": "CA",
    "MAROC": "MA",
    "ALGERIE": "DZ",
    "ALGÉRIE": "DZ",
    "TUNISIE": "TN",
}


def dump_model(model: BaseModel) -> dict:
    if hasattr(model, "model_dump"):
        return model.model_dump(exclude_none=True)
    data = model.dict()
    return {key: value for key, value in data.items() if value is not None}


def parse_facture_payload(issuer: str, data: dict | None) -> dict:
    payload = {key: value for key, value in dict(data or {}).items() if value is not None}
    if issuer in ("adidas", "amazon"):
        for k in ("pays", "livraison_pays"):
            if k in payload and payload[k]:
                p = str(payload[k]).strip()
                if len(p) > 2:
                    p_upper = p.upper()
                    payload[k] = COUNTRY_NAME_TO_CODE.get(p_upper, p_upper[:2])
                elif len(p) == 2:
                    payload[k] = p.upper()
    if issuer not in ("dior", "jacquemus", "chanel", "channel", "fred", "boulanger", "sfr") and "prenom" in payload and "nom" in payload and payload["nom"] and payload["prenom"]:
        prenom = str(payload["prenom"]).strip()
        nom = str(payload["nom"]).strip()
        if prenom and prenom not in nom:
            payload["nom"] = f"{nom} {prenom}".strip()
    if "livraison_prenom" in payload and "livraison_nom" in payload and payload["livraison_nom"] and payload["livraison_prenom"]:
        l_prenom = str(payload["livraison_prenom"]).strip()
        l_nom = str(payload["livraison_nom"]).strip()
        if l_prenom and l_prenom not in l_nom:
            payload["livraison_nom"] = f"{l_nom} {l_prenom}".strip()
    if "facturation_prenom" in payload and "facturation_nom" in payload and payload["facturation_nom"] and payload["facturation_prenom"]:
        f_prenom = str(payload["facturation_prenom"]).strip()
        f_nom = str(payload["facturation_nom"]).strip()
        if f_prenom and f_prenom not in f_nom:
            payload["facturation_nom"] = f"{f_nom} {f_prenom}".strip()
    if issuer == "ami":
        nom = str(payload.get("nom") or "").strip()
        prenom = str(payload.get("prenom") or "").strip()
        if nom or prenom:
            full_nom = f"{nom} {prenom}".strip() if (nom and prenom and prenom not in nom) else (nom or prenom)
            adr = str(payload.get("adresse") or "").strip()
            if not adr or adr == "Martin Lucas - 12 Rue des Fleurs":
                payload["adresse"] = f"{full_nom} - 12 Rue des Fleurs"
            elif not adr.startswith(full_nom):
                if " - " in adr:
                    parts = adr.split(" - ", 1)
                    payload["adresse"] = f"{full_nom} - {parts[1]}"
                else:
                    payload["adresse"] = f"{full_nom} - {adr}"
        else:
            ville = str(payload.get("ville") or "").strip()
            adresse = str(payload.get("adresse") or "").strip()
            if ville and adresse and not adresse.startswith(f"{ville} -"):
                payload["adresse"] = f"{ville} - {adresse}"
    if "cp" in payload or "ville" in payload:
        cp = str(payload.get("cp") or "").strip()
        ville = str(payload.get("ville") or "").strip()
        if cp or ville:
            payload["cp_ville"] = f"{cp} {ville}".strip()
    if "livraison_cp" in payload or "livraison_ville" in payload:
        l_cp = str(payload.get("livraison_cp") or "").strip()
        l_ville = str(payload.get("livraison_ville") or "").strip()
        if l_cp or l_ville:
            payload["livraison_cp_ville"] = f"{l_cp} {l_ville}".strip()
    if "facturation_cp" in payload or "facturation_ville" in payload:
        f_cp = str(payload.get("facturation_cp") or "").strip()
        f_ville = str(payload.get("facturation_ville") or "").strip()
        if f_cp or f_ville:
            payload["facturation_cp_ville"] = f"{f_cp} {f_ville}".strip()
    if "seller_cp" in payload or "seller_ville" in payload:
        s_cp = str(payload.get("seller_cp") or "").strip()
        s_ville = str(payload.get("seller_ville") or "").strip()
        if s_cp or s_ville:
            payload["seller_cp_ville"] = f"{s_cp} {s_ville}".strip()
    if issuer == "loro_piana":
        nom = str(payload.get("nom") or "").strip()
        prenom = str(payload.get("prenom") or "").strip()
        if (nom or prenom) and (not payload.get("caissier") or payload.get("caissier") == "Martin Lucas"):
            payload["caissier"] = f"{nom} {prenom}".strip() if (nom and prenom and prenom not in nom) else (nom or prenom)
    if issuer == "fnac":
        nom_val = str(payload.get("nom") or "").strip()
        prenom_val = str(payload.get("prenom") or "").strip()
        if nom_val or prenom_val:
            full = f"{nom_val} {prenom_val}".strip() if (nom_val and prenom_val and prenom_val not in nom_val) else (nom_val or prenom_val)
            if not payload.get("livraison_nom"):
                payload["livraison_nom"] = full
            if not payload.get("facturation_nom"):
                payload["facturation_nom"] = full
        if "adresse" in payload:
            if not payload.get("livraison_adresse"):
                payload["livraison_adresse"] = payload["adresse"]
            if not payload.get("facturation_adresse"):
                payload["facturation_adresse"] = payload["adresse"]
        if "cp_ville" in payload:
            if not payload.get("livraison_cp_ville"):
                payload["livraison_cp_ville"] = payload["cp_ville"]
            if not payload.get("facturation_cp_ville"):
                payload["facturation_cp_ville"] = payload["cp_ville"]
    if issuer == "jacquemus":
        nom_val = str(payload.get("nom") or "").strip()
        prenom_val = str(payload.get("prenom") or "").strip()
        if (nom_val or prenom_val) and not payload.get("client_nom"):
            payload["client_nom"] = f"{nom_val} {prenom_val}".strip() if (nom_val and prenom_val) else (nom_val or prenom_val)
        if not payload.get("client_nom"):
            payload["client_nom"] = "Martin Lucas"
    if issuer == "dior":
        nom = str(payload.get("nom") or "").strip()
        prenom = str(payload.get("prenom") or "").strip()
        civ = str(payload.get("civilite") or "Mr").strip()
        if (nom or prenom) and not payload.get("client_nom"):
            parts = [civ] if civ else []
            if nom:
                parts.append(nom.upper())
            if prenom:
                parts.append(prenom)
            payload["client_nom"] = " ".join(parts)
    if issuer == "nocibe":
        nom = str(payload.get("nom") or "").strip()
        prenom = str(payload.get("prenom") or "").strip()
        if nom and prenom and prenom not in nom:
            payload["client_nom"] = f"{nom} {prenom} "
        elif nom and not payload.get("client_nom"):
            payload["client_nom"] = f"{nom} "
        if "adresse" in payload and not payload.get("client_rue"):
            payload["client_rue"] = payload["adresse"]
        cp = str(payload.get("cp") or "").strip()
        ville = str(payload.get("ville") or "").strip()
        if cp and ville and cp not in ville:
            payload["client_ville"] = f"{cp} {ville}"
        elif cp and not ville:
            payload["client_ville"] = cp
        elif (cp or ville) and not payload.get("client_ville"):
            payload["client_ville"] = payload.get("cp_ville") or f"{cp} {ville}".strip()
        if "pays" in payload and not payload.get("client_pays"):
            payload["client_pays"] = payload["pays"]
        l_nom = str(payload.get("livraison_nom") or "").strip()
        l_prenom = str(payload.get("livraison_prenom") or "").strip()
        if not l_nom and payload.get("client_nom"):
            payload["livraison_nom"] = payload["client_nom"]
        elif l_nom and l_prenom and l_prenom not in l_nom:
            payload["livraison_nom"] = f"{l_nom} {l_prenom} "
        elif l_nom and not payload.get("livraison_nom"):
            payload["livraison_nom"] = f"{l_nom} "
        if "livraison_adresse" in payload and not payload.get("livraison_rue"):
            payload["livraison_rue"] = payload["livraison_adresse"]
        elif not payload.get("livraison_rue") and payload.get("client_rue"):
            payload["livraison_rue"] = payload["client_rue"]
        l_cp = str(payload.get("livraison_cp") or "").strip()
        l_ville = str(payload.get("livraison_ville") or "").strip()
        if l_cp and l_ville and l_cp not in l_ville:
            payload["livraison_ville"] = f"{l_cp} {l_ville}"
        elif l_cp and not l_ville:
            payload["livraison_ville"] = l_cp
        elif (l_cp or l_ville) and not payload.get("livraison_ville"):
            payload["livraison_ville"] = payload.get("livraison_cp_ville") or f"{l_cp} {l_ville}".strip()
        elif not payload.get("livraison_ville") and payload.get("client_ville"):
            payload["livraison_ville"] = payload.get("client_ville")
        if not payload.get("livraison_pays") and payload.get("client_pays"):
            payload["livraison_pays"] = payload["client_pays"]
    if issuer == "boulanger":
        nom = str(payload.get("nom") or "").strip()
        prenom = str(payload.get("prenom") or "").strip()
        if nom and prenom and not payload.get("client_nom"):
            payload["client_nom"] = f"{prenom} {nom}"
        elif nom and not payload.get("client_nom"):
            payload["client_nom"] = nom
        if "adresse" in payload and not payload.get("client_rue"):
            payload["client_rue"] = payload["adresse"]
        if ("cp" in payload or "ville" in payload) and not payload.get("client_cp_ville"):
            cp = str(payload.get("cp") or "").strip()
            ville = str(payload.get("ville") or "").strip()
            if cp or ville:
                payload["client_cp_ville"] = f"{cp} {ville}".strip()
        if "store_cp" in payload or "store_ville" in payload:
            s_cp = str(payload.get("store_cp") or "").strip()
            s_ville = str(payload.get("store_ville") or "").strip()
            if (s_cp or s_ville) and not payload.get("store_cp_ville"):
                payload["store_cp_ville"] = f"{s_cp} {s_ville}".strip()
        if "seller_cp" in payload or "seller_ville" in payload:
            sl_cp = str(payload.get("seller_cp") or "").strip()
            sl_ville = str(payload.get("seller_ville") or "").strip()
            if (sl_cp or sl_ville) and not payload.get("seller_cp_ville"):
                payload["seller_cp_ville"] = f"{sl_cp} {sl_ville}".strip()
    if issuer == "sfr":
        nom = str(payload.get("nom") or "").strip()
        prenom = str(payload.get("prenom") or "").strip()
        if (nom or prenom) and not payload.get("destinataire_nom"):
            full = f"{prenom} {nom}".strip().upper()
            payload["destinataire_nom"] = full
        if (nom or prenom) and not payload.get("titulaire_ligne"):
            full = f"{prenom} {nom}".strip().upper()
            payload["titulaire_ligne"] = full
        if "adresse" in payload and not payload.get("destinataire_adresse"):
            payload["destinataire_adresse"] = payload["adresse"]
        cp = str(payload.get("cp") or "").strip()
        ville = str(payload.get("ville") or "").strip()
        if (cp or ville) and not payload.get("destinataire_cp_ville"):
            payload["destinataire_cp_ville"] = f"{cp} {ville}".strip()
    model_cls = FACTURE_MODELS.get(issuer)
    if model_cls is None:
        return payload
    return dump_model(model_cls(**payload))
