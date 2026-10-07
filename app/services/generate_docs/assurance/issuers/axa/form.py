from . import copy

# ----------------------------------------------------------------------


def get_form_schema() -> dict:
    return {
        "metadata": {
            "title": "GÉNÉRATEUR MÉMO VÉHICULE AXA",
            "subtitle": "Document PDF AXA France Officiel",
            "logo": "/logos/axa.svg?v=2",
            "headerBg": "bg-gradient-to-br from-blue-950/50 to-slate-950/80 border-blue-500/30",
            "priceKey": "axa",
            "apiBase": "/api/generate-docs/assurance/axa",
            "filenameTemplate": "Memo_Vehicule_Assure_AXA_{immatriculation}.pdf",
            "generateLabel": "Générer l'Attestation",
            "backHref": "/services/generate-docs/assurance",
            "backLabel": "Retour aux assurances"
        },
        "defaults": {
            "civilite": copy.CIVILITE,
            "nom": copy.NOM,
            "prenom": copy.PRENOM,
            "titulaire": copy.DESTINATAIRE_L1,
            "destinataire_l1": copy.DESTINATAIRE_L1,
            "adresse": copy.ADRESSE,
            "destinataire_l2": copy.DESTINATAIRE_L2,
            "cp": copy.CP,
            "ville": copy.VILLE,
            "cp_ville": copy.DESTINATAIRE_L3,
            "destinataire_l3": copy.DESTINATAIRE_L3,
            "num_client": copy.NUM_CLIENT,
            "info_client": copy.INFO_CLIENT,
            "num_contrat": copy.NUM_CONTRAT,
            "info_contrat": copy.INFO_CONTRAT,
            "immatriculation": copy.IMMATRICULATION,
            "vehicule_immat": copy.VEHICULE_IMMAT,
            "vehicule_marque_modele": copy.VEHICULE_MARQUE_MODELE,
            "vehicule_marque": copy.VEHICULE_MARQUE,
            "tel_sinistre": copy.TEL_SINISTRE,
            "sinistre_tel_label": copy.SINISTRE_TEL_LABEL,
            "mail_sinistre": copy.MAIL_SINISTRE,
            "sinistre_mail_val": copy.SINISTRE_MAIL_VAL,
            "tel_assistance_france": copy.TEL_ASSISTANCE_FRANCE,
            "assistance_france": copy.ASSISTANCE_FRANCE,
            "tel_assistance_etranger": copy.TEL_ASSISTANCE_ETRANGER,
            "assistance_etranger": copy.ASSISTANCE_ETRANGER,
            "date_delivrance": copy.default_date_delivrance(),
            "date_effet": copy.default_date_effet()
        },
        "sections": [
            {
                "id": "references",
                "title": "1. Références du Contrat AXA",
                "order": 1,
                "fields": [
                    {
                        "key": "num_client",
                        "label": "Numéro Client",
                        "kind": "text",
                        "span": 1,
                        "required": True,
                        "placeholder": "A084RZ",
                        "rules": {
                            "required": True,
                            "min": 2
                        }
                    },
                    {
                        "key": "num_contrat",
                        "label": "Numéro de Contrat",
                        "kind": "contract_axa",
                        "span": 1,
                        "required": True,
                        "placeholder": "D443 - 4180352981 - 4180352981   367304284920",
                        "rules": {
                            "required": True,
                            "min": 2,
                            "max": 60
                        }
                    },
                    {
                        "key": "date_delivrance",
                        "label": "Date d'Édition",
                        "kind": "date",
                        "dateFormat": "slash",
                        "span": 1,
                        "required": True,
                        "placeholder": "JJ/MM/AAAA",
                        "rules": {
                            "required": True
                        }
                    },
                    {
                        "key": "date_effet",
                        "label": "Date d'Effet",
                        "kind": "date",
                        "dateFormat": "slash",
                        "span": 1,
                        "required": True,
                        "placeholder": "JJ/MM/AAAA",
                        "rules": {
                            "required": True
                        }
                    }
                ]
            },
            {
                "id": "assure",
                "title": "2. Coordonnées de l'Assuré",
                "order": 2,
                "fields": [
                    {
                        "key": "civilite",
                        "label": "Civilité",
                        "kind": "select",
                        "span": 1,
                        "required": True,
                        "options": [
                            {"value": "MONSIEUR", "label": "MONSIEUR"},
                            {"value": "MADAME", "label": "MADAME"},
                            {"value": "__CUSTOM__", "label": "Personnalisé"}
                        ],
                        "rules": {
                            "required": True
                        }
                    },
                    {
                        "key": "nom",
                        "label": "Nom",
                        "kind": "text",
                        "span": 1,
                        "required": True,
                        "placeholder": "MARTIN",
                        "rules": {
                            "required": True,
                            "min": 2,
                            "transform": "uppercase"
                        }
                    },
                    {
                        "key": "prenom",
                        "label": "Prénom",
                        "kind": "text",
                        "span": 1,
                        "required": True,
                        "placeholder": "LUCAS",
                        "rules": {
                            "required": True,
                            "min": 2,
                            "transform": "uppercase"
                        }
                    },
                    {
                        "key": "adresse",
                        "label": "Adresse Postale",
                        "kind": "text",
                        "span": 2,
                        "required": True,
                        "autocompleteType": "address",
                        "placeholder": "12 RUE DES FLEURS",
                        "rules": {
                            "required": True,
                            "min": 3
                        }
                    },
                    {
                        "key": "cp",
                        "label": "Code Postal",
                        "kind": "text",
                        "span": 1,
                        "required": True,
                        "autocompleteType": "city",
                        "placeholder": "75011",
                        "rules": {
                            "required": True,
                            "min": 5,
                            "max": 5
                        }
                    },
                    {
                        "key": "ville",
                        "label": "Ville",
                        "kind": "text",
                        "span": 1,
                        "required": True,
                        "placeholder": "PARIS",
                        "rules": {
                            "required": True,
                            "min": 2,
                            "transform": "uppercase"
                        }
                    }
                ]
            },
            {
                "id": "vehicule",
                "title": "3. Information du Véhicule",
                "order": 3,
                "fields": [
                    {
                        "key": "immatriculation",
                        "label": "Immatriculation",
                        "kind": "text",
                        "span": 1,
                        "required": True,
                        "placeholder": "FA-120-GM",
                        "rules": {
                            "required": True,
                            "min": 4,
                            "transform": "uppercase"
                        }
                    },
                    {
                        "key": "vehicule_marque_modele",
                        "label": "Marque et Modèle",
                        "kind": "text",
                        "span": 1,
                        "required": True,
                        "placeholder": "BMW X3",
                        "rules": {
                            "required": True,
                            "min": 2
                        }
                    }
                ]
            },
            {
                "id": "contact",
                "title": "4. Assistance & Sinistres (Optionnel)",
                "order": 4,
                "fields": [
                    {
                        "key": "tel_sinistre",
                        "label": "Téléphone Sinistres",
                        "kind": "tel",
                        "span": 1,
                        "placeholder": "01.41.03.31.08"
                    },
                    {
                        "key": "mail_sinistre",
                        "label": "Email Sinistres",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "sinistres@lsa-courtage.com"
                    },
                    {
                        "key": "tel_assistance_france",
                        "label": "Assistance (France)",
                        "kind": "tel",
                        "span": 1,
                        "placeholder": "01.45.16.65.55"
                    },
                    {
                        "key": "tel_assistance_etranger",
                        "label": "Assistance (Étranger)",
                        "kind": "tel",
                        "span": 1,
                        "placeholder": "(33).1.45.16.65.55"
                    }
                ]
            }
        ],
        "customLayout": {
            "sections": [
                {"id": "header", "label": "En-tête"},
                {"id": "middle", "label": "Corps du mémo"},
                {"id": "footer", "label": "Pied de page"}
            ],
            "blocks": [
                {"id": "header", "label": "En-tête", "master": True, "section": "header"},
                {"id": "header_logo", "label": "Logo AXA", "section": "header"},
                {"id": "header_recipient", "label": "Destinataire & Date d'édition", "section": "header"},
                {"id": "header_carte_verte", "label": "Rappel Carte Verte (Article R.211-14-0)", "section": "header"},
                {"id": "header_notice", "label": "Bandeau Mémo Véhicule Assuré", "section": "header"},
                {"id": "header_presomption", "label": "Présomption d'assurance & FVA", "section": "header"},
                {"id": "middle", "label": "Corps du mémo", "master": True, "section": "middle"},
                {"id": "middle_vehicule", "label": "Véhicule & Contrat", "section": "middle"},
                {"id": "middle_remorque", "label": "Extension Remorque", "section": "middle"},
                {"id": "middle_assureur", "label": "Coordonnées de l'assureur", "section": "middle"},
                {"id": "middle_couverture", "label": "Couverture géographique", "section": "middle"},
                {"id": "footer", "label": "Pied de page", "master": True, "section": "footer"},
                {"id": "footer_numeros_utiles", "label": "Numéros utiles (Sinistres & Assistance)", "section": "footer"},
                {"id": "footer_questions", "label": "Questions & Informations utiles", "section": "footer"},
                {"id": "footer_legal", "label": "Mentions légales", "section": "footer"}
            ],
            "visible": {
                "header": True,
                "header_logo": True,
                "header_recipient": True,
                "header_carte_verte": True,
                "header_notice": True,
                "header_presomption": True,
                "middle": True,
                "middle_vehicule": True,
                "middle_remorque": True,
                "middle_assureur": True,
                "middle_couverture": True,
                "footer": True,
                "footer_numeros_utiles": True,
                "footer_questions": True,
                "footer_legal": True
            }
        }
    }
