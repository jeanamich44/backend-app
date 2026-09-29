import html
import hmac
import json
import uuid
import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, Header, HTTPException, Request
from app.config import settings
from app.db import get_db_pool
from app.services.telegram import send_telegram_message

# =====================================================================

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/telegram", tags=["telegram"])

# =====================================================================

@router.post("/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: Optional[str] = Header(None, alias="X-Telegram-Bot-Api-Secret-Token")
):
    expected_secret = settings.internal_api_secret
    if not expected_secret or not x_telegram_bot_api_secret_token:
        raise HTTPException(status_code=403, detail="Forbidden")

    if not hmac.compare_digest(x_telegram_bot_api_secret_token, expected_secret):
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        update: Dict[str, Any] = await request.json()
    except Exception:
        return {"ok": True}

    message = update.get("message")
    if not message:
        return {"ok": True}

    chat = message.get("chat")
    from_user = message.get("from")
    if not chat or not from_user:
        return {"ok": True}

    chat_id = chat.get("id")
    user_id = from_user.get("id")
    username = from_user.get("username")
    first_name = from_user.get("first_name")
    last_name = from_user.get("last_name")
    text = (message.get("text") or "").strip()

    pool = await get_db_pool()
    async with pool.acquire() as conn:
        upsert_query = """
        INSERT INTO users (id, username, first_name, last_name, updated_at)
        VALUES ($1, $2, $3, $4, NOW())
        ON CONFLICT (id) DO UPDATE SET
            username = EXCLUDED.username,
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            updated_at = NOW()
        RETURNING is_banned;
        """
        user_row = await conn.fetchrow(upsert_query, user_id, username, first_name, last_name)
        if user_row and user_row["is_banned"]:
            ban_msg = "⚠️ <b>Votre compte est suspendu.</b>\nVeuillez contacter le support pour toute réclamation."
            await send_telegram_message(chat_id=chat_id, text=ban_msg)
            return {"ok": True}

        if text.startswith("/start"):
            await conn.execute(
                "INSERT INTO bot_logs (id, user_id, action, details, created_at) VALUES ($1, $2, $3, $4, NOW())",
                uuid.uuid4(),
                user_id,
                "START",
                json.dumps({"username": username, "first_name": first_name, "chat_id": chat_id})
            )

            safe_name = html.escape(first_name or "Cher client")
            safe_bot = html.escape(settings.bot_name or "ChezRheyy")
            welcome_text = (
                f"👋 Bonjour <b>{safe_name}</b> !\n\n"
                f"Bienvenue sur <b>{safe_bot}</b>.\n"
                f"Accédez à nos services et gérez votre compte directement depuis notre application :"
            )

            inline_keyboard = [
                [
                    {
                        "text": "🚀 Ouvrir l'application",
                        "web_app": {"url": settings.frontend_url}
                    }
                ]
            ]
            if settings.support_telegram:
                supp = settings.support_telegram.lstrip("@")
                inline_keyboard.append([
                    {
                        "text": "💬 Support",
                        "url": f"https://t.me/{supp}"
                    }
                ])

            reply_markup = {"inline_keyboard": inline_keyboard}
            await send_telegram_message(chat_id=chat_id, text=welcome_text, reply_markup=reply_markup)
            return {"ok": True}

        safe_bot = html.escape(settings.bot_name or "ChezRheyy")
        default_text = (
            f"Pour accéder à vos commandes et aux services de <b>{safe_bot}</b>, cliquez ci-dessous :"
        )
        default_kb = [
            [
                {
                    "text": "🚀 Ouvrir l'application",
                    "web_app": {"url": settings.frontend_url}
                }
            ]
        ]
        if settings.support_telegram:
            supp = settings.support_telegram.lstrip("@")
            default_kb.append([
                {
                    "text": "💬 Support",
                    "url": f"https://t.me/{supp}"
                }
            ])
        await send_telegram_message(chat_id=chat_id, text=default_text, reply_markup={"inline_keyboard": default_kb})

    return {"ok": True}
