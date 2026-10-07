def get_form_schema() -> dict:
    return {
        "defaults": {
            "cp": "94800",
            "nom": "Malatray",
            "port": "0,00",
            "immat": "RCS BORDEAUX 424 059 822",
            "items": [
                {
                    "qte": "1",
                    "desc": "APPLE iPhone 14 128GB",
                    "montant": "271,99"
                }
            ],
            "ville": "Villejuif",
            "prenom": "Antoine",
            "adresse": "2 Rue Alexandre Dumas",
            "payment": "Carte Bancaire",
            "vendeur": "CDISCOUNT",
            "livraison_cp": "94800",
            "num_commande": "2604070231S1C0X",
            "date_commande": "07/04/2026",
            "livraison_nom": "Malatray",
            "livraison_ville": "Villejuif",
            "livraison_prenom": "Antoine",
            "livraison_adresse": "2 Rue Alexandre Dumas",
            "total": "271,99",
            "sold_by_cdiscount": "true"
        },
        "metadata": {
            "logo": "/logos/cdiscount.svg",
            "title": "GÉNÉRATEUR FACTURE CDISCOUNT",
            "apiBase": "/api/generate-docs/facture/cdiscount",
            "itemKey": "items",
            "backHref": "/services/generate-docs/facture",
            "category": "facture",
            "headerBg": "bg-white border-red-500/30",
            "maxItems": 3,
            "priceKey": "cdiscount",
            "subtitle": "Document PDF Cdiscount officiel",
            "backLabel": "Retour aux factures",
            "itemBlank": {
                "qte": "1",
                "desc": "",
                "montant": "0,00"
            },
            "itemLabel": "5. Articles",
            "generateLabel": "Générer la preuve d'achat",
            "filenameTemplate": "Facture_Cdiscount.pdf"
        },
        "sections": [
            {
                "title": "1. Modèle de vente",
                "fields": [
                    {
                        "key": "sold_by_cdiscount",
                        "kind": "select",
                        "span": 2,
                        "label": "Modèle de vente",
                        "options": [
                            {
                                "label": "Vendu par Cdiscount (Cdiscount SA)",
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
                "title": "2. Facturation",
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
                        }
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
                    }
                ]
            },
            {
                "title": "3. Livraison",
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
                        }
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
                    }
                ]
            },
            {
                "title": "4. Vendeur Marketplace",
                "condition": {"key": "sold_by_cdiscount", "value": "false"},
                "fields": [
                    {
                        "key": "vendeur",
                        "kind": "text",
                        "span": 1,
                        "label": "Nom du vendeur",
                        "rules": {
                            "max": 40,
                            "min": 2,
                            "required": True
                        },
                        "placeholder": "KXYTRADE"
                    },
                    {
                        "key": "immat",
                        "kind": "text",
                        "span": 1,
                        "label": "Numéro d'immatriculation",
                        "rules": {
                            "max": 30,
                            "min": 4,
                            "required": True
                        },
                        "placeholder": "J2025074480006"
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
                            "max": 24,
                            "min": 5,
                            "required": True
                        },
                        "placeholder": "2604070231S1C0X"
                    },
                    {
                        "key": "date_commande",
                        "kind": "date",
                        "span": 1,
                        "label": "Date de commande",
                        "dateFormat": "slash",
                        "rules": {
                            "required": True
                        }
                    },
                    {
                        "key": "payment",
                        "kind": "text",
                        "span": 2,
                        "label": "Mode de règlement",
                        "rules": {
                            "max": 24,
                            "min": 2,
                            "required": True
                        },
                        "placeholder": "Carte Bancaire"
                    }
                ]
            },
            {
                "title": "6. Totaux",
                "position": "after_items",
                "fields": [
                    {
                        "key": "port",
                        "kind": "text",
                        "span": 1,
                        "label": "Frais de port (€)",
                        "rules": {
                            "max": 10,
                            "required": True
                        },
                        "placeholder": "0,00"
                    },
                    {
                        "key": "total",
                        "kind": "text",
                        "span": 1,
                        "label": "Total TTC",
                        "rules": {
                            "max": 12,
                            "required": True
                        },
                        "placeholder": "271,99"
                    }
                ]
            }
        ],
        "itemBlank": {
            "qte": "1",
            "desc": "",
            "montant": "0,00"
        },
        "itemColumns": [
            {
                "key": "desc",
                "label": "Désignation"
            },
            {
                "key": "qte",
                "label": "Qté"
            },
            {
                "key": "montant",
                "label": "Montant TTC"
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
                    "id": "header_banner",
                    "label": "Bandeau Cdiscount",
                    "section": "header"
                },
                {
                    "id": "header_logo",
                    "label": "Logo Cdiscount",
                    "section": "header"
                },
                {
                    "id": "header_title",
                    "label": "Titre PREUVE D'ACHAT",
                    "section": "header"
                },
                {
                    "id": "header_order",
                    "label": "Numéro & Date de commande",
                    "section": "header"
                },
                {
                    "id": "header_addresses",
                    "label": "Adresses Facturation & Livraison",
                    "section": "header"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture complet",
                    "master": True,
                    "section": "middle"
                },
                {
                    "id": "middle_heading",
                    "label": "En-tête du tableau",
                    "section": "middle"
                },
                {
                    "id": "middle_columns",
                    "label": "Colonnes des articles",
                    "section": "middle"
                },
                {
                    "id": "middle_rows",
                    "label": "Lignes des articles",
                    "section": "middle"
                },
                {
                    "id": "middle_totals",
                    "label": "Totaux & Port",
                    "section": "middle"
                },
                {
                    "id": "middle_vendor",
                    "label": "Bloc Vendeur & Immatriculation",
                    "section": "middle"
                },
                {
                    "id": "footer",
                    "label": "Pied de page complet",
                    "master": True,
                    "section": "footer"
                },
                {
                    "id": "footer_note",
                    "label": "Note d'information",
                    "section": "footer"
                },
                {
                    "id": "footer_cgu",
                    "label": "Conditions générales",
                    "section": "footer"
                },
                {
                    "id": "footer_legal",
                    "label": "Mentions légales Cdiscount",
                    "section": "footer"
                }
            ],
            "visible": {
                "footer": True,
                "header": True,
                "middle": True,
                "footer_cgu": True,
                "footer_note": False,
                "header_logo": True,
                "middle_rows": True,
                "footer_legal": True,
                "header_order": True,
                "header_title": True,
                "header_banner": True,
                "middle_totals": True,
                "middle_vendor": True,
                "middle_columns": True,
                "middle_heading": True,
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
