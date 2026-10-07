def get_form_schema() -> dict:
    return {
        "metadata": {
            "slug": "nocibe",
            "title": "Nocibé",
            "subtitle": "Générateur de facture Nocibé",
            "logo": "/logos/nocibe.svg",
            "headerBg": "bg-white border-pink-500/30",
            "logoClass": "scale-100 md:scale-105",
            "priceKey": "nocibe",
            "itemKey": "items",
            "itemLabel": "5. Articles",
            "maxItems": 3,
            "apiBase": "/api/generate-docs/facture/nocibe",
            "backHref": "/services/generate-docs/facture",
            "backLabel": "Retour aux factures",
            "filenameTemplate": "Facture_Nocibe.pdf",
            "generateLabel": "Générer la facture Nocibé",
            "version": 3
        },
        "defaults": {
            "header": True,
            "header_logo": True,
            "header_titre": True,
            "facture_num": "27414163",
            "date_emission": "23/08/2023",
            "header_facturation": True,
            "nom": "Martin",
            "prenom": "Lucas",
            "adresse": "12 Rue des Fleurs",
            "cp": "75011",
            "ville": "Paris",
            "pays": "FR",
            "header_livraison": True,
            "livraison_nom": "Martin",
            "livraison_prenom": "Lucas",
            "livraison_adresse": "12 Rue des Fleurs",
            "livraison_cp": "75011",
            "livraison_ville": "Paris",
            "livraison_pays": "FR",
            "header_commande": True,
            "commande_date": "23/08/2023",
            "commande_mode": "Click & Collect",
            "commande_expedition": "23/08/2023",
            "middle": True,
            "middle_table": True,
            "middle_totals": True,
            "middle_details": True,
            "items": [
                {
                    "ref": "222876",
                    "desc": "Sauvage - Parfum pour homme - Notes santal & fève tonka - 100ml",
                    "tva_rate": "20.00",
                    "qty": "1",
                    "unit_price": "91.25",
                    "remise": "0.00",
                    "remise_code": "",
                    "net_ht": "91.25"
                }
            ],
            "total_ttc": "109.50",
            "reglement_date": "23/08/2023",
            "reglement_mode": "Carte Bleue"
        },
        "sections": [
            {
                "title": "1. Facturation",
                "fields": [
                    {
                        "key": "nom",
                        "kind": "text",
                        "span": 1,
                        "label": "Nom",
                        "rules": {
                            "min": 2,
                            "max": 35,
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
                            "min": 2,
                            "max": 35,
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
                            "min": 4,
                            "max": 80,
                            "required": True
                        },
                        "placeholder": "12 Rue des Fleurs",
                        "autocompleteType": "address"
                    },
                    {
                        "key": "cp",
                        "kind": "text",
                        "span": 1,
                        "label": "Code postal",
                        "rules": {
                            "min": 4,
                            "max": 10,
                            "required": True
                        },
                        "placeholder": "75011",
                        "autocompleteType": "postal-code"
                    },
                    {
                        "key": "ville",
                        "kind": "text",
                        "span": 1,
                        "label": "Ville",
                        "rules": {
                            "min": 2,
                            "max": 40,
                            "required": True
                        },
                        "placeholder": "Paris",
                        "autocompleteType": "city"
                    },
                    {
                        "key": "pays",
                        "kind": "text",
                        "span": 2,
                        "label": "Pays",
                        "rules": {
                            "min": 2,
                            "max": 30,
                            "required": False
                        },
                        "placeholder": "FR",
                        "advanced": True
                    }
                ]
            },
            {
                "title": "2. Livraison",
                "fields": [
                    {
                        "key": "livraison_nom",
                        "kind": "text",
                        "span": 1,
                        "label": "Nom",
                        "rules": {
                            "min": 2,
                            "max": 35,
                            "required": True
                        },
                        "placeholder": "Martin"
                    },
                    {
                        "key": "livraison_prenom",
                        "kind": "text",
                        "span": 1,
                        "label": "Prénom",
                        "rules": {
                            "min": 2,
                            "max": 35,
                            "required": True
                        },
                        "placeholder": "Lucas"
                    },
                    {
                        "key": "livraison_adresse",
                        "kind": "text",
                        "span": 2,
                        "label": "Adresse",
                        "rules": {
                            "min": 4,
                            "max": 80,
                            "required": True
                        },
                        "placeholder": "12 Rue des Fleurs",
                        "autocompleteType": "address"
                    },
                    {
                        "key": "livraison_cp",
                        "kind": "text",
                        "span": 1,
                        "label": "Code postal",
                        "rules": {
                            "min": 4,
                            "max": 10,
                            "required": True
                        },
                        "placeholder": "75011",
                        "autocompleteType": "postal-code"
                    },
                    {
                        "key": "livraison_ville",
                        "kind": "text",
                        "span": 1,
                        "label": "Ville",
                        "rules": {
                            "min": 2,
                            "max": 40,
                            "required": True
                        },
                        "placeholder": "Paris",
                        "autocompleteType": "city"
                    },
                    {
                        "key": "livraison_pays",
                        "kind": "text",
                        "span": 2,
                        "label": "Pays",
                        "rules": {
                            "min": 2,
                            "max": 30,
                            "required": False
                        },
                        "placeholder": "FR",
                        "advanced": True
                    }
                ]
            },
            {
                "title": "3. Commande & Facture",
                "fields": [
                    {
                        "key": "facture_num",
                        "kind": "text",
                        "span": 1,
                        "label": "N° de facture",
                        "rules": {
                            "min": 2,
                            "max": 20,
                            "required": True
                        },
                        "placeholder": "27414163"
                    },
                    {
                        "key": "date_emission",
                        "kind": "date",
                        "dateFormat": "slash",
                        "span": 1,
                        "label": "Date d'émission",
                        "rules": {
                            "required": True
                        },
                        "placeholder": "JJ/MM/AAAA"
                    },
                    {
                        "key": "commande_date",
                        "kind": "date",
                        "dateFormat": "slash",
                        "span": 1,
                        "label": "Date de commande",
                        "rules": {
                            "required": True
                        },
                        "placeholder": "JJ/MM/AAAA"
                    },
                    {
                        "key": "commande_mode",
                        "kind": "text",
                        "span": 1,
                        "label": "Mode de livraison",
                        "rules": {
                            "min": 2,
                            "max": 50,
                            "required": True
                        },
                        "placeholder": "Click & Collect"
                    },
                    {
                        "key": "commande_expedition",
                        "kind": "date",
                        "dateFormat": "slash",
                        "span": 1,
                        "label": "Date d'expédition / retrait",
                        "rules": {
                            "required": False
                        },
                        "advanced": True,
                        "placeholder": "JJ/MM/AAAA"
                    }
                ]
            },
            {
                "title": "4. Totaux & Règlement",
                "position": "after_items",
                "fields": [
                    {
                        "key": "total_ttc",
                        "kind": "text",
                        "span": 1,
                        "label": "Total TTC (€)",
                        "rules": {
                            "max": 20,
                            "required": True
                        },
                        "placeholder": "109.50"
                    },
                    {
                        "key": "reglement_mode",
                        "kind": "select",
                        "span": 1,
                        "label": "Mode de règlement",
                        "rules": {
                            "max": 30,
                            "required": True
                        },
                        "options": [
                            {
                                "label": "Carte Bleue",
                                "value": "Carte Bleue"
                            },
                            {
                                "label": "Carte Bancaire",
                                "value": "Carte Bancaire"
                            },
                            {
                                "label": "Visa",
                                "value": "Visa"
                            },
                            {
                                "label": "Mastercard",
                                "value": "Mastercard"
                            },
                            {
                                "label": "PayPal",
                                "value": "PayPal"
                            }
                        ]
                    },
                    {
                        "key": "reglement_date",
                        "kind": "date",
                        "dateFormat": "slash",
                        "span": 1,
                        "label": "Date du règlement",
                        "rules": {
                            "required": True
                        },
                        "placeholder": "JJ/MM/AAAA"
                    }
                ]
            }
        ],
        "itemsConfig": {
            "key": "items",
            "label": "5. Articles (3 maximum)",
            "enabled": True,
            "maxItems": 3,
            "blankItem": {
                "qty": "1",
                "ref": "",
                "desc": "",
                "net_ht": "0.00",
                "remise": "0.00",
                "tva_rate": "20.00",
                "unit_price": "0.00",
                "remise_code": ""
            },
            "columns": [
                {
                    "key": "ref",
                    "kind": "text",
                    "label": "Réf. article",
                    "required": True,
                    "placeholder": "222876"
                },
                {
                    "key": "desc",
                    "kind": "text",
                    "label": "Désignation",
                    "required": True,
                    "placeholder": "Sauvage - Parfum..."
                },
                {
                    "key": "qty",
                    "kind": "text",
                    "label": "Qté",
                    "required": True,
                    "placeholder": "1"
                },
                {
                    "key": "unit_price",
                    "kind": "text",
                    "label": "Prix Brut HT",
                    "required": True,
                    "placeholder": "91.25"
                },
                {
                    "key": "remise",
                    "kind": "text",
                    "label": "Remise HT",
                    "required": False,
                    "advanced": True,
                    "placeholder": "0.00"
                },
                {
                    "key": "remise_code",
                    "kind": "text",
                    "label": "Code remise",
                    "required": False,
                    "advanced": True,
                    "placeholder": "Ex: 25%..."
                },
                {
                    "key": "tva_rate",
                    "kind": "text",
                    "label": "Taux TVA %",
                    "required": False,
                    "advanced": True,
                    "placeholder": "20.00"
                }
            ]
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
                    "label": "Logo Nocibé",
                    "section": "header"
                },
                {
                    "id": "header_titre",
                    "label": "N° et date de facture",
                    "section": "header"
                },
                {
                    "id": "header_facturation",
                    "label": "Adresse de facturation",
                    "section": "header"
                },
                {
                    "id": "header_livraison",
                    "label": "Adresse de livraison",
                    "section": "header"
                },
                {
                    "id": "header_commande",
                    "label": "Bloc commande & expédition",
                    "section": "header"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture complet",
                    "master": True,
                    "section": "middle"
                },
                {
                    "id": "middle_table",
                    "label": "Tableau des articles",
                    "section": "middle"
                },
                {
                    "id": "middle_totals",
                    "label": "Bloc des totaux",
                    "section": "middle"
                },
                {
                    "id": "middle_details",
                    "label": "Détails TVA et règlements",
                    "section": "middle"
                }
            ],
            "visible": {
                "header": True,
                "header_logo": True,
                "header_titre": True,
                "header_facturation": True,
                "header_livraison": True,
                "header_commande": True,
                "middle": True,
                "middle_table": True,
                "middle_totals": True,
                "middle_details": True
            },
            "sections": [
                {
                    "id": "header",
                    "label": "En-tête"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture"
                }
            ]
        }
    }
