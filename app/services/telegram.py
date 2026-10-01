import json
import logging
from typing import Optional, Dict, Any, List, Tuple
import httpx
from app.config import settings

# =====================================================================

logger = logging.getLogger(__name__)
_telegram_client: Optional[httpx.AsyncClient] = None

# =====================================================================

def _get_client() -> httpx.AsyncClient:
    global _telegram_client
    if _telegram_client is None or _telegram_client.is_closed:
        _telegram_client = httpx.AsyncClient(timeout=30.0)
    return _telegram_client

# =====================================================================

async def send_telegram_message(
    chat_id: int | str,
    text: str,
    reply_markup: Optional[Dict[str, Any]] = None,
    parse_mode: str = "HTML"
) -> Optional[Dict[str, Any]]:
    if not settings.telegram_bot_token:
        logger.error("telegram_bot_token non configure")
        return None

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    payload: Dict[str, Any] = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        client = _get_client()
        resp = await client.post(url, json=payload)
        if resp.status_code != 200:
            logger.error(f"Erreur Telegram sendMessage: {resp.status_code} - {resp.text}")
            return None
        data = resp.json()
        return data.get("result")
    except Exception as e:
        logger.error(f"Exception Telegram sendMessage: {e}")
        return None

# =====================================================================

async def edit_telegram_message_text(
    chat_id: int | str,
    message_id: int | str,
    text: str,
    reply_markup: Optional[Dict[str, Any]] = None,
    parse_mode: str = "HTML"
) -> bool:
    if not settings.telegram_bot_token:
        logger.error("telegram_bot_token non configure")
        return False

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/editMessageText"
    payload: Dict[str, Any] = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": parse_mode
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        client = _get_client()
        resp = await client.post(url, json=payload)
        if resp.status_code != 200:
            logger.error(f"Erreur Telegram editMessageText: {resp.status_code} - {resp.text}")
            return False
        return True
    except Exception as e:
        logger.error(f"Exception Telegram editMessageText: {e}")
        return False

# =====================================================================

async def answer_callback_query(
    callback_query_id: str,
    text: Optional[str] = None,
    show_alert: bool = False
) -> bool:
    if not settings.telegram_bot_token:
        return False

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/answerCallbackQuery"
    payload: Dict[str, Any] = {
        "callback_query_id": callback_query_id,
        "show_alert": show_alert
    }
    if text:
        payload["text"] = text

    try:
        client = _get_client()
        resp = await client.post(url, json=payload)
        return resp.status_code == 200
    except Exception as e:
        logger.error(f"Exception answerCallbackQuery: {e}")
        return False

# =====================================================================

async def send_telegram_photo(
    chat_id: int | str,
    filename: str,
    content_bytes: bytes,
    caption: Optional[str] = None
) -> Optional[str]:
    if not settings.telegram_bot_token:
        return None

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendPhoto"
    data: Dict[str, Any] = {"chat_id": str(chat_id)}
    if caption:
        data["caption"] = caption
        data["parse_mode"] = "HTML"

    files = {"photo": (filename, content_bytes)}
    try:
        client = _get_client()
        resp = await client.post(url, data=data, files=files)
        if resp.status_code == 200:
            result = resp.json().get("result", {})
            photos = result.get("photo", [])
            if photos:
                return photos[-1].get("file_id")
        return None
    except Exception as e:
        logger.error(f"Exception sendPhoto: {e}")
        return None

# =====================================================================

async def send_telegram_document(
    chat_id: int | str,
    filename: str,
    content_bytes: bytes,
    mime_type: str = "application/octet-stream",
    caption: Optional[str] = None
) -> Optional[str]:
    if not settings.telegram_bot_token:
        return None

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendDocument"
    data: Dict[str, Any] = {"chat_id": str(chat_id)}
    if caption:
        data["caption"] = caption
        data["parse_mode"] = "HTML"

    files = {"document": (filename, content_bytes, mime_type)}
    try:
        client = _get_client()
        resp = await client.post(url, data=data, files=files)
        if resp.status_code == 200:
            result = resp.json().get("result", {})
            doc = result.get("document", {})
            return doc.get("file_id")
        return None
    except Exception as e:
        logger.error(f"Exception sendDocument: {e}")
        return None

# =====================================================================

async def send_telegram_media_group(
    chat_id: int | str,
    files_list: Optional[List[Tuple[str, bytes, str]]] = None,
    file_ids: Optional[List[Tuple[str, str]]] = None
) -> Optional[List[Tuple[str, str]]]:
    if not settings.telegram_bot_token:
        return None

    client = _get_client()
    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMediaGroup"

    if file_ids:
        media_array = [{"type": m_type, "media": f_id} for m_type, f_id in file_ids]
        try:
            resp = await client.post(url, json={"chat_id": str(chat_id), "media": media_array})
            return file_ids if resp.status_code == 200 else None
        except Exception as e:
            logger.error(f"Exception sendMediaGroup file_ids: {e}")
            return None

    if not files_list:
        return None

    if len(files_list) == 1:
        fname, fbytes, ftype = files_list[0]
        if ftype.startswith("image/"):
            fid = await send_telegram_photo(chat_id, fname, fbytes)
            if fid:
                return [("photo", fid)]
        fid = await send_telegram_document(chat_id, fname, fbytes, ftype)
        return [("document", fid)] if fid else None

    all_photos = all(mime.startswith("image/") for _, _, mime in files_list)
    media_type = "photo" if all_photos else "document"

    media_array = []
    files_payload: Dict[str, Tuple[str, bytes, str]] = {}

    for idx, (filename, content_bytes, mime_type) in enumerate(files_list):
        attach_key = f"doc_{idx}"
        media_array.append({
            "type": media_type,
            "media": f"attach://{attach_key}"
        })
        files_payload[attach_key] = (filename, content_bytes, mime_type)

    data_payload = {
        "chat_id": str(chat_id),
        "media": json.dumps(media_array)
    }

    try:
        resp = await client.post(url, data=data_payload, files=files_payload)
        if resp.status_code != 200:
            logger.error(f"Erreur Telegram sendMediaGroup: {resp.status_code} - {resp.text}")
            return None

        result_msgs = resp.json().get("result", [])
        extracted: List[Tuple[str, str]] = []
        for msg in result_msgs:
            if "photo" in msg and msg["photo"]:
                extracted.append(("photo", msg["photo"][-1]["file_id"]))
            elif "document" in msg and msg["document"]:
                extracted.append(("document", msg["document"]["file_id"]))
        return extracted if extracted else None
    except Exception as e:
        logger.error(f"Exception sendMediaGroup: {e}")
        return None

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
    client = _get_client()
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
    client = _get_client()
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
    client = _get_client()
    resp = await client.post(url, json=payload)
    return resp.json()
