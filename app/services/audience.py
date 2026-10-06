import os
import asyncio
import httpx
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.config import settings
from app.db import get_db_pool

# =====================================================================

_IS_SCANNING = False
_SCAN_PROGRESS = {"scanned": 0, "total": 0, "found_reachable": 0, "found_unreachable": 0}

# =====================================================================

async def get_audience_overview() -> Dict[str, Any]:
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        total_users = await conn.fetchval("SELECT COUNT(*) FROM users") or 0
        reachable_count = await conn.fetchval("SELECT COUNT(*) FROM users WHERE reachable_status = 'REACHABLE'") or 0
        unreachable_count = await conn.fetchval("SELECT COUNT(*) FROM users WHERE reachable_status = 'UNREACHABLE'") or 0
        blocked_count = await conn.fetchval("SELECT COUNT(*) FROM users WHERE reachable_status = 'BLOCKED'") or 0
        pending_count = await conn.fetchval("SELECT COUNT(*) FROM users WHERE reachable_status = 'PENDING' OR reachable_status IS NULL") or 0
        last_checked = await conn.fetchval("SELECT MAX(reachable_checked_at) FROM users WHERE reachable_checked_at IS NOT NULL")

    pct = round((reachable_count / total_users) * 100.0, 1) if total_users > 0 else 0.0

    return {
        "total_users": total_users,
        "reachable_count": reachable_count,
        "unreachable_count": unreachable_count,
        "blocked_count": blocked_count,
        "pending_count": pending_count,
        "reachable_percent": pct,
        "is_scanning": _IS_SCANNING,
        "scan_progress": _SCAN_PROGRESS,
        "last_checked_at": last_checked.isoformat() if last_checked else None,
        "bot_username": settings.bot_name or "ChezRheyy2Bot"
    }

# =====================================================================

async def mark_user_reachable(user_id: int) -> None:
    try:
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            await conn.execute("""
                UPDATE users 
                SET reachable_status = 'REACHABLE', reachable_checked_at = NOW() 
                WHERE id = $1
            """, user_id)
    except Exception:
        pass

# =====================================================================

async def run_audience_scan(batch_size: int = 50, rate_limit_delay: float = 0.25) -> None:
    global _IS_SCANNING, _SCAN_PROGRESS
    if _IS_SCANNING:
        return

    _IS_SCANNING = True
    bot_token = settings.telegram_bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        _IS_SCANNING = False
        return

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        token_row = await conn.fetchval("SELECT general->>'telegramBotToken' FROM settings WHERE id = 'global'")
        active_token = token_row or bot_token

        limit_clause = f"LIMIT {batch_size}" if batch_size > 0 else ""
        users_to_scan = await conn.fetch(f"""
            SELECT id, username 
            FROM users 
            WHERE reachable_status = 'PENDING' OR reachable_status IS NULL
            ORDER BY updated_at DESC
            {limit_clause}
        """)

    total_to_scan = len(users_to_scan)
    _SCAN_PROGRESS = {
        "scanned": 0,
        "total": total_to_scan,
        "found_reachable": 0,
        "found_unreachable": 0
    }

    if total_to_scan == 0:
        _IS_SCANNING = False
        return

    async with httpx.AsyncClient(timeout=8.0) as client:
        for u in users_to_scan:
            user_id = u["id"]
            new_status = "PENDING"
            extra_username = None

            try:
                resp = await client.post(
                    f"https://api.telegram.org/bot{active_token}/getChat",
                    json={"chat_id": user_id}
                )
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get("ok"):
                        new_status = "REACHABLE"
                        _SCAN_PROGRESS["found_reachable"] += 1
                        chat_info = data.get("result", {})
                        extra_username = chat_info.get("username")
                elif resp.status_code == 400:
                    new_status = "UNREACHABLE"
                    _SCAN_PROGRESS["found_unreachable"] += 1
                elif resp.status_code == 403:
                    new_status = "BLOCKED"
                    _SCAN_PROGRESS["found_unreachable"] += 1
                elif resp.status_code == 429:
                    retry_sec = 2.0
                    try:
                        retry_sec = float(resp.json().get("parameters", {}).get("retry_after", 2.0))
                    except Exception:
                        pass
                    await asyncio.sleep(retry_sec + 0.5)
                    resp = await client.post(
                        f"https://api.telegram.org/bot{active_token}/getChat",
                        json={"chat_id": user_id}
                    )
                    if resp.status_code == 200:
                        new_status = "REACHABLE"
                        _SCAN_PROGRESS["found_reachable"] += 1
                    elif resp.status_code in (400, 403):
                        new_status = "UNREACHABLE" if resp.status_code == 400 else "BLOCKED"
                        _SCAN_PROGRESS["found_unreachable"] += 1
            except Exception:
                pass

            if new_status != "PENDING":
                try:
                    async with pool.acquire() as conn:
                        if extra_username:
                            await conn.execute("""
                                UPDATE users 
                                SET reachable_status = $1, reachable_checked_at = NOW(), username = COALESCE(username, $2)
                                WHERE id = $3
                            """, new_status, extra_username, user_id)
                        else:
                            await conn.execute("""
                                UPDATE users 
                                SET reachable_status = $1, reachable_checked_at = NOW() 
                                WHERE id = $2
                            """, new_status, user_id)
                except Exception:
                    pass

            _SCAN_PROGRESS["scanned"] += 1
            await asyncio.sleep(rate_limit_delay)

    _IS_SCANNING = False

# =====================================================================

async def reset_audience_statuses() -> None:
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        await conn.execute("""
            UPDATE users 
            SET reachable_status = 'PENDING', reachable_checked_at = NULL
        """)
        await conn.execute("""
            UPDATE users 
            SET reachable_status = 'REACHABLE', reachable_checked_at = NOW()
            WHERE id IN (
                SELECT DISTINCT user_id 
                FROM bot_logs 
                WHERE created_at > NOW() - INTERVAL '48 hours'
            )
        """)
