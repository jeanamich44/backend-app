import os
import re
import json
import html
import uuid
from typing import Optional, Dict, Any, List, Tuple
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Header, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.auth import get_current_user, validate_telegram_init_data
from app.db import get_db_pool
from app.services.telegram import (
    send_telegram_message,
    send_telegram_media_group
)
from app.services.cache import get_cached_service, get_cached_active_admins

# =====================================================================

router = APIRouter(prefix="/api/amendes", tags=["amendes"])

# =====================================================================

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads", "amendes")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024

# =====================================================================

class PayAmendePayload(BaseModel):
    amendeId: Optional[str] = None
    amende_id: Optional[str] = None

# =====================================================================

def _sanitize_filename(name: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_\-\.]", "_", name)
    return cleaned[:100]

# =====================================================================

@router.get("/list")
async def list_user_amendes(user: Dict[str, Any] = Depends(get_current_user)):
    user_id = user["id"]
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT id, status, price, file_urls, note, admin_notes, created_at, updated_at
            FROM amendes
            WHERE user_id = $1
            ORDER BY created_at DESC
        """, user_id)

        amendes = []
        for r in rows:
            raw_urls = r["file_urls"]
            while isinstance(raw_urls, str):
                try:
                    raw_urls = json.loads(raw_urls)
                except Exception:
                    raw_urls = []
            if not isinstance(raw_urls, list):
                raw_urls = []
            clean_urls = [u.replace("/api/amendes/file/", "/api/proxy/amendes/file/") for u in raw_urls]

            amendes.append({
                "id": str(r["id"]),
                "status": r["status"],
                "price": float(r["price"]) if r["price"] is not None else None,
                "file_urls": clean_urls,
                "note": r["note"] or "",
                "admin_notes": r["admin_notes"] or "",
                "created_at": r["created_at"].isoformat() if r["created_at"] else None,
                "updated_at": r["updated_at"].isoformat() if r["updated_at"] else None
            })

        return {"amendes": amendes}

# =====================================================================

async def _notify_admins_new_amende(
    amende_id: uuid.UUID,
    decision_text: str,
    reply_markup: Dict[str, Any],
    telegram_files: List[Tuple[str, bytes, str]]
) -> None:
    admin_rows = await get_cached_active_admins()
    if not admin_rows:
        return

    msg_mappings: List[Dict[str, Any]] = []
    uploaded_media = None
    for r in admin_rows:
        aid = r["id"]
        if telegram_files:
            try:
                if not uploaded_media:
                    uploaded_media = await send_telegram_media_group(aid, files_list=telegram_files)
                else:
                    await send_telegram_media_group(aid, file_ids=uploaded_media)
            except Exception:
                pass
        try:
            res = await send_telegram_message(
                chat_id=aid,
                text=decision_text,
                reply_markup=reply_markup
            )
            if res and "message_id" in res:
                msg_mappings.append({"chat_id": aid, "message_id": res["message_id"]})
        except Exception:
            pass

    if msg_mappings:
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            await conn.execute(
                "UPDATE amendes SET telegram_message_ids = $1 WHERE id = $2",
                json.dumps(msg_mappings), amende_id
            )

# =====================================================================

@router.post("/submit")
async def submit_amende(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    note: Optional[str] = Form(None),
    user: Dict[str, Any] = Depends(get_current_user)
):
    service_info = await get_cached_service("amendes")
    if not service_info or not service_info.get("is_active"):
        raise HTTPException(
            status_code=403,
            detail="Le service d'annulation d'amende est temporairement suspendu."
        )

    if not files or len(files) == 0:
        raise HTTPException(status_code=400, detail="Veuillez fournir au moins un fichier.")
    if len(files) > 4:
        raise HTTPException(status_code=400, detail="Maximum 4 fichiers autorisés.")

    user_id = user["id"]
    sanitized_note = (note or "").strip()[:200]

    saved_urls: List[str] = []
    telegram_files: List[Tuple[str, bytes, str]] = []

    for f in files:
        ext = os.path.splitext(f.filename or "")[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Format non supporté ({f.filename}). Formats acceptés: JPEG, PNG, PDF."
            )

        content = await f.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Fichier trop volumineux ({f.filename}). Limite: 10 Mo par document."
            )

        safe_base = _sanitize_filename(f.filename or "amende_doc")
        unique_name = f"{uuid.uuid4().hex}_{safe_base}"
        target_path = os.path.join(UPLOAD_DIR, unique_name)

        with open(target_path, "wb") as out_f:
            out_f.write(content)

        file_url = f"/api/proxy/amendes/file/{unique_name}"
        saved_urls.append(file_url)

        mime = f.content_type or ("application/pdf" if ext == ".pdf" else "image/jpeg")
        telegram_files.append((safe_base, content, mime))

    amende_id = uuid.uuid4()
    pool = await get_db_pool()

    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO amendes (id, user_id, status, file_urls, note, telegram_message_ids, created_at, updated_at)
            VALUES ($1, $2, 'PENDING', $3, $4, '[]'::jsonb, NOW(), NOW())
        """, amende_id, user_id, json.dumps(saved_urls), sanitized_note)

    client_str = f"@{user['username']}" if user.get("username") else f"{user.get('first_name', '')} (ID: <code>{user_id}</code>)"
    safe_note = html.escape(sanitized_note) if sanitized_note else "<i>Aucune</i>"
    decision_text = (
        f"📑 <b>Nouvelle Demande d'Annulation d'Amende</b>\n\n"
        f"<b>ID Dossier</b> : <code>{amende_id}</code>\n"
        f"<b>Client</b> : {client_str}\n"
        f"<b>Documents</b> : {len(saved_urls)} pièce(s) jointe(s)\n"
        f"<b>Note</b> : {safe_note}\n\n"
        f"Veuillez valider ou refuser la prise en charge :"
    )

    reply_markup = {
        "inline_keyboard": [
            [
                {"text": "✅ Accepter", "callback_data": f"fine_yes:{amende_id}"},
                {"text": "❌ Refuser", "callback_data": f"fine_no:{amende_id}"}
            ]
        ]
    }

    background_tasks.add_task(
        _notify_admins_new_amende,
        amende_id,
        decision_text,
        reply_markup,
        telegram_files
    )

    return {
        "success": True,
        "amende_id": str(amende_id),
        "file_urls": saved_urls
    }

# =====================================================================

async def _notify_admins_payment(admin_ids: List[int], text: str) -> None:
    for aid in admin_ids:
        try:
            await send_telegram_message(chat_id=aid, text=text)
        except Exception:
            pass

# =====================================================================

@router.post("/pay")
async def pay_amende(
    payload: PayAmendePayload,
    background_tasks: BackgroundTasks,
    user: Dict[str, Any] = Depends(get_current_user)
):
    service_info = await get_cached_service("amendes")
    if not service_info or not service_info.get("is_active"):
        raise HTTPException(
            status_code=403,
            detail="Le service d'annulation d'amende est temporairement suspendu."
        )

    target_id_str = payload.amendeId or payload.amende_id
    if not target_id_str:
        raise HTTPException(status_code=400, detail="ID de dossier manquant.")

    try:
        amende_uuid = uuid.UUID(target_id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Format d'identifiant de dossier invalide.")

    user_id = user["id"]
    pool = await get_db_pool()

    async with pool.acquire() as conn:
        async with conn.transaction():
            amende_row = await conn.fetchrow("""
                SELECT id, user_id, status, price
                FROM amendes
                WHERE id = $1
                FOR UPDATE
            """, amende_uuid)

            if not amende_row or amende_row["user_id"] != user_id:
                raise HTTPException(status_code=404, detail="Dossier d'amende introuvable.")

            if amende_row["status"] == "PAID" or amende_row["status"] == "FINISHED":
                raise HTTPException(status_code=400, detail="Ce dossier a déjà été réglé.")

            if amende_row["status"] != "ACCEPTED":
                raise HTTPException(status_code=400, detail="Ce dossier n'est pas prêt pour le paiement.")

            price = float(amende_row["price"] or 0)
            if price <= 0:
                raise HTTPException(status_code=400, detail="Tarif non fixé pour ce dossier.")

            user_row = await conn.fetchrow("SELECT balance FROM users WHERE id = $1 FOR UPDATE", user_id)
            user_balance = float(user_row["balance"] or 0)

            if user_balance < price:
                raise HTTPException(
                    status_code=400,
                    detail=f"Solde insuffisant ({user_balance:.2f} € disponible, {price:.2f} € requis)."
                )

            await conn.execute("UPDATE users SET balance = balance - $1, updated_at = NOW() WHERE id = $2", price, user_id)

            await conn.execute("""
                UPDATE amendes
                SET status = 'PAID', updated_at = NOW()
                WHERE id = $1
            """, amende_uuid)

            await conn.execute("""
                INSERT INTO transactions (user_id, brand, code, pin, value, price, notes, created_at)
                VALUES ($1, 'amendes', $2, 'PAID', $3, $3, $4, NOW())
            """, user_id, str(amende_uuid), price, f"Annulation amende dossier {amende_uuid}")

            new_bal_row = await conn.fetchval("SELECT balance FROM users WHERE id = $1", user_id)
            new_balance = float(new_bal_row or 0)

    admin_rows = await get_cached_active_admins()

    client_display = f"@{user['username']}" if user.get("username") else f"{user.get('first_name', '')} (<code>{user_id}</code>)"
    admin_notify_text = (
        f"💳 <b>Amende Réglée par le Client !</b>\n\n"
        f"<b>Dossier</b> : <code>{amende_uuid}</code>\n"
        f"<b>Client</b> : {client_display}\n"
        f"<b>Montant débité</b> : {price:.2f} €\n"
        f"<b>Statut</b> : PAID\n\n"
        f"<i>Le traitement de l'annulation peut commencer.</i>"
    )

    admin_ids = [r["id"] for r in admin_rows]
    background_tasks.add_task(_notify_admins_payment, admin_ids, admin_notify_text)

    return {
        "success": True,
        "new_balance": new_balance,
        "status": "PAID"
    }

# =====================================================================

@router.get("/file/{filename}")
async def get_amende_file(
    filename: str,
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data"),
    authorization: Optional[str] = Header(None, alias="Authorization")
):
    if not x_telegram_init_data and not authorization:
        raise HTTPException(status_code=401, detail="Authentification requise.")

    if not re.match(r"^[a-zA-Z0-9_\-\.]+$", filename):
        raise HTTPException(status_code=400, detail="Nom de fichier invalide.")

    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier introuvable.")

    ext = os.path.splitext(filename)[1].lower()
    media_type = "application/pdf" if ext == ".pdf" else "image/jpeg" if ext in (".jpg", ".jpeg") else "image/png" if ext == ".png" else "application/octet-stream"

    return FileResponse(file_path, media_type=media_type, content_disposition_type="inline")
