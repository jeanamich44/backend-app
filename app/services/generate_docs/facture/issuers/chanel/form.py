def get_form_schema() -> dict:
    return {
        "version": 7,
        "defaults": {
            "cp": "75011",
            "nom": "Martin",
            "pays": "France",
            "items": [
                {
                    "qty": "1",
                    "ref": "107360",
                    "desc": "Eau de parfum vaporisateur - 100ml",
                    "total": "132,00",
                    "unit_price": "132,00"
                }
            ],
            "ville": "Paris",
            "prenom": "Lucas",
            "adresse": "12 Rue des Fleurs",
            "civilite": "Monsieur",
            "total_ht": "110,00",
            "total_tva": "22,00",
            "total_ttc": "132,00",
            "folio_num": "1",
            "caisse_num": "AA1/AA105",
            "client_tel": "",
            "conseiller": "Amélie",
            "date_vente": "05/09/2023",
            "client_code": "AA01454795",
            "facture_num": "735179",
            "heure_vente": "14:34",
            "store_line_1": "31 rue Cambon - 75001 PARIS",
            "store_line_2": "TEL : +33 (0) 1 44 50 66 00",
            "mode_paiement": "ESPECES EUROS"
        },
        "metadata": {
            "logo": "/logos/chanel.png",
            "title": "Chanel",
            "apiBase": "/api/generate-docs/facture/chanel",
            "itemKey": "items",
            "backHref": "/services/generate-docs/facture",
            "headerBg": "bg-white border-neutral-800/30",
            "maxItems": 3,
            "priceKey": "chanel",
            "subtitle": "Facture boutique Chanel Mode & Joaillerie",
            "backLabel": "Retour aux factures",
            "itemLabel": "Articles",
            "logoClass": "scale-[1.8] md:scale-[2.0]",
            "generateLabel": "Générer la facture Chanel",
            "filenameTemplate": "Facture_Chanel.pdf"
        },
        "sections": [
            {
                "title": "1. Coordonnées client",
                "fields": [
                    {
                        "key": "civilite",
                        "kind": "select",
                        "span": 1,
                        "label": "Civilité",
                        "rules": {
                            "required": True
                        },
                        "options": [
                            {
                                "label": "Monsieur",
                                "value": "Monsieur"
                            },
                            {
                                "label": "Madame",
                                "value": "Madame"
                            }
                        ]
                    },
                    {
                        "key": "nom",
                        "kind": "text",
                        "span": 1,
                        "label": "Nom",
                        "rules": {
                            "max": 35,
                            "min": 2,
                            "required": True
                        },
                        "placeholder": "Martin"
                    },
                    {
                        "key": "prenom",
                        "kind": "text",
                        "span": 1,
                        "label": "Prénom",
                        "rules": {
                            "max": 35,
                            "min": 2,
                            "required": True
                        },
                        "placeholder": "Lucas"
                    },
                    {
                        "key": "adresse",
                        "kind": "text",
                        "span": 2,
                        "label": "Adresse",
                        "rules": {
                            "max": 80,
                            "min": 4,
                            "required": True
                        },
                        "placeholder": "12 Rue des Fleurs"
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
                        "placeholder": "75011",
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
                        "placeholder": "Paris",
                        "autocompleteType": "city"
                    },
                    {
                        "key": "pays",
                        "kind": "text",
                        "span": 1,
                        "label": "Pays",
                        "rules": {
                            "max": 40,
                            "min": 2,
                            "required": True
                        },
                        "placeholder": "France"
                    },
                    {
                        "key": "client_tel",
                        "kind": "text",
                        "span": 1,
                        "label": "Téléphone",
                        "rules": {
                            "max": 20,
                            "required": False,
                            "transform": "digits_only"
                        },
                        "advanced": True,
                        "placeholder": "06 12 34 56 78"
                    },
                    {
                        "key": "client_code",
                        "kind": "text",
                        "span": 1,
                        "label": "Code client",
                        "rules": {
                            "max": 20,
                            "required": False
                        },
                        "advanced": True,
                        "placeholder": "AA01454795"
                    }
                ]
            },
            {
                "title": "2. Vente en boutique",
                "fields": [
                    {
                        "key": "date_vente",
                        "kind": "date",
                        "span": 1,
                        "label": "Date de la vente",
                        "rules": {
                            "required": True
                        },
                        "dateFormat": "slash",
                        "placeholder": "05/09/2023"
                    },
                    {
                        "key": "heure_vente",
                        "kind": "time",
                        "span": 1,
                        "label": "Heure de la vente",
                        "rules": {
                            "required": True
                        },
                        "placeholder": "14:34"
                    },
                    {
                        "key": "facture_num",
                        "kind": "text",
                        "span": 1,
                        "label": "N° de facture",
                        "rules": {
                            "max": 20,
                            "min": 3,
                            "required": True
                        },
                        "placeholder": "735179"
                    },
                    {
                        "key": "conseiller",
                        "kind": "text",
                        "span": 1,
                        "label": "Conseiller de vente",
                        "rules": {
                            "max": 40,
                            "min": 2,
                            "required": True
                        },
                        "placeholder": "Amélie"
                    },
                    {
                        "key": "mode_paiement",
                        "kind": "select",
                        "span": 1,
                        "label": "Mode de règlement",
                        "rules": {
                            "max": 30,
                            "required": True
                        },
                        "options": [
                            {
                                "label": "Espèces Euros",
                                "value": "ESPECES EUROS"
                            },
                            {
                                "label": "Carte Bancaire",
                                "value": "CARTE BANCAIRE"
                            },
                            {
                                "label": "American Express",
                                "value": "AMERICAN EXPRESS"
                            },
                            {
                                "label": "Visa",
                                "value": "VISA"
                            },
                            {
                                "label": "Mastercard",
                                "value": "MASTERCARD"
                            }
                        ]
                    },
                    {
                        "key": "caisse_num",
                        "kind": "text",
                        "span": 1,
                        "label": "N° de caisse",
                        "rules": {
                            "max": 20,
                            "required": False
                        },
                        "advanced": True,
                        "placeholder": "AA1/AA105"
                    },
                    {
                        "key": "folio_num",
                        "kind": "text",
                        "span": 1,
                        "label": "N° de folio",
                        "rules": {
                            "max": 10,
                            "required": False
                        },
                        "advanced": True,
                        "placeholder": "1"
                    },
                    {
                        "key": "store_line_1",
                        "kind": "text",
                        "span": 1,
                        "label": "Adresse boutique",
                        "rules": {
                            "max": 60,
                            "required": False
                        },
                        "advanced": True,
                        "placeholder": "31 rue Cambon - 75001 PARIS"
                    },
                    {
                        "key": "store_line_2",
                        "kind": "text",
                        "span": 1,
                        "label": "Téléphone boutique",
                        "rules": {
                            "max": 40,
                            "required": False
                        },
                        "advanced": True,
                        "placeholder": "TEL : +33 (0) 1 44 50 66 00"
                    }
                ]
            },
            {
                "title": "3. Totaux & Taxes",
                "position": "after_items",
                "fields": [
                    {
                        "key": "total_ttc",
                        "kind": "text",
                        "span": 2,
                        "label": "Total TTC",
                        "rules": {
                            "max": 30,
                            "required": False
                        },
                        "placeholder": "132,00"
                    },
                    {
                        "key": "total_ht",
                        "kind": "text",
                        "span": 1,
                        "label": "Total HT",
                        "rules": {
                            "max": 30,
                            "required": False
                        },
                        "advanced": True,
                        "placeholder": "110,00"
                    },
                    {
                        "key": "total_tva",
                        "kind": "text",
                        "span": 1,
                        "label": "TVA (20%)",
                        "rules": {
                            "max": 30,
                            "required": False
                        },
                        "advanced": True,
                        "placeholder": "22,00"
                    }
                ]
            }
        ],
        "itemBlank": {
            "qty": "1",
            "ref": "",
            "desc": "",
            "total": "0,00",
            "unit_price": "0,00"
        },
        "itemColumns": [
            {
                "key": "desc",
                "label": "Désignation",
                "rules": {
                    "max": 60
                }
            },
            {
                "key": "ref",
                "label": "Référence",
                "rules": {
                    "max": 30
                }
            },
            {
                "key": "qty",
                "label": "Qté",
                "rules": {
                    "max": 10
                }
            },
            {
                "key": "unit_price",
                "label": "Prix Unitaire TTC",
                "rules": {
                    "max": 20
                }
            },
            {
                "key": "total",
                "label": "Montant TTC",
                "rules": {
                    "max": 20
                }
            }
        ],
        "itemsConfig": {
            "key": "items",
            "label": "Articles (3 maximum)",
            "columns": [
                {
                    "key": "desc",
                    "kind": "text",
                    "label": "Désignation",
                    "required": True
                },
                {
                    "key": "ref",
                    "kind": "text",
                    "label": "Référence",
                    "required": True
                },
                {
                    "key": "qty",
                    "kind": "text",
                    "label": "Qté",
                    "required": True
                },
                {
                    "key": "unit_price",
                    "kind": "text",
                    "label": "Prix Unitaire TTC",
                    "required": True
                },
                {
                    "key": "total",
                    "kind": "text",
                    "label": "Montant TTC",
                    "required": True
                }
            ],
            "enabled": True,
            "maxItems": 3,
            "blankItem": {
                "qty": "1",
                "ref": "",
                "desc": "",
                "total": "0,00",
                "unit_price": "0,00"
            }
        },
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
                    "label": "Logo Chanel",
                    "section": "header"
                },
                {
                    "id": "header_contact",
                    "label": "Coordonnées boutique",
                    "section": "header"
                },
                {
                    "id": "header_client",
                    "label": "Coordonnées client",
                    "section": "header"
                },
                {
                    "id": "header_meta",
                    "label": "Date, caisse et folio",
                    "section": "header"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture complet",
                    "master": True,
                    "section": "middle"
                },
                {
                    "id": "middle_accueil",
                    "label": "Accueil conseiller",
                    "section": "middle"
                },
                {
                    "id": "middle_table",
                    "label": "Tableau d'articles",
                    "section": "middle"
                },
                {
                    "id": "middle_totaux",
                    "label": "Bloc totaux et TVA",
                    "section": "middle"
                },
                {
                    "id": "middle_paiement",
                    "label": "Mode de paiement",
                    "section": "middle"
                },
                {
                    "id": "footer",
                    "label": "Pied de page",
                    "master": True,
                    "section": "footer"
                }
            ],
            "visible": {
                "footer": False,
                "header": True,
                "middle": True,
                "header_logo": True,
                "header_meta": True,
                "middle_table": True,
                "header_client": True,
                "middle_totaux": True,
                "header_contact": True,
                "middle_accueil": True,
                "middle_paiement": True
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
