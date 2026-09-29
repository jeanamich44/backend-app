import asyncio
import html
import hmac
import json
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from zoneinfo import ZoneInfo
import httpx
from fastapi import APIRouter, Header, HTTPException, Request
from app.config import settings
from app.db import get_db_pool
from app.services.telegram import send_telegram_message

# =====================================================================

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/telegram", tags=["telegram"])

# =====================================================================

DEFAULT_ADMIN_IDS = [8740419947, 6298536933, 8676919760, 5883885733, 1461973886]
env_admin_ids = os.getenv("TELEGRAM_ADMIN_IDS", "")
if env_admin_ids.strip():
    try:
        TELEGRAM_ADMIN_IDS = [int(x.strip()) for x in env_admin_ids.split(",") if x.strip()]
    except Exception:
        TELEGRAM_ADMIN_IDS = DEFAULT_ADMIN_IDS
else:
    TELEGRAM_ADMIN_IDS = DEFAULT_ADMIN_IDS

ADMIN_COMMANDS = [
    "/addmoney",
    "/removemoney",
    "/ban",
    "/deban",
    "/stat",
    "/commandes",
    "/info",
    "/crypto",
    "/message",
    "/maintenance",
    "/panel",
    "/bank",
    "/compteapi",
    "/comptepanel",
    "/demoiptv",
    "/help"
]

HELP_DETAILS = {
    "addmoney": (
        "Ajoute du solde en euros à un utilisateur Telegram.",
        "/addmoney <id> <montant>",
        "/addmoney 123456789 25"
    ),
    "removemoney": (
        "Retire du solde en euros à un utilisateur.",
        "/removemoney <id> <montant>",
        "/removemoney 123456789 10"
    ),
    "ban": (
        "Bannit un utilisateur avec une raison optionnelle.",
        "/ban <id> [raison]",
        "/ban 123456789 ou /ban 123456789 Fraude"
    ),
    "deban": (
        "Débannit un utilisateur préalablement banni.",
        "/deban <id>",
        "/deban 123456789"
    ),
    "stat": (
        "Affiche les statistiques globales des ventes et le CA par marque depuis la BDD.",
        "/stat",
        "/stat"
    ),
    "commandes": (
        "Recherche l'historique des achats par ID utilisateur, nom de marque ou code carte.",
        "/commandes [id|marque|code] [jours]",
        "/commandes 123456789 ou /commandes carr 14"
    ),
    "info": (
        "Affiche les informations d'un utilisateur (solde, nombre d'achats, statut banni).",
        "/info <id>",
        "/info 123456789"
    ),
    "crypto": (
        "Interroge l'API OxaPay pour connaître le statut en direct d'une transaction.",
        "/crypto <trackId>",
        "/crypto track_123456"
    ),
    "message": (
        "Envoie un message de diffusion (broadcast) à tous les utilisateurs du bot.",
        "/message - <texte>",
        "/message - Bonjour à tous !"
    ),
    "maintenance": (
        "Active ou désactive le mode maintenance du bot et de la TMA.",
        "/maintenance [on|off]",
        "/maintenance on ou /maintenance off"
    ),
    "panel": (
        "Affiche l'URL secrète d'accès au Panel d'Administration Web.",
        "/panel",
        "/panel"
    ),
    "bank": (
        "Affiche ou modifie la banque active pour les paiements SumUp.",
        "/bank [1|2]",
        "/bank 1 ou /bank 2"
    ),
    "compteapi": (
        "Affiche ou change le compte API IPTV actif (abonnements payants 1/3/6/12 mois).",
        "/compteapi [n°|nom]",
        "/compteapi 2"
    ),
    "comptepanel": (
        "Affiche ou change le compte panel IPTV actif (pour les démos TMA).",
        "/comptepanel [n°|nom]",
        "/comptepanel 1"
    ),
    "demoiptv": (
        "Active ou désactive le bouton d'achat démo IPTV dans la Mini App.",
        "/demoiptv [on|off]",
        "/demoiptv on ou /demoiptv off"
    ),
    "help": (
        "Affiche l'aide des commandes administration.",
        "/help [commande|all]",
        "/help stat ou /help all"
    )
}

# =====================================================================

def _parse_json(val: Any) -> Dict[str, Any]:
    if not val:
        return {}
    res = val
    while isinstance(res, str):
        try:
            res = json.loads(res)
        except Exception:
            return {}
    return res if isinstance(res, dict) else {}

def _escape_html(text: Any) -> str:
    if text is None:
        return ""
    return html.escape(str(text))

async def _notify_admins(text: str, exclude_id: Optional[int] = None) -> None:
    for aid in TELEGRAM_ADMIN_IDS:
        if exclude_id and aid == exclude_id:
            continue
        try:
            await send_telegram_message(chat_id=aid, text=text)
        except Exception:
            pass

# =====================================================================

async def _handle_addmoney(chat_id: int, admin_id: int, admin_username: Optional[str], args: List[str], conn: Any) -> None:
    if len(args) < 2:
        await send_telegram_message(chat_id, "Erreur: Mauvais format ex: /addmoney <id> <montant>")
        return
    try:
        target_id = int(args[0])
        amount = float(args[1].replace(",", "."))
        if amount <= 0:
            raise ValueError()
    except Exception:
        await send_telegram_message(chat_id, "Erreur: Mauvais format ex: /addmoney <id> <montant>")
        return

    row = await conn.fetchrow(
        "UPDATE users SET balance = balance + $1, updated_at = NOW() WHERE id = $2 RETURNING balance",
        amount, target_id
    )
    if not row:
        await send_telegram_message(chat_id, f"❌ Utilisateur <code>{target_id}</code> introuvable en BDD.")
        return

    new_balance = float(row["balance"] or 0)
    try:
        await send_telegram_message(target_id, f"💰 {amount:g}€ reçus sur votre solde.")
    except Exception:
        pass

    pseudo_str = f"@{admin_username}" if admin_username else "Admin"
    resp = (
        f"💰 <b>[ADMIN] Ajout de Solde</b>\n"
        f"<b>User</b>: <code>{target_id}</code>\n"
        f"<b>Montant</b>: +{amount:g}€\n"
        f"<b>Nouveau Solde</b>: {new_balance:.2f}€\n"
        f"<b>Par</b>: {pseudo_str} (<code>{admin_id}</code>)"
    )
    await send_telegram_message(chat_id, resp)
    await _notify_admins(resp, exclude_id=chat_id)

# =====================================================================

async def _handle_removemoney(chat_id: int, admin_id: int, admin_username: Optional[str], args: List[str], conn: Any) -> None:
    if len(args) < 2:
        await send_telegram_message(chat_id, "Erreur: Mauvais format ex: /removemoney <id> <montant>")
        return
    try:
        target_id = int(args[0])
        amount = float(args[1].replace(",", "."))
        if amount <= 0:
            raise ValueError()
    except Exception:
        await send_telegram_message(chat_id, "Erreur: Mauvais format ex: /removemoney <id> <montant>")
        return

    row = await conn.fetchrow(
        "UPDATE users SET balance = GREATEST(0, balance - $1), updated_at = NOW() WHERE id = $2 RETURNING balance",
        amount, target_id
    )
    if not row:
        await send_telegram_message(chat_id, f"❌ Utilisateur <code>{target_id}</code> introuvable en BDD.")
        return

    new_balance = float(row["balance"] or 0)
    try:
        await send_telegram_message(target_id, f"📉 {amount:g}€ retirés de votre solde. Nouveau solde : {new_balance:.2f}€.")
    except Exception:
        pass

    pseudo_str = f"@{admin_username}" if admin_username else "Admin"
    resp = (
        f"📉 <b>[ADMIN] Retrait de Solde</b>\n"
        f"<b>User</b>: <code>{target_id}</code>\n"
        f"<b>Montant</b>: -{amount:g}€\n"
        f"<b>Nouveau Solde</b>: {new_balance:.2f}€\n"
        f"<b>Par</b>: {pseudo_str} (<code>{admin_id}</code>)"
    )
    await send_telegram_message(chat_id, resp)
    await _notify_admins(resp, exclude_id=chat_id)

# =====================================================================

async def _handle_ban(chat_id: int, args: List[str], conn: Any) -> None:
    if len(args) < 1:
        await send_telegram_message(chat_id, "Erreur: Mauvais format ex: /ban <id> [raison]")
        return
    try:
        target_id = int(args[0])
    except Exception:
        await send_telegram_message(chat_id, "Erreur: Mauvais format ex: /ban <id> [raison]")
        return

    reason = " ".join(args[1:]).strip() if len(args) > 1 else ""
    await conn.execute("""
        INSERT INTO users (id, is_banned, updated_at)
        VALUES ($1, TRUE, NOW())
        ON CONFLICT (id) DO UPDATE SET is_banned = TRUE, updated_at = NOW()
    """, target_id)

    await conn.execute(
        "INSERT INTO bot_logs (id, user_id, action, details, created_at) VALUES ($1, $2, 'BAN', $3, NOW())",
        uuid.uuid4(), target_id, json.dumps({"reason": reason})
    )

    resp = f"L'ID {target_id} a bien été banni." + (f"\nRaison : {reason}" if reason else "")
    await send_telegram_message(chat_id, resp)
    await _notify_admins(f"BAN USER: {target_id}\nRaison: {reason or 'Aucune'}", exclude_id=chat_id)

# =====================================================================

async def _handle_deban(chat_id: int, args: List[str], conn: Any) -> None:
    if len(args) < 1:
        await send_telegram_message(chat_id, "Erreur: Mauvais format ex: /deban <id>")
        return
    try:
        target_id = int(args[0])
    except Exception:
        await send_telegram_message(chat_id, "Erreur: Mauvais format ex: /deban <id>")
        return

    await conn.execute("UPDATE users SET is_banned = FALSE, updated_at = NOW() WHERE id = $1", target_id)
    await conn.execute(
        "INSERT INTO bot_logs (id, user_id, action, details, created_at) VALUES ($1, $2, 'DEBAN', '{}', NOW())",
        uuid.uuid4(), target_id
    )

    resp = f"L'ID {target_id} a bien été débanni."
    await send_telegram_message(chat_id, resp)
    await _notify_admins(f"DEBAN USER: {target_id}", exclude_id=chat_id)

# =====================================================================

async def _handle_stat(chat_id: int, conn: Any) -> None:
    rows = await conn.fetch("""
        SELECT brand, COUNT(*) as count, COALESCE(SUM(price), 0) as total
        FROM transactions
        GROUP BY brand
        ORDER BY total DESC
    """)
    total_users = await conn.fetchval("SELECT COUNT(*) FROM users") or 0

    lines = ["📊 <b>Statistiques des ventes (BDD PostgreSQL) :</b>\n"]
    if not rows:
        lines.append("Aucune vente enregistrée.")
    else:
        grand_total_sales = 0
        grand_total_ca = 0.0
        for r in rows:
            b_name = (r["brand"] or "Inconnu").upper()
            c = int(r["count"])
            t = float(r["total"])
            grand_total_sales += c
            grand_total_ca += t
            lines.append(f"• <b>{b_name}</b> → {c} ventes, total = {t:.2f}€")

        lines.append(f"\n<b>Total global :</b> {grand_total_sales} ventes | {grand_total_ca:.2f}€")
        lines.append(f"<b>Utilisateurs enregistrés :</b> {total_users}")

    await send_telegram_message(chat_id, "\n".join(lines))

# =====================================================================

async def _handle_commandes(chat_id: int, args: List[str], conn: Any) -> None:
    days = 7
    search_arg: Optional[str] = None
    show_all = False

    if len(args) == 0:
        show_all = True
        days = 1
    elif len(args) == 1:
        search_arg = args[0].strip()
    else:
        search_arg = args[0].strip()
        try:
            d = int(args[1].strip())
            if 0 < d <= 3650:
                days = d
        except Exception:
            pass

    if show_all:
        search_title = "Global (Tous clients - 24h Max)"
        rows = await conn.fetch("""
            SELECT brand, code, pin, value, price, created_at, user_id
            FROM transactions
            WHERE created_at >= NOW() - INTERVAL '1 day'
            ORDER BY created_at DESC
            LIMIT 100
        """)
    else:
        search_title = search_arg or ""
        search_uid = int(search_arg) if search_arg and search_arg.isdigit() else 0
        rows = await conn.fetch("""
            SELECT brand, code, pin, value, price, created_at, user_id
            FROM transactions
            WHERE created_at >= NOW() - ($1 || ' days')::INTERVAL
              AND (user_id = $2 OR LOWER(brand) = LOWER($3) OR code ILIKE '%' || $3 || '%')
            ORDER BY created_at DESC
            LIMIT 100
        """, str(days), search_uid, search_arg)

    if not rows:
        header_days = "24h" if days == 1 else f"{days} jours"
        await send_telegram_message(
            chat_id,
            f"⚠️ <b>Aucune commande trouvée pour :</b> <code>{_escape_html(search_title)}</code> <i>(sur {header_days})</i>"
        )
        return

    grouped: Dict[str, List[Any]] = {}
    for r in rows:
        b = (r["brand"] or "PRODUIT").upper()
        grouped.setdefault(b, []).append(r)

    paris_tz = ZoneInfo("Europe/Paris")
    lines = []

    for brand_key, tx_list in grouped.items():
        lines.append(f"📦 <b>{brand_key}</b> (<b>{len(tx_list)}</b>)")
        for tx in tx_list[:15]:
            dt_raw = tx["created_at"]
            if dt_raw:
                dt_paris = dt_raw.astimezone(paris_tz)
                date_str = dt_paris.strftime("%d/%m à %H:%M")
            else:
                date_str = "N/A"

            code_str = _escape_html(tx["code"] or "")
            pin_str = _escape_html(tx["pin"] or "")
            price_val = float(tx["price"] or 0)
            val_num = float(tx["value"]) if tx["value"] is not None else 0.0

            if (tx["brand"] or "").lower() == "iptv":
                lines.append(f"• <code>{code_str}</code> | {price_val:.2f}€ | <i>{date_str}</i>")
            elif val_num <= 0:
                pin_part = f" | <b>PIN :</b> <code>{pin_str}</code>" if pin_str else ""
                lines.append(f"• <code>{code_str}</code>{pin_part} | {price_val:.2f}€ | <i>{date_str}</i>")
            else:
                pin_part = f" | <b>PIN :</b> <code>{pin_str}</code>" if pin_str else ""
                lines.append(f"• <code>{code_str}</code>{pin_part} | {val_num:g}€ ({price_val:.2f}€) | <i>{date_str}</i>")

        if len(tx_list) > 15:
            lines.append(f"<i>... (+{len(tx_list) - 15} autres entrées)</i>")
        lines.append("")

    header_days = "Aujourd'hui (1 jour)" if days == 1 else f"{days} jours"
    summary_text = (
        f"📋 <b>Historique d'Achats :</b> <code>{_escape_html(search_title)}</code> "
        f"(Total: <b>{len(rows)}</b> | <b>{header_days}</b>)\n\n" + "\n".join(lines)
    )
    await send_telegram_message(chat_id, summary_text)

# =====================================================================

async def _handle_info(chat_id: int, args: List[str], conn: Any) -> None:
    if len(args) < 1:
        await send_telegram_message(chat_id, "Erreur format: /info <id>")
        return
    try:
        target_id = int(args[0])
    except Exception:
        await send_telegram_message(chat_id, "Erreur format: /info <id>")
        return

    row = await conn.fetchrow("""
        SELECT id, username, first_name, last_name, balance, is_banned, admin, created_at
        FROM users WHERE id = $1
    """, target_id)

    if not row:
        await send_telegram_message(chat_id, f"Erreur: {target_id} ID introuvable !!")
        return

    tx_stats = await conn.fetchrow("""
        SELECT COUNT(*) as count, COALESCE(SUM(price), 0) as total
        FROM transactions WHERE user_id = $1
    """, target_id)
    purchases_count = int(tx_stats["count"] or 0)
    purchases_total = float(tx_stats["total"] or 0)

    u_balance = float(row["balance"] or 0)
    is_ban = bool(row["is_banned"])
    is_adm = bool(row["admin"])
    u_name = _escape_html(row["username"] or "N/A")
    first = _escape_html(row["first_name"] or "")
    last = _escape_html(row["last_name"] or "")

    resp = (
        f"📋 <b>Informations Utilisateur :</b> <code>{target_id}</code>\n\n"
        f"• <b>Identité :</b> {first} {last} (@{u_name})\n"
        f"• <b>Achats :</b> {purchases_count} ({purchases_total:.2f}€)\n"
        f"• <b>Solde :</b> {u_balance:.2f}€\n"
        f"• <b>Admin :</b> {'OUI 🔑' if is_adm else 'NON'}\n"
        f"• <b>Banni :</b> {'OUI 🔴' if is_ban else 'NON 🟢'}"
    )
    await send_telegram_message(chat_id, resp)

# =====================================================================

async def _handle_crypto(chat_id: int, args: List[str], conn: Any) -> None:
    if len(args) < 1:
        await send_telegram_message(chat_id, "Erreur commandes: /crypto <trackId>")
        return

    track_id = args[0].strip()
    s_row = await conn.fetchrow("SELECT payments FROM settings WHERE id = 'global'")
    pay_data = _parse_json(s_row["payments"]) if s_row else {}
    api_key = pay_data.get("oxapayApiKey") or os.getenv("OXAPAY_API_KEY", "")

    if not api_key:
        await send_telegram_message(chat_id, "❌ Clé API OxaPay non configurée en base de données.")
        return

    url = f"https://api.oxapay.com/v1/payment/{track_id}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers={"merchant_api_key": api_key})
            if resp.status_code == 404:
                await send_telegram_message(chat_id, f"Transaction {track_id} introuvable.")
                return
            data_json = resp.json()
            data = data_json.get("data", {})
            st = data.get("status", "Inconnu")
            amt = data.get("amount", "0")
            await send_telegram_message(chat_id, f"Transaction {track_id} [Montant={amt}€ | Status={st}]")
    except Exception as e:
        await send_telegram_message(chat_id, f"❌ Erreur lors de la requête OxaPay : {str(e)}")

# =====================================================================

async def _handle_message(chat_id: int, full_text: str, conn: Any) -> None:
    dash_idx = full_text.find("-")
    if dash_idx == -1 or dash_idx + 1 >= len(full_text):
        await send_telegram_message(chat_id, "Erreur format: /message - <votre message>")
        return

    broadcast_content = full_text[dash_idx + 1:].strip()
    if not broadcast_content:
        await send_telegram_message(chat_id, "Erreur format: /message - <votre message>")
        return

    rows = await conn.fetch("SELECT id FROM users WHERE is_banned = FALSE")
    success_count = 0
    total_count = len(rows)

    for r in rows:
        uid = r["id"]
        try:
            ok = await send_telegram_message(chat_id=uid, text=broadcast_content)
            if ok:
                success_count += 1
            await asyncio.sleep(0.035)
        except Exception:
            pass

    await send_telegram_message(
        chat_id,
        f"✅ Message envoyé à {success_count}/{total_count} utilisateurs."
    )

# =====================================================================

async def _handle_maintenance(chat_id: int, args: List[str], conn: Any) -> None:
    s_row = await conn.fetchrow("SELECT general FROM settings WHERE id = 'global'")
    gen_data = _parse_json(s_row["general"]) if s_row else {}
    cur_state = bool(gen_data.get("maintenanceMode", False))

    if len(args) > 0:
        arg = args[0].strip().lower()
        if arg in ("on", "1", "true"):
            new_state = True
        elif arg in ("off", "0", "false"):
            new_state = False
        else:
            new_state = not cur_state
    else:
        new_state = not cur_state

    gen_data["maintenanceMode"] = new_state
    await conn.execute("UPDATE settings SET general = $1 WHERE id = 'global'", json.dumps(gen_data))
    await settings.load_from_db(conn)

    status_text = "ACTIVÉ 🔴" if new_state else "DÉSACTIVÉ 🟢"
    await send_telegram_message(chat_id, f"🛠️ Mode Maintenance : <b>{status_text}</b>")

# =====================================================================

async def _handle_panel(chat_id: int, conn: Any) -> None:
    s_row = await conn.fetchrow("SELECT security FROM settings WHERE id = 'global'")
    sec_data = _parse_json(s_row["security"]) if s_row else {}
    slug = (sec_data.get("adminSlug") or "admin").strip("/")
    base_url = settings.frontend_url.rstrip("/")
    full_url = f"{base_url}/{slug}/"
    await send_telegram_message(chat_id, f"🔑 <b>URL d'Accès au Panel Admin Web :</b>\n\n<code>{full_url}</code>")

# =====================================================================

async def _handle_bank(chat_id: int, args: List[str], conn: Any) -> None:
    s_row = await conn.fetchrow("SELECT payments FROM settings WHERE id = 'global'")
    pay_data = _parse_json(s_row["payments"]) if s_row else {}

    active_bank = pay_data.get("activeBank", "bank1")
    b1 = pay_data.get("bank1", {})
    b2 = pay_data.get("bank2", {})

    b1_name = b1.get("name") or "Banque 1"
    b1_email = b1.get("payToEmail") or "N/A"
    b2_name = b2.get("name") or "Banque 2"
    b2_email = b2.get("payToEmail") or "N/A"

    if len(args) == 0:
        cur_name = b2_name if active_bank == "bank2" else b1_name
        cur_email = b2_email if active_bank == "bank2" else b1_email
        txt = (
            f"🏦 <b>BANQUE SUMUP ACTUELLE</b>\n\n"
            f"• Banque active : <b>{_escape_html(cur_name)}</b>\n"
            f"• E-mail associé : <code>{_escape_html(cur_email)}</code>\n\n"
            f"<b>Changer de banque :</b>\n"
            f"• <code>/bank 1</code> : {_escape_html(b1_name)}\n"
            f"• <code>/bank 2</code> : {_escape_html(b2_name)}"
        )
        await send_telegram_message(chat_id, txt)
        return

    choice = args[0].strip().lower()
    if choice in ("1", "bank1", "sumup"):
        pay_data["activeBank"] = "bank1"
        await conn.execute("UPDATE settings SET payments = $1 WHERE id = 'global'", json.dumps(pay_data))
        await send_telegram_message(
            chat_id,
            f"✅ <b>Banque SumUp modifiée !</b>\n\nCompte actif : <b>{_escape_html(b1_name)}</b>\nE-mail : <code>{_escape_html(b1_email)}</code>"
        )
    elif choice in ("2", "bank2", "sumup_bank2"):
        pay_data["activeBank"] = "bank2"
        await conn.execute("UPDATE settings SET payments = $1 WHERE id = 'global'", json.dumps(pay_data))
        await send_telegram_message(
            chat_id,
            f"✅ <b>Banque SumUp modifiée !</b>\n\nCompte actif : <b>{_escape_html(b2_name)}</b>\nE-mail : <code>{_escape_html(b2_email)}</code>"
        )
    else:
        await send_telegram_message(chat_id, "❌ Choix invalide. Utilisez <code>/bank 1</code> ou <code>/bank 2</code>.")

# =====================================================================

async def _handle_compteapi(chat_id: int, args: List[str], conn: Any) -> None:
    row = await conn.fetchrow("SELECT config FROM services WHERE slug = 'iptv'")
    config = _parse_json(row["config"]) if row else {}
    accounts = config.get("accounts", [])

    if len(args) == 0:
        lines = ["📡 <b>COMPTES API IPTV</b>\n"]
        if not accounts:
            lines.append("Aucun compte configuré.")
        else:
            for idx, a in enumerate(accounts):
                nom = _escape_html(a.get("name") or f"Compte {idx + 1}")
                pack = _escape_html(a.get("pack") or "")
                actif = " — <b>ACTIF</b>" if a.get("active") else ""
                lines.append(f"{idx + 1}. {nom} | pack <code>{pack}</code>{actif}")
            lines.append("\nChanger : <code>/compteapi 1</code> ou <code>/compteapi Nom</code>")
        await send_telegram_message(chat_id, "\n".join(lines))
        return

    arg = args[0].strip()
    target_idx = -1
    if arg.isdigit():
        val = int(arg) - 1
        if 0 <= val < len(accounts):
            target_idx = val
    else:
        for idx, a in enumerate(accounts):
            if (a.get("name") or "").lower() == arg.lower():
                target_idx = idx
                break

    if target_idx == -1:
        await send_telegram_message(chat_id, f"❌ Compte API introuvable : <code>{_escape_html(arg)}</code>")
        return

    for idx, a in enumerate(accounts):
        a["active"] = (idx == target_idx)

    active_acc = accounts[target_idx]
    config["accounts"] = accounts
    config["api_key"] = active_acc.get("api_key", "")
    config["pack"] = active_acc.get("pack", "")
    config["package_id"] = active_acc.get("pack", "")
    config["bouquet"] = active_acc.get("pack", "")
    if active_acc.get("api_url"):
        config["api_url"] = active_acc.get("api_url")

    await conn.execute("UPDATE services SET config = $1 WHERE slug = 'iptv'", json.dumps(config))
    lbl = _escape_html(active_acc.get("name") or f"Compte {target_idx + 1}")
    await send_telegram_message(chat_id, f"✅ Compte API actif : <b>{lbl}</b>")

# =====================================================================

async def _handle_comptepanel(chat_id: int, args: List[str], conn: Any) -> None:
    row = await conn.fetchrow("SELECT config FROM services WHERE slug = 'iptv'")
    config = _parse_json(row["config"]) if row else {}
    panel_accounts = config.get("panel_accounts", [])

    if len(args) == 0:
        lines = ["🖥 <b>COMPTES PANEL IPTV</b>\n"]
        if not panel_accounts:
            lines.append("Aucun compte configuré.")
        else:
            for idx, p in enumerate(panel_accounts):
                nom = _escape_html(p.get("name") or p.get("username") or f"Compte {idx + 1}")
                user_str = _escape_html(p.get("username") or "")
                actif = " — <b>ACTIF</b>" if p.get("active") else ""
                lines.append(f"{idx + 1}. {nom} | user <code>{user_str}</code>{actif}")
            lines.append("\nChanger : <code>/comptepanel 1</code> ou <code>/comptepanel Nom</code>")
        await send_telegram_message(chat_id, "\n".join(lines))
        return

    arg = args[0].strip()
    target_idx = -1
    if arg.isdigit():
        val = int(arg) - 1
        if 0 <= val < len(panel_accounts):
            target_idx = val
    else:
        for idx, p in enumerate(panel_accounts):
            if (p.get("name") or "").lower() == arg.lower() or (p.get("username") or "").lower() == arg.lower():
                target_idx = idx
                break

    if target_idx == -1:
        await send_telegram_message(chat_id, f"❌ Compte panel introuvable : <code>{_escape_html(arg)}</code>")
        return

    for idx, p in enumerate(panel_accounts):
        p["active"] = (idx == target_idx)

    active_p = panel_accounts[target_idx]
    config["panel_accounts"] = panel_accounts
    config["username"] = active_p.get("username", "")
    config["password"] = active_p.get("password", "")

    await conn.execute("UPDATE services SET config = $1 WHERE slug = 'iptv'", json.dumps(config))
    lbl = _escape_html(active_p.get("name") or active_p.get("username") or f"Compte {target_idx + 1}")
    await send_telegram_message(chat_id, f"✅ Compte panel actif : <b>{lbl}</b>")

# =====================================================================

async def _handle_demoiptv(chat_id: int, args: List[str], conn: Any) -> None:
    row = await conn.fetchrow("SELECT config, prices FROM services WHERE slug = 'iptv'")
    config = _parse_json(row["config"]) if row else {}
    prices = _parse_json(row["prices"]) if row else {}

    raw_demo = config.get("demo_enabled")
    cur_state = str(raw_demo).strip().lower() in ("true", "1", "on")
    price_demo = prices.get("price_demo", 1)

    if len(args) == 0:
        etat = "ACTIVÉES 🟢" if cur_state else "DÉSACTIVÉES 🔴"
        txt = (
            f"📺 <b>ACHATS DÉMO IPTV</b>\n\n"
            f"État : <b>{etat}</b>\n"
            f"Prix : <b>{price_demo}€</b>\n\n"
            f"• <code>/demoiptv on</code> : afficher le bouton Démo et autoriser l'achat\n"
            f"• <code>/demoiptv off</code> : cacher le bouton et bloquer l'achat"
        )
        await send_telegram_message(chat_id, txt)
        return

    arg = args[0].strip().lower()
    if arg in ("on", "1", "true", "enable"):
        new_state = True
    elif arg in ("off", "0", "false", "disable"):
        new_state = False
    else:
        await send_telegram_message(chat_id, "❌ Utilise <code>/demoiptv on</code> ou <code>/demoiptv off</code>.")
        return

    config["demo_enabled"] = new_state
    await conn.execute("UPDATE services SET config = $1 WHERE slug = 'iptv'", json.dumps(config))
    status_text = "ACTIVÉES 🟢" if new_state else "DÉSACTIVÉES 🔴"
    await send_telegram_message(chat_id, f"📺 Achats démo IPTV : <b>{status_text}</b>")

# =====================================================================

async def _handle_help(chat_id: int, args: List[str]) -> None:
    if len(args) == 0:
        lines = ["📋 <b>Commandes Administrateur :</b>\n"]
        for cmd in ADMIN_COMMANDS:
            lines.append(f"• <code>{cmd}</code>")
        lines.append("\n💡 <i>Tapez <code>/help &lt;commande&gt;</code> pour voir la description et l'exemple.</i>")
        lines.append("💡 <i>Tapez <code>/help all</code> pour afficher le manuel complet.</i>")
        await send_telegram_message(chat_id, "\n".join(lines))
        return

    sub = args[0].strip().lstrip("/").lower()

    if sub == "all":
        lines = ["📖 <b>Manuel Complet des Commandes Administrateur</b>\n"]
        for cmd in ADMIN_COMMANDS:
            k = cmd.lstrip("/").lower()
            if k in HELP_DETAILS:
                desc, usg, ex = HELP_DETAILS[k]
                lines.append(f"🔹 <b>{cmd}</b>")
                lines.append(f"• <b>Description</b> : {_escape_html(desc)}")
                lines.append(f"• <b>Usage</b> : <code>{_escape_html(usg)}</code>")
                lines.append(f"• <b>Exemple</b> : <code>{_escape_html(ex)}</code>\n")
        await send_telegram_message(chat_id, "\n".join(lines))
        return

    if sub in HELP_DETAILS:
        desc, usg, ex = HELP_DETAILS[sub]
        lines = [
            f"ℹ️ <b>Aide pour la commande <code>/{sub}</code></b>\n",
            f"• <b>Description</b> : {_escape_html(desc)}",
            f"• <b>Usage</b> : <code>{_escape_html(usg)}</code>",
            f"• <b>Exemple</b> : <code>{_escape_html(ex)}</code>"
        ]
        await send_telegram_message(chat_id, "\n".join(lines))
    else:
        await send_telegram_message(
            chat_id,
            f"❌ Commande <code>/{_escape_html(sub)}</code> inconnue. Tapez <code>/help</code> pour la liste des commandes."
        )

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
        RETURNING is_banned, admin;
        """
        user_row = await conn.fetchrow(upsert_query, user_id, username, first_name, last_name)
        if user_row and user_row["is_banned"]:
            ban_msg = "⚠️ <b>Votre compte est suspendu.</b>\nVeuillez contacter le support pour toute réclamation."
            await send_telegram_message(chat_id=chat_id, text=ban_msg)
            return {"ok": True}

        is_admin = (user_id in TELEGRAM_ADMIN_IDS) or bool(user_row and user_row["admin"])

        if not is_admin:
            if text.startswith("/start"):
                await conn.execute(
                    "INSERT INTO bot_logs (id, user_id, action, details, created_at) VALUES ($1, $2, 'START', $3, NOW())",
                    uuid.uuid4(),
                    user_id,
                    json.dumps({"username": username, "first_name": first_name, "chat_id": chat_id})
                )
                safe_name = _escape_html(first_name or "Cher client")
                safe_bot = _escape_html(settings.bot_name or "ChezRheyy")
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
                await send_telegram_message(chat_id=chat_id, text=welcome_text, reply_markup={"inline_keyboard": inline_keyboard})
            return {"ok": True}

        if text.startswith("/start"):
            await conn.execute(
                "INSERT INTO bot_logs (id, user_id, action, details, created_at) VALUES ($1, $2, 'ADMIN_START', $3, NOW())",
                uuid.uuid4(),
                user_id,
                json.dumps({"username": username, "first_name": first_name, "chat_id": chat_id})
            )
            safe_name = _escape_html(first_name or "Admin")
            safe_bot = _escape_html(settings.bot_name or "ChezRheyy")
            welcome_text = (
                f"👋 Bonjour <b>{safe_name}</b> (Mode Administrateur) !\n\n"
                f"Bienvenue sur <b>{safe_bot}</b>.\n"
                f"Tapez <code>/help</code> pour consulter les commandes d'administration ou ouvrez l'application :"
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
            await send_telegram_message(chat_id=chat_id, text=welcome_text, reply_markup={"inline_keyboard": inline_keyboard})
            return {"ok": True}

        if text.startswith("/"):
            parts = text.split()
            cmd_raw = parts[0].split("@")[0].lower()
            cmd_args = parts[1:]

            if cmd_raw == "/addmoney":
                await _handle_addmoney(chat_id, user_id, username, cmd_args, conn)
            elif cmd_raw == "/removemoney":
                await _handle_removemoney(chat_id, user_id, username, cmd_args, conn)
            elif cmd_raw == "/ban":
                await _handle_ban(chat_id, cmd_args, conn)
            elif cmd_raw == "/deban":
                await _handle_deban(chat_id, cmd_args, conn)
            elif cmd_raw == "/stat":
                await _handle_stat(chat_id, conn)
            elif cmd_raw == "/commandes":
                await _handle_commandes(chat_id, cmd_args, conn)
            elif cmd_raw == "/info":
                await _handle_info(chat_id, cmd_args, conn)
            elif cmd_raw == "/crypto":
                await _handle_crypto(chat_id, cmd_args, conn)
            elif cmd_raw == "/message":
                await _handle_message(chat_id, text, conn)
            elif cmd_raw == "/maintenance":
                await _handle_maintenance(chat_id, cmd_args, conn)
            elif cmd_raw == "/panel":
                await _handle_panel(chat_id, conn)
            elif cmd_raw in ("/bank", "/sumupbank"):
                await _handle_bank(chat_id, cmd_args, conn)
            elif cmd_raw == "/compteapi":
                await _handle_compteapi(chat_id, cmd_args, conn)
            elif cmd_raw == "/comptepanel":
                await _handle_comptepanel(chat_id, cmd_args, conn)
            elif cmd_raw == "/demoiptv":
                await _handle_demoiptv(chat_id, cmd_args, conn)
            elif cmd_raw == "/help":
                await _handle_help(chat_id, cmd_args)
            else:
                await send_telegram_message(
                    chat_id,
                    f"❌ Commande <code>{_escape_html(cmd_raw)}</code> non reconnue. Tapez <code>/help</code>."
                )
            return {"ok": True}

        safe_bot = _escape_html(settings.bot_name or "ChezRheyy")
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
