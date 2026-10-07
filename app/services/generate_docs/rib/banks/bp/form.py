from . import copy

def get_form_schema() -> dict:
    return {
        "metadata": {
            "title": "GÉNÉRATEUR RIB BANQUE POPULAIRE",
            "logo": "bp",
            "apiBase": "/api/generate-docs/rib/bp",
            "headerBg": "bg-gradient-to-br from-cyan-950/40 to-slate-950/80 border-cyan-500/30",
            "priceKey": "bp",
            "subtitle": "Document PDF Banque Populaire officiel",
            "filenameTemplate": f"RIB_BP_{copy.NOM}.pdf"
        },
        "defaults": {
            "civilite": copy.CIVILITE,
            "nom": copy.NOM,
            "prenom": copy.PRENOM,
            "adresse": copy.ADRESSE,
            "cp": copy.CP,
            "ville": copy.VILLE,
            "domiciliation": copy.DOMICILIATION,
            "code_banque": copy.BANQUE,
            "guichet": copy.GUICHET,
            "compte": copy.COMPTE,
            "cle": copy.CLE,
            "iban": copy.IBAN,
            "bic": copy.BIC,
            "header": "true",
            "header_logo": "true",
            "header_title": "true",
            "middle": "true",
            "middle_domiciliation": "true",
            "middle_table": "true",
            "middle_iban": "true",
            "middle_bic": "true",
            "middle_titulaire": "true",
            "middle_adresse": "true",
            "middle_notice": "true",
            "middle_separator": "true",
            "footer": "true",
            "footer_page": "true",
            "footer_rib": "true",
            "header_title_text": copy.TITLE,
            "middle_notice_text": copy.NOTICE,
            "footer_page_text": copy.FOOTER_PAGE,
            "footer_rib_text": copy.FOOTER_RIB
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
                    },
                    {
                        "key": "domiciliation",
                        "label": "Domiciliation",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "EX: AG ECO SOCIALE SOLIDAIRE",
                        "rules": {"required": True, "min": 2, "max": 60, "transform": "uppercase"}
                    }
                ]
            },
            {
                "id": "coordonnees_bancaires",
                "title": "Coordonnées Bancaires",
                "order": 2,
                "fields": [
                    {
                        "key": "code_banque",
                        "label": "Code Banque",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "banque",
                        "placeholder": "18707",
                        "rules": {"required": True, "min": 5, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "guichet",
                        "label": "Code Guichet",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "guichet",
                        "placeholder": "00656",
                        "rules": {"required": True, "min": 5, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "compte",
                        "label": "N° de Compte",
                        "kind": "alnum",
                        "span": 1,
                        "autoIban": "compte",
                        "placeholder": "00012345678",
                        "rules": {"required": True, "min": 11, "max": 11, "transform": "uppercase"}
                    },
                    {
                        "key": "cle",
                        "label": "Clé RIB",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "cle",
                        "placeholder": "30",
                        "rules": {"required": True, "min": 2, "max": 2, "transform": "digits_only"}
                    },
                    {
                        "key": "iban",
                        "label": "IBAN",
                        "kind": "iban",
                        "span": 2,
                        "placeholder": "FR76 1870 7006 5600 0123 4567 830",
                        "rules": {"required": True, "min": 27, "max": 34, "transform": "uppercase"}
                    },
                    {
                        "key": "bic",
                        "label": "BIC / SWIFT",
                        "kind": "bic",
                        "span": 2,
                        "placeholder": "CCBPFRPPVER",
                        "rules": {"required": True, "min": 8, "max": 11, "transform": "uppercase"}
                    }
                ]
            },
            {
                "id": "header_section",
                "title": "En-tête",
                "order": 3,
                "hasAdvancedMode": True,
                "fields": [
                    {
                        "key": "header_title_text",
                        "label": "Titre de l'en-tête",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "RELEVE D'IDENTITE BANCAIRE",
                        "rules": {"max": 40}
                    }
                ]
            },
            {
                "id": "middle_section",
                "title": "Corps",
                "order": 4,
                "hasAdvancedMode": True,
                "fields": [
                    {
                        "key": "middle_notice_text",
                        "label": "Notice explicative",
                        "kind": "textarea",
                        "span": 2,
                        "placeholder": "Ce relevé d'identité bancaire est à utiliser...",
                        "rules": {"max": 400}
                    }
                ]
            },
            {
                "id": "footer_section",
                "title": "Pied de page",
                "order": 5,
                "hasAdvancedMode": True,
                "fields": [
                    {
                        "key": "footer_page_text",
                        "label": "Numéro de page",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "1 / 1",
                        "rules": {"max": 10}
                    },
                    {
                        "key": "footer_rib_text",
                        "label": "Code document",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "RIBS0000",
                        "rules": {"max": 20}
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
                {"id": "middle", "label": "Corps du document", "master": True, "section": "middle"},
                {"id": "middle_domiciliation", "label": "Bloc domiciliation", "master": False, "section": "middle"},
                {"id": "middle_table", "label": "Tableau RIB", "master": False, "section": "middle"},
                {"id": "middle_iban", "label": "IBAN", "master": False, "section": "middle"},
                {"id": "middle_bic", "label": "BIC", "master": False, "section": "middle"},
                {"id": "middle_titulaire", "label": "Bloc titulaire", "master": False, "section": "middle"},
                {"id": "middle_adresse", "label": "Bloc adresse", "master": False, "section": "middle"},
                {"id": "middle_notice", "label": "Notice", "master": False, "section": "middle"},
                {"id": "middle_separator", "label": "Séparateur", "master": False, "section": "middle"},
                {"id": "footer", "label": "Pied de page", "master": True, "section": "footer"},
                {"id": "footer_page", "label": "Numéro de page", "master": False, "section": "footer"},
                {"id": "footer_rib", "label": "Code RIB", "master": False, "section": "footer"}
            ],
            "visible": {
                "header": True,
                "header_logo": True,
                "header_title": True,
                "middle": True,
                "middle_domiciliation": True,
                "middle_table": True,
                "middle_iban": True,
                "middle_bic": True,
                "middle_titulaire": True,
                "middle_adresse": True,
                "middle_notice": True,
                "middle_separator": True,
                "footer": True,
                "footer_page": True,
                "footer_rib": True
            }
        }
    }
