import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
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
