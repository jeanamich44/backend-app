import os
import re
import json
import time
import hmac
import hashlib
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
    action: Optional[str] = "set"
    amount: float

class UserBanPayload(BaseModel):
    userId: Any
    banned: Optional[bool] = None
    ban: Optional[bool] = None
    reason: Optional[str] = ""

class UserDeletePayload(BaseModel):
    userId: Any

class UserSyncPayload(BaseModel):
    userId: Any

class OxaPayPayload(BaseModel):
    api_key: str

class IptvSettingsPayload(BaseModel):
    host: Optional[str] = ""
    type: Optional[str] = "m3u"
    message_footer: Optional[str] = ""
    price_1m: Optional[str] = "10"
    price_3m: Optional[str] = "25"
    price_6m: Optional[str] = "45"
    price_12m: Optional[str] = "70"
    price_demo: Optional[str] = "1"
    demo_enabled: Optional[bool] = True
    accounts: Optional[List[Dict[str, Any]]] = []
    panel_accounts: Optional[List[Dict[str, Any]]] = []

class BankItemPayload(BaseModel):
    id: Optional[str] = "bank1"
    name: Optional[str] = ""
    pay_to_email: str
    api_key: str
    client_id: str
    client_secret: str

class SumUpSettingsPayload(BaseModel):
    active: str
    expiration_minutes: Any
    banks: Optional[Any] = None
    banks_list: Optional[List[BankItemPayload]] = None

class MaintenancePayload(BaseModel):
    maintenance: bool

class PasswordPayload(BaseModel):
    password: str

# =====================================================================

def _generate_admin_token() -> str:
    ts = int(time.time())
    rand = secrets.token_hex(16)
    payload = f"{ts}:{rand}"
    secret = (ADMIN_PASSWORD + os.getenv("INTERNAL_API_SECRET", "c8b9f1d0a83e47229b12480ad2e08e6f")).encode("utf-8")
    sig = hmac.new(secret, payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{payload}:{sig}"

def _is_valid_session(token: str) -> bool:
    if not token:
        return False
    parts = token.split(":")
    if len(parts) == 3:
        ts_str, rand, sig = parts
        try:
            ts = int(ts_str)
            if time.time() - ts > 86400:
                return False
            secret = (ADMIN_PASSWORD + os.getenv("INTERNAL_API_SECRET", "c8b9f1d0a83e47229b12480ad2e08e6f")).encode("utf-8")
            expected_sig = hmac.new(secret, f"{ts}:{rand}".encode("utf-8"), hashlib.sha256).hexdigest()
            return hmac.compare_digest(sig, expected_sig)
        except Exception:
            return False
    if token in _admin_sessions:
        exp = _admin_sessions[token]
        if datetime.now(timezone.utc) > exp:
            _admin_sessions.pop(token, None)
            return False
        return True
    return False

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

    token = _generate_admin_token()
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
    total_users = 0
    total_payments = 0
    total_payments_vol = 0.0
    total_stock = 0
    total_transactions = 0
    total_sales_vol = 0.0
    gen_count = 0
    recent_sales = []
    recent_payments = []
    maintenance_mode = False

    async with pool.acquire() as conn:
        try:
            u_row = await conn.fetchval("SELECT COUNT(*) FROM tma_users")
            total_users = int(u_row or 0)
        except Exception:
            pass

        try:
            p_row = await conn.fetchrow("SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM tma_payments WHERE status = 'PAID'")
            if p_row:
                total_payments = int(p_row[0] or 0)
                total_payments_vol = float(p_row[1] or 0.0)
        except Exception:
            pass

        try:
            s_row = await conn.fetchval("SELECT COUNT(*) FROM stock WHERE brand = 'carr' AND is_sold = FALSE")
            total_stock = int(s_row or 0)
        except Exception:
            pass

        try:
            t_row = await conn.fetchrow("SELECT COUNT(*), COALESCE(SUM(price), 0) FROM transactions")
            if t_row:
                total_transactions = int(t_row[0] or 0)
                total_sales_vol = float(t_row[1] or 0.0)
        except Exception:
            pass

        try:
            g_row = await conn.fetchval("SELECT COUNT(*) FROM tma_generations")
            gen_count = int(g_row or 0)
        except Exception:
            pass

        try:
            tx_rows = await conn.fetch("SELECT id, user_id, brand, price, created_at FROM transactions ORDER BY created_at DESC LIMIT 10")
            recent_sales = [
                {
                    "id": row["id"],
                    "userId": str(row["user_id"]),
                    "brand": row["brand"],
                    "price": float(row["price"] or 0),
                    "createdAt": row["created_at"].isoformat() if row["created_at"] else ""
                }
                for row in tx_rows
            ]
        except Exception:
            pass

        try:
            pm_rows = await conn.fetch("SELECT id, user_id, checkout_id, amount, status, created_at FROM tma_payments ORDER BY created_at DESC LIMIT 10")
            recent_payments = [
                {
                    "id": str(row["id"]),
                    "chatId": str(row["user_id"]),
                    "trackId": row["checkout_id"] or "N/A",
                    "amount": float(row["amount"] or 0),
                    "method": "CB",
                    "status": row["status"] or "PAID",
                    "createdAt": row["created_at"].isoformat() if row["created_at"] else ""
                }
                for row in pm_rows
            ]
        except Exception:
            pass

        try:
            s_row = await conn.fetchrow("SELECT general FROM settings WHERE id = 'global'")
            if s_row and s_row["general"]:
                raw_g = s_row["general"]
                while isinstance(raw_g, str):
                    raw_g = json.loads(raw_g)
                if isinstance(raw_g, dict):
                    maintenance_mode = bool(raw_g.get("maintenanceMode", False))
        except Exception:
            pass

    total_ca = total_payments_vol if total_payments_vol > 0 else total_sales_vol
    total_sales = total_transactions if total_transactions > 0 else total_payments

    metrics = {
        "telegramReceived": 0,
        "telegramSent": 0,
        "sumupReceived": total_payments,
        "sumupSent": 0,
        "oxapayReceived": 0,
        "oxapaySent": 0,
        "commandsExecuted": 0,
        "errorsCount": 0,
        "adminLogins": 1
    }

    graph = {
        "today": [{"label": f"{h:02d}h-{(h+2):02d}h", "volume": 0} for h in range(0, 24, 2)],
        "days7": [{"label": f"J-{i}", "volume": 0} for i in range(6, -1, -1)],
        "days30": [{"label": f"J-{i}", "volume": 0} for i in range(29, -1, -1)]
    }

    return {
        "totalCa": float(total_ca),
        "totalSales": int(total_sales),
        "totalUsers": int(total_users),
        "totalStock": int(total_stock),
        "recentSales": recent_sales,
        "recentPayments": recent_payments,
        "maintenance": maintenance_mode,
        "metrics": metrics,
        "graph": graph,
        "users_count": int(total_users),
        "payments_count": int(total_sales),
        "payments_volume": float(total_ca),
        "stock_count": int(total_stock),
        "generations_count": int(gen_count),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

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
    try:
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
    except Exception as e:
        import traceback
        return Response(content=json.dumps({"error": str(e), "trace": traceback.format_exc()}), status_code=500, media_type="application/json")

# =====================================================================

@router.post("/users/solde")
async def admin_update_user_solde(payload: UserSoldePayload, admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    try:
        uid = int(str(payload.userId).strip())
    except Exception:
        return Response(status_code=400)

    val = float(payload.amount)
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        current_bal = await conn.fetchval("SELECT balance FROM tma_users WHERE id = $1", uid)
        if current_bal is None:
            return Response(status_code=404)
        if payload.action == "set":
            new_bal = max(0.0, val)
        elif payload.action == "add":
            new_bal = float(current_bal) + abs(val)
        else:
            new_bal = max(0.0, float(current_bal) - abs(val))
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

    is_banned = payload.banned if payload.banned is not None else (payload.ban if payload.ban is not None else False)
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute("UPDATE tma_users SET is_banned = $1, updated_at = NOW() WHERE id = $2", is_banned, uid)
    return {"success": True}

# =====================================================================

@router.post("/users/delete")
async def admin_delete_user(payload: UserDeletePayload, admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    try:
        uid = int(str(payload.userId).strip())
    except Exception:
        return Response(status_code=400)

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM tma_users WHERE id = $1", uid)
    return {"success": True}

# =====================================================================

@router.post("/users/sync-user")
async def admin_sync_user(payload: UserSyncPayload, admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    return {"success": True}

# =====================================================================

@router.post("/metrics/reset")
async def admin_reset_metrics(admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    return {"success": True}

# =====================================================================

@router.get("/payments")
async def admin_get_payments(admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT id, user_id, amount, currency, status, checkout_id, created_at
            FROM tma_payments
            ORDER BY created_at DESC
            LIMIT 200
        """)
        payments = [
            {
                "id": str(row["id"]),
                "chatId": str(row["user_id"]),
                "trackId": row["checkout_id"] or "N/A",
                "amount": float(row["amount"] or 0),
                "method": "CB",
                "status": row["status"] or "PAID",
                "createdAt": row["created_at"].isoformat() if row["created_at"] else ""
            }
            for row in rows
        ]
    return {"payments": payments}

# =====================================================================

@router.get("/transactions")
async def admin_get_transactions(admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    try:
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT id, user_id, amount, status, checkout_id, created_at
                FROM tma_payments
                WHERE status = 'PAID'
                ORDER BY created_at DESC
                LIMIT 200
            """)
            txs = [
                {
                    "id": str(row["id"]),
                    "userId": str(row["user_id"]),
                    "brand": "Rechargement CB",
                    "code": row["checkout_id"] or "N/A",
                    "price": float(row["amount"] or 0),
                    "valeur": float(row["amount"] or 0),
                    "status": row["status"],
                    "createdAt": row["created_at"].isoformat() if row["created_at"] else ""
                }
                for row in rows
            ]
        return {"transactions": txs}
    except Exception as e:
        import traceback
        return Response(content=json.dumps({"error": str(e), "trace": traceback.format_exc()}), status_code=500, media_type="application/json")

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

        gen_data = {}
        if s_row and s_row["general"]:
            raw_g = s_row["general"]
            while isinstance(raw_g, str):
                raw_g = json.loads(raw_g)
            gen_data = raw_g if isinstance(raw_g, dict) else {}

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
        accounts = iptv_config.get("accounts")
        if not accounts or not isinstance(accounts, list) or len(accounts) == 0:
            acc_key = iptv_config.get("api_key", "c747279bd5a2284570cd5e888ef182f6")
            acc_pack = iptv_config.get("pack") or iptv_config.get("package_id") or iptv_config.get("bouquet") or "47013"
            acc_url = iptv_config.get("api_url", "https://4k.cms-only.ru/api/api.php")
            accounts = [{
                "name": iptv_config.get("name", "ChezRheyy"),
                "pack": str(acc_pack),
                "api_key": str(acc_key),
                "api_url": str(acc_url),
                "active": True
            }]

        panel_accounts = iptv_config.get("panel_accounts")
        if not panel_accounts or not isinstance(panel_accounts, list) or len(panel_accounts) == 0:
            p_user = iptv_config.get("username", "LABANK")
            p_pass = iptv_config.get("password", "LECOFFREFORTT")
            panel_accounts = [{
                "name": iptv_config.get("name", "ChezRheyy"),
                "username": str(p_user),
                "password": str(p_pass),
                "active": True
            }]

        active_b = pay_data.get("activeBank", "bank2")
        banks_list = []
        if isinstance(pay_data.get("banks_list"), list) and pay_data["banks_list"]:
            banks_list = pay_data["banks_list"]
        else:
            b_keys = sorted([k for k in pay_data.keys() if k.startswith("bank") and isinstance(pay_data[k], dict)])
            if not b_keys:
                b_keys = ["bank1", "bank2"]
            for idx, k in enumerate(b_keys):
                b_val = pay_data.get(k, {})
                banks_list.append({
                    "id": k,
                    "name": b_val.get("name") or f"Banque {idx + 1}",
                    "pay_to_email": b_val.get("payToEmail", ""),
                    "api_key": b_val.get("apiKey", ""),
                    "client_id": b_val.get("clientId", ""),
                    "client_secret": b_val.get("clientSecret", "")
                })

        b1 = pay_data.get("bank1", {})
        b2 = pay_data.get("bank2", {})

    return {
        "iptv": {
            "host": iptv_config.get("host") or "http://cf.business-cloud-neo.com",
            "type": iptv_config.get("type", "m3u"),
            "message_footer": iptv_config.get("message_footer", ""),
            "price_1m": str(iptv_prices.get("price_1m") or iptv_prices.get("m3u_1_mois") or 5),
            "price_3m": str(iptv_prices.get("price_3m") or iptv_prices.get("m3u_3_mois") or 10),
            "price_6m": str(iptv_prices.get("price_6m") or iptv_prices.get("m3u_6_mois") or 20),
            "price_12m": str(iptv_prices.get("price_12m") or iptv_prices.get("m3u_12_mois") or 35),
            "price_demo": str(iptv_prices.get("price_demo") or iptv_prices.get("demo") or iptv_config.get("price_demo") or 1),
            "demo_enabled": iptv_config.get("demo_enabled", True) if isinstance(iptv_config.get("demo_enabled"), bool) else str(iptv_config.get("demo_enabled", "true")).lower() in ("true", "1", "on"),
            "accounts": accounts,
            "panel_accounts": panel_accounts
        },
        "sumup": {
            "active": active_b,
            "expiration_minutes": str(pay_data.get("expirationMinutes", 15)),
            "banks_list": banks_list,
            "banks": {
                "sumup": {
                    "name": b1.get("name") or "gustave.pro@outlook.fr",
                    "pay_to_email": b1.get("payToEmail", "gustave.pro@outlook.fr"),
                    "api_key": b1.get("apiKey", ""),
                    "client_id": b1.get("clientId", ""),
                    "client_secret": b1.get("clientSecret", "")
                },
                "sumup_bank2": {
                    "name": b2.get("name") or "kevin.ebpro@outlook.fr",
                    "pay_to_email": b2.get("payToEmail", "kevin.ebpro@outlook.fr"),
                    "api_key": b2.get("apiKey", ""),
                    "client_id": b2.get("clientId", ""),
                    "client_secret": b2.get("clientSecret", "")
                }
            }
        },
        "oxapayApiKey": gen_data.get("oxapayApiKey", "UWUEMJ-HAHWDD-IYNN8Z-GDQ94H")
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
        demo_val = float(str(payload.price_demo or 1).replace(",", "."))
        prices["price_demo"] = demo_val
        prices["demo"] = demo_val

        config["host"] = payload.host or ""
        config["type"] = payload.type or "m3u"
        config["message_footer"] = payload.message_footer or ""
        config["price_demo"] = demo_val
        config["demo_enabled"] = bool(payload.demo_enabled) if payload.demo_enabled is not None else True
        config["accounts"] = payload.accounts or []
        config["panel_accounts"] = payload.panel_accounts or []

        active_acc = next((a for a in (payload.accounts or []) if a.get("active")), None)
        if not active_acc and payload.accounts:
            active_acc = payload.accounts[0]
        if active_acc:
            config["api_key"] = active_acc.get("api_key", "")
            config["pack"] = active_acc.get("pack", "")
            config["package_id"] = active_acc.get("pack", "")
            config["bouquet"] = active_acc.get("pack", "")
            if active_acc.get("api_url"):
                config["api_url"] = active_acc.get("api_url")

        active_panel = next((p for p in (payload.panel_accounts or []) if p.get("active")), None)
        if not active_panel and payload.panel_accounts:
            active_panel = payload.panel_accounts[0]
        if active_panel:
            config["username"] = active_panel.get("username", "")
            config["password"] = active_panel.get("password", "")

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

        active_bank = payload.active
        if active_bank == "sumup":
            active_bank = "bank1"
        elif active_bank == "sumup_bank2":
            active_bank = "bank2"
        pay_data["activeBank"] = active_bank

        try:
            pay_data["expirationMinutes"] = int(payload.expiration_minutes)
        except Exception:
            pay_data["expirationMinutes"] = 15

        if payload.banks_list:
            b_list_data = []
            for b in payload.banks_list:
                b_dict = {
                    "id": b.id or "bank1",
                    "name": b.name or b.id,
                    "payToEmail": b.pay_to_email.strip(),
                    "apiKey": b.api_key.strip(),
                    "clientId": b.client_id.strip(),
                    "clientSecret": b.client_secret.strip()
                }
                b_list_data.append(b_dict)
                pay_data[b.id] = b_dict
            pay_data["banks_list"] = b_list_data
            if len(b_list_data) >= 1:
                pay_data["bank1"] = b_list_data[0]
            if len(b_list_data) >= 2:
                pay_data["bank2"] = b_list_data[1]
        elif payload.banks:
            b_sumup = payload.banks.get("sumup", {}) if isinstance(payload.banks, dict) else {}
            b_sumup2 = payload.banks.get("sumup_bank2", {}) if isinstance(payload.banks, dict) else {}
            pay_data["bank1"] = {
                "name": b_sumup.get("name", "Banque 1"),
                "payToEmail": (b_sumup.get("pay_to_email") or "").strip(),
                "apiKey": (b_sumup.get("api_key") or "").strip(),
                "clientId": (b_sumup.get("client_id") or "").strip(),
                "clientSecret": (b_sumup.get("client_secret") or "").strip()
            }
            pay_data["bank2"] = {
                "name": b_sumup2.get("name", "Banque 2"),
                "payToEmail": (b_sumup2.get("pay_to_email") or "").strip(),
                "apiKey": (b_sumup2.get("api_key") or "").strip(),
                "clientId": (b_sumup2.get("client_id") or "").strip(),
                "clientSecret": (b_sumup2.get("client_secret") or "").strip()
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
    new_token = _generate_admin_token()
    return {"success": True, "token": new_token}

# =====================================================================


@router.post("/settings/oxapay")
async def admin_set_oxapay_key(payload: OxaPayPayload, admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    api_key = payload.api_key.strip()
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        s_row = await conn.fetchrow("SELECT general FROM settings WHERE id = 'global'")
        gen_data = {}
        if s_row and s_row["general"]:
            raw_g = s_row["general"]
            while isinstance(raw_g, str):
                raw_g = json.loads(raw_g)
            gen_data = raw_g if isinstance(raw_g, dict) else {}
        gen_data["oxapayApiKey"] = api_key
        await conn.execute("UPDATE settings SET general = $1 WHERE id = 'global'", json.dumps(gen_data))
    return {"success": True}
