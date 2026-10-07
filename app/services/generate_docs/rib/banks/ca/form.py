from . import copy

def get_form_schema() -> dict:
    return {
        "metadata": {
            "title": "GÉNÉRATEUR RIB CRÉDIT AGRICOLE",
            "logo": "ca",
            "apiBase": "/api/generate-docs/rib/ca",
            "headerBg": "bg-gradient-to-br from-emerald-900/40 to-slate-950/80 border-emerald-500/30",
            "priceKey": "ca",
            "subtitle": "Document PDF Crédit Agricole officiel",
            "filenameTemplate": f"RIB_CA_{copy.NOM}.pdf"
        },
        "defaults": {
            "civilite": copy.CIVILITE,
            "nom": copy.NOM,
            "prenom": copy.PRENOM,
            "adresse": copy.ADRESSE,
            "cp": copy.CP,
            "ville": copy.VILLE,
            "caisse_nom": copy.CAISSE,
            "caisse_agence": copy.AGENCE,
            "code_agence": copy.CODE,
            "caisse_tel": copy.TEL,
            "caisse_fax": copy.FAX,
            "date_edition": copy.DATE,
            "code_banque": copy.BANQUE,
            "guichet": copy.GUICHET,
            "compte": copy.COMPTE,
            "cle": copy.CLE,
            "iban": copy.IBAN,
            "bic": copy.BIC,
            "header": "true",
            "header_logo": "true",
            "header_title": "true",
            "header_crumb": "true",
            "middle": "true",
            "middle_notice": "true",
            "middle_lines": "true",
            "middle_agence": "true",
            "middle_titulaire": "true",
            "middle_domiciliation": "true",
            "middle_table": "true",
            "middle_iban": "true",
            "middle_bic": "true",
            "footer": "true",
            "header_title_text": copy.TITLE,
            "header_crumb_text": copy.CRUMB,
            "header_crumb_link": copy.CRUMB_LINK,
            "middle_notice_text": copy.NOTICE,
            "middle_titulaire_opt": copy.TITULAIRE_OPT,
            "middle_domiciliation_text": copy.DOMICILIATION
        },
        "sections": [
            {
                "id": "titulaire",
                "title": "Titulaire du compte",
                "order": 1,
                "fields": [
                    {
                        "key": "civilite",
                        "label": "Civilité",
                        "kind": "select",
                        "span": 1,
                        "options": [
                            {"label": "Monsieur (M.)", "value": "M."},
                            {"label": "Madame (MME)", "value": "MME"},
                            {"label": "Mademoiselle (MLLE)", "value": "MLLE"}
                        ],
                        "rules": {"required": True}
                    },
                    {
                        "key": "nom",
                        "label": "Nom",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "EX: MARTIN",
                        "rules": {"required": True, "min": 2, "max": 35, "transform": "uppercase"}
                    },
                    {
                        "key": "prenom",
                        "label": "Prénom",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "EX: LUCAS",
                        "rules": {"required": True, "min": 2, "max": 35, "transform": "uppercase"}
                    },
                    {
                        "key": "adresse",
                        "label": "Adresse",
                        "kind": "address",
                        "span": 2,
                        "placeholder": "EX: 12 RUE DES FLEURS",
                        "rules": {"required": True, "min": 5, "max": 60, "transform": "uppercase"}
                    },
                    {
                        "key": "cp",
                        "label": "Code postal",
                        "kind": "cp",
                        "span": 1,
                        "placeholder": "EX: 75011",
                        "rules": {"required": True, "min": 5, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "ville",
                        "label": "Ville",
                        "kind": "ville",
                        "span": 1,
                        "placeholder": "EX: PARIS",
                        "rules": {"required": True, "min": 2, "max": 45, "transform": "uppercase"}
                    }
                ]
            },
            {
                "id": "caisse_agence",
                "title": "Caisse & Agence",
                "order": 2,
                "fields": [
                    {
                        "key": "caisse_nom",
                        "label": "Caisse régionale",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "EX: CR TOULOUSE 31",
                        "rules": {"required": True, "min": 2, "max": 40, "transform": "uppercase"}
                    },
                    {
                        "key": "caisse_agence",
                        "label": "Agence",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "EX: TOULOUSE CAPITOLE",
                        "rules": {"required": True, "min": 2, "max": 40, "transform": "uppercase"}
                    },
                    {
                        "key": "code_agence",
                        "label": "Code agence",
                        "kind": "digits",
                        "span": 1,
                        "placeholder": "00350",
                        "rules": {"required": True, "min": 1, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "caisse_tel",
                        "label": "Téléphone",
                        "kind": "digits",
                        "span": 1,
                        "placeholder": "0562107433",
                        "rules": {"required": False, "min": 10, "max": 20, "transform": "digits_only"}
                    },
                    {
                        "key": "caisse_fax",
                        "label": "Fax",
                        "kind": "digits",
                        "span": 1,
                        "placeholder": "0810031204",
                        "rules": {"required": False, "min": 10, "max": 20, "transform": "digits_only"}
                    },
                    {
                        "key": "date_edition",
                        "label": "Date d'édition",
                        "kind": "date",
                        "span": 2,
                        "placeholder": "JJ/MM/AAAA",
                        "rules": {"required": False, "max": 10}
                    }
                ]
            },
            {
                "id": "coordonnees_bancaires",
                "title": "Coordonnées Bancaires",
                "order": 3,
                "fields": [
                    {
                        "key": "code_banque",
                        "label": "Code Banque",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "banque",
                        "placeholder": "13106",
                        "rules": {"required": True, "min": 5, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "guichet",
                        "label": "Code Guichet",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "guichet",
                        "placeholder": "00500",
                        "rules": {"required": True, "min": 5, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "compte",
                        "label": "N° de Compte",
                        "kind": "alnum",
                        "span": 1,
                        "autoIban": "compte",
                        "placeholder": "30021598310",
                        "rules": {"required": True, "min": 11, "max": 11, "transform": "uppercase"}
                    },
                    {
                        "key": "cle",
                        "label": "Clé RIB",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "cle",
                        "placeholder": "07",
                        "rules": {"required": True, "min": 2, "max": 2, "transform": "digits_only"}
                    },
                    {
                        "key": "iban",
                        "label": "IBAN",
                        "kind": "iban",
                        "span": 2,
                        "placeholder": "FR76 1310 6005 0030 0215 9831 007",
                        "rules": {"required": True, "min": 27, "max": 34, "transform": "uppercase"}
                    },
                    {
                        "key": "bic",
                        "label": "BIC / SWIFT",
                        "kind": "bic",
                        "span": 2,
                        "placeholder": "AGRIFRPP831",
                        "rules": {"required": True, "min": 8, "max": 11, "transform": "uppercase"}
                    }
                ]
            },
            {
                "id": "header_section",
                "title": "En-tête",
                "order": 4,
                "hasAdvancedMode": True,
                "fields": [
                    {
                        "key": "header_title_text",
                        "label": "Titre de l'en-tête",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "RELEVÉ D'IDENTITÉ BANCAIRE",
                        "rules": {"max": 40, "transform": "uppercase"}
                    },
                    {
                        "key": "header_crumb_text",
                        "label": "Fil d'Ariane (texte)",
                        "kind": "textarea",
                        "span": 2,
                        "placeholder": "Accueil (/ca-toulouse31/association/operations/synthese.html)",
                        "rules": {"max": 90}
                    },
                    {
                        "key": "header_crumb_link",
                        "label": "Lien du fil d'Ariane",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "Editez un RIB",
                        "rules": {"max": 24}
                    }
                ]
            },
            {
                "id": "middle_section",
                "title": "Corps",
                "order": 5,
                "hasAdvancedMode": True,
                "fields": [
                    {
                        "key": "middle_notice_text",
                        "label": "Notice explicative",
                        "kind": "textarea",
                        "span": 2,
                        "placeholder": "Ce relevé est destiné à tout organisme...",
                        "rules": {"max": 400}
                    },
                    {
                        "key": "middle_titulaire_opt",
                        "label": "Complément titulaire",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "Optionnel...",
                        "rules": {"max": 62, "transform": "uppercase"}
                    },
                    {
                        "key": "middle_domiciliation_text",
                        "label": "Domiciliation",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "Optionnel...",
                        "rules": {"max": 40, "transform": "uppercase"}
                    }
                ]
            }
        ],
        "customLayout": {
            "sections": [
                {"id": "header", "label": "En-tête"},
                {"id": "middle", "label": "Corps du document"},
                {"id": "footer", "label": "Pied de page"}
            ],
            "blocks": [
                {"id": "header", "label": "En-tête", "master": True, "section": "header"},
                {"id": "header_logo", "label": "Logo", "master": False, "section": "header"},
                {"id": "header_title", "label": "Titre", "master": False, "section": "header"},
                {"id": "header_crumb", "label": "Fil d'Ariane", "master": False, "section": "header"},
                {"id": "middle", "label": "Corps du document", "master": True, "section": "middle"},
                {"id": "middle_notice", "label": "Notice", "master": False, "section": "middle"},
                {"id": "middle_lines", "label": "Filets / lignes", "master": False, "section": "middle"},
                {"id": "middle_agence", "label": "Bloc agence", "master": False, "section": "middle"},
                {"id": "middle_titulaire", "label": "Bloc titulaire", "master": False, "section": "middle"},
                {"id": "middle_domiciliation", "label": "Bloc domiciliation", "master": False, "section": "middle"},
                {"id": "middle_table", "label": "Tableau RIB", "master": False, "section": "middle"},
                {"id": "middle_iban", "label": "IBAN", "master": False, "section": "middle"},
                {"id": "middle_bic", "label": "BIC", "master": False, "section": "middle"},
                {"id": "footer", "label": "Pied de page", "master": True, "section": "footer"}
            ],
            "visible": {
                "header": True,
                "header_logo": True,
                "header_title": True,
                "header_crumb": True,
                "middle": True,
                "middle_notice": True,
                "middle_lines": True,
                "middle_agence": True,
                "middle_titulaire": True,
                "middle_domiciliation": True,
                "middle_table": True,
                "middle_iban": True,
                "middle_bic": True,
                "footer": True
            }
        }
    }
