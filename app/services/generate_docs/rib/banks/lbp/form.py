from . import copy

def get_form_schema() -> dict:
    return {
        "metadata": {
            "title": "GÉNÉRATEUR RIB LA BANQUE POSTALE",
            "logo": "lbp",
            "apiBase": "/api/generate-docs/rib/lbp",
            "headerBg": "bg-gradient-to-br from-blue-900/60 to-slate-950 border-blue-500/30",
            "logoClass": "scale-110",
            "priceKey": "lbp",
            "subtitle": "RIB La Banque Postale certifié",
            "filenameTemplate": f"RIB_LBP_{copy.NOM}.pdf"
        },
        "defaults": {
            "civilite": copy.CIVILITE,
            "nom": copy.NOM,
            "prenom": copy.PRENOM,
            "adresse": copy.TITULAIRE_RUE,
            "cp": copy.CP,
            "ville": copy.VILLE,
            "domiciliation": copy.DOMICILIATION,
            "code_banque": copy.ETABLISSEMENT,
            "code_guichet": copy.GUICHET,
            "num_compte": copy.COMPTE,
            "cle_rib": copy.CLE,
            "iban": copy.IBAN,
            "bic": copy.BIC,
            "header": "true",
            "header_title": "true",
            "header_notice_fr": "true",
            "header_notice_en": "true",
            "middle": "true",
            "middle_logo": "true",
            "middle_title": "true",
            "middle_table": "true",
            "middle_iban_bic": "true",
            "middle_titulaire": "true",
            "middle_separator": "true",
            "footer": "true",
            "footer_mentions": "true",
            "header_title_text": copy.TITLE,
            "header_notice_fr_text": copy.NOTICE_FR,
            "header_notice_en_text": copy.NOTICE_EN,
            "middle_title_text": copy.TABLE_TITLE,
            "middle_titulaire_opt1": copy.TITULAIRE_OPT1,
            "middle_titulaire_opt2": copy.TITULAIRE_OPT2,
            "footer_line1_text": copy.FOOTER_L1,
            "footer_line2_text": copy.FOOTER_L2,
            "footer_code_text": copy.FOOTER_CODE
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
                            {"label": "M.", "value": "MR"},
                            {"label": "Mme", "value": "MME"},
                            {"label": "Mlle", "value": "MLLE"}
                        ],
                        "rules": {"required": True}
                    },
                    {
                        "key": "nom",
                        "label": "Nom",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "ex: MARTIN",
                        "rules": {"required": True, "min": 2, "max": 35, "transform": "uppercase"}
                    },
                    {
                        "key": "prenom",
                        "label": "Prénom",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "ex: LUCAS",
                        "rules": {"required": True, "min": 2, "max": 35, "transform": "uppercase"}
                    },
                    {
                        "key": "adresse",
                        "label": "Adresse",
                        "kind": "address",
                        "span": 2,
                        "placeholder": "ex: 12 RUE DES FLEURS",
                        "rules": {"required": True, "min": 5, "max": 60}
                    },
                    {
                        "key": "cp",
                        "label": "Code postal",
                        "kind": "cp",
                        "span": 1,
                        "placeholder": "75011",
                        "rules": {"required": True, "min": 5, "max": 5}
                    },
                    {
                        "key": "ville",
                        "label": "Ville",
                        "kind": "ville",
                        "span": 1,
                        "placeholder": "PARIS",
                        "rules": {"required": True, "min": 2, "max": 45}
                    },
                    {
                        "key": "domiciliation",
                        "label": "Domiciliation",
                        "kind": "text",
                        "span": 2,
                        "placeholder": "ex: LA BANQUE POSTALE PARIS IDF CENTRE FINANCIER",
                        "rules": {"required": True, "min": 2, "max": 60}
                    }
                ]
            },
            {
                "id": "banque",
                "title": "Coordonnées Bancaires",
                "order": 2,
                "fields": [
                    {
                        "key": "code_banque",
                        "label": "Code Banque",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "banque",
                        "rules": {"required": True, "min": 5, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "code_guichet",
                        "label": "Code Guichet",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "guichet",
                        "rules": {"required": True, "min": 5, "max": 5, "transform": "digits_only"}
                    },
                    {
                        "key": "num_compte",
                        "label": "N° de Compte",
                        "kind": "alnum",
                        "span": 1,
                        "autoIban": "compte",
                        "rules": {"required": True, "min": 11, "max": 11, "transform": "uppercase"}
                    },
                    {
                        "key": "cle_rib",
                        "label": "Clé RIB",
                        "kind": "digits",
                        "span": 1,
                        "autoIban": "cle",
                        "rules": {"required": True, "min": 2, "max": 2, "transform": "digits_only"}
                    },
                    {
                        "key": "iban",
                        "label": "IBAN",
                        "kind": "iban",
                        "span": 2,
                        "rules": {"required": True, "min": 15, "max": 34, "transform": "uppercase"}
                    },
                    {
                        "key": "bic",
                        "label": "BIC / SWIFT",
                        "kind": "bic",
                        "span": 2,
                        "rules": {"required": True, "min": 8, "max": 11, "transform": "uppercase"}
                    }
                ]
            },
            {
                "id": "header",
                "title": "En-tête",
                "order": 3,
                "hasAdvancedMode": True,
                "fields": [
                    {
                        "key": "header_title_text",
                        "label": "Titre de l'en-tête",
                        "kind": "text",
                        "span": 1,
                        "rules": {"max": 40}
                    },
                    {
                        "key": "header_notice_fr_text",
                        "label": "Notice de confidentialité (FR)",
                        "kind": "textarea",
                        "span": 2,
                        "rules": {"max": 800}
                    },
                    {
                        "key": "header_notice_en_text",
                        "label": "Notice de confidentialité (EN)",
                        "kind": "textarea",
                        "span": 2,
                        "rules": {"max": 500}
                    }
                ]
            },
            {
                "id": "middle",
                "title": "Corps",
                "order": 4,
                "hasAdvancedMode": True,
                "fields": [
                    {
                        "key": "middle_title_text",
                        "label": "Titre du corps",
                        "kind": "text",
                        "span": 1,
                        "rules": {"max": 40}
                    },
                    {
                        "key": "middle_titulaire_opt1",
                        "label": "Complément d'adresse 1",
                        "kind": "text",
                        "span": 1,
                        "rules": {"max": 60}
                    },
                    {
                        "key": "middle_titulaire_opt2",
                        "label": "Complément d'adresse 2",
                        "kind": "text",
                        "span": 1,
                        "rules": {"max": 60}
                    }
                ]
            },
            {
                "id": "footer",
                "title": "Pied de page",
                "order": 5,
                "hasAdvancedMode": True,
                "fields": [
                    {
                        "key": "footer_line1_text",
                        "label": "Mentions légales (ligne 1)",
                        "kind": "textarea",
                        "span": 2,
                        "rules": {"max": 220}
                    },
                    {
                        "key": "footer_line2_text",
                        "label": "Mentions légales (ligne 2)",
                        "kind": "textarea",
                        "span": 2,
                        "rules": {"max": 220}
                    },
                    {
                        "key": "footer_code_text",
                        "label": "Code document",
                        "kind": "text",
                        "span": 1,
                        "rules": {"max": 16}
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
                {"id": "header_title", "label": "Titre", "master": False, "section": "header"},
                {"id": "header_notice_fr", "label": "Notice FR", "master": False, "section": "header"},
                {"id": "header_notice_en", "label": "Notice EN", "master": False, "section": "header"},
                {"id": "middle", "label": "Corps du document", "master": True, "section": "middle"},
                {"id": "middle_logo", "label": "Logo", "master": False, "section": "middle"},
                {"id": "middle_title", "label": "Titre", "master": False, "section": "middle"},
                {"id": "middle_table", "label": "Tableau RIB", "master": False, "section": "middle"},
                {"id": "middle_iban_bic", "label": "IBAN & BIC", "master": False, "section": "middle"},
                {"id": "middle_titulaire", "label": "Bloc titulaire", "master": False, "section": "middle"},
                {"id": "middle_separator", "label": "Séparateur", "master": False, "section": "middle"},
                {"id": "footer", "label": "Pied de page", "master": True, "section": "footer"},
                {"id": "footer_mentions", "label": "Mentions légales", "master": False, "section": "footer"}
            ],
            "visible": {
                "header": True,
                "header_title": True,
                "header_notice_fr": True,
                "header_notice_en": True,
                "middle": True,
                "middle_logo": True,
                "middle_title": True,
                "middle_table": True,
                "middle_iban_bic": True,
                "middle_titulaire": True,
                "middle_separator": True,
                "footer": True,
                "footer_mentions": True
            }
        }
    }
