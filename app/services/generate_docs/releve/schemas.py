from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field, field_validator

class ReleveLBPGenerateRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    mode: str = "facile"
    duree_mois: int = Field(1, ge=1, le=12)
    mois_debut: int = Field(1, ge=1, le=12)
    annee_debut: int = Field(2026, ge=2020, le=2035)
    numero_releve_debut: int = Field(1, ge=1)

    civilite: str = "M."
    nom: Optional[str] = "MARTIN"
    prenom: Optional[str] = "LUCAS"
    nom_prenom: Optional[str] = None
    adresse: str = "12 RUE DES FLEURS"
    complement_adresse: Optional[str] = None
    cp: str = "75011"
    ville: str = "PARIS"
    centre_financier: str = "PARIS CENTRE FINANCIER"

    identifiant: str = "1455835203"
    iban: str = "FR7620041010010012345678984"
    numero_compte: str = "00123456789"
    cle_compte: str = "84"
    bic: str = "PSSTFRPPPAR"
    card_number: str = "456"
    decouvert_autorise: str = "300,00"
    afficher_ccp: bool = True

    include_epargne: bool = False
    epargne_type: str = "LIVRET_A"
    epargne_nom: str = "Livret A"
    epargne_numero: str = "210 5436798 J"
    epargne_iban: str = "FR7610011000202105436798J51"
    epargne_bic: str = "PSSTFRPPCNE"
    epargne_solde_initial: Optional[str] = "5000,00"
    epargne_taux: Optional[str] = "3,00"
    epargne_nb_tx: int = Field(2, ge=0, le=10)
    epargne_comptes: Optional[List[Dict[str, Any]]] = None

    profil: str = "normal"
    wealth_profile: str = "moyen"
    solde_initial: str = "3450,00"
    nb_transactions_moyen: int = Field(14, ge=5, le=70)
    strict_zero_incident: bool = True

    salaire_net: Optional[str] = None
    employeur_nom: Optional[str] = None
    jour_salaire: Optional[int] = Field(28, ge=1, le=31)
    loyer_montant: Optional[str] = None
    loyer_bailleur: Optional[str] = None
    prelevements_selectionnes: Optional[List[str]] = None
    target_solde_final: Optional[str] = None
    contacts_virements: Optional[str] = None

    show_annexe_carbone: bool = True
    annexe_info_type: str = "auto"
    annexe_info_custom_text: Optional[str] = ""
    date_edition_custom: Optional[str] = None
    taux_decouvert: Optional[str] = "16,00"

    custom_transactions: Optional[List[Dict[str, Any]]] = None

    @field_validator("iban")
    @classmethod
    def validate_iban(cls, v: str) -> str:
        cleaned = v.replace(" ", "")
        if len(cleaned) < 15 or len(cleaned) > 34:
            raise ValueError("IBAN invalide (longueur incorrecte)")
        return v

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, v: str) -> str:
        if v not in ("facile", "personnalise"):
            raise ValueError("Mode invalide (seuls 'facile' et 'personnalise' sont autorisés)")
        return v

    @field_validator("profil")
    @classmethod
    def validate_profil(cls, v: str) -> str:
        allowed = ("normal", "locataire", "famille", "investisseur", "demandeur_credit", "fonctionnaire", "retraite", "artisan", "etudiant", "chomage", "independant")
        if v not in allowed:
            raise ValueError("Profil invalide")
        return v

    @field_validator("wealth_profile")
    @classmethod
    def validate_wealth_profile(cls, v: str) -> str:
        if v not in ("pauvre", "moyen", "riche"):
            raise ValueError("Profil de richesse invalide")
        return v

    @field_validator("custom_transactions")
    @classmethod
    def validate_custom_transactions(cls, v: Optional[List[Dict[str, Any]]]) -> Optional[List[Dict[str, Any]]]:
        if not v:
            return v
        validated_list = []
        for idx, tx in enumerate(v):
            if not isinstance(tx, dict):
                continue
            raw_montant = tx.get("montant") if tx.get("montant") is not None else tx.get("amount")
            if raw_montant is None:
                continue
            amt_str = str(raw_montant).replace("€", "").replace("¤", "").replace("+", "").replace(" ", "").replace(",", ".").strip()
            try:
                amt_val = float(amt_str)
            except ValueError:
                raise ValueError(f"Transaction #{idx + 1} : Montant invalide '{raw_montant}'")
            if amt_val <= 0:
                raise ValueError(f"Transaction #{idx + 1} : Le montant doit être supérieur à 0")

            signe = str(tx.get("signe", "-")).strip()
            if signe not in ("+", "-"):
                signe = "+" if signe == "credit" else "-"

            lib = str(tx.get("libelle") or tx.get("label") or "OPERATION SUR MESURE").strip()
            if not lib:
                lib = "OPERATION SUR MESURE"

            raw_date = str(tx.get("date", "15")).strip()
            if "/" in raw_date:
                day_p = raw_date.split("/")[0].strip()
            else:
                day_p = raw_date.strip()
            if not day_p.isdigit() or not (1 <= int(day_p) <= 31):
                day_p = "15"

            month_val = tx.get("month", 1)
            try:
                month_int = int(month_val)
                if not (1 <= month_int <= 12):
                    month_int = 1
            except Exception:
                month_int = 1

            is_all = tx.get("all_months") is True or str(tx.get("all_months")).lower() in ("true", "all", "1")

            validated_list.append({
                "id": str(tx.get("id", idx + 1)),
                "month": month_int,
                "all_months": is_all,
                "date": f"{int(day_p):02d}",
                "signe": signe,
                "montant": f"{amt_val:,.2f}".replace(",", " ").replace(".", ","),
                "amount": round(amt_val, 2),
                "libelle": lib.upper(),
                "type": str(tx.get("type") or ("VIREMENT" if signe == "+" else "ACHAT CB")).upper()
            })
        return validated_list
