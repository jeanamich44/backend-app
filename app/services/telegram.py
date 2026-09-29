import httpx
import logging
from typing import Optional, Dict, Any, List
from app.config import settings

# =====================================================================

logger = logging.getLogger(__name__)

# =====================================================================

async def send_telegram_message(
    chat_id: int | str,
    text: str,
    reply_markup: Optional[Dict[str, Any]] = None,
    parse_mode: str = "HTML"
) -> bool:
    if not settings.telegram_bot_token:
        logger.error("telegram_bot_token non configure")
        return False

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    payload: Dict[str, Any] = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code != 200:
                logger.error(f"Erreur Telegram sendMessage: {resp.status_code} - {resp.text}")
                return False
            return True
    except Exception as e:
        logger.error(f"Exception Telegram sendMessage: {e}")
        return False

# =====================================================================

async def set_telegram_webhook(webhook_url: str, secret_token: str) -> Dict[str, Any]:
    if not settings.telegram_bot_token:
        raise ValueError("telegram_bot_token non configure")

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/setWebhook"
    payload = {
        "url": webhook_url,
        "secret_token": secret_token,
        "allowed_updates": ["message", "callback_query"],
        "drop_pending_updates": True
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(url, json=payload)
        return resp.json()

# =====================================================================

async def set_telegram_commands() -> Dict[str, Any]:
    if not settings.telegram_bot_token:
        raise ValueError("telegram_bot_token non configure")

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/setMyCommands"
    payload = {
        "commands": [
            {"command": "start", "description": "Démarrer le bot et ouvrir l'application"}
        ]
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(url, json=payload)
        return resp.json()

# =====================================================================

async def set_telegram_menu_button(web_app_url: str) -> Dict[str, Any]:
    if not settings.telegram_bot_token:
        raise ValueError("telegram_bot_token non configure")

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/setChatMenuButton"
    payload = {
        "menu_button": {
            "type": "web_app",
            "text": "Ouvrir",
            "web_app": {
                "url": web_app_url
            }
        }
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(url, json=payload)
        return resp.json()
