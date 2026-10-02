import os
import re
import json
import time
import hmac
import hashlib
import secrets
import httpx
from uuid import UUID
from decimal import Decimal
from datetime import datetime, timedelta, timezone, date
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Depends, Header, Response, Request, Query, HTTPException
from pydantic import BaseModel
from app.auth import validate_telegram_init_data
from app.config import settings
from app.db import get_db_pool
from app.services.iptv_panel import get_reseller_panel_stats
from app.services.telegram import send_telegram_message, edit_telegram_message_text
from app.services.cache import (
    get_cached_settings,
    invalidate_settings,
    invalidate_service,
    invalidate_active_admins
)
from app.version import get_git_info

# =====================================================================

router = APIRouter(prefix="/api/admin", tags=["admin"])

# =====================================================================

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD") or os.getenv("ADMIN_PANEL_PASSWORD") or ""


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

class UserAdminPayload(BaseModel):
    userId: Any
    admin: bool

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
    price_demo: Optional[str] = None
    demo_enabled: Optional[bool] = None
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

class GeneralSettingsPayload(BaseModel):
    frontendUrl: Optional[str] = None
    telegramBotToken: Optional[str] = None
    botName: Optional[str] = None
    supportTelegram: Optional[str] = None
    channelTelegram: Optional[str] = None
    backendUrl: Optional[str] = None
    marqueeText: Optional[str] = None
    marqueeStyle: Optional[str] = None
    maintenanceMode: Optional[bool] = None

class SecuritySettingsPayload(BaseModel):
    internalApiSecret: Optional[str] = None
    apiSecretKey: Optional[str] = None
    adminSlug: Optional[str] = None
    jwtExpirationMinutes: Optional[int] = None

class PaymentsLimitsPayload(BaseModel):
    paymentEnabled: Optional[bool] = None
    minPaymentAmount: Optional[float] = None
    maxPaymentAmount: Optional[float] = None
    maxPendingPaymentsPerClient: Optional[int] = None

class GenerateDocsSettingsPayload(BaseModel):
    isActive: Optional[bool] = None
    flattenPdf: Optional[bool] = None
    previewOff: Optional[bool] = None
    previewCooldownEnabled: Optional[bool] = None
    previewCooldownSeconds: Optional[int] = None
    subcategories: Optional[Dict[str, Any]] = None
    prices: Optional[Dict[str, Any]] = None

class ServiceTogglePayload(BaseModel):
    slug: str
    isActive: bool

class AmendeDecisionPayload(BaseModel):
    action: str
    price: Optional[float] = None
    adminNotes: Optional[str] = None
    admin_notes: Optional[str] = None

# =====================================================================

def _generate_admin_token() -> str:
    ts = int(time.time())
    rand = secrets.token_hex(16)
    payload = f"{ts}:{rand}"
    secret = (ADMIN_PASSWORD + settings.internal_api_secret).encode("utf-8")
    sig = hmac.new(secret, payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{payload}:{sig}"

def _is_valid_session(token: str, max_age_seconds: int = 86400) -> bool:
    if not token:
        return False
    parts = token.split(":")
    if len(parts) == 3:
        ts_str, rand, sig = parts
        try:
            ts = int(ts_str)
            if time.time() - ts > max_age_seconds:
                return False
            secret = (ADMIN_PASSWORD + settings.internal_api_secret).encode("utf-8")
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

async def _get_admin_password_hash() -> str:
    try:
        s_data = await get_cached_settings()
        if s_data and s_data.get("security"):
            raw_s = s_data["security"]
            if isinstance(raw_s, dict) and raw_s.get("adminPasswordHash"):
                return str(raw_s["adminPasswordHash"])
    except Exception:
        pass
    if ADMIN_PASSWORD.strip():
        return hashlib.sha256(ADMIN_PASSWORD.strip().encode("utf-8")).hexdigest()
    return ""

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
            is_adm = False
            try:
                pool = await get_db_pool()
                async with pool.acquire() as conn:
                    is_adm = await conn.fetchval("SELECT admin FROM users WHERE id = $1", user_id)
            except Exception:
                pass
            if is_adm is True:
                return {
                    "type": "telegram",
                    "id": user_id,
                    "username": user_data.get("username", ""),
                    "first_name": user_data.get("first_name", "")
                }

    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:].strip()
        max_age = 86400
        try:
            s_data = await get_cached_settings()
            if s_data and s_data.get("security"):
                raw_min = s_data["security"].get("jwtExpirationMinutes")
                if raw_min:
                    max_age = int(raw_min) * 60
        except Exception:
            pass
        if _is_valid_session(token, max_age_seconds=max_age):
            return {
                "type": "web",
                "token": token
            }

    return Response(status_code=444)

# =====================================================================

@router.post("/login")
async def admin_login(payload: AdminLoginRequest):
    pwd_input = payload.password.strip()
    input_hash = hashlib.sha256(pwd_input.encode("utf-8")).hexdigest()
    expected_hash = await _get_admin_password_hash()

    if not expected_hash:
        return Response(status_code=444)

    is_valid_hash = secrets.compare_digest(input_hash, expected_hash)
    is_valid_plain = bool(ADMIN_PASSWORD.strip() and secrets.compare_digest(pwd_input, ADMIN_PASSWORD.strip()))

    if not (is_valid_hash or is_valid_plain):
        return Response(status_code=444)

    token = _generate_admin_token()
    exp_seconds = 86400
    try:
        s_data = await get_cached_settings()
        if s_data and s_data.get("security"):
            raw_min = s_data["security"].get("jwtExpirationMinutes")
            if raw_min:
                exp_seconds = int(raw_min) * 60
    except Exception:
        pass
    return {
        "success": True,
        "token": token,
        "expires_in": exp_seconds
    }

# =====================================================================

@router.get("/verify-slug")
async def verify_admin_slug(
    slug: str = Query(...),
    x_internal_secret: Optional[str] = Header(None, alias="X-Internal-Secret")
):
    s_data = await get_cached_settings()
    sec_data = s_data.get("security") if s_data else {}
    db_slug = (sec_data.get("adminSlug") or "espace-sec-x9k2m7").strip().strip("/")
    clean_slug = slug.strip().strip("/")
    if secrets.compare_digest(clean_slug, db_slug):
        return {"valid": True, "slug": db_slug}
    raise HTTPException(status_code=404, detail="Slug invalide")

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
            u_row = await conn.fetchval("SELECT COUNT(*) FROM users")
            total_users = int(u_row or 0)
        except Exception:
            pass

        try:
            p_row = await conn.fetchrow("SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM payments WHERE status = 'PAID'")
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
            g_row = await conn.fetchval("SELECT COUNT(*) FROM generations")
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
            pm_rows = await conn.fetch("SELECT id, user_id, checkout_id, amount, status, created_at FROM payments ORDER BY created_at DESC LIMIT 10")
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
            s_data = await get_cached_settings()
            if s_data and s_data.get("general"):
                maintenance_mode = bool(s_data["general"].get("maintenanceMode", False))
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
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": get_git_info()
    }

# =====================================================================

@router.get("/version")
async def admin_get_version(admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    return get_git_info()

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
                SELECT u.id, u.username, u.first_name, u.balance, u.is_banned, u.admin, u.created_at,
                       COALESCE(p.achats, 0) as achats
                FROM users u
                LEFT JOIN (
                    SELECT user_id, COUNT(*) as achats
                    FROM payments
                    WHERE status = 'PAID'
                    GROUP BY user_id
                ) p ON p.user_id = u.id
                ORDER BY u.created_at DESC
            """)
            users = [
                {
                    "id": str(row["id"]),
                    "userNumber": idx + 1,
                    "username": row["username"] or row["first_name"] or "Anonyme",
                    "solde": float(row["balance"] or 0),
                    "isBanned": bool(row["is_banned"]),
                    "isAdmin": bool(row["admin"]),
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
        current_bal = await conn.fetchval("SELECT balance FROM users WHERE id = $1", uid)
        if current_bal is None:
            return Response(status_code=404)
        if payload.action == "set":
            new_bal = max(0.0, val)
        elif payload.action == "add":
            new_bal = float(current_bal) + abs(val)
        else:
            new_bal = max(0.0, float(current_bal) - abs(val))
        await conn.execute("UPDATE users SET balance = $1, updated_at = NOW() WHERE id = $2", new_bal, uid)
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
        await conn.execute("UPDATE users SET is_banned = $1, updated_at = NOW() WHERE id = $2", is_banned, uid)
    invalidate_active_admins()
    return {"success": True}

# =====================================================================

@router.post("/users/admin")
async def admin_toggle_admin(payload: UserAdminPayload, admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    try:
        uid = int(str(payload.userId).strip())
    except Exception:
        return Response(status_code=400)

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute("UPDATE users SET admin = $1, updated_at = NOW() WHERE id = $2", payload.admin, uid)
    invalidate_active_admins()
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
        await conn.execute("DELETE FROM users WHERE id = $1", uid)
    invalidate_active_admins()
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
            FROM payments
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
                SELECT id, user_id, brand, code, pin, value, price, notes, created_at
                FROM transactions
                ORDER BY created_at DESC
                LIMIT 500
            """)
            txs = [
                {
                    "id": str(row["id"]),
                    "userId": str(row["user_id"]),
                    "brand": row["brand"] or "",
                    "code": row["code"] or "",
                    "pin": row["pin"] or "",
                    "value": float(row["value"] or 0),
                    "valeur": float(row["value"] or 0),
                    "price": float(row["price"] or 0),
                    "notes": row["notes"] or "",
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
        s_row = await conn.fetchrow("SELECT payments, general, security FROM settings WHERE id = 'global'")
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

        sec_data = {}
        if s_row and s_row["security"]:
            raw_s = s_row["security"]
            while isinstance(raw_s, str):
                raw_s = json.loads(raw_s)
            sec_data = raw_s if isinstance(raw_s, dict) else {}

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
            acc_key = iptv_config.get("api_key") or ""
            acc_pack = iptv_config.get("pack") or iptv_config.get("package_id") or iptv_config.get("bouquet") or ""
            acc_url = iptv_config.get("api_url") or ""
            accounts = [{
                "name": iptv_config.get("name") or "Principal",
                "pack": str(acc_pack),
                "api_key": str(acc_key),
                "api_url": str(acc_url),
                "active": True
            }]

        panel_accounts = iptv_config.get("panel_accounts")
        if not panel_accounts or not isinstance(panel_accounts, list):
            panel_accounts = []

        active_b = pay_data.get("activeBank", "bank2")
        active_sumup = "sumup_bank2" if active_b in ("bank2", "sumup_bank2") else "sumup"
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

        services_rows = await conn.fetch("SELECT slug, name, is_active, prices, config FROM services")
        services_dict = {}
        for s_r in services_rows:
            s_slug = s_r["slug"]
            s_cfg = s_r["config"]
            while isinstance(s_cfg, str):
                s_cfg = json.loads(s_cfg)
            s_pr = s_r["prices"]
            while isinstance(s_pr, str):
                s_pr = json.loads(s_pr)
            services_dict[s_slug] = {
                "name": s_r["name"],
                "isActive": bool(s_r["is_active"]),
                "config": s_cfg if isinstance(s_cfg, dict) else {},
                "prices": s_pr if isinstance(s_pr, dict) else {}
            }

        gd = services_dict.get("generate-docs", {})
        gd_cfg = gd.get("config", {})
        generate_docs_data = {
            "isActive": gd.get("isActive", True),
            "flattenPdf": bool(gd_cfg.get("flattenPdf", True)),
            "previewOff": bool(gd_cfg.get("previewOff", False)),
            "previewCooldownEnabled": bool(gd_cfg.get("previewCooldownEnabled", True)),
            "previewCooldownSeconds": int(gd_cfg.get("previewCooldownSeconds", 30)),
            "subcategories": gd_cfg.get("subcategories", {}),
            "prices": gd.get("prices", {})
        }

    return {
        "iptv": {
            "host": iptv_config.get("host") or "",
            "type": iptv_config.get("type", "m3u"),
            "message_footer": iptv_config.get("message_footer", ""),
            "price_1m": str(iptv_prices.get("price_1m", "")),
            "price_3m": str(iptv_prices.get("price_3m", "")),
            "price_6m": str(iptv_prices.get("price_6m", "")),
            "price_12m": str(iptv_prices.get("price_12m", "")),
            "price_demo": str(iptv_prices.get("price_demo", "")),
            "demo_enabled": bool(iptv_config.get("demo_enabled", True)),
            "accounts": accounts,
            "panel_accounts": panel_accounts
        },
        "sumup": {
            "active": active_sumup,
            "expiration_minutes": str(pay_data.get("expirationMinutes", 15)),
            "banks_list": banks_list,
            "banks": {
                "sumup": {
                    "name": b1.get("name") or "",
                    "pay_to_email": b1.get("payToEmail") or "",
                    "api_key": b1.get("apiKey", ""),
                    "client_id": b1.get("clientId", ""),
                    "client_secret": b1.get("clientSecret", "")
                },
                "sumup_bank2": {
                    "name": b2.get("name") or "",
                    "pay_to_email": b2.get("payToEmail") or "",
                    "api_key": b2.get("apiKey", ""),
                    "client_id": b2.get("clientId", ""),
                    "client_secret": b2.get("clientSecret", "")
                }
            }
        },
        "oxapayApiKey": pay_data.get("oxapayApiKey") or "",
        "adminSlug": sec_data.get("adminSlug") or "espace-sec-x9k2m7",
        "frontendUrl": gen_data.get("frontendUrl", ""),
        "telegramBotToken": gen_data.get("telegramBotToken", ""),
        "botName": gen_data.get("botName", ""),
        "supportTelegram": gen_data.get("supportTelegram", ""),
        "channelTelegram": gen_data.get("channelTelegram", ""),
        "backendUrl": gen_data.get("backendUrl", ""),
        "marqueeText": gen_data.get("marqueeText", ""),
        "marqueeStyle": gen_data.get("marqueeStyle", "standard"),
        "maintenanceMode": bool(gen_data.get("maintenanceMode", False)),
        "apiSecretKey": sec_data.get("apiSecretKey") or sec_data.get("internalApiSecret") or "",
        "jwtExpirationMinutes": int(sec_data.get("jwtExpirationMinutes") or 1440),
        "paymentEnabled": bool(pay_data.get("paymentEnabled", True)),
        "minPaymentAmount": pay_data.get("minPaymentAmount", 1.0),
        "maxPaymentAmount": pay_data.get("maxPaymentAmount", 500.0),
        "maxPendingPaymentsPerClient": pay_data.get("maxPendingPaymentsPerClient", 2),
        "generateDocs": generate_docs_data,
        "services": services_dict
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
        for legacy_k in ("m3u_1_mois", "m3u_3_mois", "m3u_6_mois", "m3u_12_mois", "demo"):
            prices.pop(legacy_k, None)
        if payload.price_demo is not None:
            demo_val = float(str(payload.price_demo).replace(",", "."))
            prices["price_demo"] = demo_val

        config["host"] = payload.host or ""
        config["type"] = payload.type or "m3u"
        config["message_footer"] = payload.message_footer or ""
        config.pop("price_demo", None)
        if payload.demo_enabled is not None:
            config["demo_enabled"] = bool(payload.demo_enabled)
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
    invalidate_service("iptv")
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

    try:
        stats = await get_reseller_panel_stats(active_panel, force_refresh=True)
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Échec de connexion au panel: {str(e)}"
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
    invalidate_settings()
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
        invalidate_settings()
        await settings.load_from_db(conn)
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
    new_hash = hashlib.sha256(ADMIN_PASSWORD.encode("utf-8")).hexdigest()
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        s_row = await conn.fetchrow("SELECT security FROM settings WHERE id = 'global'")
        sec_data = {}
        if s_row and s_row["security"]:
            raw_s = s_row["security"]
            while isinstance(raw_s, str):
                raw_s = json.loads(raw_s)
            sec_data = raw_s if isinstance(raw_s, dict) else {}
        sec_data["adminPasswordHash"] = new_hash
        await conn.execute("UPDATE settings SET security = $1 WHERE id = 'global'", json.dumps(sec_data))
        invalidate_settings()
        await settings.load_from_db(conn)
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
        s_row = await conn.fetchrow("SELECT payments FROM settings WHERE id = 'global'")
        pay_data = {}
        if s_row and s_row["payments"]:
            raw_p = s_row["payments"]
            while isinstance(raw_p, str):
                raw_p = json.loads(raw_p)
            pay_data = raw_p if isinstance(raw_p, dict) else {}
        pay_data["oxapayApiKey"] = api_key
        await conn.execute("UPDATE settings SET payments = $1 WHERE id = 'global'", json.dumps(pay_data))
        invalidate_settings()
    return {"success": True}

# =====================================================================

@router.post("/settings/general")
async def admin_save_general(payload: GeneralSettingsPayload, admin: Any = Depends(get_current_admin)):
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
        if payload.frontendUrl is not None:
            val = payload.frontendUrl.strip()
            if not val:
                raise HTTPException(status_code=400, detail="L'URL frontend ne peut pas être vide")
            gen_data["frontendUrl"] = val
        if payload.telegramBotToken is not None:
            val = payload.telegramBotToken.strip()
            if not val:
                raise HTTPException(status_code=400, detail="Le token bot Telegram ne peut pas être vide")
            gen_data["telegramBotToken"] = val
        if payload.botName is not None:
            gen_data["botName"] = payload.botName.strip()
        if payload.supportTelegram is not None:
            gen_data["supportTelegram"] = payload.supportTelegram.strip()
        if payload.channelTelegram is not None:
            gen_data["channelTelegram"] = payload.channelTelegram.strip()
        if payload.backendUrl is not None:
            gen_data["backendUrl"] = payload.backendUrl.strip()
        if payload.marqueeText is not None:
            gen_data["marqueeText"] = payload.marqueeText.strip()
        if payload.marqueeStyle is not None:
            gen_data["marqueeStyle"] = payload.marqueeStyle.strip()
        if payload.maintenanceMode is not None:
            gen_data["maintenanceMode"] = payload.maintenanceMode
        await conn.execute("UPDATE settings SET general = $1 WHERE id = 'global'", json.dumps(gen_data))
        invalidate_settings()
        await settings.load_from_db(conn)
    return {"success": True}

# =====================================================================

@router.post("/settings/security")
async def admin_save_security(payload: SecuritySettingsPayload, admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        s_row = await conn.fetchrow("SELECT security FROM settings WHERE id = 'global'")
        sec_data = {}
        if s_row and s_row["security"]:
            raw_s = s_row["security"]
            while isinstance(raw_s, str):
                raw_s = json.loads(raw_s)
            sec_data = raw_s if isinstance(raw_s, dict) else {}
        sec_key = payload.apiSecretKey or payload.internalApiSecret
        if sec_key is not None:
            val = sec_key.strip()
            if not val:
                raise HTTPException(status_code=400, detail="La clé secrète API ne peut pas être vide")
            sec_data["apiSecretKey"] = val
            sec_data.pop("internalApiSecret", None)
        if payload.adminSlug is not None:
            sec_data["adminSlug"] = payload.adminSlug.strip()
        if payload.jwtExpirationMinutes is not None:
            sec_data["jwtExpirationMinutes"] = int(payload.jwtExpirationMinutes)
        await conn.execute("UPDATE settings SET security = $1 WHERE id = 'global'", json.dumps(sec_data))
        invalidate_settings()
        await settings.load_from_db(conn)
    return {"success": True}

# =====================================================================

@router.post("/settings/payments-limits")
async def admin_save_payments_limits(payload: PaymentsLimitsPayload, admin: Any = Depends(get_current_admin)):
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
        if payload.paymentEnabled is not None:
            pay_data["paymentEnabled"] = payload.paymentEnabled
        if payload.minPaymentAmount is not None:
            pay_data["minPaymentAmount"] = float(payload.minPaymentAmount)
        if payload.maxPaymentAmount is not None:
            pay_data["maxPaymentAmount"] = float(payload.maxPaymentAmount)
        if payload.maxPendingPaymentsPerClient is not None:
            pay_data["maxPendingPaymentsPerClient"] = int(payload.maxPendingPaymentsPerClient)
        await conn.execute("UPDATE settings SET payments = $1 WHERE id = 'global'", json.dumps(pay_data))
        invalidate_settings()
    return {"success": True}

# =====================================================================

@router.post("/settings/services/toggle")
async def admin_toggle_service(payload: ServiceTogglePayload, admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    clean_slug = re.sub(r'[^a-zA-Z0-9_\-]', '', payload.slug)
    if not clean_slug:
        return Response(status_code=400, content='{"error": "Slug invalide"}', media_type="application/json")
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute("UPDATE services SET is_active = $1 WHERE slug = $2", payload.isActive, clean_slug)
    invalidate_service(clean_slug)
    return {"success": True, "slug": clean_slug, "isActive": payload.isActive}

# =====================================================================

@router.post("/settings/generate-docs")
async def admin_save_generate_docs(payload: GenerateDocsSettingsPayload, admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT is_active, config, prices FROM services WHERE slug = 'generate-docs'")
        if not row:
            return Response(status_code=404, content='{"error": "Service generate-docs introuvable"}', media_type="application/json")
        
        cfg = row["config"]
        while isinstance(cfg, str):
            cfg = json.loads(cfg)
        cfg_data = cfg if isinstance(cfg, dict) else {}

        pr = row["prices"]
        while isinstance(pr, str):
            pr = json.loads(pr)
        pr_data = pr if isinstance(pr, dict) else {}

        is_active = row["is_active"]
        if payload.isActive is not None:
            is_active = payload.isActive

        if payload.flattenPdf is not None:
            cfg_data["flattenPdf"] = bool(payload.flattenPdf)
        if payload.previewOff is not None:
            cfg_data["previewOff"] = bool(payload.previewOff)
        if payload.previewCooldownEnabled is not None:
            cfg_data["previewCooldownEnabled"] = bool(payload.previewCooldownEnabled)
        if payload.previewCooldownSeconds is not None:
            cfg_data["previewCooldownSeconds"] = max(0, int(payload.previewCooldownSeconds))

        if payload.subcategories is not None:
            if "subcategories" not in cfg_data or not isinstance(cfg_data["subcategories"], dict):
                cfg_data["subcategories"] = {}
            for sub_key, sub_val in payload.subcategories.items():
                if isinstance(sub_val, dict):
                    if sub_key not in cfg_data["subcategories"] or not isinstance(cfg_data["subcategories"][sub_key], dict):
                        cfg_data["subcategories"][sub_key] = {}
                    if "enabled" in sub_val:
                        cfg_data["subcategories"][sub_key]["enabled"] = bool(sub_val["enabled"])
                    cfg_data["subcategories"][sub_key].pop("allowed_roles", None)
                    cfg_data["subcategories"][sub_key].pop("allowedRoles", None)
                    if "documents" in sub_val and isinstance(sub_val["documents"], dict):
                        if "documents" not in cfg_data["subcategories"][sub_key] or not isinstance(cfg_data["subcategories"][sub_key]["documents"], dict):
                            cfg_data["subcategories"][sub_key]["documents"] = {}
                        for doc_k, doc_v in sub_val["documents"].items():
                            if isinstance(doc_v, dict):
                                cfg_data["subcategories"][sub_key]["documents"][doc_k] = {
                                    "enabled": bool(doc_v.get("enabled", True))
                                }

        if payload.prices is not None and isinstance(payload.prices, dict):
            for p_k, p_v in payload.prices.items():
                try:
                    pr_data[p_k] = float(p_v)
                except Exception:
                    pass

        await conn.execute(
            "UPDATE services SET is_active = $1, config = $2, prices = $3 WHERE slug = 'generate-docs'",
            is_active, json.dumps(cfg_data), json.dumps(pr_data)
        )
    invalidate_service("generate-docs")
    return {"success": True}

# =====================================================================

def _serialize_db_value(val: Any) -> Any:
    if val is None:
        return None
    if isinstance(val, (datetime, date)):
        return val.isoformat()
    if isinstance(val, (Decimal, float)):
        return float(val)
    if isinstance(val, UUID):
        return str(val)
    if isinstance(val, bytes):
        return val.hex()
    if isinstance(val, (dict, list)):
        return val
    return val

# =====================================================================

@router.get("/database/tables")
async def admin_get_database_tables(admin: Any = Depends(get_current_admin)):
    if isinstance(admin, Response):
        return admin
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        t_rows = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
              AND table_type = 'BASE TABLE'
            ORDER BY table_name ASC;
        """)
        tables = []
        for r in t_rows:
            tname = r["table_name"]
            try:
                cnt = await conn.fetchval(f'SELECT COUNT(*) FROM "{tname}"')
            except Exception:
                cnt = 0
            c_rows = await conn.fetch("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = $1
                ORDER BY ordinal_position ASC;
            """, tname)
            tables.append({
                "name": tname,
                "count": cnt or 0,
                "columns": [
                    {
                        "name": c["column_name"],
                        "type": c["data_type"],
                        "nullable": c["is_nullable"] == "YES",
                        "default": c["column_default"]
                    }
                    for c in c_rows
                ]
            })
        return {"tables": tables}

# =====================================================================

@router.get("/database/query")
async def admin_query_database_table(
    table: str,
    page: int = 1,
    limit: int = 25,
    search: Optional[str] = None,
    sort_col: Optional[str] = None,
    sort_dir: Optional[str] = "asc",
    admin: Any = Depends(get_current_admin)
):
    if isinstance(admin, Response):
        return admin
    clean_table = re.sub(r'[^a-zA-Z0-9_]', '', table)
    if not clean_table:
        return Response(status_code=400, content='{"error": "Nom de table invalide"}', media_type="application/json")
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        t_exists = await conn.fetchval("""
            SELECT 1 FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = $1
        """, clean_table)
        if not t_exists:
            return Response(status_code=404, content='{"error": "Table introuvable"}', media_type="application/json")
        c_rows = await conn.fetch("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = $1
            ORDER BY ordinal_position ASC;
        """, clean_table)
        columns = [
            {
                "name": c["column_name"],
                "type": c["data_type"],
                "nullable": c["is_nullable"] == "YES",
                "default": c["column_default"]
            }
            for c in c_rows
        ]
        col_names = {c["name"] for c in columns}
        where_clauses = []
        params = []
        param_idx = 1
        if search and search.strip():
            term = f"%{search.strip()}%"
            search_conds = []
            for c in columns:
                c_type = c["type"].lower()
                c_name = c["name"]
                if any(t in c_type for t in ["text", "char", "varchar", "uuid", "json"]):
                    search_conds.append(f'"{clean_table}"."{c_name}"::text ILIKE ${param_idx}')
            if search_conds:
                where_clauses.append("(" + " OR ".join(search_conds) + ")")
                params.append(term)
                param_idx += 1
        where_sql = (" WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
        count_sql = f'SELECT COUNT(*) FROM "{clean_table}"{where_sql}'
        total = await conn.fetchval(count_sql, *params)
        order_sql = ""
        if sort_col and sort_col in col_names:
            direction = "DESC" if str(sort_dir).lower() == "desc" else "ASC"
            order_sql = f' ORDER BY "{clean_table}"."{sort_col}" {direction}'
        else:
            primary_candidates = ["id", "created_at", "createdAt", "updated_at"]
            for cand in primary_candidates:
                if cand in col_names:
                    order_sql = f' ORDER BY "{clean_table}"."{cand}" DESC'
                    break
        page = max(1, page)
        limit = min(max(1, limit), 100)
        offset = (page - 1) * limit
        query_sql = f'SELECT * FROM "{clean_table}"{where_sql}{order_sql} LIMIT {limit} OFFSET {offset}'
        rows = await conn.fetch(query_sql, *params)
        serialized_rows = []
        for r in rows:
            row_dict = {}
            for col in columns:
                val = r.get(col["name"])
                row_dict[col["name"]] = _serialize_db_value(val)
            serialized_rows.append(row_dict)
        return {
            "table": clean_table,
            "columns": columns,
            "rows": serialized_rows,
            "total": total or 0,
            "page": page,
            "limit": limit
        }

# =====================================================================

@router.get("/amendes")
async def admin_get_amendes(
    status: Optional[str] = None,
    admin: Any = Depends(get_current_admin)
):
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        query = """
            SELECT a.id, a.user_id, a.status, a.price, a.file_urls, a.note,
                   a.admin_notes, a.created_at, a.updated_at,
                   u.username, u.first_name, u.last_name, u.balance
            FROM amendes a
            LEFT JOIN users u ON a.user_id = u.id
        """
        params = []
        if status and status.upper() != "ALL":
            query += " WHERE a.status = $1"
            params.append(status.upper())
        query += " ORDER BY a.created_at DESC"
        rows = await conn.fetch(query, *params)
        results = []
        for r in rows:
            raw_urls = r["file_urls"]
            while isinstance(raw_urls, str):
                try:
                    raw_urls = json.loads(raw_urls)
                except Exception:
                    raw_urls = []
            if not isinstance(raw_urls, list):
                raw_urls = []
            results.append({
                "id": str(r["id"]),
                "user_id": r["user_id"],
                "username": r["username"] or "",
                "first_name": r["first_name"] or "",
                "last_name": r["last_name"] or "",
                "user_balance": float(r["balance"] or 0),
                "status": r["status"],
                "price": float(r["price"]) if r["price"] is not None else None,
                "file_urls": raw_urls,
                "note": r["note"] or "",
                "admin_notes": r["admin_notes"] or "",
                "created_at": r["created_at"].isoformat() if r["created_at"] else None,
                "updated_at": r["updated_at"].isoformat() if r["updated_at"] else None
            })
        return {"amendes": results}

# =====================================================================

@router.post("/amendes/{amende_id}/decision")
async def admin_amende_decision(
    amende_id: str,
    payload: AmendeDecisionPayload,
    admin: Any = Depends(get_current_admin)
):
    try:
        amende_uuid = UUID(amende_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Identifiant de dossier invalide")

    action = payload.action.strip().lower()
    admin_notes = payload.adminNotes or payload.admin_notes
    price = payload.price

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        amende = await conn.fetchrow("SELECT * FROM amendes WHERE id = $1", amende_uuid)
        if not amende:
            raise HTTPException(status_code=404, detail="Dossier d'amende introuvable")

        raw_maps = amende["telegram_message_ids"]
        while isinstance(raw_maps, str):
            try:
                raw_maps = json.loads(raw_maps)
            except Exception:
                raw_maps = []
        if not isinstance(raw_maps, list):
            raw_maps = []

        if action == "accept":
            if price is None or price <= 0:
                raise HTTPException(status_code=400, detail="Le tarif doit être supérieur à 0 pour accepter.")
            rounded_price = round(price, 2)
            await conn.execute("""
                UPDATE amendes
                SET status = 'ACCEPTED', price = $1, admin_notes = COALESCE($2, admin_notes), updated_at = NOW()
                WHERE id = $3
            """, rounded_price, admin_notes, amende_uuid)

            for m in raw_maps:
                if m.get("chat_id") and m.get("message_id"):
                    try:
                        await edit_telegram_message_text(
                            chat_id=m["chat_id"],
                            message_id=m["message_id"],
                            text=f"✅ <b>Dossier validé via le panel</b> (<code>{amende_id}</code>) au tarif de <b>{rounded_price:.2f} €</b>."
                        )
                    except Exception:
                        pass

            try:
                await send_telegram_message(
                    chat_id=amende["user_id"],
                    text=(
                        f"✅ <b>Votre dossier d'annulation d'amende a été accepté !</b>\n\n"
                        f"<b>Dossier</b> : <code>{amende_id}</code>\n"
                        f"<b>Montant fixé</b> : <b>{rounded_price:.2f} €</b>\n\n"
                        f"Vous pouvez dès à présent régler ce dossier depuis l'application en débitant votre solde."
                    ),
                    reply_markup={"inline_keyboard": [[{"text": "💳 Payer dans l'application", "web_app": {"url": settings.frontend_url}}]]}
                )
            except Exception:
                pass

            return {"success": True, "status": "ACCEPTED", "price": rounded_price}

        elif action == "reject":
            await conn.execute("""
                UPDATE amendes
                SET status = 'REJECTED', admin_notes = COALESCE($1, admin_notes), updated_at = NOW()
                WHERE id = $2
            """, admin_notes, amende_uuid)

            for m in raw_maps:
                if m.get("chat_id") and m.get("message_id"):
                    try:
                        await edit_telegram_message_text(
                            chat_id=m["chat_id"],
                            message_id=m["message_id"],
                            text=f"❌ <b>Dossier refusé via le panel</b> (<code>{amende_id}</code>)."
                        )
                    except Exception:
                        pass

            try:
                await send_telegram_message(
                    chat_id=amende["user_id"],
                    text=f"❌ <b>Information Dossier d'Amende</b>\nVotre dossier <code>{amende_id}</code> ne peut malheureusement pas être pris en charge et a été refusé."
                )
            except Exception:
                pass

            return {"success": True, "status": "REJECTED"}

        elif action in ("finish", "termine"):
            await conn.execute("""
                UPDATE amendes
                SET status = 'FINISHED', admin_notes = COALESCE($1, admin_notes), updated_at = NOW()
                WHERE id = $2
            """, admin_notes, amende_uuid)

            for m in raw_maps:
                if m.get("chat_id") and m.get("message_id"):
                    try:
                        await edit_telegram_message_text(
                            chat_id=m["chat_id"],
                            message_id=m["message_id"],
                            text=f"🏁 <b>Dossier clôturé</b> (<code>{amende_id}</code>)."
                        )
                    except Exception:
                        pass

            return {"success": True, "status": "FINISHED"}

        else:
            raise HTTPException(status_code=400, detail=f"Action '{action}' non reconnue")
