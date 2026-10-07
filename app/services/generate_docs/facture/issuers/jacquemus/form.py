def get_form_schema() -> dict:
    return {
        "version": 3,
        "defaults": {
            "cp": "75011",
            "nom": "Martin",
            "items": [
                {
                    "nom": "Le pichoto",
                    "qte": "1",
                    "ref": "213BA01-213",
                    "pays": "Italie",
                    "prix": "€360.00",
                    "taille": "Unique",
                    "couleur": "Noir",
                    "sous_total": "€360.00"
                }
            ],
            "ville": "Paris",
            "prenom": "Lucas",
            "adresse": "12 Rue des Fleurs",
            "tot_tva": "€60.00",
            "tot_total": "€360.00",
            "client_tel": "06 12 34 56 78",
            "complement": "",
            "client_pays": "France",
            "val_facture": "48949848",
            "val_payment": "Carte Bancaire",
            "val_commande": "20541994",
            "val_delivery": "United Parcel Service - UPS Standard",
            "contact_email": "boutique@jacquemus.com",
            "date_commande": "13 mai 2024",
            "tot_livraison": "GRATUIT",
            "heure_commande": "14:26",
            "tot_sous_total": "€300.00"
        },
        "metadata": {
            "logo": "/logos/jacquemus.svg",
            "title": "Jacquemus",
            "apiBase": "/api/generate-docs/facture/jacquemus",
            "itemKey": "items",
            "backHref": "/services/generate-docs/facture",
            "headerBg": "bg-white border-neutral-800/30",
            "maxItems": 4,
            "priceKey": "jacquemus",
            "subtitle": "Facture commande en ligne Jacquemus",
            "backLabel": "Retour aux factures",
            "itemLabel": "Articles",
            "logoClass": "scale-[0.70] md:scale-[0.75]",
            "generateLabel": "Générer la facture Jacquemus",
            "filenameTemplate": "Facture_Jacquemus.pdf"
        },
        "sections": [
            {
                "title": "1. Coordonnées client",
                "fields": [
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
                        "label": "Adresse (rue)",
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
                        "key": "client_tel",
                        "kind": "text",
                        "span": 1,
                        "label": "Téléphone",
                        "rules": {
                            "max": 20,
                            "min": 10,
                            "required": True,
                            "transform": "digits_only"
                        },
                        "placeholder": "06 12 34 56 78"
                    },
                    {
                        "key": "client_pays",
                        "kind": "country",
                        "span": 1,
                        "label": "Pays",
                        "rules": {
                            "max": 30,
                            "min": 2,
                            "required": True
                        },
                        "advanced": True
                    },
                    {
                        "key": "complement",
                        "kind": "text",
                        "span": 2,
                        "label": "Complément d'adresse",
                        "rules": {
                            "max": 60,
                            "required": False
                        },
                        "advanced": True
                    }
                ]
            },
            {
                "title": "2. Références de commande",
                "fields": [
                    {
                        "key": "val_commande",
                        "kind": "text",
                        "span": 1,
                        "label": "N° de commande",
                        "rules": {
                            "max": 30,
                            "min": 3,
                            "required": True
                        }
                    },
                    {
                        "key": "val_facture",
                        "kind": "text",
                        "span": 1,
                        "label": "N° de facture",
                        "rules": {
                            "max": 30,
                            "min": 3,
                            "required": True
                        }
                    },
                    {
                        "key": "date_commande",
                        "kind": "date",
                        "span": 1,
                        "label": "Date de la commande",
                        "rules": {
                            "required": True
                        },
                        "dateFormat": "french_short",
                        "placeholder": "13 sept. 2024"
                    },
                    {
                        "key": "heure_commande",
                        "kind": "time",
                        "span": 1,
                        "label": "Heure de la commande",
                        "rules": {
                            "required": True
                        },
                        "placeholder": "14:26"
                    },
                    {
                        "key": "val_payment",
                        "kind": "select",
                        "span": 1,
                        "label": "Méthode de paiement",
                        "rules": {
                            "max": 100,
                            "required": True
                        },
                        "options": [
                            {
                                "label": "Carte Bancaire",
                                "value": "Carte Bancaire"
                            },
                            {
                                "label": "Paiement en 3 fois sans frais",
                                "value": "Paiement en 3 fois sans frais"
                            },
                            {
                                "label": "PayPal",
                                "value": "PayPal"
                            },
                            {
                                "label": "Apple Pay",
                                "value": "Apple Pay"
                            },
                            {
                                "label": "Visa / Mastercard",
                                "value": "Visa / Mastercard"
                            }
                        ]
                    },
                    {
                        "key": "val_delivery",
                        "kind": "select",
                        "span": 1,
                        "label": "Mode de livraison",
                        "rules": {
                            "max": 100,
                            "required": True
                        },
                        "options": [
                            {
                                "label": "United Parcel Service - UPS Standard",
                                "value": "United Parcel Service - UPS Standard"
                            },
                            {
                                "label": "DHL Express",
                                "value": "DHL Express"
                            },
                            {
                                "label": "Colissimo International",
                                "value": "Colissimo International"
                            },
                            {
                                "label": "Chronopost Express",
                                "value": "Chronopost Express"
                            }
                        ]
                    }
                ]
            },
            {
                "title": "3. Totaux & Taxes",
                "position": "after_items",
                "fields": [
                    {
                        "key": "tot_sous_total",
                        "kind": "text",
                        "span": 1,
                        "label": "Sous-total (€)",
                        "rules": {
                            "max": 40,
                            "required": True
                        },
                        "advanced": True
                    },
                    {
                        "key": "tot_tva",
                        "kind": "text",
                        "span": 1,
                        "label": "TVA (20%)",
                        "rules": {
                            "max": 40,
                            "required": True
                        },
                        "advanced": True
                    },
                    {
                        "key": "tot_livraison",
                        "kind": "text",
                        "span": 1,
                        "label": "Frais de livraison",
                        "rules": {
                            "max": 40,
                            "required": True
                        },
                        "advanced": True
                    },
                    {
                        "key": "tot_total",
                        "kind": "text",
                        "span": 1,
                        "label": "Total TTC (€)",
                        "rules": {
                            "max": 40,
                            "required": True
                        }
                    }
                ]
            }
        ],
        "itemBlank": {
            "nom": "",
            "qte": "1",
            "ref": "",
            "pays": "",
            "prix": "€0.00",
            "taille": "",
            "couleur": "",
            "sous_total": "€0.00"
        },
        "itemColumns": [
            {
                "key": "nom",
                "label": "Désignation",
                "rules": {
                    "max": 50
                }
            },
            {
                "key": "ref",
                "label": "Réf / SKU",
                "rules": {
                    "max": 30
                }
            },
            {
                "key": "couleur",
                "label": "Couleur",
                "rules": {
                    "max": 30
                }
            },
            {
                "key": "taille",
                "label": "Taille",
                "rules": {
                    "max": 20
                }
            },
            {
                "key": "pays",
                "label": "Origine",
                "rules": {
                    "max": 30
                }
            },
            {
                "key": "prix",
                "label": "Prix unitaire",
                "rules": {
                    "max": 20
                }
            },
            {
                "key": "qte",
                "label": "Qté",
                "rules": {
                    "max": 10
                }
            },
            {
                "key": "sous_total",
                "label": "Sous-total",
                "rules": {
                    "max": 20
                }
            }
        ],
        "itemsConfig": {
            "key": "items",
            "label": "Articles (4 maximum)",
            "columns": [
                {
                    "key": "nom",
                    "kind": "text",
                    "label": "Désignation",
                    "required": True
                },
                {
                    "key": "ref",
                    "kind": "text",
                    "label": "Réf / SKU",
                    "required": False
                },
                {
                    "key": "couleur",
                    "kind": "text",
                    "label": "Couleur",
                    "required": False
                },
                {
                    "key": "taille",
                    "kind": "text",
                    "label": "Taille",
                    "required": False
                },
                {
                    "key": "pays",
                    "kind": "text",
                    "label": "Origine",
                    "required": False
                },
                {
                    "key": "prix",
                    "kind": "text",
                    "label": "Prix unitaire",
                    "required": True
                },
                {
                    "key": "qte",
                    "kind": "text",
                    "label": "Qté",
                    "required": True
                },
                {
                    "key": "sous_total",
                    "kind": "text",
                    "label": "Sous-total",
                    "required": True
                }
            ],
            "enabled": True,
            "maxItems": 4,
            "blankItem": {
                "nom": "",
                "qte": "1",
                "ref": "",
                "pays": "",
                "prix": "€0.00",
                "taille": "",
                "couleur": "",
                "sous_total": "€0.00"
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
                    "label": "Logo Jacquemus",
                    "section": "header"
                },
                {
                    "id": "header_contact",
                    "label": "Email contact boutique",
                    "section": "header"
                },
                {
                    "id": "header_client",
                    "label": "Adresse et coordonnées client",
                    "section": "header"
                },
                {
                    "id": "header_meta",
                    "label": "Références commande & date",
                    "section": "header"
                },
                {
                    "id": "middle",
                    "label": "Corps de facture complet",
                    "master": True,
                    "section": "middle"
                },
                {
                    "id": "middle_payment",
                    "label": "Bloc méthode de paiement",
                    "section": "middle"
                },
                {
                    "id": "middle_delivery",
                    "label": "Bloc mode de livraison",
                    "section": "middle"
                },
                {
                    "id": "middle_table",
                    "label": "En-tête du tableau d'articles",
                    "section": "middle"
                },
                {
                    "id": "middle_rows",
                    "label": "Lignes d'articles",
                    "section": "middle"
                },
                {
                    "id": "middle_totals",
                    "label": "Bloc totaux et TVA",
                    "section": "middle"
                },
                {
                    "id": "footer",
                    "label": "Pied de page complet",
                    "master": True,
                    "section": "footer"
                },
                {
                    "id": "footer_legal",
                    "label": "Mentions légales société",
                    "section": "footer"
                },
                {
                    "id": "footer_notice",
                    "label": "Déclaration douanière d'exportation",
                    "section": "footer"
                }
            ],
            "visible": {
                "footer": True,
                "header": True,
                "middle": True,
                "header_logo": True,
                "header_meta": True,
                "middle_rows": True,
                "footer_legal": True,
                "middle_table": True,
                "footer_notice": True,
                "header_client": True,
                "middle_totals": True,
                "header_contact": True,
                "middle_payment": True,
                "middle_delivery": True
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
