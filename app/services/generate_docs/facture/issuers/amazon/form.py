def get_form_schema() -> dict:
    return {
        "defaults": {
            "cp": "75011",
            "nom": "Martin",
            "pays": "FR",
            "items": [
                {
                    "nom": "Casque audio sans fil Bluetooth, autonomie 30 h.",
                    "qte": "1",
                    "asin": "B0C3D81M43",
                    "note": "Information indisponible sur les pièces détachées",
                    "pu_ht": "100,00",
                    "pu_ttc": "120,00"
                }
            ],
            "total": "120,00",
            "ville": "Paris",
            "prenom": "Lucas",
            "adresse": "12 Rue des Fleurs",
            "cp_ville": "75011 Paris",
            "tva_rate": "20 %",
            "remise_ht": "0,00",
            "seller_cp": "92110",
            "remise_ttc": "0,00",
            "seller_nom": "Amazon EU S.à r.l., Succursale Française",
            "seller_tva": "LU19647148",
            "num_facture": "DS-ASE-INV-FR-2022-172445727",
            "payment_ref": "2MVI3VL9HC4A0NEC",
            "seller_pays": "France",
            "livraison_cp": "75011",
            "num_commande": "403-2699905-9515527",
            "seller_ville": "Clichy",
            "expedition_ht": "0,00",
            "livraison_nom": "Martin",
            "expedition_ttc": "0,00",
            "livraison_pays": "FR",
            "seller_adresse": "67 Boulevard du General Leclerc",
            "sold_by_amazon": "true",
            "livraison_ville": "Paris",
            "seller_adresse2": "",
            "seller_cp_ville": "Clichy 92110",
            "livraison_prenom": "Lucas",
            "livraison_adresse": "12 Rue des Fleurs",
            "livraison_cp_ville": "75011 Paris"
        },
        "metadata": {
            "logo": "/logos/amazon.svg",
            "title": "GÉNÉRATEUR FACTURE AMAZON",
            "apiBase": "/api/generate-docs/facture/amazon",
            "itemKey": "items",
            "backHref": "/services/generate-docs/facture",
            "headerBg": "bg-white border-amber-500/30",
            "maxItems": 20,
            "priceKey": "amazon",
            "subtitle": "Document PDF Amazon officiel",
            "backLabel": "Retour aux factures",
            "itemLabel": "6. Articles",
            "generateLabel": "Générer la facture",
            "filenameTemplate": "Facture_Amazon.pdf"
        },
        "sections": [
            {
                "title": "1. Version de facture",
                "fields": [
                    {
                        "key": "sold_by_amazon",
                        "kind": "select",
                        "span": 2,
                        "label": "Modèle de facture",
                        "options": [
                            {
                                "label": "Vendu par Amazon (Amazon EU S.à r.l.)",
                                "value": "true"
                            },
                            {
                                "label": "Vendu par un vendeur tiers (Marketplace)",
                                "value": "false"
                            }
                        ]
                    }
                ]
            },
            {
                "title": "2. Adresse de facturation",
                "fields": [
                    {
                        "key": "nom",
                        "kind": "text",
                        "span": 1,
                        "label": "Nom",
                        "rules": {
                            "max": 40,
                            "min": 2,
                            "required": True
                        }
                    },
                    {
                        "key": "prenom",
                        "kind": "text",
                        "span": 1,
                        "label": "Prénom",
                        "rules": {
                            "max": 40,
                            "min": 2,
                            "required": True
                        }
                    },
                    {
                        "key": "adresse",
                        "kind": "text",
                        "span": 2,
                        "label": "Adresse",
                        "rules": {
                            "max": 50,
                            "min": 4,
                            "required": True
                        },
                        "autocompleteType": "address"
                    },
                    {
                        "key": "cp",
                        "kind": "text",
                        "span": 1,
                        "label": "Code postal",
                        "rules": {
                            "max": 10,
                            "min": 4,
                            "required": True
                        },
                        "autocompleteType": "city"
                    },
                    {
                        "key": "ville",
                        "kind": "text",
                        "span": 1,
                        "label": "Ville",
                        "rules": {
                            "max": 40,
                            "min": 2,
                            "required": True
                        },
                        "autocompleteType": "city"
                    },
                    {
                        "key": "pays",
                        "kind": "country",
                        "span": 2,
                        "label": "Pays",
                        "rules": {
                            "max": 12,
                            "min": 2,
                            "required": True
                        },
                        "advanced": True,
                        "placeholder": "Sélectionner un pays"
                    }
                ]
            },
            {
                "title": "3. Adresse de livraison",
                "fields": [
                    {
                        "key": "livraison_nom",
                        "kind": "text",
                        "span": 1,
                        "label": "Nom",
                        "rules": {
                            "max": 40,
                            "min": 2,
                            "required": True
                        }
                    },
                    {
                        "key": "livraison_prenom",
                        "kind": "text",
                        "span": 1,
                        "label": "Prénom",
                        "rules": {
                            "max": 40,
                            "min": 2,
                            "required": True
                        }
                    },
                    {
                        "key": "livraison_adresse",
                        "kind": "text",
                        "span": 2,
                        "label": "Adresse",
                        "rules": {
                            "max": 50,
                            "min": 4,
                            "required": True
                        },
                        "autocompleteType": "address"
                    },
                    {
                        "key": "livraison_cp",
                        "kind": "text",
                        "span": 1,
                        "label": "Code postal",
                        "rules": {
                            "max": 10,
                            "min": 4,
                            "required": True
                        },
                        "autocompleteType": "city"
                    },
                    {
                        "key": "livraison_ville",
                        "kind": "text",
                        "span": 1,
                        "label": "Ville",
                        "rules": {
                            "max": 40,
                            "min": 2,
                            "required": True
                        },
                        "autocompleteType": "city"
                    },
                    {
                        "key": "livraison_pays",
                        "kind": "country",
                        "span": 2,
                        "label": "Pays",
                        "rules": {
                            "max": 12,
                            "min": 2,
                            "required": True
                        },
                        "advanced": True,
                        "placeholder": "Sélectionner un pays"
                    }
                ]
            },
            {
                "title": "4. Vendeur",
                "condition": {"key": "sold_by_amazon", "value": "false"},
                "fields": [
                    {
                        "key": "seller_nom",
                        "kind": "text",
                        "span": 2,
                        "label": "Nom",
                        "rules": {
                            "max": 56,
                            "min": 2,
                            "required": True
                        }
                    },
                    {
                        "key": "seller_adresse",
                        "kind": "text",
                        "span": 1,
                        "label": "Adresse",
                        "rules": {
                            "max": 50,
                            "min": 4,
                            "required": True
                        }
                    },
                    {
                        "key": "seller_adresse2",
                        "kind": "text",
                        "span": 1,
                        "label": "Adresse 2",
                        "rules": {
                            "max": 50,
                            "required": False
                        }
                    },
                    {
                        "key": "seller_cp",
                        "kind": "text",
                        "span": 1,
                        "label": "Code postal",
                        "rules": {
                            "max": 10,
                            "min": 4,
                            "required": True
                        }
                    },
                    {
                        "key": "seller_ville",
                        "kind": "text",
                        "span": 1,
                        "label": "Ville",
                        "rules": {
                            "max": 40,
                            "min": 2,
                            "required": True
                        }
                    },
                    {
                        "key": "seller_pays",
                        "kind": "text",
                        "span": 1,
                        "label": "Pays",
                        "rules": {
                            "max": 20,
                            "min": 2,
                            "required": True
                        }
                    },
                    {
                        "key": "seller_tva",
                        "kind": "text",
                        "span": 1,
                        "label": "TVA",
                        "rules": {
                            "max": 20,
                            "min": 4,
                            "required": True
                        },
                        "placeholder": "LU19647148"
                    }
                ]
            },
            {
                "title": "5. Commande",
                "fields": [
                    {
                        "key": "num_commande",
                        "kind": "text",
                        "span": 1,
                        "label": "N° de commande",
                        "rules": {
                            "max": 30,
                            "min": 5,
                            "required": True
                        },
                        "placeholder": "403-2699905-9515527"
                    },
                    {
                        "key": "date_commande",
                        "kind": "date",
                        "span": 1,
                        "label": "Date de commande",
                        "rules": {
                            "required": True
                        },
                        "dateFormat": "french"
                    },
                    {
                        "key": "num_facture",
                        "kind": "text",
                        "span": 1,
                        "label": "N° de facture",
                        "rules": {
                            "max": 40,
                            "min": 5,
                            "required": True
                        },
                        "placeholder": "DS-ASE-INV-FR-2022-172445727"
                    },
                    {
                        "key": "date_facture",
                        "kind": "date",
                        "span": 1,
                        "label": "Date de facture",
                        "rules": {
                            "required": True
                        },
                        "dateFormat": "french"
                    },
                    {
                        "key": "payment_ref",
                        "kind": "text",
                        "span": 2,
                        "label": "Référence de paiement",
                        "rules": {
                            "max": 40,
                            "required": False
                        },
                        "placeholder": "2MVI3VL9HC4A0NEC"
                    }
                ]
            },
            {
                "title": "7. Calculs & Montants",
                "fields": [
                    {
                        "key": "total",
                        "kind": "text",
                        "span": 2,
                        "label": "Total à payer",
                        "rules": {
                            "max": 14,
                            "min": 1,
                            "required": True
                        }
                    },
                    {
                        "key": "expedition_ht",
                        "kind": "text",
                        "span": 1,
                        "label": "Expédition HT",
                        "rules": {
                            "max": 14,
                            "required": False
                        },
                        "advanced": True
                    },
                    {
                        "key": "expedition_ttc",
                        "kind": "text",
                        "span": 1,
                        "label": "Expédition TTC",
                        "rules": {
                            "max": 14,
                            "required": False
                        },
                        "advanced": True
                    },
                    {
                        "key": "remise_ht",
                        "kind": "text",
                        "span": 1,
                        "label": "Remise HT",
                        "rules": {
                            "max": 14,
                            "required": False
                        },
                        "advanced": True
                    },
                    {
                        "key": "remise_ttc",
                        "kind": "text",
                        "span": 1,
                        "label": "Remise TTC",
                        "rules": {
                            "max": 14,
                            "required": False
                        },
                        "advanced": True
                    },
                    {
                        "key": "tva_rate",
                        "kind": "text",
                        "span": 1,
                        "label": "Taux TVA",
                        "rules": {
                            "max": 8,
                            "required": False
                        },
                        "advanced": True
                    }
                ],
                "position": "after_items"
            }
        ],
        "itemBlank": {
            "nom": "",
            "qte": "1",
            "asin": "",
            "note": "",
            "pu_ht": "0,00",
            "pu_ttc": "0,00"
        },
        "itemColumns": [
            {
                "key": "nom",
                "label": "Description"
            },
            {
                "key": "note",
                "label": "Note"
            },
            {
                "key": "qte",
                "label": "Qté"
            },
            {
                "key": "pu_ht",
                "label": "Prix unitaire HT"
            },
            {
                "key": "pu_ttc",
                "label": "Prix unitaire TTC"
            },
            {
                "key": "asin",
                "label": "ASIN",
                "placeholder": "B0C3D81M43"
            }
        ],
        "customLayout": {
            "blocks": [
                {
                    "id": "header",
                    "label": "En-tête complet",
                    "master": True,
                    "section": "header"
                },
                {
                    "id": "header_logo",
                    "label": "Logo Amazon",
                    "master": False,
                    "section": "header"
                },
                {
                    "id": "header_title",
                    "label": "Titre Facture",
                    "master": False,
                    "section": "header"
                },
                {
                    "id": "header_identity",
                    "label": "Identité Vendeur / Numéro",
                    "master": False,
                    "section": "header"
                },
                {
                    "id": "header_pay",
                    "label": "Bloc Référence de paiement",
                    "master": False,
                    "section": "header"
                },
                {
                    "id": "header_contact",
                    "label": "Bloc Contact Amazon",
                    "master": False,
                    "section": "header"
                },
                {
                    "id": "header_addresses",
                    "label": "Adresses Facturation, Livraison & Vendeur",
                    "master": False,
                    "section": "header"
                },
                {
                    "id": "header_order",
                    "label": "Détails de commande",
                    "master": False,
                    "section": "header"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture complet",
                    "master": True,
                    "section": "middle"
                },
                {
                    "id": "middle_columns",
                    "label": "En-tête colonnes tableau",
                    "master": False,
                    "section": "middle"
                },
                {
                    "id": "middle_rows",
                    "label": "Lignes d'articles",
                    "master": False,
                    "section": "middle"
                },
                {
                    "id": "middle_totals",
                    "label": "Totaux & Frais",
                    "master": False,
                    "section": "middle"
                },
                {
                    "id": "middle_vat",
                    "label": "Tableau récapitulatif TVA",
                    "master": False,
                    "section": "middle"
                },
                {
                    "id": "footer",
                    "label": "Pied de page complet",
                    "master": True,
                    "section": "footer"
                },
                {
                    "id": "footer_line",
                    "label": "Ligne de séparation",
                    "master": False,
                    "section": "footer"
                },
                {
                    "id": "footer_legal",
                    "label": "Mentions légales",
                    "master": False,
                    "section": "footer"
                },
                {
                    "id": "footer_page",
                    "label": "Numérotation de page",
                    "master": False,
                    "section": "footer"
                }
            ],
            "visible": {
                "footer": True,
                "header": True,
                "middle": True,
                "header_pay": True,
                "middle_vat": True,
                "footer_line": True,
                "footer_page": True,
                "header_logo": True,
                "middle_rows": True,
                "footer_legal": True,
                "header_order": True,
                "header_title": True,
                "middle_totals": True,
                "header_contact": True,
                "middle_columns": True,
                "header_identity": True,
                "header_addresses": True
            },
            "sections": [
                {
                    "id": "header",
                    "label": "En-tête"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture"
                },
                {
                    "id": "footer",
                    "label": "Pied de page"
                }
            ]
        }
    }
