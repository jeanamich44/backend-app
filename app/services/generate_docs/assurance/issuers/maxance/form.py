from . import copy

# ----------------------------------------------------------------------


def get_form_schema() -> dict:
    return {
        "metadata": {
            "title": "Attestation Maxance",
            "subtitle": "Document PDF Maxance Assurances Officiel",
            "logo": "/logos/maxance.svg",
            "headerBg": "bg-gradient-to-br from-red-950/50 to-slate-950/80 border-rose-500/30",
            "priceKey": "maxance",
            "apiBase": "/api/generate-docs/assurance/maxance",
            "filenameTemplate": "Memo_Vehicule_Assure_Maxance_{immatriculation}.pdf"
        },
        "defaults": {
            "civilite": copy.CIVILITE,
            "nom": copy.NOM,
            "prenom": copy.PRENOM,
            "adresse": copy.ADRESSE,
            "cp": copy.CP,
            "ville": copy.VILLE,
            "pays": copy.PAYS,
            "courtier": copy.COURTIER,
            "num_client": copy.NUM_CLIENT,
            "num_contrat": copy.NUM_CONTRAT,
            "num_orias": copy.NUM_ORIAS,
            "immatriculation": copy.IMMATRICULATION,
            "vehicule_marque_modele": copy.VEHICULE_MARQUE_MODELE,
            "date_delivrance": copy.DATE_DELIVRANCE,
            "date_effet": copy.DATE_EFFET,
            "date_effet_jour": copy.DATE_EFFET_JOUR,
            "date_effet_mois": copy.DATE_EFFET_MOIS,
            "date_effet_annee": copy.DATE_EFFET_ANNEE,
            "titulaire": copy.TITULAIRE,
            "cp_ville": copy.CP_VILLE
        },
        "sections": [
            {
                "id": "references",
                "title": "1. Références du Contrat Maxance",
                "order": 1,
                "fields": [
                    {
                        "key": "num_client",
                        "label": "Numéro Client",
                        "kind": "text",
                        "span": 1,
                        "rules": {
                            "min": 4,
                            "max": 30,
                            "required": True
                        }
                    },
                    {
                        "key": "num_contrat",
                        "label": "Numéro Contrat",
                        "kind": "text",
                        "span": 1,
                        "rules": {
                            "min": 4,
                            "max": 30,
                            "required": True
                        }
                    },
                    {
                        "key": "num_orias",
                        "label": "N° ORIAS",
                        "kind": "text",
                        "span": 1,
                        "rules": {
                            "min": 3,
                            "max": 20,
                            "required": True
                        }
                    },
                    {
                        "key": "courtier",
                        "label": "Courtier",
                        "kind": "text",
                        "span": 2,
                        "rules": {
                            "max": 60,
                            "required": False
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
                        "options": [
                            {"label": "M.", "value": "M."},
                            {"label": "MME", "value": "MME"},
                            {"label": "MLLE", "value": "MLLE"},
                            {"label": "Rien", "value": "__NONE__"},
                            {"label": "Personnalisé", "value": "__CUSTOM__"}
                        ],
                        "rules": {
                            "required": False
                        }
                    },
                    {
                        "key": "nom",
                        "label": "Nom",
                        "kind": "text",
                        "span": 1,
                        "rules": {
                            "min": 2,
                            "max": 40,
                            "required": True,
                            "transform": "uppercase"
                        }
                    },
                    {
                        "key": "prenom",
                        "label": "Prénom",
                        "kind": "text",
                        "span": 1,
                        "rules": {
                            "min": 2,
                            "max": 40,
                            "required": True,
                            "transform": "uppercase"
                        }
                    },
                    {
                        "key": "adresse",
                        "label": "Adresse Postale",
                        "kind": "text",
                        "span": 2,
                        "autocompleteType": "address",
                        "rules": {
                            "min": 4,
                            "max": 60,
                            "required": True,
                            "transform": "uppercase"
                        }
                    },
                    {
                        "key": "cp",
                        "label": "Code Postal",
                        "kind": "text",
                        "span": 1,
                        "autocompleteType": "city",
                        "rules": {
                            "min": 4,
                            "max": 10,
                            "required": True
                        }
                    },
                    {
                        "key": "ville",
                        "label": "Ville",
                        "kind": "text",
                        "span": 1,
                        "autocompleteType": "city",
                        "rules": {
                            "min": 2,
                            "max": 50,
                            "required": True,
                            "transform": "uppercase"
                        }
                    },
                    {
                        "key": "pays",
                        "label": "Pays",
                        "kind": "text",
                        "span": 2,
                        "rules": {
                            "min": 2,
                            "max": 30,
                            "required": True,
                            "transform": "uppercase"
                        }
                    }
                ]
            },
            {
                "id": "vehicule_dates",
                "title": "3. Information du Véhicule & Dates",
                "order": 3,
                "fields": [
                    {
                        "key": "immatriculation",
                        "label": "Immatriculation",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "ex: AH-120-PO",
                        "rules": {
                            "min": 4,
                            "max": 16,
                            "required": True,
                            "transform": "uppercase"
                        }
                    },
                    {
                        "key": "vehicule_marque_modele",
                        "label": "Marque / Modèle / Cylindrée",
                        "kind": "text",
                        "span": 1,
                        "placeholder": "ex: YAMAHA X-MAX (SCOOTER 125 cc)",
                        "rules": {
                            "min": 3,
                            "max": 80,
                            "required": True
                        }
                    },
                    {
                        "key": "date_delivrance",
                        "label": "Date de Délivrance du Document",
                        "kind": "date",
                        "dateFormat": "slash",
                        "span": 2,
                        "rules": {
                            "required": True
                        }
                    },
                    {
                        "key": "date_effet",
                        "label": "Date d'Effet (Jour / Mois / Année)",
                        "kind": "date",
                        "dateFormat": "slash",
                        "span": 2,
                        "rules": {
                            "required": True
                        }
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
                {"id": "header", "label": "En-tête complet", "master": True, "section": "header"},
                {"id": "header_logo", "label": "Logo Maxance", "master": False, "section": "header"},
                {"id": "header_identity", "label": "Coordonnées de l'assuré & courtier", "master": False, "section": "header"},
                {"id": "header_banner", "label": "Bandeau d'avertissement rouge", "master": False, "section": "header"},
                {"id": "middle", "label": "Corps du mémo (véhicule, contrat & dates)", "master": True, "section": "middle"},
                {"id": "footer", "label": "Pied de page (Section 9, ORIAS & RCS)", "master": True, "section": "footer"}
            ],
            "visible": {
                "header": True,
                "header_logo": True,
                "header_identity": True,
                "header_banner": True,
                "middle": True,
                "footer": True
            }
        }
    }
