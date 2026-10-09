import asyncio
import json
import urllib.parse
from typing import Optional
from app.services.telegram import dispatch_admin_notification

# =====================================================================

def format_user_label(init_data: Optional[str] = None, email: Optional[str] = None) -> Optional[str]:
    if init_data:
        try:
            parsed = urllib.parse.parse_qs(init_data)
            user_str = parsed.get("user", [None])[0]
            if user_str:
                u = json.loads(user_str)
                uid = u.get("id")
                username = u.get("username")
                first_name = u.get("first_name")
                if username:
                    user_disp = f"@{username}"
                elif first_name:
                    user_disp = first_name
                else:
                    user_disp = "Utilisateur"
                if uid:
                    return f"{user_disp} (<code>{uid}</code>)"
                return user_disp
        except Exception:
            pass
    if email and str(email).strip():
        return str(email).strip()
    return None

# =====================================================================

def format_doc_title(category: str, slug: str, period: str = "default") -> str:
    dur_str = f" ({period.replace('m', ' mois')})" if period and period != "default" else ""
    if category == "rib":
        return f"RIB {slug.upper()}"
    if category == "emploi":
        return f"Bulletin de Paie{dur_str}"
    if category == "releve":
        return f"Relevé Bancaire {slug.upper()}{dur_str}"
    if category == "assurance":
        return f"Attestation Assurance {slug.upper()}"
    if category == "facture":
        return f"Facture {slug.replace('_', ' ').capitalize()}"
    if category == "justificatif":
        return f"Justificatif {slug.replace('_', ' ').capitalize()}"
    return f"{category.capitalize()} - {slug}{dur_str}"

# =====================================================================

def dispatch_stat(
    pool,
    category: str,
    slug: str,
    action: str,
    period: str = "default",
    init_data: Optional[str] = None,
    email: Optional[str] = None,
) -> None:
    if not pool:
        return
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(record_stat(pool, category, slug, action, period))
        doc_title = format_doc_title(category, slug, period)
        user_line = ""
        user_label = format_user_label(init_data, email)
        if user_label:
            user_line = f"\n👤 <b>Utilisateur</b> : {user_label}"

        if action == "preview":
            dispatch_admin_notification(
                f"👁 <b>Aperçu Document</b>\n"
                f"{user_line}\n"
                f"📄 <b>Document</b> : {doc_title}\n"
                f"📁 <b>Catégorie</b> : {category.upper()}"
            )
        elif action == "generate":
            dispatch_admin_notification(
                f"📄 <b>Nouveau Document Acheté</b>\n"
                f"{user_line}\n"
                f"📄 <b>Document</b> : {doc_title}\n"
                f"📁 <b>Catégorie</b> : {category.upper()}"
            )
    except RuntimeError:
        pass

# --------------------------------------------------------------------------
async def record_stat(
    pool,
    category: str,
    slug: str,
    action: str,
    period: str = "default",
) -> None:
    if not pool:
        return
    stat_key = f"{category}:{slug}:{period}:{action}" if period != "default" else f"{category}:{slug}:{action}"
    try:
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO services (name, slug, config)
                VALUES ('Génération de documents', 'generate-docs', jsonb_build_object('stats', jsonb_build_object(CAST($1 AS text), 1)))
                ON CONFLICT (slug) DO UPDATE
                SET config = jsonb_set(
                  CASE
                    WHEN services.config IS NULL THEN '{"stats": {}}'::jsonb
                    WHEN services.config->'stats' IS NULL THEN jsonb_set(services.config, '{stats}', '{}'::jsonb, true)
                    ELSE services.config
                  END,
                  ARRAY['stats', CAST($1 AS text)],
                  to_jsonb(COALESCE((services.config->'stats'->>CAST($1 AS text))::bigint, 0) + 1),
                  true
                )
                """,
                stat_key,
            )
    except Exception as e:
        print(f"[STATS_RECORD_ERROR] {stat_key}: {e}", flush=True)
