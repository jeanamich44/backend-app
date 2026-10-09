import random
import re

CURRENT_BANK_TYPE = "lbp"
CURRENT_ALLOW_EPARGNE = False
CURRENT_CONTACTS_EMIS = []
CURRENT_CONTACTS_RECU = []

# ==========================================
# 1. DONNÉES GLOBALES (BASE DE MARCHANDS)
# ==========================================
MERCHANTS_SUPERMARCHE = ["LECLERC", "CARREFOUR", "AUCHAN", "INTERMARCHE", "LIDL", "ALDI", "GRAND FRAIS", "MONOPRIX", "U EXPRESS", "CASINO"]
MERCHANTS_CARBURANT = ["TOTALENERGIES", "RELAIS ESSO", "STATION SERVICE", "RELAIS BP", "STATION CARREFOUR", "ENI", "AVIA"]
MERCHANTS_RESTO = ["MCDONALDS", "BURGER KING", "KFC", "UBER EATS", "DELIVEROO", "PIZZA HUT", "BOULANGERIE [VILLE]", "BRASSERIE [VILLE]", "SUSHI SHOP"]
MERCHANTS_SHOPPING = ["AMAZON", "FNAC", "DARTY", "DECATHLON", "ZARA", "H&M", "VINTED", "IKEA", "LEROY MERLIN", "ASOS", "ZALANDO PAYMEN"]
MERCHANTS_LOISIRS = ["CINEMA PATHE", "UGC", "PHARMACIE [VILLE]", "TABAC PRESSE [VILLE]"]
MERCHANTS_ONLINE = ["NETFLIX COM", "SPOTIFY", "AMAZON PRIME", "APPLE COM BILL", "PAYPAL *"]

DEFAULT_BANK_NAMES = {
    "lbp": "LA BANQUE POSTALE",
    "sg": "SOCIETE GENERALE",
    "ca": "CREDIT AGRICOLE",
    "bnp": "BNP PARIBAS",
    "lcl": "LCL",
    "bp": "BANQUE POPULAIRE",
    "ce": "CAISSE D EPARGNE",
    "cm": "CREDIT MUTUEL",
    "cic": "CIC",
    "boursobank": "BOURSOBANK",
    "revolut": "REVOLUT",
}

PRELEVEMENT_TYPES = {
    'EDF': {
        "nom": "EDF clients particul",
        "ident": "FR47EDF001007",
        "format": "IDENT_ONLY",
        "montants_base": 68.0
    },
    'ENGIE': {
        "nom": "Engie",
        "ident": "FR03SYM002381",
        "mandat_template": "00S0{digits}",
        "montants_base": 54.0
    },
    'FREE_MOBILE': {
        "nom": "FREE MOBILE",
        "ident": "FR07ZZZ591778",
        "mandat_template": "FM-{digits}-1",
        "montants": [9.99, 15.99, 19.99]
    },
    'FREE_TELECOM': {
        "nom": "Free Telecom",
        "ident": "FR83ZZZ459654",
        "mandat_template": "{digits}",
        "montants": [29.99, 39.99, 49.99]
    },
    'GMF': {
        "nom": "GMF ASSURANCES",
        "ident": "FR92ZZZ620803",
        "format": "GMF_SPECIAL",
        "montants_base": 44.0
    },
    'MUTUELLE': {
        "nom": "MNFCT COTISATIONS-MU",
        "ident": "FR92ZZZ127655",
        "format": "MNFCT_STYLE",
        "montants_base": 42.0
    },
    'LOGIREP': {
        "nom": "LOGIREP",
        "ident": "FR97ZZZ607618",
        "format": "LOGIREP_STYLE",
        "montants_base": 650.0
    },
    'FLOA': {
        "nom": "Floa SA",
        "ident": "FR40ZZZ457615",
        "mandat_template": "14628000{digits}",
        "montants_base": 35.0
    },
    'ORANGE': {
        "nom": "ORANGE FRANCE",
        "ident": "FR48ZZZ918273",
        "mandat_template": "ORG-{digits}-1",
        "montants": [14.99, 34.99, 69.99]
    },
    'BOUYGUES': {
        "nom": "BOUYGUES TELECOM",
        "ident": "FR32ZZZ837462",
        "mandat_template": "BYG-{digits}-01",
        "montants": [14.99, 24.99, 34.99]
    },
    'EAU_SERVICES': {
        "nom": "VEOLIA EAU",
        "ident": "FR67ZZZ829103",
        "mandat_template": "VEO-00{digits}",
        "montants_base": 34.0
    },
    'MAIF': {
        "nom": "MAIF ASSURANCES",
        "ident": "FR22ZZZ192834",
        "mandat_template": "MAIF-{digits}",
        "montants_base": 48.0
    },
    'MACIF': {
        "nom": "MACIF ASSURANCES",
        "ident": "FR18ZZZ736251",
        "mandat_template": "MAC-{digits}-A",
        "montants_base": 39.0
    },
    'MGEN': {
        "nom": "MGEN SECTION EXTRA SCOLAIRE",
        "ident": "FR41ZZZ392817",
        "mandat_template": "MGN-{digits}-01",
        "montants_base": 65.0
    },
    'MNT': {
        "nom": "MNT MUTUELLE",
        "ident": "FR59ZZZ491823",
        "mandat_template": "MNT-ADH-{digits}",
        "montants_base": 55.0
    },
    'INTERIALE': {
        "nom": "INTERIALE MUTUELLE",
        "ident": "FR73ZZZ628190",
        "mandat_template": "INT-CONTRAT-{digits}",
        "montants_base": 58.0
    },
    'CASDEN': {
        "nom": "CASDEN BANQUE POPULAIRE",
        "ident": "FR15ZZZ293847",
        "mandat_template": "CSD-PRET-{digits}",
        "montants_base": 115.0
    },
    'PRO_BTP': {
        "nom": "PRO BTP COTISATIONS",
        "ident": "FR89ZZZ239481",
        "mandat_template": "BTP-ADH-{digits}",
        "montants_base": 140.0
    },
    'SMABTP': {
        "nom": "SMABTP ASSURANCE DECENNALE",
        "ident": "FR14ZZZ839201",
        "mandat_template": "SMA-DEC-{digits}",
        "montants_base": 185.0
    },
    'TOTAL_FLEET': {
        "nom": "TOTALENERGIES FLEET CARBURANT",
        "ident": "FR65ZZZ491028",
        "mandat_template": "TOT-FLT-{digits}",
        "montants_base": 95.0
    },
    'TELEPEAGE': {
        "nom": "APRR TELEPEAGE",
        "ident": "FR02ZZZ192837",
        "mandat_template": "APRR-BADGE-{digits}",
        "montants_base": 45.0
    },
    'MAIRIE_SCOLAIRE': {
        "nom": "REGIE SCOLAIRE ET PERISCOLAIRE",
        "ident": "FR33ZZZ102938",
        "mandat_template": "MAI-PERISCOL-{digits}",
        "montants_base": 95.0
    },
    'CRECHE': {
        "nom": "CRECHE MUNICIPALE",
        "ident": "FR88ZZZ492817",
        "mandat_template": "CRE-ACCUEIL-{digits}",
        "montants_base": 240.0
    },
    'SYNDIC_FONCIA': {
        "nom": "FONCIA GESTION IMMOBILIERE",
        "ident": "FR51ZZZ394820",
        "mandat_template": "FON-COPRO-{digits}",
        "montants_base": 180.0
    },
    'SYNDIC_CITYA': {
        "nom": "CITYA IMMOBILIER SYNDIC",
        "ident": "FR94ZZZ819203",
        "mandat_template": "CIT-LOT-{digits}",
        "montants_base": 165.0
    },
    'CNP_ASSURANCE': {
        "nom": "CNP ASSURANCES LBP",
        "ident": "FR29ZZZ736291",
        "mandat_template": "CNP-AV-{digits}",
        "montants_base": 350.0
    },
    'ASSURANCE': {
        "nom": "ALLIANZ ASSURANCES",
        "ident": "FR99ZZZ458291",
        "mandat_template": "ALZ-HAB-{digits}",
        "montants_base": 32.0
    },
    'FITNESS_PARK': {
        "nom": "FITNESS PARK",
        "ident": "FR34ZZZ643719",
        "mandat_template": "FP-ADH-{digits}",
        "montants": [29.99, 29.99, 29.99]
    },
    'BASIC_FIT': {
        "nom": "BASIC FIT",
        "ident": "NL12ZZZ998877",
        "mandat_template": "BF-{digits}-1",
        "montants": [19.99, 29.99, 29.99]
    }
}

PRENOMS_VIREMENT = [
    "Emma", "Gabriel", "Jade", "Léo", "Louise", "Raphaël", "Ambre", "Maël", "Alba", "Louis",
    "Rose", "Noah", "Alice", "Jules", "Romy", "Arthur", "Anna", "Adam", "Lina", "Lucas",
    "Léna", "Liam", "Mia", "Sacha", "Lou", "Isaac", "Julia", "Gabin", "Chloé", "Éden",
    "Alma", "Hugo", "Agathe", "Naël", "Iris", "Aaron", "Inès", "Mohamed", "Léa", "Léon",
    "Charlie", "Paul", "Mila", "Gaspard", "Juliette", "Ethan", "Léonie", "Marceau", "Zoé", "Tom",
    "Jeanne", "Nathanaël", "Nina", "Tiago", "Eva", "Ayden", "Luna", "Malo", "Victoria", "Milo",
    "Olivia", "Timéo", "Romane", "Nolan", "Lya", "Elio", "Margaux", "Enzo", "Adèle", "Marius",
    "Lucie", "Andrea", "Camille", "Victor", "Lola", "Robin", "Nour", "Axel", "Sofia", "Antoine",
    "Charlotte", "Ilyes", "Alix", "Martin", "Sarah", "Samuel", "Aya", "Noé", "Léana", "Simon",
    "Margot", "Baptiste", "Mathilde", "Evan", "Clémence", "Ibrahim", "Apolline", "Eden", "Lise", "Ali",
    "Capucine", "Lyam", "Joy", "Nino", "Lily", "Mathis", "Elena", "Côme", "Clara", "Amir",
    "Lilia", "Léandre", "Eden", "Yanis", "Anaïs", "Augustin", "Maloé", "Maxime", "Constance", "Naïm",
    "Elina", "Gauthier", "Yasmine", "Oscar", "Salomé", "Alexandre", "Zélia", "Basile", "Maëlys", "Ismaël",
    "Alicia", "Léandro", "Suzanne", "Kaïs", "Héloïse", "Mathys", "Eléa", "Camille", "Amélia", "Clément",
    "Louna", "Imran", "Maya", "Théo", "Thaïs", "Julian", "Manon", "Zélie", "Soan",
    "Célia", "Pablo", "Assia", "Maxence", "Isaure", "Milan", "Emy", "Rayan", "Lila", "Youssef",
    "Louane", "Alessio", "Céleste", "Charly", "Nora", "Anton", "Roxane", "Valentin", "Mélina", "Sohan",
    "Albane", "Yassine", "Laly", "Gaston", "Noémie", "Ilan", "Diane", "Diego", "Soline", "Wassim",
    "Aline", "Soren", "Fanny", "Charlie", "Emeline", "Mady", "Garance", "Eliott", "Flora", "Owen",
    "Océane", "Romy", "Myriam", "Loup", "Hortense", "Ewan", "Maëlle", "Maden", "Elinor", "Lenny",
    "Stella", "Jean", "Youna", "Marcus", "Nola", "Kelian", "Zohra", "Nael", "Livia", "Ayoub",
    "Pia", "Elian", "Sienna", "Joachim", "Thea", "Mahé", "Tia", "Roméo", "Sasha", "Timo",
    "Clea", "Aymen", "Amandine", "Zadig", "Bérénice", "Colin", "Blandine", "Kenzo", "Carole", "Lilian",
    "Céline", "Ruben", "Delphine", "Anatole", "Elodie", "Ezra", "Estelle", "Kamil", "Justine", "Mael",
    "Karine", "Elias", "Laetitia", "Livio", "Marine", "Ousmane", "Marlène", "Paco", "Nadège", "Ugo",
    "Ophélie", "Armand", "Pauline", "Darius", "Sandrine", "Gino", "Sophie", "Hector", "Sylvie", "Joris",
    "Valérie", "Loris", "Virginie", "Matteo", "Audrey", "Niels", "Aurore", "Oihan", "Béatrice", "Vadim",
    "Cécile", "Yvan", "Claire", "Zian", "Coralie", "Aurel", "Emilie", "Boris", "Faustine", "Celian",
    "Flavie", "Dorian", "Gaëlle", "Emile", "Géraldine", "Félix", "Hélène", "Gianni", "Isabelle", "Harry",
    "Joëlle", "Ivan", "Laurine", "Jonas", "Ludivine", "Kyan", "Magali", "Lelio", "Marion", "Mano",
    "Mélanie", "Nadim", "Muriel", "Orso", "Noémie", "Priam", "Pascale", "Quentin", "Sabrina", "Rudy",
    "Séverine", "Samy", "Tatiana", "Tilio", "Vanessa", "Ulysse", "Agnès", "Vianney", "Angélique", "William",
    "Aurélie", "Xavier", "Blandine", "Yann", "Brigitte", "Zacharie", "Caroline", "Abel", "Catherine", "Bastien",
    "Christine", "Cyprien", "Corinne", "Dario", "Danièle", "Elouan", "Dominique", "Florent", "Elisabeth", "Gael",
    "Evelyne", "Habib", "Fabienne", "Idriss", "Florence", "Jude", "Françoise", "Kylian", "Geneviève", "Lasse",
    "Gisèle", "Marin", "Jacqueline", "Noham", "Josiane", "Omer", "Laurence", "Philemon", "Martine", "Qassim",
    "Michèle", "Raoul", "Monique", "Sacha", "Nathalie", "Titouan", "Nicole", "Uriel", "Odile", "Vasco",
    "Patricia", "Wael", "Sylviane", "Xander", "Thérèse", "Younes", "Véronique", "Zephyr", "Yves", "Aaron",
    "Alain", "Benoit", "Bernard", "Corentin", "Christian", "David", "Claude", "Esteban", "Daniel", "Florian",
    "Denis", "Guillaume", "Didier", "Hassan", "Eric", "Igor", "François", "Jeremie", "Gérard", "Kevin",
    "Gilles", "Loic", "Guy", "Marc", "Jacques", "Nicolas", "Jean-Claude", "Olivier", "Jean-Luc", "Pierre",
    "Jean-Marc", "Romain", "Jean-Paul", "Stephane", "Jean-Pierre", "Thomas", "Laurent", "Vincent", "Luc", "Yannick",
    "Marcel", "Adrien", "Michel", "Alexis", "Pascal", "Benoît", "Patrick", "Bruno", "Philippe", "Christophe",
    "René", "Clément", "Richard", "Cyril", "Robert", "Damien", "Thierry", "Fabrice", "Julien", "Sylvain"
]


# ==========================================
# 2. GENERATEURS AIDES ET EXCEPTIONNELS
# ==========================================

DEPT_CAF = {
    "01": "DE L AIN", "02": "DE L AISNE", "03": "DE L ALLIER", "04": "DES ALPES DE HAUTE PROVENCE", "05": "DES HAUTES ALPES", "06": "DES ALPES MARITIMES", "07": "DE L ARDECHE", "08": "DES ARDENNES", "09": "DE L ARIEGE",
    "10": "DE L AUBE", "11": "DE L AUDE", "12": "DE L AVEYRON", "13": "DES BOUCHES DU RHONE", "14": "DU CALVADOS", "15": "DU CANTAL", "16": "DE LA CHARENTE", "17": "DE LA CHARENTE MARITIME", "18": "DU CHER", "19": "DE LA CORREZE",
    "2A": "DE CORSE DU SUD", "2B": "DE HAUTE CORSE", "20": "DE CORSE", "21": "DE LA COTE D OR", "22": "DES COTES D ARMOR", "23": "DE LA CREUSE", "24": "DE LA DORDOGNE", "25": "DU DOUBS", "26": "DE LA DROME", "27": "DE L EURE", "28": "D EURE ET LOIR", "29": "DU FINISTERE",
    "30": "DU GARD", "31": "DE LA HAUTE GARONNE", "32": "DU GERS", "33": "DE LA GIRONDE", "34": "DE L HERAULT", "35": "D ILLE ET VILAINE", "36": "DE L INDRE", "37": "D INDRE ET LOIRE", "38": "DE L ISERE", "39": "DU JURA",
    "40": "DES LANDES", "41": "DU LOIR ET CHER", "42": "DE LA LOIRE", "43": "DE LA HAUTE LOIRE", "44": "DE LOIRE ATLANTIQUE", "45": "DU LOIRET", "46": "DU LOT", "47": "DU LOT ET GARONNE", "48": "DE LA LOZERE", "49": "DE MAINE ET LOIRE",
    "50": "DE LA MANCHE", "51": "DE LA MARNE", "52": "DE LA HAUTE MARNE", "53": "DE LA MAYENNE", "54": "DE MEURTHE ET MOSELLE", "55": "DE LA MEUSE", "56": "DU MORBIHAN", "57": "DE LA MOSELLE", "58": "DE LA NIEVRE", "59": "DU NORD",
    "60": "DE L OISE", "61": "DE L ORNE", "62": "DU PAS DE CALAIS", "63": "DU PUY DE DOME", "64": "DES PYRENEES ATLANTIQUES", "65": "DES HAUTES PYRENEES", "66": "DES PYRENEES ORIENTALES", "67": "DU BAS RHIN", "68": "DU HAUT RHIN", "69": "DU RHONE",
    "70": "DE LA HAUTE SAONE", "71": "DE SAONE ET LOIRE", "72": "DE LA SARTHE", "73": "DE LA SAVOIE", "74": "DE LA HAUTE SAVOIE", "75": "DE PARIS", "76": "DE SEINE MARITIME", "77": "DE SEINE ET MARNE", "78": "DES YVELINES", "79": "DES DEUX SEVRES",
    "80": "DE LA SOMME", "81": "DU TARN", "82": "DU TARN ET GARONNE", "83": "DU VAR", "84": "DE VAUCLUSE", "85": "DE LA VENDEE", "86": "DE LA VIENNE", "87": "DE LA HAUTE VIENNE", "88": "DES VOSGES", "89": "DE L YONNE",
    "90": "DU TERRITOIRE DE BELFORT", "91": "DE L ESSONNE", "92": "DES HAUTS DE SEINE", "93": "DE SEINE SAINT DENIS", "94": "DU VAL DE MARNE", "95": "DU VAL D OISE"
}

def generate_caf(month, year, nom_titulaire="DUPONT JEAN", wealth_profile="moyen", cp="75000"):
    day = random.choice([4, 5, 6])
    date_op = f"{str(day).zfill(2)}/{str(month).zfill(2)}"
    
    if wealth_profile == "pauvre":
        amount = random.uniform(250, 450)
    else:
        amount = random.uniform(100, 250)
        
    code_alpha = "".join(random.choices("0123456789V", k=11))
    num_alloc = "".join(random.choices("0123456789", k=7)) + "R"
    
    nom_famille = nom_titulaire.split()[0].replace(" ", "").upper()
    if nom_titulaire.startswith("MR ") or nom_titulaire.startswith("MME "):
        try:
            nom_famille = nom_titulaire.split()[1].replace(" ", "").upper()
        except:
            pass
            
    _, annee_4 = get_year_strings(year)
    mois_annee = f"{str(month).zfill(2)}{annee_4}ME"
    ref = "01900" + "".join(random.choices("0123456789", k=11))
    
    dept_code = str(cp)[:2] if cp else "75"
    dept_caf = DEPT_CAF.get(dept_code, f"DU DEPARTEMENT {dept_code}")
    
    lignes = [
        f"VIREMENT DE CAF {dept_caf}",
        f"{code_alpha}  {num_alloc}{nom_famille} {mois_annee} REFERENCE : {ref}"
    ]
        
    return {
        'date': date_op, 'lignes': lignes,
        'montant': f"{amount:.2f}".replace('.', ','),
        'type': 'VIREMENT EN VOTRE FAVEUR', 'signe': '+', 'amount': float(amount)
    }

def generate_cpam(month, year, cp="75000"):
    max_days = get_days_in_month(month, year)
    day = random.randint(10, min(25, max_days))
    date_op = f"{str(day).zfill(2)}/{str(month).zfill(2)}"
    amount = random.uniform(15, 85)
    
    dept_code = str(cp)[:2] if cp else "75"
    num1 = "26" + "".join(random.choices("0123456789", k=10))
    ref = "01890" + "".join(random.choices("0123456789", k=11))
    
    lignes = [
        f"VIREMENT DE CPAM {dept_code}",
        f"{num1}  {num1} REFERENCE : {ref}"
    ]
    return {
        'date': date_op, 'lignes': lignes,
        'montant': f"{amount:.2f}".replace('.', ','),
        'type': 'VIREMENT EN VOTRE FAVEUR', 'signe': '+', 'amount': float(amount)
    }

def generate_mutuelle(month, year, nom_titulaire="DUPONT JEAN"):
    max_days = get_days_in_month(month, year)
    day = random.randint(5, max_days)
    date_op = f"{str(day).zfill(2)}/{str(month).zfill(2)}"
    amount = random.uniform(20, 60)
    
    code_contrat = f"D{random.randint(1000000, 9999999)}"
    num1 = "".join(random.choices("0123456789", k=10))
    ref = "01900" + "".join(random.choices("0123456789", k=11))
    
    nom_upper = nom_titulaire.upper()
    if nom_upper.startswith("MR "): nom_upper = nom_upper[3:]
    if nom_upper.startswith("MME "): nom_upper = nom_upper[4:]
    
    l2_base = f"LECT TERRITORIALE {code_contrat} /00000001/{num1} Vir Prest {code_contrat} D "
    if len(l2_base + nom_upper) > 75:
        l2 = (l2_base + nom_upper)[:72]
        reste_nom = (l2_base + nom_upper)[72:]
        lignes = [
            "VIREMENT DE MUTUEL NATION FONCT COL",
            l2,
            f"{reste_nom} REFERENCE : {ref}"
        ]
    else:
        lignes = [
            "VIREMENT DE MUTUEL NATION FONCT COL",
            l2_base + nom_upper,
            f"REFERENCE : {ref}"
        ]
        
    return {
        'date': date_op, 'lignes': lignes,
        'montant': f"{amount:.2f}".replace('.', ','),
        'type': 'VIREMENT EN VOTRE FAVEUR', 'signe': '+', 'amount': float(amount)
    }

def generate_virement_permanent(month, year, titulaire_nom="DUPONT JEAN", titulaire_sexe="M", dest_iban=None):
    max_days = get_days_in_month(month, year)
    day = min(random.choice([1, 2, 5, 28, 30, 31]), max_days)
    date_op = f"{str(day).zfill(2)}/{str(month).zfill(2)}"
    amount = random.choice([50.0, 100.0, 150.0, 200.0])
    
    nom_clean = titulaire_nom.upper()
    if nom_clean.startswith("MR ") or nom_clean.startswith("MME "):
        nom_complet = nom_clean
    else:
        prefix = "MR" if str(titulaire_sexe).upper() == "M" else "MME"
        nom_complet = f"{prefix} {nom_clean}"
        
    if dest_iban and len(str(dest_iban).strip()) >= 15:
        rib_iban = str(dest_iban).replace(" ", "").upper()
    else:
        cle_iban = "".join(random.choices("0123456789", k=2))
        compte_num = "".join(random.choices("0123456789", k=11))
        cle_rib = "".join(random.choices("0123456789", k=2))
        lettre = random.choice(["S", "H", "K", "L", "J"])
        rib_iban = f"FR{cle_iban}1001100020{compte_num}{lettre}{cle_rib}"
    ref = "0226" + "".join(random.choices("0123456789", k=12))
    
    lignes = [
        "VIREMENT PERMANENT POUR",
        f"{nom_complet} COMPTE {rib_iban}",
        f"REFERENCE : {ref} REFERENCE : {ref}"
    ]
    return {
        'date': date_op, 'lignes': lignes,
        'montant': f"{amount:.2f}".replace('.', ','),
        'type': 'VIREMENT EMIS', 'signe': '-', 'amount': float(amount)
    }

def generate_remise_cheque(month, year):
    max_d = get_days_in_month(month, year)
    day = random.randint(3, max_d)
    date_op = f"{str(day).zfill(2)}/{str(month).zfill(2)}"
    amount = random.uniform(35, 280)
    
    num_cheque = "".join(random.choices("0123456789", k=7))
    lignes = [
        "REMISE DE CHEQUE",
        f"CHEQUE N° {num_cheque}"
    ]
    return {
        'date': date_op, 'lignes': lignes,
        'montant': f"{amount:.2f}".replace('.', ','),
        'type': 'REMISE DE CHEQUE', 'signe': '+', 'amount': float(amount)
    }

def generate_fdj(month, year):
    """Gain Loto / Euromillions / FDJ"""
    day = random.randint(1, 28)
    date_op = f"{str(day).zfill(2)}/{str(month).zfill(2)}"
    amount = random.choice([50.0, 120.0, 250.0, 318.0, 500.0, 1250.0, 2650.0])
    
    id_tech = "I" + "".join(random.choices("0123456789", k=13))
    id_gain = "".join(random.choices("0123456789", k=15))
    ref = "0190" + "".join(random.choices("0123456789", k=12))
    
    lignes = [
        "VIREMENT DE LA FRANCAISE DES JEUX",
        f"{id_tech}  {id_gain} REFERENCE : {ref}"
    ]
    return {
        'date': date_op, 'lignes': lignes,
        'montant': f"{amount:.2f}".replace('.', ','),
        'type': 'VIREMENT EN VOTRE FAVEUR', 'signe': '+', 'amount': float(amount)
    }

def generate_edf_remboursement(month, year, nom_titulaire="DUPONT JEAN"):
    """Remboursement trop-perçu régularisation EDF"""
    day = random.randint(1, 28)
    date_op = f"{str(day).zfill(2)}/{str(month).zfill(2)}"
    amount = random.uniform(18, 180)
    
    # Nettoyage du nom pour le format EDF
    nom_propre = nom_titulaire.lower()
    if nom_propre.startswith("mr ") or nom_propre.startswith("m. "): nom_propre = nom_propre[3:]
    elif nom_propre.startswith("mme "): nom_propre = nom_propre[4:]
    
    num_dossier = "".join(random.choices("0123456789", k=12))
    num_contrat = "".join(random.choices("0123456789", k=5))
    ref = "01890" + "".join(random.choices("0123456789", k=11))
    
    lignes = [
        "VIREMENT DE EDF CLT PART RBT SCT",
        f"){num_dossier} {num_contrat} 1 EDF VRS {nom_propre}  ){num_dossier} EDF VRS REM",
        f"BOURSEMENT COMPTE CREDITEUR REFERENCE : {ref}"
    ]
    return {
        'date': date_op, 'lignes': lignes,
        'montant': f"{amount:.2f}".replace('.', ','),
        'type': 'VIREMENT EN VOTRE FAVEUR', 'signe': '+', 'amount': float(amount)
    }

def generate_virement_interne(month, year, titulaire_nom="DUPONT JEAN", titulaire_sexe="M", destination="LIVRET A", dest_iban=None):
    """Virement interne CCP vers Livret A ou Épargne"""
    day = random.choice([2, 5, 10, 15, 21, 28])
    date_op = f"{str(day).zfill(2)}/{str(month).zfill(2)}"
    amount = random.choice([50.0, 100.0, 250.0, 500.0, 1000.0, 2000.0])
    
    nom_clean = titulaire_nom.upper()
    if nom_clean.startswith("MR ") or nom_clean.startswith("MME "):
        nom_complet = nom_clean
    else:
        prefix = "M" if str(titulaire_sexe).upper() == "M" else "MME"
        nom_complet = f"{prefix} {nom_clean}"
        
    if dest_iban and len(str(dest_iban).strip()) >= 15:
        rib_iban = str(dest_iban).replace(" ", "").upper()
    else:
        cle_iban = "".join(random.choices("0123456789", k=2))
        compte_num = "".join(random.choices("0123456789", k=11))
        cle_rib = "".join(random.choices("0123456789", k=2))
        lettre = random.choice(["J", "K", "L", "S"])
        rib_iban = f"FR{cle_iban}1001100020{compte_num}{lettre}{cle_rib}"
    ref = "0329" + "".join(random.choices("0123456789", k=12))
    
    label_dest = "CCP VERS LIVRET A" if "LIVRET" in destination.upper() else "CCP VERS EPARGNE"
    
    lignes = [
        "VIREMENT POUR",
        f"{nom_complet} COMPTE {rib_iban} {label_dest}",
        f"{label_dest} REFERENCE : {ref}"
    ]
    return {
        'date': date_op, 'lignes': lignes,
        'montant': f"{amount:.2f}".replace('.', ','),
        'type': 'VIREMENT EMIS', 'signe': '-', 'amount': float(amount)
    }

# ==========================================
# 3. GENERATEURS FACTURES ET PRELEVEMENTS
# ==========================================


def get_days_in_month(month, year):
    try:
        m = int(month)
        y = int(str(year))
        if y < 100:
            y = 2000 + y
    except Exception:
        return 30
        
    if m == 2:
        is_bissextile = (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)
        return 29 if is_bissextile else 28
    elif m in [4, 6, 9, 11]:
        return 30
    else:
        return 31

def get_year_strings(year):
    y_str = str(year).strip()
    year_2 = y_str[-2:] if len(y_str) >= 2 else y_str.zfill(2)
    year_4 = f"20{year_2}"
    return year_2, year_4

def get_tx_date_sort_key(tx):
    d_str = str(tx.get('date', '15/01')).strip()
    try:
        if '/' in d_str:
            parts = d_str.split('/')
            day = int(parts[0])
            month = int(parts[1]) if len(parts) > 1 else 1
            year = int(parts[2]) if len(parts) > 2 else 0
            return (year, month, day)
        elif '.' in d_str:
            parts = d_str.split('.')
            day = int(parts[0])
            month = int(parts[1]) if len(parts) > 1 else 1
            year = int(parts[2]) if len(parts) > 2 else 0
            return (year, month, day)
        return (0, 1, int(d_str))
    except Exception:
        return (0, 1, 15)

def format_amount(amount):
    if isinstance(amount, str):
        return amount
    s = f"{amount:,.2f}".replace(',', ' ').replace('.', ',')
    return s

def generate_random_date(month, year):
    max_days = get_days_in_month(month, year)
    day = random.randint(1, min(max_days, 28))
    year_2, _ = get_year_strings(year)
    month_str = str(month).zfill(2)
    day_str = str(day).zfill(2)
    return f"{day_str}.{month_str}.{year_2}"

PROFILE_CEILINGS = {
    "pauvre": {
        "supermarche": 80.0, "fast_food": 30.0, "pharmacie": 25.0,
        "cinema": 20.0, "tabac": 15.0, "brasserie": 25.0, "carburant": 70.0,
        "shopping_big": 150.0, "shopping_online": 60.0, "boulangerie": 12.0,
    },
    "moyen": {
        "supermarche": 200.0, "fast_food": 70.0, "pharmacie": 60.0,
        "cinema": 50.0, "tabac": 50.0, "brasserie": 55.0, "carburant": 110.0,
        "shopping_big": 450.0, "shopping_online": 200.0, "boulangerie": 20.0,
    },
    "riche": {
        "supermarche": 500.0, "fast_food": 120.0, "pharmacie": 150.0,
        "cinema": 80.0, "tabac": 80.0, "brasserie": 100.0, "carburant": 200.0,
        "shopping_big": 1500.0, "shopping_online": 600.0, "boulangerie": 30.0,
    },
}

def _get_ceiling(wealth_profile, cat):
    return PROFILE_CEILINGS.get(wealth_profile, PROFILE_CEILINGS["moyen"]).get(cat, 9999.0)

def generate_coherent_amount(merchant, wealth_profile="moyen"):
    merchant_upper = merchant.upper()
    
    if wealth_profile == "pauvre":
        scale = random.uniform(0.5, 0.8)
    elif wealth_profile == "riche":
        scale = random.uniform(1.5, 4.0)
    else:
        scale = random.uniform(0.8, 1.2)
        
    if 'NETFLIX' in merchant_upper:
        if wealth_profile == "pauvre": return random.choice(['5,99', '8,99'])
        if wealth_profile == "riche": return random.choice(['13,49', '19,99'])
        return random.choice(['5,99', '7,99', '8,99', '13,49', '19,99'])
        
    if 'SPOTIFY' in merchant_upper:
        if wealth_profile == "pauvre": return '11,99'
        return random.choice(['11,99', '14,99', '17,99'])

    cat = None
    if any(m in merchant_upper for m in ['LEROY MERLIN', 'CASTORAMA', 'FNAC', 'DARTY', 'IKEA', 'DECATHLON']):
        val = random.uniform(25.00, 250.00) * scale
        cat = "shopping_big"
    elif any(m in merchant_upper for m in ['ZALANDO', 'ALIEXPRESS', 'AMAZON', 'VINTED', 'ASOS']):
        val = random.uniform(10.00, 140.00) * scale
        cat = "shopping_online"
    elif any(m in merchant_upper for m in ['LIDL', 'CARREFOUR', 'AUCHAN', 'MARKET', 'LECLERC', 'INTERMARCHE', 'MONOPRIX', 'PICARD', 'GRAND FRAIS', 'U EXPRESS', 'CASINO']):
        val = random.uniform(12.00, 120.00) * scale
        cat = "supermarche"
    elif any(m in merchant_upper for m in ['MCDONALDS', 'BURGER KING', 'UBER EATS', 'DELIVEROO', 'KFC', 'PIZZA HUT', 'SUSHI']):
        val = random.uniform(8.00, 45.00) * scale
        cat = "fast_food"
    elif any(m in merchant_upper for m in ['TOTALENERGIES', 'RELAIS', 'JUMBO PNEU', 'STATION', 'ENI', 'AVIA']):
        val = random.uniform(40.00, 110.00) * scale
        cat = "carburant"
    elif any(m in merchant_upper for m in ['SANEF', 'APRR']):
        val = random.uniform(2.50, 45.00) * scale
    elif any(m in merchant_upper for m in ['SNCF', 'UBER', 'LECAB', 'BOLT', 'AIR FRANCE']):
        val = random.uniform(15.00, 120.00) * scale
    elif 'PHARMACIE' in merchant_upper:
        val = random.uniform(4.50, 50.00) * scale
        cat = "pharmacie"
    elif any(m in merchant_upper for m in ['PATHE', 'UGC', 'CINEMA']):
        val = random.uniform(8.50, 30.00) * scale
        cat = "cinema"
    elif 'BAR ' in merchant_upper or 'BRASSERIE' in merchant_upper:
        val = random.uniform(8.00, 45.00) * scale
        cat = "brasserie"
    elif 'TABAC' in merchant_upper:
        val = random.uniform(5.00, 30.00) * scale
        cat = "tabac"
    elif 'BL ' in merchant_upper or 'BOULANGERIE' in merchant_upper:
        val = random.uniform(1.20, 18.00) * scale
        cat = "boulangerie"
    elif 'STATIONN' in merchant_upper:
        val = random.uniform(1.50, 25.00)
    else:
        val = random.uniform(5.00, 60.00) * scale

    if cat:
        ceil = _get_ceiling(wealth_profile, cat)
        val = min(val, ceil)
        
    return f"{val:.2f}".replace('.', ',')


def generate_retrait(card_number_suffix, month, year, wealth_profile="moyen", forced_day=None):
    if wealth_profile == "pauvre":
        montant = random.choice([20, 20, 40, 40, 50])
    elif wealth_profile == "riche":
        montant = random.choice([100, 150, 200, 300, 500])
    else:
        montant = random.choice([20, 40, 50, 60, 80, 100])
        
    max_days = get_days_in_month(month, year)
    if forced_day is not None:
        day = min(max_days, max(1, int(forced_day)))
    else:
        date_retrait = generate_random_date(month, year) 
        day = int(date_retrait.split('.')[0])
        
    _, yr_str = get_year_strings(year)
    mo_str = str(month).zfill(2)
    day_str = str(day).zfill(2)
    
    hour = str(random.randint(8, 20)).zfill(2)
    minute = str(random.randint(0, 59)).zfill(2)
    
    is_external = random.random() < 0.20
    if is_external:
        external_banks = ["CAISSE D EPARGNE", "CREDIT AGRICOLE", "SOCIETE GENERALE", "BNP PARIBAS", "LCL", "CREDIT MUTUEL", "BANQUE POPULAIRE", "CIC"]
        bank_name = random.choice(external_banks)
    else:
        bank_name = DEFAULT_BANK_NAMES.get(CURRENT_BANK_TYPE, "LA BANQUE POSTALE")
        
    lignes = [
        f"CARTE X{card_number_suffix} {day_str}/{mo_str}/{str(yr_str)[-2:]} A {hour}H{minute}",
        f"RETRAIT DAB {bank_name}"
    ]
    
    op_day = min(max_days, day + random.randint(0, 1))
    date_op = f"{str(op_day).zfill(2)}/{mo_str}"
    
    return {
        'date': date_op,
        'lignes': lignes,
        'montant': f"{montant:.2f}".replace('.', ','),
        'type': 'RETRAIT',
        'signe': '-',
        'amount': float(montant)
    }

def generate_spaced_retraits(num_requested, card_number, month, year, wealth_profile="moyen"):
    txs = []
    if num_requested <= 0:
        return txs
    max_days = get_days_in_month(month, year)
    if num_requested == 1:
        days = [random.randint(10, min(18, max_days - 2))]
    elif num_requested == 2:
        days = [random.randint(5, min(11, max_days - 15)), random.randint(min(18, max_days - 10), min(26, max_days - 2))]
    else:
        days = [
            random.randint(4, min(8, max_days - 20)),
            random.randint(min(12, max_days - 15), min(18, max_days - 10)),
            random.randint(min(22, max_days - 6), min(27, max_days - 1))
        ]
    for d in days:
        tx = generate_retrait(card_number, month, year, wealth_profile=wealth_profile, forced_day=d)
        txs.append(tx)
    return txs

def generate_salaire(month, year, wealth_profile="moyen", city="PARIS", custom_employeur=None):
    city_upper = city.upper() if city else "PARIS"
    _, year_4 = get_year_strings(year)
    mois_str = str(month).zfill(2)
    max_d = get_days_in_month(month, year)
    
    if custom_employeur and isinstance(custom_employeur, dict):
        nom_emp = custom_employeur.get("nom", "CAPGEMINI TECHNOLOGY SERVICES")
        mat = custom_employeur.get("matricule", "491823")
        base_amt = float(custom_employeur.get("base_amount", 2450.0))
        if custom_employeur.get("is_exact"):
            amt_sal = round(base_amt, 2)
        else:
            micro_var = custom_employeur.get("variation", random.uniform(-12.0, 12.0))
            amt_sal = max(1420.0, round(base_amt + micro_var, 2))
        day_sal = min(max_d, custom_employeur.get("day", 28))
        ref_sepa = custom_employeur.get("ref_prefix", "TRF" + "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8)))
        ref_num = custom_employeur.get("ref_num", "".join(random.choices("0123456789", k=16)))
        
        lignes = [
            f"VIREMENT DE {nom_emp}",
            f"SALAIRES {mois_str}/{year_4} MATRICULE {mat} {ref_sepa}",
            f"REFERENCE : {ref_num}"
        ]
    else:
        if wealth_profile == "pauvre":
            amt_sal = random.uniform(1420.0, 1750.0)
        elif wealth_profile == "riche":
            amt_sal = random.uniform(4200.0, 7800.0)
        else:
            amt_sal = random.uniform(2100.0, 3400.0)
            
        employeurs = [
            "ORANGE SA", "CAPGEMINI TECHNOLOGY SERVICES", "GROUPE RENAULT SAS", 
            "SOCIETE GENERALE SA", "THALES SIX GTS FRANCE SAS", "DASSAULT AVIATION SA", 
            "AIRBUS COMMERCIAL AIRCRAFT", "SANOFI WINTHROP INDUSTRIE", "ENGIE SOLUTIONS FRANCE"
        ]
        nom_emp = random.choice(employeurs)
        mat = "".join(random.choices("0123456789", k=6))
        ref_sepa = "TRF" + "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=12))
        ref_num = "".join(random.choices("0123456789", k=16))
        day_sal = min(max_d, random.choice([27, 28, 29, 30, max_d]))
        
        lignes = [
            f"VIREMENT DE {nom_emp}",
            f"SALAIRES {mois_str}/{year_4} MATRICULE {mat} {ref_sepa}",
            f"REFERENCE : {ref_num}"
        ]
        
    montant = f"{amt_sal:.2f}".replace('.', ',')
    date_op = f"{str(day_sal).zfill(2)}/{mois_str}"
    
    return {
        'date': date_op,
        'lignes': lignes,
        'montant': montant,
        'type': 'VIREMENT EN VOTRE FAVEUR',
        'signe': '+',
        'amount': amt_sal
    }

def generate_salaire_fonctionnaire(month, year, city="PARIS", wealth_profile="moyen"):
    if wealth_profile == "pauvre":
        amt_sal = random.uniform(1600.0, 2050.0)
    elif wealth_profile == "riche":
        amt_sal = random.uniform(3400.0, 5600.0)
    else:
        amt_sal = random.uniform(2150.0, 3200.0)
        
    montant = f"{amt_sal:.2f}".replace('.', ',')
    city_upper = city.upper() if city else "PARIS"
    _, year_4 = get_year_strings(year)
    mois_str = str(month).zfill(2)
    
    employeurs = [
        f"DDFIP DE {city_upper}", 
        f"DRFIP {city_upper}", 
        "DGFIP FINANCES PUBLIQUES",
        f"CENTRE HOSPITALIER UNIVERSITAIRE DE {city_upper}", 
        "MINISTERE DE L EDUCATION NATIONALE", 
        "MINISTERE DE L INTERIEUR",
        f"SGC {city_upper}",
        f"CONSEIL DEPARTEMENTAL {city_upper}"
    ]
    nom_emp = random.choice(employeurs)
    
    ref_alpha_1 = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=14))
    ref_alpha_2 = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
    ref_num = "0190" + "".join(random.choices("0123456789", k=12))
    
    lignes = [
        f"VIREMENT DE {nom_emp}",
        f"{ref_alpha_1} TRAITEMENT {mois_str}/{year_4} {ref_alpha_2}",
        f"REFERENCE : {ref_num}"
    ]
    
    max_d = get_days_in_month(month, year)
    day_sal = max(1, max_d - random.choice([1, 2, 3]))
    date_op = f"{str(day_sal).zfill(2)}/{mois_str}"
    
    return {
        'date': date_op,
        'lignes': lignes,
        'montant': montant,
        'amount': round(amt_sal, 2),
        'type': 'VIREMENT EN VOTRE FAVEUR',
        'signe': '+'
    }

def generate_france_travail(month, year, wealth_profile="pauvre"):
    if wealth_profile == "pauvre":
        amt = random.uniform(850.0, 1180.0)
    elif wealth_profile == "riche":
        amt = random.uniform(1900.0, 2600.0)
    else:
        amt = random.uniform(1220.0, 1650.0)
        
    montant = f"{amt:.2f}".replace('.', ',')
    _, year_4 = get_year_strings(year)
    mois_str = str(month).zfill(2)
    
    org_label = "FRANCE TRAVAIL" if int(str(year_4)) >= 2024 else "POLE EMPLOI"
    ref_alloc = "".join(random.choices("0123456789", k=8))
    ref_num = "0190" + "".join(random.choices("0123456789", k=12))
    
    day = random.randint(1, 4)
    date_op = f"{str(day).zfill(2)}/{mois_str}"
    
    lignes = [
        f"VIREMENT DE {org_label}",
        f"ALLOCATION ARE DU {mois_str}/{year_4} ID {ref_alloc}",
        f"REFERENCE : {ref_num}"
    ]
    
    return {
        'date': date_op,
        'lignes': lignes,
        'montant': montant,
        'amount': round(amt, 2),
        'type': 'VIREMENT EN VOTRE FAVEUR',
        'signe': '+'
    }

def generate_virement_chantier_client(month, year, wealth_profile="moyen"):
    if wealth_profile == "riche":
        amt = random.uniform(1800.0, 4800.0)
    elif wealth_profile == "pauvre":
        amt = random.uniform(350.0, 1200.0)
    else:
        amt = random.uniform(750.0, 2600.0)
        
    montant = f"{amt:.2f}".replace('.', ',')
    mois_str = str(month).zfill(2)
    
    client_family = random.choice(["M ET MME " + random.choice(PRENOMS_VIREMENT).upper(), "SCI " + random.choice(["DU PARC", "DES FLEURS", "IMMO CONCEPT", "LE CEDRE", "PROVENCE"]), "SYNDIC FONCIA", "SYNDIC NEXITY"])
    chantier_type = random.choice(["ACOMPTE CHANTIER RENOVATION", "SOLDE FACTURE TRAVAUX", "TRAVAUX PLOMBERIE SANITAIRE", "TRAVAUX ELECTRICITE", "INSTALLATION CLIMATISATION", "PEINTURE INTERIEURE"])
    ref_fac = f"FAC-{random.randint(100, 999)}"
    
    max_d = get_days_in_month(month, year)
    day = random.randint(4, max_d)
    date_op = f"{str(day).zfill(2)}/{mois_str}"
    
    lignes = [
        f"VIREMENT DE {client_family}",
        f"{chantier_type} {ref_fac}"
    ]
    
    return {
        'date': date_op,
        'lignes': lignes,
        'montant': montant,
        'amount': round(amt, 2),
        'type': 'VIREMENT EN VOTRE FAVEUR',
        'signe': '+'
    }

def generate_caf_famille(month, year, cp="75000"):
    amt = random.choice([148.52, 235.40, 338.80, 422.08, 516.32])
    montant = f"{amt:.2f}".replace('.', ',')
    mois_str = str(month).zfill(2)
    _, year_4 = get_year_strings(year)
    
    dept_code = str(cp)[:2] if cp else "75"
    dept_label = DEPT_CAF.get(dept_code, dept_code)
    
    day = random.choice([4, 5, 6])
    date_op = f"{str(day).zfill(2)}/{mois_str}"
    ref_num = "01890" + "".join(random.choices("0123456789", k=11))
    
    lignes = [
        f"VIREMENT DE CAF {dept_label}",
        f"ALLOCATIONS FAMILIALES ET PAJE {mois_str}/{year_4}",
        f"REFERENCE : {ref_num}"
    ]
    return {
        'date': date_op,
        'lignes': lignes,
        'montant': montant,
        'amount': float(amt),
        'type': 'VIREMENT EN VOTRE FAVEUR',
        'signe': '+'
    }

def generate_loyer_recu_investisseur(month, year, wealth_profile="riche"):
    if wealth_profile == "riche":
        amt = random.uniform(950.0, 1850.0)
    else:
        amt = random.uniform(620.0, 1100.0)
        
    montant = f"{amt:.2f}".replace('.', ',')
    mois_str = str(month).zfill(2)
    _, year_4 = get_year_strings(year)
    
    locataire_nom = random.choice(["M ET MME " + random.choice(PRENOMS_VIREMENT).upper(), "SCI " + random.choice(["DU PARC", "IMMO CONCEPT", "LE CEDRE", "PROVENCE"])])
    lot_num = random.randint(1, 12)
    
    day = random.randint(1, 6)
    date_op = f"{str(day).zfill(2)}/{mois_str}"
    
    lignes = [
        f"VIREMENT DE {locataire_nom}",
        f"LOYER APPARTEMENT LOT {lot_num} {mois_str}/{year_4}"
    ]
    return {
        'date': date_op,
        'lignes': lignes,
        'montant': montant,
        'amount': round(amt, 2),
        'type': 'VIREMENT EN VOTRE FAVEUR',
        'signe': '+'
    }

def generate_virement_epargne(month, year, wealth_profile="moyen"):
    if wealth_profile == "riche":
        amt = random.uniform(350.0, 1200.0)
    elif wealth_profile == "pauvre":
        amt = random.uniform(50.0, 150.0)
    else:
        amt = random.uniform(150.0, 450.0)
        
    montant = f"{amt:.2f}".replace('.', ',')
    mois_str = str(month).zfill(2)
    day = random.choice([5, 6, 7, 8])
    date_op = f"{str(day).zfill(2)}/{mois_str}"
    
    target_livret = random.choice(["VERS LIVRET A", "VERS PEL EPARGNE LOGEMENT", "VERS LIVRET DE DEVELOPPEMENT DURABLE", "VERS COMPTE EPARGNE LOGEMENT"])
    
    lignes = [
        "VIREMENT EMIS",
        f"{target_livret}",
        f"VIREMENT DU {date_op}"
    ]
    return {
        'date': date_op,
        'lignes': lignes,
        'montant': montant,
        'amount': round(amt, 2),
        'type': 'VIREMENT EMIS',
        'signe': '-'
    }

def generate_prelevement_loyer_bailleur(month, year, wealth_profile="moyen"):
    if wealth_profile == "riche":
        amt = random.uniform(950.0, 1600.0)
    elif wealth_profile == "pauvre":
        amt = random.uniform(450.0, 700.0)
    else:
        amt = random.uniform(650.0, 980.0)
        
    montant = f"{amt:.2f}".replace('.', ',')
    mois_str = str(month).zfill(2)
    day = random.choice([1, 2, 3, 4, 5])
    date_op = f"{str(day).zfill(2)}/{mois_str}"
    
    bailleur = random.choice(["FONCIA GESTION LOCATIVE", "NEXITY GESTION IMMOBILIERE", "IMMOBILIERE 3F", "PARIS HABITAT OPH", "CDC HABITAT", "GESTION IMMOBILIERE DE FRANCE"])
    ref_lot = f"LOT-{random.randint(100, 999)}"
    ref_mandat = f"MDT-{random.randint(100000, 999999)}"
    
    lignes = [
        f"PRELEVEMENT DE {bailleur}",
        f"REF : {ref_lot} IDENT : FR76ZZZ{random.randint(100000, 999999)}",
        f"MANDAT : {ref_mandat}"
    ]
    return {
        'date': date_op,
        'lignes': lignes,
        'montant': montant,
        'amount': round(amt, 2),
        'type': 'PRELEVEMENT',
        'signe': '-'
    }

def generate_virement_inst_emis(month, year, wealth_profile="moyen"):
    if wealth_profile == "pauvre":
        amt = random.uniform(5, 30)
    elif wealth_profile == "riche":
        amt = random.uniform(50, 400)
    else:
        amt = random.uniform(15, 200)
        
    if CURRENT_CONTACTS_EMIS:
        prenom = random.choice(CURRENT_CONTACTS_EMIS)
    else:
        prenom = random.choice(PRENOMS_VIREMENT)
    
    variant = random.random()
    if variant < 0.70:
        # Variant A: Prenom + Bank Reference Code
        ref_prefix = "OBA" if CURRENT_BANK_TYPE == "lbp" else "REF"
        code_oba = ref_prefix + "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=14))
        l2 = f"{prenom}  {code_oba}"
    else:
        # Variant B: Just Prenom
        if random.random() < 0.5:
            l2 = prenom.upper()
        else:
            l2 = prenom
            
    lignes = [
        "VIREMENT INSTANTANE A",
        l2
    ]
    
    date_op = generate_random_date(month, year)
    day, mo, _ = date_op.split('.')
    date_finale = f"{day}/{mo}"
    
    return {
        'date': date_finale,
        'lignes': lignes,
        'montant': f"{amt:.2f}".replace('.', ','),
        'type': 'VIREMENT EMIS',
        'signe': '-',
        'amount': float(amt)
    }

def generate_virement_inst_recu(month, year, wealth_profile="moyen"):
    if wealth_profile == "pauvre":
        amt = random.uniform(10, 50)
    elif wealth_profile == "riche":
        amt = random.uniform(100, 800)
    else:
        amt = random.uniform(20, 200)
        
    if CURRENT_CONTACTS_RECU:
        prenom = random.choice(CURRENT_CONTACTS_RECU)
    else:
        prenom = random.choice(PRENOMS_VIREMENT)
    
    motifs = [
        "Envoye depuis Revolut", "Achat xmax", "Achat LBC", "Achat Vinted", 
        "Cadeau", "Remboursement resto", "Participation", "Avance de frais", 
        "Courses", "Pour le loyer", "Billets concert", "Vacances", "Remboursement",
        "Cadeau anniversaire", "Participation cadeau", "remboursement cine", ""
    ]
    
    motif = random.choice(motifs)
    if motif:
        l2 = f"{prenom} {motif}"
    else:
        l2 = prenom
        
    lignes = [
        "VIREMENT INSTANTANE DE",
        l2
    ]
    
    date_op = generate_random_date(month, year)
    day, mo, _ = date_op.split('.')
    date_finale = f"{day}/{mo}"
    
    return {
        'date': date_finale,
        'lignes': lignes,
        'montant': f"{amt:.2f}".replace('.', ','),
        'type': 'VIREMENT EN VOTRE FAVEUR',
        'signe': '+',
        'amount': float(amt)
    }

def generate_frais_bancaires(month, year, wealth_profile="moyen", age_profile="adulte"):
    """
    Génère la cotisation de la Formule de Compte (trimestrielle pour LBP, mensuelle pour les autres).
    """
    try:
        m_int = int(month)
    except Exception:
        m_int = 1
        
    if CURRENT_BANK_TYPE == "lbp":
        if m_int not in [1, 4, 7, 10]:
            return None
            
    day = random.choice([3, 4, 5, 6])
    date_op = f"{str(day).zfill(2)}/{str(m_int).zfill(2)}"
    
    if CURRENT_BANK_TYPE == "lbp":
        if age_profile == "jeune":
            # Tarifs avec réduction 18-25 ans
            amount = random.choice([11.31, 14.10, 14.55, 15.60])
            reduction = f"{amount:.2f}".replace('.', ',')
            lignes = [
                "COTISATION TRIMESTRIELLE",
                f"DE VOTRE FORMULE DE COMPTE APRES REDUCTION JEUNES 18-25 ANS DE {reduction} ¤"
            ]
        else:
            # Tarifs adultes (Classique ou Premier)
            if wealth_profile == "riche":
                amount = random.choice([39.50, 42.00, 45.80]) # Visa Premier / Platinum
            else:
                amount = random.choice([17.20, 18.50, 19.90, 21.00]) # Visa Classic
                
            lignes = [
                "COTISATION TRIMESTRIELLE",
                "DE VOTRE FORMULE DE COMPTE"
            ]
    else:
        # Autres banques (frais mensuels)
        if age_profile == "jeune":
            amount = random.choice([2.50, 3.00, 3.90])
            lignes = [
                "COTISATION MENSUELLE",
                "OFFRE SERVICES JEUNES"
            ]
        else:
            if wealth_profile == "riche":
                amount = random.choice([14.90, 18.50, 22.00])
            else:
                amount = random.choice([6.90, 7.50, 8.20])
                
            lignes = [
                "COTISATION FORFAITAIRE MENSUELLE",
                "OFFRE DE SERVICES GROUPES"
            ]

    return {
        'date': date_op,
        'lignes': lignes,
        'montant': f"{amount:.2f}".replace('.', ','),
        'type': 'FRAIS BANCAIRES',
        'signe': '-',
        'amount': float(amount),
        'is_frais': True,
        'has_arrow': True
    }

def generate_prelevement(type_prelev, month, year=2025, wealth_profile="moyen"):
    day = random.choice([4, 5, 12, 15, 20])
    mois_str = str(month).zfill(2)
    _, annee_4 = get_year_strings(year)
    date_op = f"{str(day).zfill(2)}/{mois_str}"
    
    if type_prelev in PRELEVEMENT_TYPES:
        data = PRELEVEMENT_TYPES[type_prelev]
        
        if "montants" in data:
            if wealth_profile == "pauvre":
                val = data["montants"][0]
            elif wealth_profile == "riche":
                val = data["montants"][-1]
            else:
                val = data["montants"][len(data["montants"]) // 2]
        else:
            base = data.get("montants_base", 30)
            if wealth_profile == "pauvre":
                val = random.uniform(base * 0.5, base * 0.8)
            elif wealth_profile == "riche":
                val = random.uniform(base * 1.5, base * 3.0)
            else:
                val = random.uniform(base * 0.9, base * 1.3)
                
        montant = f"{val:.2f}".replace('.', ',')
        nom = data["nom"]
        ident = data["ident"]
        p_format = data.get("format", "STANDARD")
        
        if p_format == "IDENT_ONLY":
            lignes = [
                f"PRELEVEMENT DE {nom}",
                f"IDENT : {ident}"
            ]
        elif p_format == "GMF_SPECIAL":
            rum_num = "".join(random.choices("0123456789", k=7))
            pt_num = "".join(random.choices("0123456789", k=9))
            lignes = [
                f"PRELEVEMENT DE {nom}",
                f"PRELEVEMENT GMF ASSURANCES (ICS: {ident}) MENSU Votre RUM: 40000000{rum_num} PT {pt_num}",
                f"IDENT : {ident}",
                f"MANDAT : 40000000{rum_num}"
            ]
        elif p_format == "LOGIREP_STYLE":
            ref_c = "".join(random.choices("0123456789", k=6))
            lignes = [
                f"PRELEVEMENT DE {nom}",
                f"REF : 0100000{ref_c}CPRELEVEMENT",
                f"IDENT : {ident}",
                f"MANDAT : 00-01-00000{ref_c}-{mois_str}-{annee_4}"
            ]
        elif p_format == "MNFCT_STYLE":
            hex_part = "".join(random.choices("0123456789ABCDEF", k=8))
            dig_part = "".join(random.choices("0123456789", k=6))
            lignes = [
                f"PRELEVEMENT DE {nom}",
                f"IDENT : {ident}",
                f"MANDAT : ++1230FF{hex_part}49448D71 9A{dig_part}"
            ]
        else:
            mandat_tmpl = data.get("mandat_template", "SEPA-{digits}-1")
            rand_digits = "".join(random.choices("0123456789", k=8))
            mandat = mandat_tmpl.replace("{digits}", rand_digits)
            lignes = [
                f"PRELEVEMENT DE {nom}",
                f"IDENT : {ident}",
                f"MANDAT : {mandat}"
            ]
    else:
        val = 29.99
        montant = "29,99"
        rand_id = "".join(random.choices("0123456789", k=6))
        rand_m = "".join(random.choices("0123456789", k=8))
        lignes = [
            f"PRELEVEMENT DE {type_prelev}",
            f"IDENT : FR75ZZZ{rand_id}",
            f"MANDAT : SEPA-{rand_m}"
        ]
        
    return {
        'date': date_op,
        'lignes': lignes,
        'montant': montant,
        'amount': float(val),
        'type': 'PRELEVEMENT',
        'signe': '-'
    }

def generate_virement_instantane(month, beneficiaire=None, montant=None, year=2026):
    if not beneficiaire:
        beneficiaire = random.choice(PRENOMS_VIREMENT)
    if montant is None:
        montant = random.choice(['10,00', '15,00', '20,00', '30,00', '50,00'])
        
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    ref_prefix = "OBA" if CURRENT_BANK_TYPE == "lbp" else "REF"
    ref = ref_prefix + "".join(random.choice(chars) for _ in range(14))
    
    lignes = [
        "VIREMENT INSTANTANE A",
        f"{beneficiaire}  {ref}"
    ]
    
    max_days = get_days_in_month(month, year)
    day = random.randint(1, max_days)
    date_op = f"{str(day).zfill(2)}/{str(month).zfill(2)}"
    amt_val = float(str(montant).replace(' ', '').replace(',', '.'))
    
    return {
        'date': date_op,
        'lignes': lignes,
        'montant': montant,
        'amount': amt_val,
        'type': 'VIREMENT EMIS',
        'signe': '-'
    }

def get_dynamic_achats_cb(city, card_number, month, year, nb_transactions=5, 
                          custom_supermarche=None, custom_carburant=None, 
                          custom_resto=None, custom_shopping=None, 
                          custom_loisirs=None, custom_online=None,
                          wealth_profile="moyen"):
    """
    Générateur d'achats CB avec isolation stricte des catégories si des listes personnalisées sont fournies.
    """
    m_supermarche = custom_supermarche if custom_supermarche is not None else MERCHANTS_SUPERMARCHE
    m_carburant = custom_carburant if custom_carburant is not None else MERCHANTS_CARBURANT
    m_resto = custom_resto if custom_resto is not None else MERCHANTS_RESTO
    m_shopping = custom_shopping if custom_shopping is not None else MERCHANTS_SHOPPING
    m_loisirs = custom_loisirs if custom_loisirs is not None else MERCHANTS_LOISIRS
    m_online = custom_online if custom_online is not None else MERCHANTS_ONLINE
    
    has_custom = any(x is not None for x in [custom_supermarche, custom_carburant, custom_resto, custom_shopping, custom_loisirs, custom_online])
    
    available_cats = []
    cat_weights = []
    if has_custom:
        if custom_supermarche is not None and custom_supermarche: available_cats.append("SUPERMARCHE"); cat_weights.append(35)
        if custom_carburant is not None and custom_carburant: available_cats.append("CARBURANT"); cat_weights.append(10)
        if custom_resto is not None and custom_resto: available_cats.append("RESTO"); cat_weights.append(20)
        if custom_shopping is not None and custom_shopping: available_cats.append("SHOPPING"); cat_weights.append(20)
        if custom_loisirs is not None and custom_loisirs: available_cats.append("LOISIRS"); cat_weights.append(10)
        if custom_online is not None and custom_online: available_cats.append("ONLINE"); cat_weights.append(5)
    
    if not available_cats:
        available_cats = ["SUPERMARCHE", "CARBURANT", "RESTO", "SHOPPING", "LOISIRS", "ONLINE"]
        cat_weights = [35, 10, 20, 20, 10, 5]
    
    results = []
    used_merchants_per_day = {}
    used_subscriptions = set()
    
    for _ in range(nb_transactions):
        valid = False
        attempts = 0
        while not valid and attempts < 10:
            attempts += 1
            cat_choice = random.choices(available_cats, weights=cat_weights)[0]
            
            if cat_choice == "SUPERMARCHE" and m_supermarche:
                merchant = random.choice(m_supermarche)
            elif cat_choice == "CARBURANT" and m_carburant:
                merchant = random.choice(m_carburant)
            elif cat_choice == "RESTO" and m_resto:
                merchant = random.choice(m_resto)
            elif cat_choice == "SHOPPING" and m_shopping:
                merchant = random.choice(m_shopping)
            elif cat_choice == "LOISIRS" and m_loisirs:
                merchant = random.choice(m_loisirs)
            elif cat_choice == "ONLINE" and m_online:
                merchant = random.choice(m_online)
                if merchant in used_subscriptions:
                    continue  
            else:
                merchant = "ACHAT DIVERS"
                
            if "[VILLE]" in merchant and city:
                merchant = merchant.replace("[VILLE]", city.upper())
                
            date_achat = generate_random_date(month, year)
            
            if merchant not in used_merchants_per_day.get(date_achat, set()):
                valid = True
                
        if not valid:
            continue 
            
        if cat_choice == "ONLINE":
            used_subscriptions.add(merchant)
            
        if date_achat not in used_merchants_per_day:
            used_merchants_per_day[date_achat] = set()
        used_merchants_per_day[date_achat].add(merchant)
            
        montant = generate_coherent_amount(merchant, wealth_profile=wealth_profile)
        
        lignes = []
        lignes.append(f"ACHAT CB {merchant} {date_achat}")
        
        # Variante EUR réservée aux marchands internationaux
        marchands_internationaux = m_online + ["AMAZON", "UBER", "UBER EATS", "DELIVEROO", "VINTED", "ASOS", "ZALANDO PAYMEN", "APPLE"]
        is_international = any(inter in merchant for inter in marchands_internationaux)
        
        if is_international and random.random() > 0.4:
            lignes.append(f"EUR {montant} CARTE NO {card_number}")
        else:
            lignes.append(f"CARTE NUMERO {card_number}")
            
        max_days = get_days_in_month(month, year)
        day, mo, yr = date_achat.split('.')
        op_day = int(day) + random.randint(0, 2)
        if op_day > max_days: op_day = max_days
        date_op = f"{str(op_day).zfill(2)}/{mo}"
        amt_val = float(str(montant).replace(' ', '').replace(',', '.'))
        
        results.append({
            'date': date_op,
            'lignes': lignes,
            'montant': montant,
            'amount': amt_val,
            'type': 'ACHAT CB',
            'signe': '-'
        })
        
    results.sort(key=get_tx_date_sort_key)
    return results

# ==========================================
# 3. ORCHESTRATEURS DE PROFILS (LOGIQUE METIER)
# ==========================================

OFFICIAL_SAVINGS_RATES = {
    2020: {'LIVRET_A': 0.0050, 'CEL': 0.0075},
    2021: {'LIVRET_A': 0.0050, 'CEL': 0.0075},
    2022: {'LIVRET_A': 0.01375, 'CEL': 0.0096},
    2023: {'LIVRET_A': 0.0292, 'CEL': 0.0194},
    2024: {'LIVRET_A': 0.0300, 'CEL': 0.0200},
    2025: {'LIVRET_A': 0.0216, 'CEL': 0.0144},
    2026: {'LIVRET_A': 0.0160, 'CEL': 0.01125},
}

def get_annual_interest_rate(account_type="LIVRET_A", year=2025):
    try:
        y = int(str(year))
        if y < 100:
            y = 2000 + y
    except Exception:
        y = 2025
        
    rates = OFFICIAL_SAVINGS_RATES.get(y)
    acc_key = 'LIVRET_A' if 'LIVRET' in str(account_type).upper() else 'CEL'
    if not rates:
        return 0.0200 if acc_key == 'LIVRET_A' else 0.0125
    return rates.get(acc_key, 0.02)

def generate_profile_epargne(num_tx, month, year, wealth_profile="moyen", titulaire_nom="DUPONT JEAN", account_type="LIVRET_A", mirror_txs=None, solde_ancien=None, custom_taux=None):
    if num_tx <= 0:
        return []
    txs = []
    if mirror_txs:
        txs.extend(mirror_txs)
        
    remaining = max(0, num_tx - len(txs))
    mois_str = str(month).zfill(2)
    _, year_4 = get_year_strings(year)
    max_days = get_days_in_month(month, year)
    
    if int(month) == 12:
        if custom_taux is not None:
            taux = float(custom_taux)
        else:
            taux = get_annual_interest_rate(account_type, year)
            
        if solde_ancien is not None:
            try:
                s_base = float(str(solde_ancien).replace('€', '').replace('¤', '').replace('+', '').replace(' ', '').replace(',', '.'))
            except Exception:
                s_base = 10000.0 if wealth_profile == "moyen" else (3000.0 if wealth_profile == "pauvre" else 22000.0)
        else:
            s_base = 10000.0 if wealth_profile == "moyen" else (3000.0 if wealth_profile == "pauvre" else 22000.0)
            
        interets = round(max(0.50, s_base * taux), 2)
        tx_interets = {
            "date": f"31/{mois_str}",
            "lignes": [f"INTERETS ACQUIS AU 31/12/{year_4}"],
            "montant": f"{interets:,.2f}".replace(',', ' ').replace('.', ','),
            "amount": interets,
            "signe": "+",
            "type": "INTERETS"
        }
        if remaining > 0:
            txs.append(tx_interets)
            remaining -= 1
        elif len(txs) == 0 and num_tx > 0:
            txs.append(tx_interets)
        
    for _ in range(remaining):
        day = random.randint(1, max_days)
        day_str = f"{day:02d}"
        if wealth_profile == "pauvre":
            amt = random.choice([20.0, 30.0, 50.0, 70.0, 100.0])
        elif wealth_profile == "riche":
            amt = random.choice([200.0, 300.0, 500.0, 800.0, 1000.0, 1500.0, 2000.0])
        else:
            amt = random.choice([50.0, 80.0, 100.0, 150.0, 200.0, 250.0, 300.0, 500.0])
            
        if random.random() > 0.35:
            nom_propre = " ".join(titulaire_nom.upper().split())
            if nom_propre.startswith("MR "): nom_propre = nom_propre[3:]
            elif nom_propre.startswith("MME "): nom_propre = nom_propre[4:]
            elif nom_propre.startswith("M "): nom_propre = nom_propre[2:]
            
            txs.append({
                "date": f"{day_str}/{mois_str}",
                "lignes": [
                    f"VIREMENT DE {nom_propre}",
                    f"DATE DE VALEUR : {day_str} {mois_str} {year_4}"
                ],
                "montant": f"{amt:,.2f}".replace(',', ' ').replace('.', ','),
                "amount": amt,
                "signe": "+",
                "type": "VIREMENT"
            })
        else:
            txs.append({
                "date": f"{day_str}/{mois_str}",
                "lignes": [
                    "VIREMENT VERS COMPTE COURANT",
                    f"DATE DE VALEUR : {day_str} {mois_str} {year_4}"
                ],
                "montant": f"{amt:,.2f}".replace(',', ' ').replace('.', ','),
                "amount": amt,
                "signe": "-",
                "type": "VIREMENT"
            })
            
    txs.sort(key=get_tx_date_sort_key)
    return txs[:num_tx]

def generate_profile_normal(num_tx, city, month, year, card_number="790", wealth_profile="moyen", age_profile="adulte", titulaire_nom="DUPONT JEAN", cp="75000", titulaire_sexe="M", dest_iban=None):
    if num_tx <= 0:
        return []
    orig_num_tx = int(num_tx)
    txs = []
    
    # Frais Bancaires (Cotisation)
    if num_tx > 0:
        tx_frais = generate_frais_bancaires(month, year, wealth_profile=wealth_profile, age_profile=age_profile)
        if tx_frais:
            txs.append(tx_frais)
            num_tx -= 1

    # Aides sociales (CAF)
    if num_tx > 0 and (wealth_profile == "pauvre" or (wealth_profile == "moyen" and random.random() < 0.25)):
        txs.append(generate_caf(month, year, nom_titulaire=titulaire_nom, wealth_profile=wealth_profile, cp=cp))
        num_tx -= 1

    # Remboursement Santé (CPAM/Mutuelle)
    if num_tx > 0:
        if random.random() < 0.4:
            txs.append(generate_cpam(month, year, cp=cp))
            num_tx -= 1
        elif random.random() < 0.2:
            txs.append(generate_mutuelle(month, year, nom_titulaire=titulaire_nom))
            num_tx -= 1

    # Virement Permanent ou Remise de chèque
    if num_tx > 0 and random.random() < 0.2:
        txs.append(generate_virement_permanent(month, year, titulaire_nom=titulaire_nom, titulaire_sexe=titulaire_sexe, dest_iban=dest_iban))
        num_tx -= 1
    if num_tx > 0 and random.random() < 0.1:
        txs.append(generate_remise_cheque(month, year))
        num_tx -= 1

    # 1. Salaire
    if num_tx > 0:
        tx = generate_salaire(month, year, wealth_profile=wealth_profile, city=city)
        txs.append(tx)
        num_tx -= 1

    # Virements Instantanés Reçus (Amis)
    nb_vir_recu = min(num_tx, random.randint(0, 2))
    for _ in range(nb_vir_recu):
        tx = generate_virement_inst_recu(month, year, wealth_profile=wealth_profile)
        txs.append(tx)
        num_tx -= 1

    # Virements Instantanés Emis (Amis)
    nb_vir_emis = min(num_tx, random.randint(1, 3))
    for _ in range(nb_vir_emis):
        tx = generate_virement_inst_emis(month, year, wealth_profile=wealth_profile)
        txs.append(tx)
        num_tx -= 1

    # 2. Prélèvements (Normal)
    if num_tx > 0:
        nb_prel = min(num_tx, random.randint(2, 4))
        available_prelevs = list(PRELEVEMENT_TYPES.keys())
        selected_prel = random.sample(available_prelevs, min(nb_prel, len(available_prelevs)))
        for type_prel in selected_prel:
            tx = generate_prelevement(type_prel, month, year=year, wealth_profile=wealth_profile)
            txs.append(tx)
            num_tx -= 1

    # 3. Retraits (Normal) - Espacés avec minimum 12 jours d'intervalle
    if num_tx > 0:
        nb_retraits = min(num_tx, random.randint(1, 2))
        retraits_list = generate_spaced_retraits(nb_retraits, card_number, month, year, wealth_profile=wealth_profile)
        txs.extend(retraits_list)
        num_tx -= len(retraits_list)

    # 4. Achats CB (Normal)
    if num_tx > 0:
        txs.extend(get_dynamic_achats_cb(city, card_number, month, year, num_tx, wealth_profile=wealth_profile))

    txs.sort(key=get_tx_date_sort_key)
    return txs[:orig_num_tx]

def generate_profile_locataire(num_tx, city, month, year, card_number="790", wealth_profile="moyen", age_profile="adulte", titulaire_nom="DUPONT JEAN", cp="75000", titulaire_sexe="M", dest_iban=None):
    if num_tx <= 0:
        return []
    orig_num_tx = int(num_tx)
    txs = []
    
    # Frais Bancaires (Cotisation)
    if num_tx > 0:
        tx_frais = generate_frais_bancaires(month, year, wealth_profile=wealth_profile, age_profile=age_profile)
        if tx_frais:
            txs.append(tx_frais)
            num_tx -= 1

    # Aides sociales (CAF)
    if num_tx > 0 and (wealth_profile == "pauvre" or (wealth_profile == "moyen" and random.random() < 0.25)):
        txs.append(generate_caf(month, year, nom_titulaire=titulaire_nom, wealth_profile=wealth_profile, cp=cp))
        num_tx -= 1

    # Remboursement Santé (CPAM/Mutuelle)
    if num_tx > 0:
        if random.random() < 0.4:
            txs.append(generate_cpam(month, year, cp=cp))
            num_tx -= 1
        elif random.random() < 0.2:
            txs.append(generate_mutuelle(month, year, nom_titulaire=titulaire_nom))
            num_tx -= 1

    # 1. Salaire (Revenus clairs et réguliers)
    if num_tx > 0:
        tx = generate_salaire(month, year, wealth_profile=wealth_profile, city=city)
        txs.append(tx)
        num_tx -= 1

    # Virements Instantanés Reçus (Amis)
    nb_vir_recu = min(num_tx, random.randint(0, 1))
    for _ in range(nb_vir_recu):
        tx = generate_virement_inst_recu(month, year, wealth_profile=wealth_profile)
        txs.append(tx)
        num_tx -= 1

    # Virements Instantanés Emis (Amis)
    nb_vir_emis = min(num_tx, random.randint(0, 2))
    for _ in range(nb_vir_emis):
        tx = generate_virement_inst_emis(month, year, wealth_profile=wealth_profile)
        txs.append(tx)
        num_tx -= 1

    # 2. Prélèvements Filtrés
    if num_tx > 0:
        nb_prel = min(num_tx, random.randint(2, 3))
        available_prelevs = ['FREE_MOBILE', 'FITNESS_PARK', 'ORANGE', 'BOUYGUES', 'MUTUELLE'] 
        selected_prel = random.sample(available_prelevs, min(nb_prel, len(available_prelevs)))
        for type_prel in selected_prel:
            tx = generate_prelevement(type_prel, month, year=year, wealth_profile=wealth_profile)
            txs.append(tx)
            num_tx -= 1

    # 3. Retraits
    if num_tx > 0 and random.random() < 0.6:
        retraits_list = generate_spaced_retraits(1, card_number, month, year, wealth_profile=wealth_profile)
        txs.extend(retraits_list)
        num_tx -= len(retraits_list)

    # 4. Achats CB
    if num_tx > 0:
        locataire_resto = ["BOULANGERIE [VILLE]", "MCDONALDS"] 
        locataire_shopping = ["DECATHLON", "IKEA", "H&M"] 
        txs.extend(get_dynamic_achats_cb(
            city, card_number, month, year, num_tx,
            custom_resto=locataire_resto,
            custom_shopping=locataire_shopping,
            wealth_profile=wealth_profile
        ))

    txs.sort(key=get_tx_date_sort_key)
    return txs[:orig_num_tx]

def generate_profile_fonctionnaire(num_tx, city, month, year, card_number="790", wealth_profile="moyen", age_profile="adulte", titulaire_nom="DUPONT JEAN", cp="75000", titulaire_sexe="M", dest_iban=None):
    if num_tx <= 0:
        return []
    orig_num_tx = int(num_tx)
    txs = []
    
    if num_tx > 0:
        tx_frais = generate_frais_bancaires(month, year, wealth_profile=wealth_profile, age_profile=age_profile)
        if tx_frais:
            txs.append(tx_frais)
            num_tx -= 1

    if num_tx > 0:
        txs.append(generate_salaire_fonctionnaire(month, year, city=city, wealth_profile=wealth_profile))
        num_tx -= 1

    if num_tx > 0:
        if random.random() < 0.5:
            txs.append(generate_cpam(month, year, cp=cp))
            num_tx -= 1
        elif random.random() < 0.5:
            txs.append(generate_mutuelle(month, year, nom_titulaire=titulaire_nom))
            num_tx -= 1

    if num_tx > 0:
        nb_prel = min(num_tx, random.randint(2, 4))
        available = ['MGEN', 'MNT', 'INTERIALE', 'CASDEN', 'GMF', 'EDF', 'ORANGE', 'ENGIE']
        selected = random.sample(available, min(nb_prel, len(available)))
        for p in selected:
            txs.append(generate_prelevement(p, month, year=year, wealth_profile=wealth_profile))
            num_tx -= 1

    if num_tx > 0 and random.random() < 0.3:
        txs.append(generate_virement_permanent(month, year, titulaire_nom=titulaire_nom, titulaire_sexe=titulaire_sexe, dest_iban=dest_iban))
        num_tx -= 1

    if num_tx > 0:
        nb_retraits = min(num_tx, random.randint(1, 2))
        retraits_list = generate_spaced_retraits(nb_retraits, card_number, month, year, wealth_profile=wealth_profile)
        txs.extend(retraits_list)
        num_tx -= len(retraits_list)

    if num_tx > 0:
        fonct_shopping = ["SNCF VOYAGEURS", "RATP INTERNET", "FNAC", "LIBRAIRIE DU CENTRE [VILLE]", "DECATHLON"]
        fonct_resto = ["BOULANGERIE [VILLE]", "RESTAURANT LE BISTROT [VILLE]"]
        txs.extend(get_dynamic_achats_cb(
            city, card_number, month, year, num_tx,
            custom_resto=fonct_resto,
            custom_shopping=fonct_shopping,
            wealth_profile=wealth_profile
        ))

    txs.sort(key=get_tx_date_sort_key)
    return txs[:orig_num_tx]

def generate_profile_chomage(num_tx, city, month, year, card_number="790", wealth_profile="pauvre", age_profile="adulte", titulaire_nom="DUPONT JEAN", cp="75000", titulaire_sexe="M", dest_iban=None):
    if num_tx <= 0:
        return []
    orig_num_tx = int(num_tx)
    txs = []
    
    if num_tx > 0:
        tx_frais = generate_frais_bancaires(month, year, wealth_profile=wealth_profile, age_profile=age_profile)
        if tx_frais:
            txs.append(tx_frais)
            num_tx -= 1

    if num_tx > 0:
        txs.append(generate_france_travail(month, year, wealth_profile=wealth_profile))
        num_tx -= 1

    if num_tx > 0 and random.random() < 0.75:
        txs.append(generate_caf(month, year, nom_titulaire=titulaire_nom, wealth_profile="pauvre", cp=cp))
        num_tx -= 1

    if num_tx > 0:
        txs.append(generate_cpam(month, year, cp=cp))
        num_tx -= 1

    if num_tx > 0:
        nb_prel = min(num_tx, random.randint(1, 3))
        available = ['FREE_MOBILE', 'EDF', 'MUTUELLE', 'EAU_SERVICES', 'ENGIE']
        selected = random.sample(available, min(nb_prel, len(available)))
        for p in selected:
            txs.append(generate_prelevement(p, month, year=year, wealth_profile="pauvre"))
            num_tx -= 1

    if num_tx > 0 and random.random() < 0.5:
        retraits_list = generate_spaced_retraits(1, card_number, month, year, wealth_profile="pauvre")
        txs.extend(retraits_list)
        num_tx -= len(retraits_list)

    if num_tx > 0:
        chom_shopping = ["LIDL [VILLE]", "ALDI [VILLE]", "ACTION [VILLE]", "ACTION"]
        chom_resto = ["BOULANGERIE [VILLE]", "MCDONALDS"]
        txs.extend(get_dynamic_achats_cb(
            city, card_number, month, year, num_tx,
            custom_resto=chom_resto,
            custom_shopping=chom_shopping,
            wealth_profile="pauvre"
        ))

    txs.sort(key=get_tx_date_sort_key)
    return txs[:orig_num_tx]

def generate_profile_artisan(num_tx, city, month, year, card_number="790", wealth_profile="moyen", age_profile="adulte", titulaire_nom="DUPONT JEAN", cp="75000", titulaire_sexe="M", dest_iban=None):
    if num_tx <= 0:
        return []
    orig_num_tx = int(num_tx)
    txs = []
    
    if num_tx > 0:
        tx_frais = generate_frais_bancaires(month, year, wealth_profile=wealth_profile, age_profile=age_profile)
        if tx_frais:
            txs.append(tx_frais)
            num_tx -= 1

    nb_chantiers = min(num_tx, random.randint(2, 3))
    for _ in range(nb_chantiers):
        txs.append(generate_virement_chantier_client(month, year, wealth_profile=wealth_profile))
        num_tx -= 1

    if num_tx > 0 and random.random() < 0.7:
        txs.append(generate_remise_cheque(month, year))
        num_tx -= 1

    if num_tx > 0:
        txs.append(generate_urssaf(month, year, wealth_profile=wealth_profile))
        num_tx -= 1

    if num_tx > 0:
        nb_prel = min(num_tx, random.randint(2, 3))
        available = ['PRO_BTP', 'SMABTP', 'TOTAL_FLEET', 'TELEPEAGE', 'ORANGE', 'MUTUELLE']
        selected = random.sample(available, min(nb_prel, len(available)))
        for p in selected:
            txs.append(generate_prelevement(p, month, year=year, wealth_profile=wealth_profile))
            num_tx -= 1

    if num_tx > 0:
        nb_retraits = min(num_tx, random.randint(1, 2))
        retraits_list = generate_spaced_retraits(nb_retraits, card_number, month, year, wealth_profile=wealth_profile)
        txs.extend(retraits_list)
        num_tx -= len(retraits_list)

    if num_tx > 0:
        art_shopping = ["POINT.P [VILLE]", "LEROY MERLIN [VILLE]", "BRICOMAN", "WURTH FRANCE", "TOTALENERGIES"]
        art_resto = ["RESTAURANT LE BISTROT [VILLE]", "BOULANGERIE [VILLE]"]
        txs.extend(get_dynamic_achats_cb(
            city, card_number, month, year, num_tx,
            custom_resto=art_resto,
            custom_shopping=art_shopping,
            wealth_profile=wealth_profile
        ))

    txs.sort(key=get_tx_date_sort_key)
    return txs[:orig_num_tx]

def generate_profile_famille(num_tx, city, month, year, card_number="790", wealth_profile="moyen", age_profile="adulte", titulaire_nom="DUPONT JEAN", cp="75000", titulaire_sexe="M", dest_iban=None):
    if num_tx <= 0:
        return []
    orig_num_tx = int(num_tx)
    txs = []
    
    if num_tx > 0:
        tx_frais = generate_frais_bancaires(month, year, wealth_profile=wealth_profile, age_profile=age_profile)
        if tx_frais:
            txs.append(tx_frais)
            num_tx -= 1

    if num_tx > 0:
        txs.append(generate_salaire(month, year, city=city, wealth_profile=wealth_profile))
        num_tx -= 1

    if num_tx > 0:
        txs.append(generate_caf_famille(month, year, cp=cp))
        num_tx -= 1

    if num_tx > 0:
        if random.random() < 0.6:
            txs.append(generate_cpam(month, year, cp=cp))
            num_tx -= 1
        elif random.random() < 0.6:
            txs.append(generate_mutuelle(month, year, nom_titulaire=titulaire_nom))
            num_tx -= 1

    if num_tx > 0:
        nb_prel = min(num_tx, random.randint(2, 4))
        available = ['MAIRIE_SCOLAIRE', 'CRECHE', 'MUTUELLE', 'EDF', 'ENGIE', 'FREE_TELECOM', 'ORANGE', 'EAU_SERVICES']
        selected = random.sample(available, min(nb_prel, len(available)))
        for p in selected:
            txs.append(generate_prelevement(p, month, year=year, wealth_profile=wealth_profile))
            num_tx -= 1

    if num_tx > 0 and random.random() < 0.4:
        txs.append(generate_virement_permanent(month, year, titulaire_nom=titulaire_nom, titulaire_sexe=titulaire_sexe, dest_iban=dest_iban))
        num_tx -= 1

    if num_tx > 0:
        nb_retraits = min(num_tx, random.randint(1, 2))
        retraits_list = generate_spaced_retraits(nb_retraits, card_number, month, year, wealth_profile=wealth_profile)
        txs.extend(retraits_list)
        num_tx -= len(retraits_list)

    if num_tx > 0:
        fam_shopping = ["CARREFOUR DRIVE [VILLE]", "LECLERC DRIVE [VILLE]", "AUCHAN [VILLE]", "KIABI", "ORCHESTRA", "DECATHLON", "JOUET CLUB"]
        fam_resto = ["MCDONALDS", "BURGER KING", "CINEMA UGC [VILLE]", "BOULANGERIE [VILLE]"]
        txs.extend(get_dynamic_achats_cb(
            city, card_number, month, year, num_tx,
            custom_resto=fam_resto,
            custom_shopping=fam_shopping,
            wealth_profile=wealth_profile
        ))

    txs.sort(key=get_tx_date_sort_key)
    return txs[:orig_num_tx]

def generate_profile_investisseur(num_tx, city, month, year, card_number="790", wealth_profile="riche", age_profile="adulte", titulaire_nom="DUPONT JEAN", cp="75000", titulaire_sexe="M", dest_iban=None):
    if num_tx <= 0:
        return []
    orig_num_tx = int(num_tx)
    txs = []
    
    if num_tx > 0:
        tx_frais = generate_frais_bancaires(month, year, wealth_profile="riche", age_profile=age_profile)
        if tx_frais:
            txs.append(tx_frais)
            num_tx -= 1

    if num_tx > 0:
        txs.append(generate_salaire(month, year, city=city, wealth_profile="riche"))
        num_tx -= 1

    nb_loyers = min(num_tx, random.randint(1, 2))
    for _ in range(nb_loyers):
        txs.append(generate_loyer_recu_investisseur(month, year, wealth_profile="riche"))
        num_tx -= 1

    if num_tx > 0:
        nb_prel = min(num_tx, random.randint(2, 4))
        available = ['SYNDIC_FONCIA', 'SYNDIC_CITYA', 'CNP_ASSURANCE', 'EDF', 'ORANGE', 'MUTUELLE']
        selected = random.sample(available, min(nb_prel, len(available)))
        for p in selected:
            txs.append(generate_prelevement(p, month, year=year, wealth_profile="riche"))
            num_tx -= 1

    if num_tx > 0:
        txs.append(generate_virement_permanent(month, year, titulaire_nom=titulaire_nom, titulaire_sexe=titulaire_sexe, dest_iban=dest_iban))
        num_tx -= 1

    if num_tx > 0:
        nb_retraits = min(num_tx, random.randint(1, 2))
        retraits_list = generate_spaced_retraits(nb_retraits, card_number, month, year, wealth_profile="riche")
        txs.extend(retraits_list)
        num_tx -= len(retraits_list)

    if num_tx > 0:
        inv_shopping = ["AIR FRANCE", "HOTEL MERCURE [VILLE]", "GALERIES LAFAYETTE", "FNAC", "TOTALENERGIES", "NESPRESSO"]
        inv_resto = ["RESTAURANT GASTRONOMIQUE [VILLE]", "RESTAURANT LE BISTROT [VILLE]", "BOULANGERIE [VILLE]"]
        txs.extend(get_dynamic_achats_cb(
            city, card_number, month, year, num_tx,
            custom_resto=inv_resto,
            custom_shopping=inv_shopping,
            wealth_profile="riche"
        ))

    txs.sort(key=get_tx_date_sort_key)
    return txs[:orig_num_tx]

def generate_profile_demandeur_credit(num_tx, city, month, year, card_number="790", wealth_profile="moyen", age_profile="adulte", titulaire_nom="DUPONT JEAN", cp="75000", titulaire_sexe="M", dest_iban=None):
    if num_tx <= 0:
        return []
    orig_num_tx = int(num_tx)
    txs = []
    
    if num_tx > 0:
        tx_frais = generate_frais_bancaires(month, year, wealth_profile=wealth_profile, age_profile=age_profile)
        if tx_frais:
            txs.append(tx_frais)
            num_tx -= 1

    if num_tx > 0:
        txs.append(generate_salaire(month, year, city=city, wealth_profile=wealth_profile))
        num_tx -= 1

    if num_tx > 0:
        txs.append(generate_prelevement_loyer_bailleur(month, year, wealth_profile=wealth_profile))
        num_tx -= 1

    if num_tx > 0 and random.random() < 0.6:
        txs.append(generate_cpam(month, year, cp=cp))
        num_tx -= 1

    if num_tx > 0 and CURRENT_ALLOW_EPARGNE:
        txs.append(generate_virement_epargne(month, year, wealth_profile=wealth_profile))
        num_tx -= 1

    if num_tx > 0:
        nb_prel = min(num_tx, random.randint(2, 3))
        available = ['EDF', 'ENGIE', 'ASSURANCE', 'MUTUELLE', 'ORANGE', 'EAU_SERVICES', 'BOUYGUES']
        selected = random.sample(available, min(nb_prel, len(available)))
        for p in selected:
            txs.append(generate_prelevement(p, month, year=year, wealth_profile=wealth_profile))
            num_tx -= 1

    if num_tx > 0 and random.random() < 0.5:
        retraits_list = generate_spaced_retraits(1, card_number, month, year, wealth_profile=wealth_profile)
        txs.extend(retraits_list)
        num_tx -= len(retraits_list)

    if num_tx > 0:
        credit_shopping = ["CARREFOUR", "LECLERC", "TOTALENERGIES", "PHARMACIE DE LA PLACE [VILLE]", "FNAC", "DECATHLON", "IKEA", "LEROY MERLIN"]
        credit_resto = ["BOULANGERIE [VILLE]", "RESTAURANT LE BISTROT [VILLE]"]
        txs.extend(get_dynamic_achats_cb(
            city, card_number, month, year, num_tx,
            custom_resto=credit_resto,
            custom_shopping=credit_shopping,
            wealth_profile=wealth_profile
        ))

    txs.sort(key=get_tx_date_sort_key)
    return txs[:orig_num_tx]

CROUS_ACADEMIES = {
    "75": "DE PARIS",
    "94": "DE CRETEIL", "93": "DE CRETEIL", "77": "DE CRETEIL",
    "92": "DE VERSAILLES", "78": "DE VERSAILLES", "91": "DE VERSAILLES", "95": "DE VERSAILLES",
    "13": "D AIX MARSEILLE", "84": "D AIX MARSEILLE", "04": "D AIX MARSEILLE", "05": "D AIX MARSEILLE",
    "69": "DE LYON", "42": "DE LYON", "01": "DE LYON",
    "31": "DE TOULOUSE OCCITANIE", "09": "DE TOULOUSE OCCITANIE", "12": "DE TOULOUSE OCCITANIE", "32": "DE TOULOUSE OCCITANIE", "46": "DE TOULOUSE OCCITANIE", "65": "DE TOULOUSE OCCITANIE", "81": "DE TOULOUSE OCCITANIE", "82": "DE TOULOUSE OCCITANIE",
    "33": "DE BORDEAUX AQUITAINE", "24": "DE BORDEAUX AQUITAINE", "40": "DE BORDEAUX AQUITAINE", "47": "DE BORDEAUX AQUITAINE", "64": "DE BORDEAUX AQUITAINE",
    "59": "DE LILLE NORD PAS DE CALAIS", "62": "DE LILLE NORD PAS DE CALAIS",
    "44": "DE NANTES PAYS DE LA LOIRE", "49": "DE NANTES PAYS DE LA LOIRE", "53": "DE NANTES PAYS DE LA LOIRE", "72": "DE NANTES PAYS DE LA LOIRE", "85": "DE NANTES PAYS DE LA LOIRE",
    "06": "DE NICE TOULON", "83": "DE NICE TOULON",
    "67": "DE STRASBOURG", "68": "DE STRASBOURG",
    "34": "DE MONTPELLIER OCCITANIE", "11": "DE MONTPELLIER OCCITANIE", "30": "DE MONTPELLIER OCCITANIE", "48": "DE MONTPELLIER OCCITANIE", "66": "DE MONTPELLIER OCCITANIE",
    "35": "DE RENNES BRETAGNE", "22": "DE RENNES BRETAGNE", "29": "DE RENNES BRETAGNE", "56": "DE RENNES BRETAGNE",
    "38": "DE GRENOBLE ALPES", "73": "DE GRENOBLE ALPES", "74": "DE GRENOBLE ALPES", "26": "DE GRENOBLE ALPES", "07": "DE GRENOBLE ALPES",
    "63": "DE CLERMONT AUVERGNE", "03": "DE CLERMONT AUVERGNE", "15": "DE CLERMONT AUVERGNE", "43": "DE CLERMONT AUVERGNE",
    "21": "DE DIJON", "58": "DE DIJON", "71": "DE DIJON", "89": "DE DIJON",
    "25": "DE BESANCON", "39": "DE BESANCON", "70": "DE BESANCON", "90": "DE BESANCON",
    "76": "DE NORMANDIE", "27": "DE NORMANDIE", "14": "DE NORMANDIE", "50": "DE NORMANDIE", "61": "DE NORMANDIE",
    "51": "DE REIMS", "08": "DE REIMS", "10": "DE REIMS", "52": "DE REIMS",
    "54": "DE NANCY METZ LORRAINE", "55": "DE NANCY METZ LORRAINE", "57": "DE NANCY METZ LORRAINE", "88": "DE NANCY METZ LORRAINE",
    "37": "D ORLEANS TOURS", "18": "D ORLEANS TOURS", "28": "D ORLEANS TOURS", "36": "D ORLEANS TOURS", "41": "D ORLEANS TOURS", "45": "D ORLEANS TOURS",
    "86": "DE POITIERS", "16": "DE POITIERS", "17": "DE POITIERS", "79": "DE POITIERS",
    "80": "D AMIENS", "02": "D AMIENS", "60": "D AMIENS",
    "20": "DE CORSE", "2A": "DE CORSE", "2B": "DE CORSE"
}

CARSAT_REGIONS = {
    "75": "CARSAT ILE DE FRANCE", "77": "CARSAT ILE DE FRANCE", "78": "CARSAT ILE DE FRANCE", "91": "CARSAT ILE DE FRANCE", "92": "CARSAT ILE DE FRANCE", "93": "CARSAT ILE DE FRANCE", "94": "CARSAT ILE DE FRANCE", "95": "CARSAT ILE DE FRANCE",
    "31": "CARSAT MIDI PYRENEES", "09": "CARSAT MIDI PYRENEES", "12": "CARSAT MIDI PYRENEES", "32": "CARSAT MIDI PYRENEES", "46": "CARSAT MIDI PYRENEES", "65": "CARSAT MIDI PYRENEES", "81": "CARSAT MIDI PYRENEES", "82": "CARSAT MIDI PYRENEES",
    "69": "CARSAT RHONE ALPES", "01": "CARSAT RHONE ALPES", "07": "CARSAT RHONE ALPES", "26": "CARSAT RHONE ALPES", "38": "CARSAT RHONE ALPES", "42": "CARSAT RHONE ALPES", "73": "CARSAT RHONE ALPES", "74": "CARSAT RHONE ALPES",
    "33": "CARSAT AQUITAINE", "24": "CARSAT AQUITAINE", "40": "CARSAT AQUITAINE", "47": "CARSAT AQUITAINE", "64": "CARSAT AQUITAINE",
    "13": "CARSAT DU SUD EST", "04": "CARSAT DU SUD EST", "05": "CARSAT DU SUD EST", "06": "CARSAT DU SUD EST", "83": "CARSAT DU SUD EST", "84": "CARSAT DU SUD EST",
    "59": "CARSAT HAUTS DE FRANCE", "62": "CARSAT HAUTS DE FRANCE", "80": "CARSAT HAUTS DE FRANCE", "02": "CARSAT HAUTS DE FRANCE", "60": "CARSAT HAUTS DE FRANCE",
    "44": "CARSAT PAYS DE LA LOIRE", "49": "CARSAT PAYS DE LA LOIRE", "53": "CARSAT PAYS DE LA LOIRE", "72": "CARSAT PAYS DE LA LOIRE", "85": "CARSAT PAYS DE LA LOIRE",
    "35": "CARSAT BRETAGNE", "22": "CARSAT BRETAGNE", "29": "CARSAT BRETAGNE", "56": "CARSAT BRETAGNE",
    "34": "CARSAT LANGUEDOC ROUSSILLON", "11": "CARSAT LANGUEDOC ROUSSILLON", "30": "CARSAT LANGUEDOC ROUSSILLON", "48": "CARSAT LANGUEDOC ROUSSILLON", "66": "CARSAT LANGUEDOC ROUSSILLON",
    "67": "CARSAT ALSACE MOSELLE", "68": "CARSAT ALSACE MOSELLE", "57": "CARSAT ALSACE MOSELLE",
    "76": "CARSAT NORMANDIE", "27": "CARSAT NORMANDIE", "14": "CARSAT NORMANDIE", "50": "CARSAT NORMANDIE", "61": "CARSAT NORMANDIE",
    "37": "CARSAT CENTRE VAL DE LOIRE", "18": "CARSAT CENTRE VAL DE LOIRE", "28": "CARSAT CENTRE VAL DE LOIRE", "36": "CARSAT CENTRE VAL DE LOIRE", "41": "CARSAT CENTRE VAL DE LOIRE", "45": "CARSAT CENTRE VAL DE LOIRE",
    "63": "CARSAT AUVERGNE", "03": "CARSAT AUVERGNE", "15": "CARSAT AUVERGNE", "43": "CARSAT AUVERGNE",
    "21": "CARSAT BOURGOGNE FRANCHE COMTE", "25": "CARSAT BOURGOGNE FRANCHE COMTE", "39": "CARSAT BOURGOGNE FRANCHE COMTE", "58": "CARSAT BOURGOGNE FRANCHE COMTE", "70": "CARSAT BOURGOGNE FRANCHE COMTE", "71": "CARSAT BOURGOGNE FRANCHE COMTE", "89": "CARSAT BOURGOGNE FRANCHE COMTE", "90": "CARSAT BOURGOGNE FRANCHE COMTE"
}

def generate_crous(month, year, cp="75000", city="PARIS"):
    day = random.randint(3, 7)
    date_str = f"{day:02d}/{str(month).zfill(2)}"
    mois_str = str(month).zfill(2)
    full_year = str(year) if len(str(year)) == 4 else f"20{str(year)[-2:]}"
    amt = round(random.uniform(180.0, 560.0), 2)
    dept_code = str(cp)[:2] if cp else "75"
    crous_label = CROUS_ACADEMIES.get(dept_code, f"DE {city.upper()}" if city else "DE PARIS")
    return {
        "date": date_str,
        "lignes": [
            f"VIREMENT DU CROUS {crous_label}",
            f"BOURSE SUR CRITERES SOCIAUX {mois_str}/{full_year}"
        ],
        "montant": f"{amt:,.2f}".replace(',', ' ').replace('.', ','),
        "amount": amt,
        "signe": "+",
        "type": "VIREMENT EN VOTRE FAVEUR"
    }

def generate_retraite_carsat(month, year, cp="75000", city="PARIS"):
    day = random.randint(8, 10)
    date_str = f"{day:02d}/{str(month).zfill(2)}"
    mois_str = str(month).zfill(2)
    full_year = str(year) if len(str(year)) == 4 else f"20{str(year)[-2:]}"
    amt = round(random.uniform(1150.0, 2150.0), 2)
    dept_code = str(cp)[:2] if cp else "75"
    carsat_nom = CARSAT_REGIONS.get(dept_code, "CARSAT RETRAITE")
    return {
        "date": date_str,
        "lignes": [
            f"VIREMENT DE {carsat_nom}",
            f"PENSION PRINCIPALE {mois_str}/{full_year}"
        ],
        "montant": f"{amt:,.2f}".replace(',', ' ').replace('.', ','),
        "amount": amt,
        "signe": "+",
        "type": "VIREMENT EN VOTRE FAVEUR"
    }

def generate_retraite_agirc_arrco(month, year):
    day = random.randint(2, 4)
    date_str = f"{day:02d}/{str(month).zfill(2)}"
    mois_str = str(month).zfill(2)
    full_year = str(year) if len(str(year)) == 4 else f"20{str(year)[-2:]}"
    amt = round(random.uniform(420.0, 1180.0), 2)
    return {
        "date": date_str,
        "lignes": [
            "VIREMENT DE AGIRC-ARRCO",
            f"RETRAITE COMPLEMENTAIRE {mois_str}/{full_year}"
        ],
        "montant": f"{amt:,.2f}".replace(',', ' ').replace('.', ','),
        "amount": amt,
        "signe": "+",
        "type": "VIREMENT EN VOTRE FAVEUR"
    }

def generate_virement_client_pro(month, year, wealth_profile="moyen"):
    day = random.randint(5, 27)
    date_str = f"{day:02d}/{str(month).zfill(2)}"
    client_names = [
        "NEXITY SERVICES SAS", "SOCIETE GENERALE SA", "CAPGEMINI TECHNOLOGY", 
        "AXA FRANCE IARD", "ORANGE SA", "BOUYGUES CONSTRUCTION", 
        "STUDIO DESIGN SARL", "AGENCE DIGITALE SAS", "CONSULTING EXPERTISE SAS"
    ]
    client = random.choice(client_names)
    ref_fac = f"FAC-{random.randint(1000, 9999)}"
    amt = round(random.uniform(1400.0, 4800.0) if wealth_profile == "riche" else random.uniform(650.0, 2600.0), 2)
    return {
        "date": date_str,
        "lignes": [
            f"VIREMENT DE {client}",
            f"REGLEMENT FACTURE REF {ref_fac}"
        ],
        "montant": f"{amt:,.2f}".replace(',', ' ').replace('.', ','),
        "amount": amt,
        "signe": "+",
        "type": "VIREMENT EN VOTRE FAVEUR"
    }

def generate_urssaf(month, year, wealth_profile="moyen"):
    day = random.randint(15, 22)
    date_str = f"{day:02d}/{str(month).zfill(2)}"
    amt = round(random.uniform(450.0, 1850.0) if wealth_profile == "riche" else random.uniform(140.0, 680.0), 2)
    ref_id = f"URSSAF-{random.randint(10000000, 99999999)}"
    return {
        "date": date_str,
        "lignes": [
            "PRELEVEMENT DE URSSAF",
            f"REF : {ref_id} IDENT : FR73ZZZ394821",
            f"MANDAT : {ref_id}-1"
        ],
        "montant": f"{amt:,.2f}".replace(',', ' ').replace('.', ','),
        "amount": amt,
        "signe": "-",
        "type": "PRELEVEMENT"
    }

def generate_profile_etudiant(num_tx, city, month, year, card_number="790", wealth_profile="pauvre", age_profile="jeune", titulaire_nom="DUPONT JEAN", cp="75000", titulaire_sexe="M", dest_iban=None):
    if num_tx <= 0:
        return []
    orig_num_tx = int(num_tx)
    txs = []
    
    # Frais Bancaires (Cotisation Jeune)
    if num_tx > 0:
        tx_frais = generate_frais_bancaires(month, year, wealth_profile=wealth_profile, age_profile="jeune")
        if tx_frais:
            txs.append(tx_frais)
            num_tx -= 1

    # Bourse CROUS
    if num_tx > 0:
        txs.append(generate_crous(month, year, cp=cp, city=city))
        num_tx -= 1

    # APL CAF
    if num_tx > 0 and random.random() < 0.8:
        txs.append(generate_caf(month, year, nom_titulaire=titulaire_nom, wealth_profile="pauvre", cp=cp))
        num_tx -= 1

    # Aide familiale ou Virement d'un proche
    if num_tx > 0 and random.random() < 0.6:
        txs.append(generate_virement_inst_recu(month, year, wealth_profile="pauvre"))
        num_tx -= 1

    # Petits virements entre amis
    nb_vir = min(num_tx, random.randint(1, 2))
    for _ in range(nb_vir):
        txs.append(generate_virement_inst_emis(month, year, wealth_profile="pauvre"))
        num_tx -= 1

    # Prélèvements spécifiques étudiants
    if num_tx > 0:
        nb_prel = min(num_tx, random.randint(1, 3))
        available = ['FREE_MOBILE', 'SPOTIFY', 'NETFLIX', 'FITNESS_PARK']
        selected = random.sample(available, min(nb_prel, len(available)))
        for p in selected:
            txs.append(generate_prelevement(p, month, year=year, wealth_profile="pauvre"))
            num_tx -= 1

    # Retraits
    if num_tx > 0 and random.random() < 0.5:
        retraits_list = generate_spaced_retraits(1, card_number, month, year, wealth_profile="pauvre")
        txs.extend(retraits_list)
        num_tx -= len(retraits_list)

    # Achats CB orientés étudiants
    if num_tx > 0:
        etudiant_resto = ["RESTAU U CROUS [VILLE]", "MCDONALDS", "BURGER KING", "BOULANGERIE [VILLE]"]
        etudiant_shopping = ["VINTED", "H&M", "ZARA", "DECATHLON"]
        txs.extend(get_dynamic_achats_cb(
            city, card_number, month, year, num_tx,
            custom_resto=etudiant_resto,
            custom_shopping=etudiant_shopping,
            wealth_profile="pauvre"
        ))

    txs.sort(key=get_tx_date_sort_key)
    return txs[:orig_num_tx]

def generate_profile_retraite(num_tx, city, month, year, card_number="790", wealth_profile="moyen", age_profile="senior", titulaire_nom="DUPONT JEAN", cp="75000", titulaire_sexe="M", dest_iban=None):
    if num_tx <= 0:
        return []
    orig_num_tx = int(num_tx)
    txs = []
    
    # Frais Bancaires
    if num_tx > 0:
        tx_frais = generate_frais_bancaires(month, year, wealth_profile=wealth_profile, age_profile="senior")
        if tx_frais:
            txs.append(tx_frais)
            num_tx -= 1

    # Pension principale CARSAT
    if num_tx > 0:
        txs.append(generate_retraite_carsat(month, year, cp=cp, city=city))
        num_tx -= 1

    # Pension complémentaire Agirc-Arrco
    if num_tx > 0:
        txs.append(generate_retraite_agirc_arrco(month, year))
        num_tx -= 1

    # Remboursements Santé réguliers
    if num_tx > 0:
        if random.random() < 0.5:
            txs.append(generate_cpam(month, year, cp=cp))
            num_tx -= 1
        elif random.random() < 0.5:
            txs.append(generate_mutuelle(month, year, nom_titulaire=titulaire_nom))
            num_tx -= 1

    # Remise de chèque occasionnelle
    if num_tx > 0 and random.random() < 0.4:
        txs.append(generate_remise_cheque(month, year))
        num_tx -= 1

    # Prélèvements du quotidien / Maison & Assurances mutualistes
    if num_tx > 0:
        nb_prel = min(num_tx, random.randint(2, 4))
        available = ['EDF', 'ENGIE', 'MUTUELLE', 'ORANGE', 'EAU_SERVICES', 'GMF', 'MAIF', 'MACIF']
        selected = random.sample(available, min(nb_prel, len(available)))
        for p in selected:
            txs.append(generate_prelevement(p, month, year=year, wealth_profile=wealth_profile))
            num_tx -= 1

    # Retraits DAB espacés
    if num_tx > 0:
        nb_retraits = min(num_tx, random.randint(1, 2))
        retraits_list = generate_spaced_retraits(nb_retraits, card_number, month, year, wealth_profile=wealth_profile)
        txs.extend(retraits_list)
        num_tx -= len(retraits_list)

    # Achats CB Seniors
    if num_tx > 0:
        senior_shopping = ["PHARMACIE DE LA POSTE [VILLE]", "PRESSE MAISON DE LA PRESSE", "JARDILAND", "GAMM VERT"]
        senior_resto = ["BOULANGERIE [VILLE]", "RESTAURANT LE BISTROT [VILLE]"]
        txs.extend(get_dynamic_achats_cb(
            city, card_number, month, year, num_tx,
            custom_resto=senior_resto,
            custom_shopping=senior_shopping,
            wealth_profile=wealth_profile
        ))

    txs.sort(key=get_tx_date_sort_key)
    return txs[:orig_num_tx]

def generate_profile_independant(num_tx, city, month, year, card_number="790", wealth_profile="moyen", age_profile="adulte", titulaire_nom="DUPONT JEAN", cp="75000", titulaire_sexe="M", dest_iban=None):
    if num_tx <= 0:
        return []
    orig_num_tx = int(num_tx)
    txs = []
    
    # Frais Bancaires
    if num_tx > 0:
        tx_frais = generate_frais_bancaires(month, year, wealth_profile=wealth_profile, age_profile=age_profile)
        if tx_frais:
            txs.append(tx_frais)
            num_tx -= 1

    # Encaissements clients réguliers
    nb_clients = min(num_tx, random.randint(2, 4))
    for _ in range(nb_clients):
        txs.append(generate_virement_client_pro(month, year, wealth_profile=wealth_profile))
        num_tx -= 1

    # Cotisations URSSAF
    if num_tx > 0:
        txs.append(generate_urssaf(month, year, wealth_profile=wealth_profile))
        num_tx -= 1

    # Remboursement Santé occasionnel
    if num_tx > 0 and random.random() < 0.3:
        txs.append(generate_cpam(month, year, cp=cp))
        num_tx -= 1

    # Prélèvements Pro / Télécom
    if num_tx > 0:
        nb_prel = min(num_tx, random.randint(1, 3))
        available = ['ORANGE', 'FREE_MOBILE', 'BOUYGUES', 'MUTUELLE']
        selected = random.sample(available, min(nb_prel, len(available)))
        for p in selected:
            txs.append(generate_prelevement(p, month, year=year, wealth_profile=wealth_profile))
            num_tx -= 1

    # Retraits DAB
    if num_tx > 0 and random.random() < 0.5:
        retraits_list = generate_spaced_retraits(1, card_number, month, year, wealth_profile=wealth_profile)
        txs.extend(retraits_list)
        num_tx -= len(retraits_list)

    # Achats CB Pro & Quotidiens
    if num_tx > 0:
        pro_shopping = ["ADOBE SYSTEMS", "GOOGLE WORKSPACE", "OVH HOSTING", "FNAC", "TOTALENERGIES"]
        pro_resto = ["RESTAURANT D AFFAIRES [VILLE]", "BOULANGERIE [VILLE]", "UBER EATS"]
        txs.extend(get_dynamic_achats_cb(
            city, card_number, month, year, num_tx,
            custom_resto=pro_resto,
            custom_shopping=pro_shopping,
            wealth_profile=wealth_profile
        ))

    txs.sort(key=get_tx_date_sort_key)
    return txs[:orig_num_tx]

def parse_tx_amount(amt_str):
    if not amt_str: return 0.0
    s = str(amt_str).replace('EUR', '').replace('€', '').replace('¤', '').replace(' ', '').replace('+', '').replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return 0.0

def get_tx_delta(tx):
    if tx.get('credit'): return abs(parse_tx_amount(tx['credit']))
    if tx.get('debit'): return -abs(parse_tx_amount(tx['debit']))
    signe = tx.get('signe', '+')
    raw_val = tx.get('montant') if tx.get('montant') is not None else tx.get('amount')
    if raw_val is not None:
        val = abs(parse_tx_amount(raw_val))
        return -val if signe == '-' else val
    return 0.0

def set_tx_amount(tx, new_amount, new_signe=None):
    new_amount = round(abs(new_amount), 2)
    s = f"{new_amount:,.2f}".replace(',', ' ').replace('.', ',')
    tx['montant'] = s
    tx['amount'] = new_amount
    if new_signe:
        tx['signe'] = new_signe
    if 'credit' in tx:
        if tx.get('signe') == '+':
            tx['credit'] = s
            tx.pop('debit', None)
        else:
            tx['debit'] = s
            tx.pop('credit', None)
    elif 'debit' in tx:
        if tx.get('signe') == '-':
            tx['debit'] = s
            tx.pop('credit', None)
        else:
            tx['credit'] = s
            tx.pop('debit', None)

def get_debit_max_ceiling(t, wealth_profile="moyen"):
    l_str = str(t.get('lignes', '')).upper()
    t_type = t.get('type', '')
    if any(k in l_str for k in ['MCDONALD', 'BURGER KING', 'KFC', 'PIZZA HUT', 'SUSHI', 'UBER EATS', 'DELIVEROO', 'RESTO', 'BISTROT', 'BRASSERIE']):
        return _get_ceiling(wealth_profile, "fast_food")
    if 'PHARMACIE' in l_str:
        return _get_ceiling(wealth_profile, "pharmacie")
    if 'BOULANGERIE' in l_str or 'BL ' in l_str:
        return _get_ceiling(wealth_profile, "boulangerie")
    if 'TABAC' in l_str or 'PRESSE' in l_str:
        return _get_ceiling(wealth_profile, "tabac")
    if any(k in l_str for k in ['PATHE', 'UGC', 'CINEMA']):
        return _get_ceiling(wealth_profile, "cinema")
    if any(k in l_str for k in ['CARBURANT', 'TOTAL', 'ESSO', 'AVIA', 'BP', 'ENI']):
        return _get_ceiling(wealth_profile, "carburant")
    if any(k in l_str for k in ['SUPERMARCHE', 'LECLERC', 'CARREFOUR', 'AUCHAN', 'INTERMARCHE', 'LIDL', 'ALDI', 'GRAND FRAIS', 'MONOPRIX', 'PICARD']):
        return _get_ceiling(wealth_profile, "supermarche")
    if any(k in l_str for k in ['IKEA', 'LEROY MERLIN', 'FNAC', 'DARTY', 'DECATHLON', 'BRICOMAN', 'POINT.P', 'WURTH', 'BOULANGER']):
        return _get_ceiling(wealth_profile, "shopping_big")
    if any(k in l_str for k in ['ZALANDO', 'ASOS', 'AMAZON', 'VINTED', 'ZARA', 'H&M']):
        return _get_ceiling(wealth_profile, "shopping_online")
    if t_type == 'RETRAIT' or 'RETRAIT DAB' in l_str:
        if wealth_profile == "pauvre": return 50.0
        if wealth_profile == "riche": return 300.0
        return 120.0
    if t_type == 'ACHAT CB':
        return 80.0
    return 600.0

def calibrate_transactions_to_delta(txs, target_delta, city="PARIS", month="01", year="25", wealth_profile="moyen"):
    """
    Solver universel calibrant la somme d'une liste de transactions au centime près
    pour correspondre exactement à target_delta (Nouveau Solde - Ancien Solde).
    Préserve les flux miroirs, respecte les plafonds stricts par marchand (max 80€ fast-food/pharma)
    et injecte des transactions logiques crédibles si nécessaire.
    """
    if not txs: return txs
    target_delta = round(target_delta, 2)
    cur_sum_initial = round(sum(get_tx_delta(t) for t in txs), 2)
    if cur_sum_initial == target_delta:
        return txs
        
    _, year_4 = get_year_strings(year)
    mois_str = str(month).zfill(2)
    is_ep_txs = any(('EPARGNE' in str(t.get('lignes')) or 'LIVRET' in str(t.get('lignes')) or 'INTERETS' in str(t.get('lignes'))) for t in txs)
    pivot = None
    min_floor = 10.0 if is_ep_txs else 1.0
    
    def is_protected_credit(t):
        if t.get('is_protected'):
            return True
        l_str = str(t.get('lignes', '')).upper()
        return any(p in l_str for p in ['CPAM', 'MUTUEL', 'MUTUELLE', 'CAF', 'REMISE DE CHEQUE', 'ALLOCATION'])
        
    def is_primary_income(t):
        if is_protected_credit(t):
            return False
        l_str = str(t.get('lignes', '')).upper()
        return any(k in l_str for k in ['SALAIRE', 'PAYE', 'TRAITEMENT', 'BOURSE', 'PENSION', 'FRANCE TRAVAIL', 'POLE EMPLOI', 'CHANTIER', 'ACOMPTE', 'FACTURE', 'LOYER APPARTEMENT', 'HONORAIRES'])
    
    if target_delta >= 0:
        debits = [t for t in txs if get_tx_delta(t) < 0]
        credits = [t for t in txs if get_tx_delta(t) > 0]
        sum_debits = sum(abs(get_tx_delta(t)) for t in debits)
        required_credits = round(sum_debits + target_delta, 2)
        
        if not credits:
            c_tx = txs[0]
            if is_ep_txs:
                c_tx['lignes'] = ['VIREMENT EN VOTRE FAVEUR', f'DATE DE VALEUR : 15 {mois_str} {year_4}']
                c_tx['type'] = 'VIREMENT'
            else:
                c_tx['lignes'] = ['VIREMENT EN VOTRE FAVEUR', f'VIREMENT RECU DU 15/{mois_str}']
                c_tx['type'] = 'VIREMENT EN VOTRE FAVEUR'
            c_tx['signe'] = '+'
            credits = [c_tx]
            debits = txs[1:]
            sum_debits = sum(abs(get_tx_delta(t)) for t in debits)
            required_credits = round(sum_debits + target_delta, 2)
            
        non_mirror_credits = [t for t in credits if not t.get('is_mirror') and not is_protected_credit(t)]
        primary_incomes = [t for t in non_mirror_credits if is_primary_income(t)]
        flexible_credits = [t for t in non_mirror_credits if not is_protected_credit(t)]
        
        if primary_incomes:
            pivot = primary_incomes[0]
            orig_amt = pivot.get('amount', 2200.0)
            p_lignes = str(pivot.get('lignes', '')).upper()
            if 'BOURSE' in p_lignes or 'CROUS' in p_lignes:
                income_floor = 350.0
            elif 'FRANCE TRAVAIL' in p_lignes or 'POLE EMPLOI' in p_lignes:
                income_floor = 950.0
            elif 'FONCTION' in p_lignes or 'MINISTERE' in p_lignes or 'DGFIP' in p_lignes or 'SGC' in p_lignes:
                income_floor = 1800.0
            else:
                income_floor = 1420.0
        elif flexible_credits:
            pivot = flexible_credits[0]
            orig_amt = pivot.get('amount', 50.0)
            income_floor = min_floor
        elif non_mirror_credits:
            pivot = non_mirror_credits[0]
            orig_amt = pivot.get('amount', 50.0)
            income_floor = min_floor
        else:
            pivot = {
                "date": f"12/{mois_str}",
                "lignes": ["VIREMENT EN VOTRE FAVEUR", "DE M OU MME MARTIN"],
                "montant": "50,00",
                "signe": "+",
                "amount": 50.0,
                "type": "VIREMENT"
            }
            txs.append(pivot)
            credits.append(pivot)
            orig_amt = 50.0
            income_floor = min_floor
            
        other_credits = [t for t in credits if t is not pivot]
        sum_other = sum(get_tx_delta(t) for t in other_credits)
        target_pivot_amt = required_credits - sum_other
        
        if target_pivot_amt >= income_floor:
            set_tx_amount(pivot, target_pivot_amt, '+')
        else:
            final_pivot_amt = max(orig_amt, income_floor)
            set_tx_amount(pivot, final_pivot_amt, '+')
            extra_debit_needed = round((final_pivot_amt + sum_other) - (sum_debits + target_delta), 2)
            
            if extra_debit_needed > 0:
                used_days = set()
                for t in txs:
                    try:
                        used_days.add(int(str(t.get('date', '15/01')).split('/')[0]))
                    except Exception:
                        pass

                while extra_debit_needed > 0.01:
                    day_val = random.randint(3, 27)
                    day_str = f"{str(day_val).zfill(2)}/{mois_str}"
                    card_suffix = "790"
                    for t in txs:
                        l_all = " ".join(t.get('lignes', []))
                        m_card = re.search(r'CARTE (?:NUMERO|NO) (\d+)', l_all)
                        if m_card:
                            card_suffix = m_card.group(1)
                            break
                            
                    if extra_debit_needed >= 150.0:
                        chunk = round(min(extra_debit_needed, random.uniform(120.0, min(350.0, extra_debit_needed))), 2)
                        m_shop = random.choice(["FNAC", "DARTY", "IKEA", "LEROY MERLIN", "DECATHLON", "BOULANGER"])
                        tx_new = {
                            "date": day_str,
                            "lignes": [f"ACHAT CB {m_shop} {day_str.replace('/', '.')}.{year_4[-2:]}", f"CARTE NUMERO {card_suffix}"],
                            "montant": f"{chunk:,.2f}".replace(",", " ").replace(".", ","),
                            "signe": "-",
                            "amount": chunk,
                            "type": "ACHAT CB"
                        }
                    elif extra_debit_needed >= 40.0:
                        chunk = round(min(extra_debit_needed, random.uniform(40.0, extra_debit_needed)), 2)
                        m_sup = random.choice(["LECLERC", "CARREFOUR", "AUCHAN", "GRAND FRAIS", "INTERMARCHE"])
                        tx_new = {
                            "date": day_str,
                            "lignes": [f"ACHAT CB {m_sup} {day_str.replace('/', '.')}.{year_4[-2:]}", f"CARTE NUMERO {card_suffix}"],
                            "montant": f"{chunk:,.2f}".replace(",", " ").replace(".", ","),
                            "signe": "-",
                            "amount": chunk,
                            "type": "ACHAT CB"
                        }
                    else:
                        chunk = round(extra_debit_needed, 2)
                        m_shop_small = random.choice(["BOULANGERIE", "PHARMACIE", "TABAC PRESSE", "MONOPRIX", "RELAY"])
                        tx_new = {
                            "date": day_str,
                            "lignes": [f"ACHAT CB {m_shop_small} {day_str.replace('/', '.')}.{year_4[-2:]}", f"CARTE NUMERO {card_suffix}"],
                            "montant": f"{chunk:,.2f}".replace(",", " ").replace(".", ","),
                            "signe": "-",
                            "amount": chunk,
                            "type": "ACHAT CB"
                        }
                        
                    txs.append(tx_new)
                    extra_debit_needed = round(extra_debit_needed - chunk, 2)
            
    else:
        debits = [t for t in txs if get_tx_delta(t) < 0]
        credits = [t for t in txs if get_tx_delta(t) > 0]
        sum_credits = sum(get_tx_delta(t) for t in credits)
        required_debits = round(sum_credits + abs(target_delta), 2)
        
        if not debits:
            d_tx = txs[0]
            if is_ep_txs:
                d_tx['lignes'] = ['VIREMENT VERS COMPTE COURANT', f'DATE DE VALEUR : 15 {mois_str} {year_4}']
                d_tx['type'] = 'VIREMENT'
            else:
                d_tx['lignes'] = ['VIREMENT EMIS', f'VIREMENT EN DATE DU 15/{mois_str}']
                d_tx['type'] = 'VIREMENT EMIS'
            d_tx['signe'] = '-'
            debits = [d_tx]
            credits = txs[1:]
            sum_credits = sum(get_tx_delta(t) for t in credits)
            required_debits = round(sum_credits + abs(target_delta), 2)
            
        non_mirror_debits = [t for t in debits if not t.get('is_mirror')]
        
        def is_fixed_debit(t):
            if t.get('is_protected'):
                return True
            t_type = t.get('type', '')
            l_str = str(t.get('lignes', '')).upper()
            if t.get('is_frais') or t_type == 'FRAIS BANCAIRES':
                return True
            if t_type == 'RETRAIT' or 'RETRAIT DAB' in l_str or 'RETRAIT' in l_str:
                return True
            if t_type == 'PRELEVEMENT' or 'PRELEVEMENT' in l_str:
                return True
            if 'VIREMENT PERMANENT' in l_str or 'VERS LIVRET' in l_str or 'VERS PEL' in l_str:
                return True
            return False

        def get_debit_min_floor(t):
            t_type = t.get('type', '')
            l_str = str(t.get('lignes', '')).upper()
            if t_type == 'RETRAIT' or 'RETRAIT DAB' in l_str:
                return 20.0
            if t_type == 'PRELEVEMENT' or 'PRELEVEMENT' in l_str:
                return 15.0
            if any(k in l_str for k in ['CARBURANT', 'TOTAL', 'ESSO', 'AVIA', 'BP', 'ENI']):
                return 20.0
            if any(k in l_str for k in ['SUPERMARCHE', 'LECLERC', 'CARREFOUR', 'AUCHAN', 'INTERMARCHE', 'LIDL', 'ALDI', 'MONOPRIX']):
                return 15.0
            return 5.0

        cb_shopping = [t for t in non_mirror_debits if not t.get('is_protected') and t.get('type') == 'ACHAT CB' and any(k in str(t.get('lignes', '')).upper() for k in ['IKEA', 'LEROY MERLIN', 'FNAC', 'DARTY', 'AMAZON', 'ZARA', 'DECATHLON', 'ASOS', 'ZALANDO'])]
        cb_general = [t for t in non_mirror_debits if not t.get('is_protected') and t.get('type') == 'ACHAT CB']
        flexible_debits = [t for t in non_mirror_debits if not is_fixed_debit(t)]
        
        if cb_shopping:
            pivot = cb_shopping[0]
        elif cb_general:
            pivot = cb_general[0]
        elif flexible_debits:
            pivot = flexible_debits[0]
        else:
            card_suffix = "790"
            for t in txs:
                l_all = " ".join(t.get('lignes', []))
                m_card = re.search(r'CARTE (?:NUMERO|NO) (\d+)', l_all)
                if m_card:
                    card_suffix = m_card.group(1)
                    break
            pivot = {
                "date": f"16/{mois_str}",
                "lignes": [f"ACHAT CB CARREFOUR 16.{mois_str}.{year_4[-2:]}", f"CARTE NUMERO {card_suffix}"],
                "montant": "50,00",
                "signe": "-",
                "amount": 50.0,
                "type": "ACHAT CB"
            }
            txs.append(pivot)
            debits.append(pivot)
            
        other_debits = [t for t in debits if t is not pivot]
        sum_other = sum(abs(get_tx_delta(t)) for t in other_debits)
        pivot_floor = get_debit_min_floor(pivot)
        pivot_ceiling = get_debit_max_ceiling(pivot, wealth_profile=wealth_profile)
        
        target_p = required_debits - sum_other
        if target_p >= pivot_floor and target_p <= pivot_ceiling:
            set_tx_amount(pivot, target_p, '-')
        elif target_p > pivot_ceiling:
            set_tx_amount(pivot, pivot_ceiling, '-')
            remain = round(target_p - pivot_ceiling, 2)
            used_days_neg = set()
            for t in txs:
                try:
                    used_days_neg.add(int(str(t.get('date', '15/01')).split('/')[0]))
                except Exception:
                    pass
            card_suffix = "790"
            for t in txs:
                l_all = " ".join(t.get('lignes', []))
                m_card = re.search(r'CARTE (?:NUMERO|NO) (\d+)', l_all)
                if m_card:
                    card_suffix = m_card.group(1)
                    break
            while remain > 0.01:
                day_val = random.randint(3, 27)
                day_str = f"{str(day_val).zfill(2)}/{mois_str}"
                if remain >= 120.0:
                    chunk = round(min(remain, random.uniform(120.0, min(350.0, remain))), 2)
                    m_shop = random.choice(["FNAC", "DARTY", "IKEA", "LEROY MERLIN", "DECATHLON"])
                    tx_new = {
                        "date": day_str,
                        "lignes": [f"ACHAT CB {m_shop} {day_str.replace('/', '.')}.{year_4[-2:]}", f"CARTE NUMERO {card_suffix}"],
                        "montant": f"{chunk:,.2f}".replace(",", " ").replace(".", ","),
                        "signe": "-", "amount": chunk, "type": "ACHAT CB"
                    }
                elif remain >= 40.0:
                    chunk = round(min(remain, random.uniform(40.0, remain)), 2)
                    m_sup = random.choice(["LECLERC", "CARREFOUR", "AUCHAN", "GRAND FRAIS"])
                    tx_new = {
                        "date": day_str,
                        "lignes": [f"ACHAT CB {m_sup} {day_str.replace('/', '.')}.{year_4[-2:]}", f"CARTE NUMERO {card_suffix}"],
                        "montant": f"{chunk:,.2f}".replace(",", " ").replace(".", ","),
                        "signe": "-", "amount": chunk, "type": "ACHAT CB"
                    }
                else:
                    chunk = round(remain, 2)
                    m_shop_small = random.choice(["BOULANGERIE", "PHARMACIE", "TABAC PRESSE", "MONOPRIX", "RELAY"])
                    tx_new = {
                        "date": day_str,
                        "lignes": [f"ACHAT CB {m_shop_small} {day_str.replace('/', '.')}.{year_4[-2:]}", f"CARTE NUMERO {card_suffix}"],
                        "montant": f"{chunk:,.2f}".replace(",", " ").replace(".", ","),
                        "signe": "-", "amount": chunk, "type": "ACHAT CB"
                    }
                txs.append(tx_new)
                remain = round(remain - chunk, 2)
        elif target_p < pivot_floor:
            set_tx_amount(pivot, pivot_floor, '-')

    cur_sum = round(sum(get_tx_delta(t) for t in txs), 2)
    rem = round(target_delta - cur_sum, 2)
    if rem != 0.0:
        if rem > 0:
            flexible_credits = [t for t in txs if not t.get('is_mirror') and t.get('signe') == '+' and not is_protected_credit(t)]
            if flexible_credits:
                p = flexible_credits[0]
                cur = get_tx_delta(p)
                set_tx_amount(p, max(1.0, round(cur + rem, 2)), '+')
            else:
                flexible_debits = [t for t in txs if not t.get('is_mirror') and not t.get('is_protected') and not t.get('is_frais') and t.get('type') != 'RETRAIT' and 'RETRAIT' not in str(t.get('lignes', '')).upper() and t.get('signe') == '-']
                if flexible_debits:
                    d = flexible_debits[0]
                    cur = abs(get_tx_delta(d))
                    set_tx_amount(d, max(1.0, round(cur - rem, 2)), '-')
        else:
            flexible_debits = [t for t in txs if not t.get('is_mirror') and not t.get('is_protected') and not t.get('is_frais') and t.get('type') != 'RETRAIT' and 'RETRAIT' not in str(t.get('lignes', '')).upper() and t.get('signe') == '-']
            if flexible_debits:
                d = flexible_debits[0]
                cur = abs(get_tx_delta(d))
                set_tx_amount(d, max(1.0, round(cur + abs(rem), 2)), '-')
            else:
                non_mirrors = [t for t in txs if not t.get('is_mirror') and not t.get('is_protected') and t.get('type') != 'RETRAIT' and 'RETRAIT' not in str(t.get('lignes', '')).upper()]
                if non_mirrors:
                    p = non_mirrors[0]
                    cur = abs(get_tx_delta(p))
                    set_tx_amount(p, max(1.0, round(cur - abs(rem), 2)), p.get('signe'))

    for t in txs:
        l_str = str(t.get('lignes', '')).upper()
        if t.get('type') == 'RETRAIT' or 'RETRAIT' in l_str:
            cur_amt = abs(parse_tx_amount(t.get('montant', 0.0)))
            remainder = round(cur_amt % 10.0, 2)
            if remainder != 0.0:
                diff_round = round(10.0 - remainder if remainder >= 5.0 else -remainder, 2)
                new_dab_amt = max(20.0, round(cur_amt + diff_round, 2))
                diff_to_compensate = round(new_dab_amt - cur_amt, 2)
                set_tx_amount(t, new_dab_amt, '-')
                cbs = [c for c in txs if c.get('type') == 'ACHAT CB' and not c.get('is_protected')]
                if cbs:
                    cb_adj = cbs[0]
                    cur_cb = abs(parse_tx_amount(cb_adj.get('montant', 0.0)))
                    set_tx_amount(cb_adj, max(1.0, round(cur_cb - diff_to_compensate, 2)), '-')
            
    final_cur_sum = round(sum(get_tx_delta(t) for t in txs), 2)
    final_rem = round(target_delta - final_cur_sum, 2)
    if final_rem != 0.0:
        cbs = [c for c in txs if c.get('type') == 'ACHAT CB' and not c.get('is_protected')]
        if cbs:
            cb_adj = cbs[0]
            cur_cb = abs(parse_tx_amount(cb_adj.get('montant', 0.0)))
            set_tx_amount(cb_adj, max(1.0, round(cur_cb - final_rem, 2)), '-')
        else:
            flex_creds = [t for t in txs if not t.get('is_mirror') and not is_protected_credit(t) and t.get('signe') == '+']
            if flex_creds:
                p = flex_creds[0]
                cur = get_tx_delta(p)
                set_tx_amount(p, max(1.0, round(cur + final_rem, 2)), '+')
            
    txs.sort(key=get_tx_date_sort_key)
    return txs

def compute_total_operations(txs):
    """
    Calcule la somme exacte des débits et crédits d'une liste de transactions.
    """
    tot_debit = 0.0
    tot_credit = 0.0
    for t in txs:
        d = get_tx_delta(t)
        if d < 0:
            tot_debit += abs(d)
        else:
            tot_credit += d
    return {
        'total_debit': f"{tot_debit:,.2f}".replace(',', ' ').replace('.', ',') if tot_debit > 0 else "",
        'total_credit': f"{tot_credit:,.2f}".replace(',', ' ').replace('.', ',') if tot_credit > 0 else "",
        'total_debit_num': round(tot_debit, 2),
        'total_credit_num': round(tot_credit, 2)
    }

def update_tx_date(tx, new_day, month_str, year_str="25"):
    new_day_str = f"{new_day:02d}"
    mois_str = str(month_str).zfill(2)
    tx['date'] = f"{new_day_str}/{mois_str}"
    
    if 'lignes' in tx and tx['lignes']:
        new_lignes = []
        for l in tx['lignes']:
            l_up = re.sub(r'DATE DE VALEUR : \d{2} (\d{2} \d{4})', f'DATE DE VALEUR : {new_day_str} \\1', l)
            l_up = re.sub(r'(CARTE X\d{3} )\d{2}/\d{2}/\d{2}', f'\\g<1>{new_day_str}/{mois_str}/{year_str}', l_up)
            l_up = re.sub(r'(CARTE NO \d{3} )\d{2}/\d{2}/\d{2}', f'\\g<1>{new_day_str}/{mois_str}/{year_str}', l_up)
            l_up = re.sub(r'(ACHAT CB .+ )\d{2}\.\d{2}\.\d{2}', f'\\g<1>{new_day_str}.{mois_str}.{year_str}', l_up)
            new_lignes.append(l_up)
        tx['lignes'] = new_lignes

def ensure_positive_running_balance(txs, solde_ancien, month="01", year="25"):
    """
    Vérifie et garantit que le solde glissant S(t) = S0 + sum(Delta_i) ne plonge
    jamais sous 0,00 € au cours du mois lorsque le compte est créditeur.
    Réordonne intelligemment les dates des transactions si nécessaire.
    """
    if not txs or solde_ancien is None:
        return txs
    try:
        s0 = float(str(solde_ancien).replace('€', '').replace('¤', '').replace('+', '').replace(' ', '').replace(',', '.'))
    except Exception:
        return txs
    
    if s0 < 0:
        return txs
        
    mois_str = str(month).zfill(2)
    year_str = str(year)[-2:] if len(str(year)) >= 2 else str(year)
    
    def parse_day(t):
        try:
            return int(str(t.get('date', '15/01')).split('/')[0])
        except Exception:
            return 15
            
    txs.sort(key=get_tx_date_sort_key)
    
    running = s0
    dip = False
    for t in txs:
        running += get_tx_delta(t)
        if running < 0:
            dip = True
            break
            
    if not dip:
        return txs
        
    credits = [t for t in txs if get_tx_delta(t) > 0]
    if not credits:
        return txs
        
    main_credit = max(credits, key=lambda c: get_tx_delta(c))
    main_day = parse_day(main_credit)
    
    secondary_credits = [c for c in credits if c is not main_credit and not c.get('is_mirror')]
    for idx, sc in enumerate(secondary_credits):
        target_day = min(5, 2 + idx)
        update_tx_date(sc, target_day, mois_str, year_str)
        
    curr_balance = s0
    sorted_txs = sorted(txs, key=get_tx_date_sort_key)
    max_days = get_days_in_month(month, year)
    post_salary_day = min(max_days - 1, max(main_day, max_days - 3) + 1)
    
    for t in sorted_txs:
        d = get_tx_delta(t)
        t_day = parse_day(t)
        if d > 0:
            curr_balance += d
        else:
            if t_day < main_day and curr_balance + d < 0:
                update_tx_date(t, min(post_salary_day, max_days), mois_str, year_str)
                post_salary_day = min(max_days, post_salary_day + 1)
            else:
                curr_balance += d
                
    txs.sort(key=get_tx_date_sort_key)
    return txs

# ==========================================
# 4. ROUTEUR PRINCIPAL (API D'ENTRÉE)
# ==========================================

def generate_random_txs(num_tx, city, month, year, is_epargne=False, profile="normal", wealth_profile="moyen", age_profile="adulte", titulaire_nom="DUPONT JEAN", card_number="790", cp="75000", titulaire_sexe="M", dest_iban=None, target_delta=None, account_type="CCP", mirror_txs=None, solde_ancien=None, custom_taux=None, bank_type="lbp", allow_epargne=False, contacts_emis=None, contacts_recu=None):
    global CURRENT_BANK_TYPE, CURRENT_ALLOW_EPARGNE, CURRENT_CONTACTS_EMIS, CURRENT_CONTACTS_RECU
    CURRENT_BANK_TYPE = bank_type
    CURRENT_ALLOW_EPARGNE = allow_epargne
    CURRENT_CONTACTS_EMIS = contacts_emis or []
    CURRENT_CONTACTS_RECU = contacts_recu or []
    
    if num_tx is not None and int(num_tx) <= 0:
        return []
        
    month_int = int(month)
    prof_clean = str(profile).lower().strip()
    
    if is_epargne:
        txs = generate_profile_epargne(num_tx, month_int, year, wealth_profile=wealth_profile, titulaire_nom=titulaire_nom, account_type=account_type, mirror_txs=mirror_txs, solde_ancien=solde_ancien, custom_taux=custom_taux)
    elif prof_clean in ["etudiant", "student", "jeune"]:
        txs = generate_profile_etudiant(num_tx, city, month_int, year, card_number=card_number, wealth_profile=wealth_profile, age_profile="jeune", titulaire_nom=titulaire_nom, cp=cp, titulaire_sexe=titulaire_sexe, dest_iban=dest_iban)
    elif prof_clean in ["retraite", "senior", "pensionnaire"]:
        txs = generate_profile_retraite(num_tx, city, month_int, year, card_number=card_number, wealth_profile=wealth_profile, age_profile="senior", titulaire_nom=titulaire_nom, cp=cp, titulaire_sexe=titulaire_sexe, dest_iban=dest_iban)
    elif prof_clean in ["independant", "freelance", "auto_entrepreneur", "autoentrepreneur", "pro"]:
        txs = generate_profile_independant(num_tx, city, month_int, year, card_number=card_number, wealth_profile=wealth_profile, age_profile=age_profile, titulaire_nom=titulaire_nom, cp=cp, titulaire_sexe=titulaire_sexe, dest_iban=dest_iban)
    elif prof_clean in ["chomage", "chomeur", "france_travail", "francetravail", "pole_emploi", "poleemploi", "are"]:
        txs = generate_profile_chomage(num_tx, city, month_int, year, card_number=card_number, wealth_profile=wealth_profile, age_profile=age_profile, titulaire_nom=titulaire_nom, cp=cp, titulaire_sexe=titulaire_sexe, dest_iban=dest_iban)
    elif prof_clean in ["artisan", "btp", "batiment", "travaux", "chantier", "macon", "plombier", "electricien"]:
        txs = generate_profile_artisan(num_tx, city, month_int, year, card_number=card_number, wealth_profile=wealth_profile, age_profile=age_profile, titulaire_nom=titulaire_nom, cp=cp, titulaire_sexe=titulaire_sexe, dest_iban=dest_iban)
    elif prof_clean in ["famille", "family", "enfants", "parent"]:
        txs = generate_profile_famille(num_tx, city, month_int, year, card_number=card_number, wealth_profile=wealth_profile, age_profile=age_profile, titulaire_nom=titulaire_nom, cp=cp, titulaire_sexe=titulaire_sexe, dest_iban=dest_iban)
    elif prof_clean in ["investisseur", "patrimoine", "patrimonial", "bailleur", "proprietaire"]:
        txs = generate_profile_investisseur(num_tx, city, month_int, year, card_number=card_number, wealth_profile=wealth_profile, age_profile=age_profile, titulaire_nom=titulaire_nom, cp=cp, titulaire_sexe=titulaire_sexe, dest_iban=dest_iban)
    elif prof_clean in ["fonctionnaire", "agent_public", "service_public", "dgfip", "mgen", "professeur", "instituteur"]:
        txs = generate_profile_fonctionnaire(num_tx, city, month_int, year, card_number=card_number, wealth_profile=wealth_profile, age_profile=age_profile, titulaire_nom=titulaire_nom, cp=cp, titulaire_sexe=titulaire_sexe, dest_iban=dest_iban)
    elif prof_clean in ["demandeur_credit", "credit", "emprunteur", "pret", "dossier_credit", "credit_conso", "pret_immo"]:
        txs = generate_profile_demandeur_credit(num_tx, city, month_int, year, card_number=card_number, wealth_profile=wealth_profile, age_profile=age_profile, titulaire_nom=titulaire_nom, cp=cp, titulaire_sexe=titulaire_sexe, dest_iban=dest_iban)
    elif prof_clean == "locataire":
        txs = generate_profile_locataire(num_tx, city, month_int, year, card_number=card_number, wealth_profile=wealth_profile, age_profile=age_profile, titulaire_nom=titulaire_nom, cp=cp, titulaire_sexe=titulaire_sexe, dest_iban=dest_iban)
    else:
        txs = generate_profile_normal(num_tx, city, month_int, year, card_number=card_number, wealth_profile=wealth_profile, age_profile=age_profile, titulaire_nom=titulaire_nom, cp=cp, titulaire_sexe=titulaire_sexe, dest_iban=dest_iban)

    if target_delta is not None and txs:
        txs = calibrate_transactions_to_delta(txs, target_delta, city=city, month=str(month), year=str(year), wealth_profile=wealth_profile)

    return txs
