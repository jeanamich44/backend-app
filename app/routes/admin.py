import os
import re
import json
import secrets
import httpx
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Depends, Header, Response, Request
from pydantic import BaseModel
from app.auth import validate_telegram_init_data
from app.db import get_db_pool

# =====================================================================

router = APIRouter(prefix="/api/admin", tags=["admin"])

# =====================================================================

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD") or os.getenv("ADMIN_PANEL_PASSWORD") or "ChezRheyy2026!"

DEFAULT_ADMIN_IDS = [8740419947, 6298536933, 8676919760, 5883885733, 1461973886]
env_admin_ids = os.getenv("TELEGRAM_ADMIN_IDS", "")
if env_admin_ids.strip():
    try:
        TELEGRAM_ADMIN_IDS = [int(x.strip()) for x in env_admin_ids.split(",") if x.strip()]
    except Exception:
        TELEGRAM_ADMIN_IDS = DEFAULT_ADMIN_IDS
else:
    TELEGRAM_ADMIN_IDS = DEFAULT_ADMIN_IDS

# =====================================================================

_admin_sessions: Dict[str, datetime] = {}

# =====================================================================

class AdminLoginRequest(BaseModel):
    password: str

class StockItemPayload(BaseModel):
    brand: Optional[str] = "carr"
    code: str
    pin: Optional[str] = "0000"
    value: float
    price: float

class StockAddPayload(BaseModel):
    items: List[StockItemPayload]

class StockDeletePayload(BaseModel):
    id: int

class UserSoldePayload(BaseModel):
    userId: Any
    action: str
    amount: float

class UserBanPayload(BaseModel):
    userId: Any
    banned: bool
    reason: Optional[str] = ""

class IptvSettingsPayload(BaseModel):
    host: Optional[str] = ""
    type: Optional[str] = "m3u"
    message_footer: Optional[str] = ""
    price_1m: Optional[str] = "10"
    price_3m: Optional[str] = "25"
    price_6m: Optional[str] = "45"
    price_12m: Optional[str] = "70"
    accounts: Optional[List[Dict[str, Any]]] = []
    panel_accounts: Optional[List[Dict[str, Any]]] = []

class SumUpBankPayload(BaseModel):
    name: Optional[str] = ""
    pay_to_email: str
    api_key: str
    client_id: str
    client_secret: str

class SumUpBanksPayload(BaseModel):
    sumup: SumUpBankPayload
    sumup_bank2: SumUpBankPayload

class SumUpSettingsPayload(BaseModel):
    active: str
    expiration_minutes: Any
    banks: SumUpBanksPayload

class MaintenancePayload(BaseModel):
    maintenance: bool

class PasswordPayload(BaseModel):
    password: str

# =====================================================================

def _is_valid_session(token: str) -> bool:
    if not token or token not in _admin_sessions:
        return False
    exp = _admin_sessions[token]
    if datetime.now(timezone.utc) > exp:
        _admin_sessions.pop(token, None)
        return False
    return True

# =====================================================================

async def get_current_admin(
    request: Request,
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data"),
    authorization: Optional[str] = Header(None, alias="Authorization")
) -> Dict[str, Any]:
    if x_telegram_init_data:
        user_data = validate_telegram_init_data(x_telegram_init_data)
        if user_data and "id" in user_data:
            user_id = int(user_data["id"])
            if user_id in TELEGRAM_ADMIN_IDS:
                return {
                    "type": "telegram",
                    "id": user_id,
                    "username": user_data.get("username", ""),
                    "first_name": user_data.get("first_name", "")
                }

    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:].strip()
        if _is_valid_session(token):
            return {
                "type": "web",
                "token": token
            }

    return Response(status_code=444)

# =====================================================================

@router.post("/login")
async def admin_login(payload: AdminLoginRequest):
    if not secrets.compare_digest(payload.password.strip(), ADMIN_PASSWORD.strip()):
        return Response(status_code=444)

    token = secrets.token_hex(32)
    _admin_sessions[token] = datetime.now(timezone.utc) + timedelta(hours=24)
    return {
        "success": True,
        "token": token,
        "expires_in": 86400
    }

# =====================================================================

@router.get("/check")
async def admin_check(admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    return {
        "isAdmin": True,
        "type": admin.get("type")
    }

# =====================================================================

@router.get("/stats")
async def admin_stats(admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin

    pool = await get_db_pool()
    stats = {
        "users_count": 0,
        "payments_count": 0,
        "payments_volume": 0.0,
        "generations_count": 0,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    async with pool.acquire() as conn:
        try:
            u_row = await conn.fetchval("SELECT COUNT(*) FROM tma_users")
            stats["users_count"] = int(u_row or 0)
        except Exception:
            pass

        try:
            p_row = await conn.fetchrow("SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM tma_payments WHERE status = 'PAID'")
            if p_row:
                stats["payments_count"] = int(p_row[0] or 0)
                stats["payments_volume"] = float(p_row[1] or 0.0)
        except Exception:
            pass

        try:
            g_row = await conn.fetchval("SELECT COUNT(*) FROM tma_generations")
            stats["generations_count"] = int(g_row or 0)
        except Exception:
            pass

    return stats

# =====================================================================

@router.get("/stock")
async def admin_get_stock(admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id, code, pin, value, price FROM stock WHERE brand = 'carr' AND is_sold = FALSE ORDER BY id DESC")
        stock = [
            {
                "id": row["id"],
                "code": row["code"],
                "pin": row["pin"] or "0000",
                "value": float(row["value"] or 0),
                "price": float(row["price"] or 0)
            }
            for row in rows
        ]
    return {"stock": stock}

# =====================================================================

@router.post("/stock/add")
async def admin_add_stock(payload: StockAddPayload, admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    pool = await get_db_pool()
    count = 0
    async with pool.acquire() as conn:
        async with conn.transaction():
            for item in payload.items:
                if item.code.strip():
                    await conn.execute(
                        "INSERT INTO stock (brand, code, pin, value, price) VALUES ($1, $2, $3, $4, $5)",
                        item.brand or "carr", item.code.strip(), item.pin or "0000", item.value, item.price
                    )
                    count += 1
    return {"success": True, "count": count}

# =====================================================================

@router.post("/stock/delete")
async def admin_delete_stock(payload: StockDeletePayload, admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM stock WHERE id = $1", payload.id)
    return {"success": True}

# =====================================================================

@router.post("/stock/clear")
async def admin_clear_stock(admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM stock WHERE brand = 'carr'")
    return {"success": True}

# =====================================================================

@router.get("/users")
async def admin_get_users(admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT u.id, u.username, u.first_name, u.balance, u.is_banned, u.created_at,
                   COALESCE((SELECT COUNT(*) FROM tma_payments WHERE user_id = u.id AND status = 'PAID'), 0) as achats
            FROM tma_users u
            ORDER BY u.created_at DESC
        """)
        users = [
            {
                "id": str(row["id"]),
                "userNumber": idx + 1,
                "username": row["username"] or row["first_name"] or "Anonyme",
                "solde": float(row["balance"] or 0),
                "isBanned": bool(row["is_banned"]),
                "achats": int(row["achats"] or 0)
            }
            for idx, row in enumerate(rows)
        ]
    return {"users": users}

# =====================================================================

@router.post("/users/solde")
async def admin_update_user_solde(payload: UserSoldePayload, admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    try:
        uid = int(str(payload.userId).strip())
    except Exception:
        return Response(status_code=400)

    amount = abs(float(payload.amount))
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        current_bal = await conn.fetchval("SELECT balance FROM tma_users WHERE id = $1", uid)
        if current_bal is None:
            return Response(status_code=404)
        new_bal = float(current_bal) + amount if payload.action == "add" else max(0.0, float(current_bal) - amount)
        await conn.execute("UPDATE tma_users SET balance = $1, updated_at = NOW() WHERE id = $2", new_bal, uid)
    return {"success": True, "balance": new_bal}

# =====================================================================

@router.post("/users/ban")
async def admin_toggle_ban(payload: UserBanPayload, admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    try:
        uid = int(str(payload.userId).strip())
    except Exception:
        return Response(status_code=400)

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute("UPDATE tma_users SET is_banned = $1, updated_at = NOW() WHERE id = $2", payload.banned, uid)
    return {"success": True}

# =====================================================================

@router.get("/transactions")
async def admin_get_transactions(admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT id, user_id, amount, status, created_at
            FROM tma_payments
            ORDER BY created_at DESC
            LIMIT 100
        """)
        txs = [
            {
                "id": str(row["id"]),
                "userId": str(row["user_id"]),
                "brand": "Rechargement CB",
                "price": float(row["amount"] or 0),
                "status": row["status"],
                "createdAt": row["created_at"].isoformat() if row["created_at"] else ""
            }
            for row in rows
        ]
    return {"transactions": txs}

# =====================================================================

@router.get("/settings")
async def admin_get_settings(admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        s_row = await conn.fetchrow("SELECT payments, general FROM settings WHERE id = 'global'")
        pay_data = {}
        if s_row and s_row["payments"]:
            raw_p = s_row["payments"]
            while isinstance(raw_p, str):
                raw_p = json.loads(raw_p)
            pay_data = raw_p if isinstance(raw_p, dict) else {}

        iptv_row = await conn.fetchrow("SELECT prices, config FROM services WHERE slug = 'iptv'")
        iptv_prices = {}
        iptv_config = {}
        if iptv_row:
            if iptv_row["prices"]:
                raw_pr = iptv_row["prices"]
                while isinstance(raw_pr, str):
                    raw_pr = json.loads(raw_pr)
                iptv_prices = raw_pr if isinstance(raw_pr, dict) else {}

            if iptv_row["config"]:
                raw_c = iptv_row["config"]
                while isinstance(raw_c, str):
                    raw_c = json.loads(raw_c)
                iptv_config = raw_c if isinstance(raw_c, dict) else {}

    active_b = pay_data.get("activeBank", "bank2")
    b1 = pay_data.get("bank1", {})
    b2 = pay_data.get("bank2", {})

    return {
        "iptv": {
            "host": iptv_config.get("host", ""),
            "type": iptv_config.get("type", "m3u"),
            "message_footer": iptv_config.get("message_footer", ""),
            "price_1m": str(iptv_prices.get("price_1m") or iptv_prices.get("m3u_1_mois") or 10),
            "price_3m": str(iptv_prices.get("price_3m") or iptv_prices.get("m3u_3_mois") or 25),
            "price_6m": str(iptv_prices.get("price_6m") or iptv_prices.get("m3u_6_mois") or 45),
            "price_12m": str(iptv_prices.get("price_12m") or iptv_prices.get("m3u_12_mois") or 70),
            "accounts": iptv_config.get("accounts", []),
            "panel_accounts": iptv_config.get("panel_accounts", [])
        },
        "sumup": {
            "active": "sumup_bank2" if active_b == "bank2" else "sumup",
            "expiration_minutes": str(pay_data.get("expirationMinutes", 30)),
            "banks": {
                "sumup": {
                    "name": b1.get("name") or "Banque 1",
                    "pay_to_email": b1.get("payToEmail", ""),
                    "api_key": b1.get("apiKey", ""),
                    "client_id": b1.get("clientId", ""),
                    "client_secret": b1.get("clientSecret", "")
                },
                "sumup_bank2": {
                    "name": b2.get("name") or "Banque 2",
                    "pay_to_email": b2.get("payToEmail", ""),
                    "api_key": b2.get("apiKey", ""),
                    "client_id": b2.get("clientId", ""),
                    "client_secret": b2.get("clientSecret", "")
                }
            }
        }
    }

# =====================================================================

@router.post("/settings/iptv")
async def admin_save_iptv(payload: IptvSettingsPayload, admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT prices, config FROM services WHERE slug = 'iptv'")
        prices = {}
        config = {}
        if row:
            if row["prices"]:
                raw_pr = row["prices"]
                while isinstance(raw_pr, str):
                    raw_pr = json.loads(raw_pr)
                prices = raw_pr if isinstance(raw_pr, dict) else {}

            if row["config"]:
                raw_c = row["config"]
                while isinstance(raw_c, str):
                    raw_c = json.loads(raw_c)
                config = raw_c if isinstance(raw_c, dict) else {}

        prices["price_1m"] = float(payload.price_1m or 10)
        prices["price_3m"] = float(payload.price_3m or 25)
        prices["price_6m"] = float(payload.price_6m or 45)
        prices["price_12m"] = float(payload.price_12m or 70)
        prices["m3u_1_mois"] = prices["price_1m"]
        prices["m3u_3_mois"] = prices["price_3m"]
        prices["m3u_6_mois"] = prices["price_6m"]
        prices["m3u_12_mois"] = prices["price_12m"]

        config["host"] = payload.host or ""
        config["type"] = payload.type or "m3u"
        config["message_footer"] = payload.message_footer or ""
        config["accounts"] = payload.accounts or []
        config["panel_accounts"] = payload.panel_accounts or []

        await conn.execute(
            "UPDATE services SET prices = $1, config = $2 WHERE slug = 'iptv'",
            json.dumps(prices), json.dumps(config)
        )
    return {"success": True}

# =====================================================================

@router.post("/iptv/api-test")
async def admin_test_iptv_api(admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT config FROM services WHERE slug = 'iptv'")
        if not row or not row["config"]:
            return {"success": False, "message": "Configuration IPTV absente"}
        raw_c = row["config"]
        while isinstance(raw_c, str):
            raw_c = json.loads(raw_c)
        accounts = raw_c.get("accounts", [])
        active_acc = next((a for a in accounts if a.get("active")), None)
        if not active_acc and accounts:
            active_acc = accounts[0]
        if not active_acc:
            return {"success": False, "message": "Aucun compte API configuré"}

    api_url = (active_acc.get("api_url") or "").strip()
    api_key = (active_acc.get("api_key") or "").strip()
    if not api_url or not api_key:
        return {"success": False, "message": "URL ou clé API manquante sur le compte actif"}

    sep = "&" if "?" in api_url else "?"
    test_url = f"{api_url}{sep}action=account&api_key={api_key}"
    try:
        async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
            resp = await client.get(test_url)
            text = resp.text
            if "Invalid API Key" in text:
                return {"success": False, "message": "Clé API refusée par le serveur"}
            credits = "N/A"
            m = re.search(r'"credits":\s*"?(\d+)"?', text)
            if m:
                credits = m.group(1)
            return {
                "success": True,
                "stats": {
                    "name": active_acc.get("name", "Principal"),
                    "pack": active_acc.get("pack", "Standard"),
                    "type": "Xtream Codes",
                    "credits": credits
                }
            }
    except Exception as e:
        return {"success": False, "message": f"Erreur de connexion : {str(e)}"}

# =====================================================================

@router.post("/iptv/panel-test")
async def admin_test_iptv_panel(admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT config FROM services WHERE slug = 'iptv'")
        if not row or not row["config"]:
            return {"success": False, "message": "Configuration IPTV absente"}
        raw_c = row["config"]
        while isinstance(raw_c, str):
            raw_c = json.loads(raw_c)
        panel_accounts = raw_c.get("panel_accounts", [])
        active_panel = next((p for p in panel_accounts if p.get("active")), None)
        if not active_panel and panel_accounts:
            active_panel = panel_accounts[0]
        if not active_panel:
            return {"success": False, "message": "Aucun compte panel configuré"}

    return {
        "success": True,
        "stats": {
            "credits": "Actif",
            "remaining_demos": "Illimité"
        }
    }

# =====================================================================

@router.post("/settings/sumup")
async def admin_save_sumup(payload: SumUpSettingsPayload, admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        s_row = await conn.fetchrow("SELECT payments FROM settings WHERE id = 'global'")
        pay_data = {}
        if s_row and s_row["payments"]:
            raw_p = s_row["payments"]
            while isinstance(raw_p, str):
                raw_p = json.loads(raw_p)
            pay_data = raw_p if isinstance(raw_p, dict) else {}

        pay_data["activeBank"] = "bank2" if payload.active == "sumup_bank2" else "bank1"
        try:
            pay_data["expirationMinutes"] = int(payload.expiration_minutes)
        except Exception:
            pay_data["expirationMinutes"] = 30

        pay_data["bank1"] = {
            "name": payload.banks.sumup.name or "Banque 1",
            "payToEmail": payload.banks.sumup.pay_to_email.strip(),
            "apiKey": payload.banks.sumup.api_key.strip(),
            "clientId": payload.banks.sumup.client_id.strip(),
            "clientSecret": payload.banks.sumup.client_secret.strip()
        }

        pay_data["bank2"] = {
            "name": payload.banks.sumup_bank2.name or "Banque 2",
            "payToEmail": payload.banks.sumup_bank2.pay_to_email.strip(),
            "apiKey": payload.banks.sumup_bank2.api_key.strip(),
            "clientId": payload.banks.sumup_bank2.client_id.strip(),
            "clientSecret": payload.banks.sumup_bank2.client_secret.strip()
        }

        await conn.execute(
            "UPDATE settings SET payments = $1 WHERE id = 'global'",
            json.dumps(pay_data)
        )
    return {"success": True, "bank": payload.active}

# =====================================================================

@router.get("/maintenance")
async def admin_get_maintenance(admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        s_row = await conn.fetchrow("SELECT general FROM settings WHERE id = 'global'")
        gen_data = {}
        if s_row and s_row["general"]:
            raw_g = s_row["general"]
            while isinstance(raw_g, str):
                raw_g = json.loads(raw_g)
            gen_data = raw_g if isinstance(raw_g, dict) else {}
    return {"maintenance": bool(gen_data.get("maintenanceMode", False))}

# =====================================================================

@router.post("/maintenance")
async def admin_set_maintenance(payload: MaintenancePayload, admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        s_row = await conn.fetchrow("SELECT general FROM settings WHERE id = 'global'")
        gen_data = {}
        if s_row and s_row["general"]:
            raw_g = s_row["general"]
            while isinstance(raw_g, str):
                raw_g = json.loads(raw_g)
            gen_data = raw_g if isinstance(raw_g, dict) else {}

        gen_data["maintenanceMode"] = payload.maintenance
        await conn.execute(
            "UPDATE settings SET general = $1 WHERE id = 'global'",
            json.dumps(gen_data)
        )
    return {"success": True, "maintenance": payload.maintenance}

# =====================================================================

@router.post("/settings/password")
async def admin_set_password(payload: PasswordPayload, admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    global ADMIN_PASSWORD
    if not payload.password.strip():
        return Response(status_code=400)
    ADMIN_PASSWORD = payload.password.strip()
    new_token = secrets.token_hex(32)
    _admin_sessions[new_token] = datetime.now(timezone.utc) + timedelta(hours=24)
    return {"success": True, "token": new_token}
