import json
import logging
import time
from typing import Any, Optional, Dict
from fastapi import HTTPException

# =====================================================================

logger = logging.getLogger(__name__)

_SERVICES_CACHE: dict[str, dict] = {}
_SERVICES_CACHE_TTL = 30.0

GENERATE_DOCS_NEW_PRICES = {
    "adidas": 5.0,
    "amazon": 5.0,
    "fnac": 5.0,
    "nike": 5.0,
    "ami": 5.0,
    "burberry": 5.0,
    "cdiscount": 5.0,
    "dafy": 5.0,
    "darty": 5.0,
    "boulanger": 5.0,
    "gaz": 5.0,
    "loro_piana": 5.0,
    "pack_moto": 5.0,
    "dior": 5.0,
    "jacquemus": 5.0,
    "chanel": 5.0,
    "channel": 5.0,
    "fred": 5.0,
    "nocibe": 5.0,
    "sfr": 5.0,
    "conduite_heures": 5.0,
    "attestation_edf": 5.0,
    "attestation_direct_energie": 5.0,
    "axa": 5.0,
    "maxance": 5.0,
    "fiche_de_paie_1m": 8.0,
    "fiche_de_paie_3m": 20.0,
    "fiche_de_paie_6m": 40.0,
    "fiche_de_paie_12m": 60.0,
    "releve_lbp_1m": 8.0,
    "releve_lbp_3m": 20.0,
    "releve_lbp_6m": 40.0,
    "releve_lbp_12m": 60.0,
}

# =====================================================================

def invalidate_service_cache(service_slug: Optional[str] = None) -> None:
    global _SERVICES_CACHE
    if service_slug:
        _SERVICES_CACHE.pop(service_slug, None)
    else:
        _SERVICES_CACHE.clear()

# =====================================================================

def safe_parse_json(val: Any) -> dict:
    if not val:
        return {}
    if isinstance(val, dict):
        return val
    if isinstance(val, str):
        try:
            parsed = json.loads(val)
            if isinstance(parsed, str):
                return safe_parse_json(parsed)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}
    return {}

# =====================================================================

async def get_service_row_cached(db_pool: Any, service_slug: str, force_refresh: bool = False) -> Optional[dict]:
    now = time.time()
    cached = _SERVICES_CACHE.get(service_slug)
    if not force_refresh and cached and (now - cached["time"]) < _SERVICES_CACHE_TTL:
        return cached["row"]
    if not db_pool:
        return None
    try:
        async with db_pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id, prices, config, is_active FROM services WHERE slug = $1",
                service_slug
            )
            if row:
                res = {
                    "id": row["id"],
                    "prices": safe_parse_json(row["prices"]),
                    "config": safe_parse_json(row["config"]),
                    "is_active": bool(row["is_active"]),
                }
                _SERVICES_CACHE[service_slug] = {"row": res, "time": now}
                return res
            return None
    except Exception:
        if cached:
            return cached["row"]
        raise

# =====================================================================

async def get_service_price(db_pool: Any, service_slug: str, action_type: str) -> tuple[float, Any]:
    svc = await get_service_row_cached(db_pool, service_slug)
    if not svc or not svc.get("is_active"):
        raise HTTPException(status_code=400, detail="Service actif introuvable")

    prices_dict = svc["prices"]

    if action_type not in prices_dict:
        if action_type == "fiche_de_paie" and "fiche_de_paie_1m" in prices_dict:
            return float(prices_dict["fiche_de_paie_1m"]), svc["id"]
        if service_slug == "generate-docs" and action_type in GENERATE_DOCS_NEW_PRICES:
            return float(GENERATE_DOCS_NEW_PRICES[action_type]), svc["id"]
        raise HTTPException(
            status_code=400,
            detail=f"Option de facturation '{action_type}' non configurée pour ce service"
        )

    return float(prices_dict[action_type]), svc["id"]

# =====================================================================

async def check_subcategory_permission(
    db_pool: Any,
    service_slug: str,
    subcategory: str,
    user_role: Optional[str] = None
) -> bool:
    svc = await get_service_row_cached(db_pool, service_slug)
    if not svc or not svc.get("is_active"):
        raise HTTPException(
            status_code=403,
            detail="Le service de génération de documents est actuellement indisponible"
        )

    raw_config = svc.get("config", {})
    subcategories = raw_config.get("subcategories", {})
    sub_info = subcategories.get(subcategory)

    if sub_info:
        is_sub_active = sub_info.get("active", sub_info.get("enabled", True))
        if not is_sub_active:
            raise HTTPException(
                status_code=403,
                detail=f"La sous-catégorie '{subcategory}' est actuellement indisponible"
            )

    return True

# =====================================================================

async def refund_balance(
    db_pool: Any,
    email: str,
    service_slug: str,
    action_type: str,
    quantity_to_refund: int,
    metadata: Optional[Dict[str, Any]] = None
) -> float:
    if quantity_to_refund <= 0:
        return 0.0

    unit_price, service_id = await get_service_price(db_pool, service_slug, action_type)
    refund_amount = unit_price * quantity_to_refund

    async with db_pool.acquire() as conn:
        async with conn.transaction():
            user = None
            ident = str(email).strip()
            if ident.isdigit():
                user = await conn.fetchrow("SELECT id, balance FROM users WHERE id = $1 FOR UPDATE", int(ident))
            if not user:
                user = await conn.fetchrow("SELECT id, balance FROM users WHERE username = $1 FOR UPDATE", ident)
            if not user:
                return 0.0

            new_balance = float(user["balance"]) + refund_amount
            await conn.execute("UPDATE users SET balance = $1, updated_at = NOW() WHERE id = $2", new_balance, user["id"])

            meta_json = json.dumps(metadata or {})
            cat = metadata.get("category", service_slug) if metadata else service_slug
            slug_v = metadata.get("slug", action_type) if metadata else action_type

            await conn.execute(
                """INSERT INTO generations (user_id, category, slug, cost, status, metadata, created_at)
                   VALUES ($1, $2, $3, $4, 'REFUNDED', $5, NOW())""",
                user["id"],
                cat,
                slug_v,
                -refund_amount,
                meta_json
            )

            logger.info(f"[BILLING] Refunded {refund_amount:.2f} € to user {user['id']} for {service_slug}:{action_type}")
            return new_balance

# =====================================================================

async def verify_and_deduct_balance(
    db_pool: Any,
    email: str,
    service_slug: str,
    action_type: str,
    quantity: int,
    metadata: Optional[Dict[str, Any]] = None,
    user_role: str = "USER"
) -> float:
    if quantity <= 0:
        return 0.0

    if service_slug == "generate-docs":
        if action_type in ("maxance", "axa"):
            subcat = "assurance"
        elif action_type.startswith("releve") or action_type.endswith("releve"):
            subcat = "releve"
        elif action_type.startswith("fiche_de_paie"):
            subcat = "emploi"
        elif action_type in (
            "adidas", "amazon", "boulanger", "fnac", "nike", "ami", "burberry",
            "cdiscount", "dafy", "darty", "gaz", "loro_piana", "pack_moto", "dior", "jacquemus",
            "chanel", "channel", "fred", "nocibe", "sfr"
        ):
            subcat = "facture"
        elif action_type in ("conduite_heures", "attestation_edf", "attestation_direct_energie"):
            subcat = "justificatif"
        else:
            subcat = "rib"
        await check_subcategory_permission(db_pool, service_slug, subcat, user_role=user_role)

    unit_price, service_id = await get_service_price(db_pool, service_slug, action_type)
    total_cost = unit_price * quantity

    async with db_pool.acquire() as conn:
        async with conn.transaction():
            user = None
            ident = str(email).strip()
            if ident.isdigit():
                user = await conn.fetchrow("SELECT id, balance, is_banned FROM users WHERE id = $1 FOR UPDATE", int(ident))
            if not user:
                user = await conn.fetchrow("SELECT id, balance, is_banned FROM users WHERE username = $1 FOR UPDATE", ident)
            if not user:
                raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

            if user["is_banned"]:
                raise HTTPException(status_code=403, detail="Compte utilisateur banni")

            current_balance = float(user["balance"])
            if current_balance < total_cost:
                raise HTTPException(
                    status_code=402,
                    detail=f"Solde insuffisant. Requis: {total_cost:.2f} €, Actuel: {current_balance:.2f} €"
                )

            new_balance = current_balance - total_cost

            await conn.execute(
                "UPDATE users SET balance = $1, updated_at = NOW() WHERE id = $2",
                new_balance,
                user["id"]
            )

            meta_json = json.dumps(metadata or {})
            cat = metadata.get("category", service_slug) if metadata else service_slug
            slug_v = metadata.get("slug", action_type) if metadata else action_type

            await conn.execute(
                """INSERT INTO generations (user_id, category, slug, cost, status, metadata, created_at)
                   VALUES ($1, $2, $3, $4, 'COMPLETED', $5, NOW())""",
                user["id"],
                cat,
                slug_v,
                total_cost,
                meta_json
            )

            logger.info(f"[BILLING] Debited {total_cost:.2f} € from user {user['id']} for {service_slug}:{action_type}")
            return new_balance
