import asyncio
import io
import traceback
import zipfile
from typing import Optional

from fastapi import APIRouter, Header, HTTPException, Response
from pydantic import BaseModel, ConfigDict, Field

from app.core.billing import (
    check_subcategory_permission,
    get_service_price,
    invalidate_service_cache,
    refund_balance,
    verify_and_deduct_balance,
)
from app.core.security import get_pool
from app.auth import validate_telegram_init_data, upsert_telegram_user
from app.services.generate_docs.forms_manager import (
    delete_form,
    get_form,
    get_form_by_cat_slug,
    list_forms,
    load_forms_cache,
    save_form,
)
from app.services.generate_docs.assurance.schemas import AssuranceMaxanceGenerateRequest
from app.services.generate_docs.assurance.service import (
    ISSUERS,
    generate_pdf_bytes as generate_assurance_pdf_bytes,
    generate_preview_jpg_bytes as generate_assurance_preview_jpg_bytes,
    validate_assurance_payload,
)
from app.services.generate_docs.facture.schemas import FactureGenerateRequest
from app.services.generate_docs.facture.service import (
    FILENAMES as FACTURE_FILENAMES,
    ISSUERS as FACTURE_ISSUERS,
    generate_pdf_bytes as generate_facture_pdf_bytes,
    generate_preview_jpg_bytes as generate_facture_preview_jpg_bytes,
    validate_facture_payload,
)
from app.services.generate_docs.justificatif.schemas import JustificatifGenerateRequest
from app.services.generate_docs.justificatif.service import (
    FILENAMES as JUSTIFICATIF_FILENAMES,
    ISSUERS as JUSTIFICATIF_ISSUERS,
    generate_pdf_bytes as generate_justificatif_pdf_bytes,
    generate_preview_jpg_bytes as generate_justificatif_preview_jpg_bytes,
    validate_justificatif_payload,
)
from app.services.generate_docs.emploi import (
    FicheDePaieGenerateRequest,
    generate_fiche_de_paie_bytes,
    generate_fiche_de_paie_preview_pdf_bytes,
    generate_fiche_de_paie_preview_pages,
)
from app.services.generate_docs.releve.lbp import generate_lbp_preview_pdf_bytes, generate_lbp_releves_bytes
from app.services.generate_docs.releve.schemas import ReleveLBPGenerateRequest
from app.services.generate_docs.rib.schemas import RibGenerateRequest
from app.services.generate_docs.config import (
    _as_bool,
    invalidate_generate_docs_config_cache,
    load_generate_docs_config,
)
from app.services.generate_docs.common.preview import flatten_pdf_bytes, flatten_zip_bytes
from app.services.generate_docs.rib.service import (
    BANKS,
    FILENAMES,
    generate_pdf_bytes,
    generate_preview_jpg_bytes,
    validate_rib_payload,
)
from app.services.generate_docs.stats_manager import dispatch_stat, record_stat

router = APIRouter(prefix="/generate-docs", tags=["generate-docs"])

NO_CACHE = {
    "Cache-Control": "no-store, no-cache, must-revalidate, private, max-age=0",
    "Pragma": "no-cache",
    "Expires": "0",
}

VALID_RELEVE_DURATIONS = {1, 3, 6, 12}
RELEVE_PRICE_KEYS = [
    (1, "releve_lbp_1m"),
    (3, "releve_lbp_3m"),
    (6, "releve_lbp_6m"),
    (12, "releve_lbp_12m"),
]

VALID_EMPLOI_DURATIONS = {1, 3, 6, 12}
EMPLOI_PRICE_KEYS = [
    (1, "fiche_de_paie_1m"),
    (3, "fiche_de_paie_3m"),
    (6, "fiche_de_paie_6m"),
    (12, "fiche_de_paie_12m"),
]


def _dump(req) -> dict:
    if hasattr(req, "model_dump"):
        data = req.model_dump(exclude_none=True)
    else:
        data = req.dict()
    return {key: value for key, value in data.items() if value is not None}


def _unknown_bank(bank: str) -> HTTPException:
    return HTTPException(status_code=404, detail=f"Banque inconnue: {bank}")


def _preview_forbidden() -> HTTPException:
    return HTTPException(status_code=403, detail="Les aperçus sont actuellement éteints")


async def _resolve_user_identifier(
    x_user_email: Optional[str] = None,
    x_telegram_init_data: Optional[str] = None,
) -> str:
    if x_telegram_init_data:
        try:
            user_data = validate_telegram_init_data(x_telegram_init_data)
            if user_data and "id" in user_data:
                await upsert_telegram_user(user_data)
                return str(user_data["id"])
        except Exception:
            pass
    if x_user_email and str(x_user_email).strip():
        return str(x_user_email).strip()
    raise HTTPException(status_code=401, detail="Authentification requise pour générer ce document")



async def _guard_document_access(
    category: str,
    slug: str,
    user_role: Optional[str] = None,
    is_preview: bool = False,
) -> None:
    db_pool = await get_pool()
    if not db_pool:
        return
    cfg = await load_generate_docs_config(db_pool)
    if not cfg.get("isActive", True):
        raise HTTPException(
            status_code=403,
            detail="Le service de génération de documents est temporairement indisponible",
        )
    if is_preview and cfg.get("previewOff"):
        raise _preview_forbidden()

    await check_subcategory_permission(db_pool, "generate-docs", category)

    if slug:
        subs = cfg.get("subcategories", {})
        cat_info = subs.get(category, {})
        docs_map = cat_info.get("documents", {})
        if docs_map and slug in docs_map and not _as_bool(docs_map[slug], True):
            raise HTTPException(
                status_code=403,
                detail=f"Le document '{slug}' est actuellement désactivé",
            )
        form = await get_form_by_cat_slug(db_pool, category, slug)
        if form and not form.get("isActive", True):
            raise HTTPException(
                status_code=403,
                detail=f"Le document '{slug}' est actuellement désactivé",
            )


async def _guard_preview(subcategory: str, user_role: Optional[str]) -> None:
    await _guard_document_access(subcategory, "", user_role, is_preview=True)


async def _process_generated_output(file_bytes: bytes, content_type: str, db_pool=None) -> bytes:
    pool = db_pool or await get_pool()
    if not pool:
        return file_bytes
    cfg = await load_generate_docs_config(pool)
    if not cfg.get("flattenPdf"):
        return file_bytes
    if content_type == "application/pdf":
        return await asyncio.to_thread(flatten_pdf_bytes, file_bytes)
    if content_type == "application/zip":
        return await asyncio.to_thread(flatten_zip_bytes, file_bytes)
    return file_bytes





@router.get("/config")
async def generate_docs_config(x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role")):
    pool = await get_pool()
    cfg = await load_generate_docs_config(pool)
    preview_off = bool(cfg.get("previewOff"))
    return {
        **cfg,
        "previewOff": preview_off,
        "previewAllowed": (not preview_off) or x_auth_role == "ADMIN",
        "flattenPdf": bool(cfg.get("flattenPdf")),
    }


@router.get("/rib/pricing")
async def rib_pricing():
    pool = await get_pool()
    cfg = await load_generate_docs_config(pool)
    first_bank = BANKS[0]
    price = cfg["prices"].get(first_bank, 1.0)
    try:
        price = float(price)
    except (TypeError, ValueError):
        price = 1.0
    return {
        "service": "generate-docs",
        "price": price,
        "currency": "EUR",
        "banks": list(BANKS),
        "previewCooldownEnabled": cfg["previewCooldownEnabled"],
        "previewCooldownSeconds": cfg["previewCooldownSeconds"],
    }


@router.post("/rib/{bank}/preview")
async def rib_preview(
    bank: str,
    req: RibGenerateRequest,
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data"),
    x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role"),
):
    if bank not in BANKS:
        raise _unknown_bank(bank)
    try:
        await _guard_document_access("rib", bank, x_auth_role, is_preview=True)
        jpg_bytes = await asyncio.to_thread(generate_preview_jpg_bytes, bank, _dump(req))
        db_pool = await get_pool()
        dispatch_stat(db_pool, category="rib", slug=bank, action="preview", init_data=x_telegram_init_data)
        return Response(
            content=jpg_bytes,
            media_type="image/jpeg",
            headers={
                **NO_CACHE,
                "Content-Disposition": "inline",
                "X-Content-Type-Options": "nosniff",
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[RIB_PREVIEW_{bank.upper()}_ERROR] {e}\n{traceback.format_exc()}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rib/{bank}/generate")
async def rib_generate(
    bank: str,
    req: RibGenerateRequest,
    x_user_email: Optional[str] = Header(None, alias="X-User-Email"),
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data"),
    x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role"),
):
    if bank not in BANKS:
        raise _unknown_bank(bank)
    user_id_str = await _resolve_user_identifier(x_user_email, x_telegram_init_data)
    charged = False
    db_pool = None
    try:
        await _guard_document_access("rib", bank, x_auth_role, is_preview=False)
        db_pool = await get_pool()
        if not db_pool:
            raise HTTPException(status_code=500, detail="Base de données inaccessible")

        pdf_name, _, label = FILENAMES[bank]
        data = _dump(req)
        validate_rib_payload(bank, data)
        await verify_and_deduct_balance(
            db_pool=db_pool,
            email=user_id_str,
            service_slug="generate-docs",
            action_type=bank,
            quantity=1,
            metadata={"document": "RIB", "bank": label},
            user_role=x_auth_role or "USER",
        )
        charged = True

        pdf_bytes = await asyncio.to_thread(generate_pdf_bytes, bank, data)
        dispatch_stat(db_pool, category="rib", slug=bank, action="generate", init_data=x_telegram_init_data, email=x_user_email)
        output_bytes = await _process_generated_output(pdf_bytes, "application/pdf", db_pool)
        return Response(
            content=output_bytes,
            media_type="application/pdf",
            headers={
                **NO_CACHE,
                "Content-Disposition": f"attachment; filename={pdf_name}",
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[RIB_{bank.upper()}_ERROR] {e}\n{traceback.format_exc()}", flush=True)
        if charged and db_pool:
            try:
                await refund_balance(
                    db_pool=db_pool,
                    email=user_id_str,
                    service_slug="generate-docs",
                    action_type=bank,
                    quantity_to_refund=1,
                    metadata={"reason": str(e)},
                )
            except Exception:
                pass
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/releve/pricing")
async def releve_pricing():
    pool = await get_pool()
    prices = {}
    for months, key in RELEVE_PRICE_KEYS:
        try:
            price, _ = await get_service_price(pool, "generate-docs", key)
            prices[f"{months}_mois"] = price
        except Exception:
            prices[f"{months}_mois"] = None
    return {
        "service": "generate-docs",
        "subcategory": "releve",
        "prices": prices,
        "currency": "EUR",
        "banks": ["lbp"],
    }


@router.post("/releve/{bank}/preview")
async def releve_preview(
    bank: str,
    req: ReleveLBPGenerateRequest,
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data"),
    x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role"),
):
    if bank != "lbp":
        raise HTTPException(status_code=404, detail=f"Relevé indisponible pour: {bank}")
    try:
        await _guard_document_access("releve", bank, x_auth_role, is_preview=True)
        duree = req.duree_mois if req.duree_mois in VALID_RELEVE_DURATIONS else 1
        pdf_bytes = await asyncio.to_thread(generate_lbp_preview_pdf_bytes, _dump(req))
        db_pool = await get_pool()
        dispatch_stat(db_pool, category="releve", slug=bank, action="preview", period=f"{duree}m", init_data=x_telegram_init_data)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                **NO_CACHE,
                "Content-Disposition": "inline; filename=apercu_releve_lbp.pdf",
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur génération aperçu: {str(e)}")


@router.post("/releve/{bank}/generate")
async def releve_generate(
    bank: str,
    req: ReleveLBPGenerateRequest,
    x_user_email: Optional[str] = Header(None, alias="X-User-Email"),
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data"),
    x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role"),
):
    if bank != "lbp":
        raise HTTPException(status_code=404, detail=f"Relevé indisponible pour: {bank}")
    user_id_str = await _resolve_user_identifier(x_user_email, x_telegram_init_data)

    await _guard_document_access("releve", bank, x_auth_role, is_preview=False)
    duree = req.duree_mois if req.duree_mois in VALID_RELEVE_DURATIONS else 1
    price_key = f"releve_lbp_{duree}m"
    pool = await get_pool()
    await verify_and_deduct_balance(
        db_pool=pool,
        email=user_id_str,
        action_type=price_key,
        service_slug="generate-docs",
        quantity=1,
        user_role=x_auth_role or "USER",
    )
    try:
        file_bytes, content_type, filename = await asyncio.to_thread(generate_lbp_releves_bytes, _dump(req))
        dispatch_stat(pool, category="releve", slug=bank, action="generate", period=f"{duree}m", init_data=x_telegram_init_data, email=x_user_email)
        output_bytes = await _process_generated_output(file_bytes, content_type, pool)
        return Response(
            content=output_bytes,
            media_type=content_type,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )
    except Exception as e:
        await refund_balance(
            db_pool=pool,
            email=user_id_str,
            service_slug="generate-docs",
            action_type=price_key,
            quantity_to_refund=1,
            metadata={"reason": str(e)},
        )
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création du relevé: {str(e)}")


@router.get("/emploi/pricing")
async def emploi_pricing():
    pool = await get_pool()
    prices = {}
    for months, key in EMPLOI_PRICE_KEYS:
        try:
            price, _ = await get_service_price(pool, "generate-docs", key)
            prices[f"{months}_mois"] = price
        except Exception:
            prices[f"{months}_mois"] = None
    return {
        "service": "generate-docs",
        "subcategory": "emploi",
        "prices": prices,
        "currency": "EUR",
        "issuers": ["fiche_de_paie"],
    }


@router.post("/emploi/{issuer}/preview")
async def emploi_preview(
    issuer: str,
    req: FicheDePaieGenerateRequest,
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data"),
    x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role"),
):
    if issuer != "fiche_de_paie":
        raise HTTPException(status_code=404, detail=f"Document emploi indisponible pour: {issuer}")
    try:
        await _guard_document_access("emploi", issuer, x_auth_role, is_preview=True)
        duree = req.duree_mois if req.duree_mois in VALID_EMPLOI_DURATIONS else 1
        pages_b64 = await asyncio.to_thread(generate_fiche_de_paie_preview_pages, _dump(req))
        db_pool = await get_pool()
        dispatch_stat(db_pool, category="emploi", slug=issuer, action="preview", period=f"{duree}m", init_data=x_telegram_init_data)
        return {"pages": pages_b64}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur génération aperçu: {str(e)}")


@router.post("/emploi/{issuer}/generate")
async def emploi_generate(
    issuer: str,
    req: FicheDePaieGenerateRequest,
    x_user_email: Optional[str] = Header(None, alias="X-User-Email"),
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data"),
    x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role"),
):
    if issuer != "fiche_de_paie":
        raise HTTPException(status_code=404, detail=f"Document emploi indisponible pour: {issuer}")
    user_id_str = await _resolve_user_identifier(x_user_email, x_telegram_init_data)

    await _guard_document_access("emploi", issuer, x_auth_role, is_preview=False)
    duree = req.duree_mois if req.duree_mois in VALID_EMPLOI_DURATIONS else 1
    price_key = f"fiche_de_paie_{duree}m"
    pool = await get_pool()
    await verify_and_deduct_balance(
        db_pool=pool,
        email=user_id_str,
        action_type=price_key,
        service_slug="generate-docs",
        quantity=1,
        user_role=x_auth_role or "USER",
    )
    try:
        file_bytes, content_type, filename = await asyncio.to_thread(generate_fiche_de_paie_bytes, _dump(req))
        dispatch_stat(pool, category="emploi", slug=issuer, action="generate", period=f"{duree}m", init_data=x_telegram_init_data, email=x_user_email)
        output_bytes = await _process_generated_output(file_bytes, content_type, pool)
        return Response(
            content=output_bytes,
            media_type=content_type,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )
    except Exception as e:
        await refund_balance(
            db_pool=pool,
            email=user_id_str,
            service_slug="generate-docs",
            action_type=price_key,
            quantity_to_refund=1,
            metadata={"reason": str(e)},
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/assurance/{issuer}/preview")
async def assurance_preview(
    issuer: str,
    req: AssuranceMaxanceGenerateRequest,
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data"),
    x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role"),
):
    if issuer not in ISSUERS:
        raise HTTPException(status_code=404, detail=f"Assureur inconnu: {issuer}")
    try:
        await _guard_document_access("assurance", issuer, x_auth_role, is_preview=True)
        jpg_bytes = await asyncio.to_thread(generate_assurance_preview_jpg_bytes, issuer, _dump(req))
        db_pool = await get_pool()
        dispatch_stat(db_pool, category="assurance", slug=issuer, action="preview", init_data=x_telegram_init_data)
        return Response(
            content=jpg_bytes,
            media_type="image/jpeg",
            headers={
                **NO_CACHE,
                "Content-Disposition": "inline",
                "X-Content-Type-Options": "nosniff",
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ASSURANCE_PREVIEW_{issuer.upper()}_ERROR] {e}\n{traceback.format_exc()}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/assurance/{issuer}/generate")
async def assurance_generate(
    issuer: str,
    req: AssuranceMaxanceGenerateRequest,
    x_user_email: Optional[str] = Header(None, alias="X-User-Email"),
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data"),
    x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role"),
):
    if issuer not in ISSUERS:
        raise HTTPException(status_code=404, detail=f"Assureur inconnu: {issuer}")
    user_id_str = await _resolve_user_identifier(x_user_email, x_telegram_init_data)
    charged = False
    db_pool = None
    try:
        await _guard_document_access("assurance", issuer, x_auth_role, is_preview=False)
        db_pool = await get_pool()
        if not db_pool:
            raise HTTPException(status_code=500, detail="Base de données inaccessible")
        data = _dump(req)
        validate_assurance_payload(data)
        await verify_and_deduct_balance(
            db_pool=db_pool,
            email=user_id_str,
            service_slug="generate-docs",
            action_type=issuer,
            quantity=1,
            metadata={"document": "Assurance", "company": issuer.upper()},
            user_role=x_auth_role or "USER",
        )
        charged = True
        pdf_bytes = await asyncio.to_thread(generate_assurance_pdf_bytes, issuer, data)
        dispatch_stat(db_pool, category="assurance", slug=issuer, action="generate", init_data=x_telegram_init_data, email=x_user_email)
        output_bytes = await _process_generated_output(pdf_bytes, "application/pdf", db_pool)
        immat = data.get("immatriculation") or data.get("vehicule_immat") or "DOC"
        return Response(
            content=output_bytes,
            media_type="application/pdf",
            headers={
                **NO_CACHE,
                "Content-Disposition": f"attachment; filename=Memo_Vehicule_Assure_{issuer.capitalize()}_{immat}.pdf",
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ASSURANCE_ERROR] {e}\n{traceback.format_exc()}", flush=True)
        if charged and db_pool:
            try:
                await refund_balance(
                    db_pool=db_pool,
                    email=user_id_str,
                    service_slug="generate-docs",
                    action_type=issuer,
                    quantity_to_refund=1,
                    metadata={"reason": str(e)},
                )
            except Exception:
                pass
        raise HTTPException(status_code=500, detail=str(e))


def _unknown_facture(issuer: str) -> HTTPException:
    return HTTPException(status_code=404, detail=f"Émetteur facture inconnu: {issuer}")


def _unknown_justificatif(issuer: str) -> HTTPException:
    return HTTPException(status_code=404, detail=f"Justificatif inconnu: {issuer}")


@router.get("/facture/pricing")
async def facture_pricing():
    pool = await get_pool()
    cfg = await load_generate_docs_config(pool)
    prices = {}
    for issuer in FACTURE_ISSUERS:
        try:
            prices[issuer] = float(cfg["prices"].get(issuer, 1.0))
        except (TypeError, ValueError):
            prices[issuer] = 1.0
    return {
        "service": "generate-docs",
        "subcategory": "facture",
        "prices": prices,
        "currency": "EUR",
        "issuers": list(FACTURE_ISSUERS),
        "previewCooldownEnabled": cfg["previewCooldownEnabled"],
        "previewCooldownSeconds": cfg["previewCooldownSeconds"],
    }


@router.post("/facture/{issuer}/preview")
async def facture_preview(
    issuer: str,
    req: FactureGenerateRequest,
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data"),
    x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role"),
):
    if issuer not in FACTURE_ISSUERS:
        raise _unknown_facture(issuer)
    try:
        await _guard_document_access("facture", issuer, x_auth_role, is_preview=True)
        jpg_bytes = await asyncio.to_thread(generate_facture_preview_jpg_bytes, issuer, _dump(req))
        db_pool = await get_pool()
        dispatch_stat(db_pool, category="facture", slug=issuer, action="preview", init_data=x_telegram_init_data)
        return Response(
            content=jpg_bytes,
            media_type="image/jpeg",
            headers={
                **NO_CACHE,
                "Content-Disposition": "inline",
                "X-Content-Type-Options": "nosniff",
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[FACTURE_PREVIEW_{issuer.upper()}_ERROR] {e}\n{traceback.format_exc()}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/facture/{issuer}/generate")
async def facture_generate(
    issuer: str,
    req: FactureGenerateRequest,
    x_user_email: Optional[str] = Header(None, alias="X-User-Email"),
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data"),
    x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role"),
):
    if issuer not in FACTURE_ISSUERS:
        raise _unknown_facture(issuer)
    user_id_str = await _resolve_user_identifier(x_user_email, x_telegram_init_data)
    db_pool = None
    charged = False
    try:
        await _guard_document_access("facture", issuer, x_auth_role, is_preview=False)
        db_pool = await get_pool()
        if not db_pool:
            raise HTTPException(status_code=500, detail="Base de données inaccessible")
        pdf_name, _, label = FACTURE_FILENAMES[issuer]
        data = _dump(req)
        validate_facture_payload(issuer, data)
        await verify_and_deduct_balance(
            db_pool=db_pool,
            email=user_id_str,
            service_slug="generate-docs",
            action_type=issuer,
            quantity=1,
            metadata={"document": "Facture", "issuer": label},
            user_role=x_auth_role or "USER",
        )
        charged = True
        pdf_bytes = await asyncio.to_thread(generate_facture_pdf_bytes, issuer, data)
        dispatch_stat(db_pool, category="facture", slug=issuer, action="generate", init_data=x_telegram_init_data, email=x_user_email)
        output_bytes = await _process_generated_output(pdf_bytes, "application/pdf", db_pool)
        return Response(
            content=output_bytes,
            media_type="application/pdf",
            headers={
                **NO_CACHE,
                "Content-Disposition": f"attachment; filename={pdf_name}",
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        if charged and db_pool:
            try:
                await refund_balance(
                    db_pool=db_pool,
                    email=user_id_str,
                    service_slug="generate-docs",
                    action_type=issuer,
                    quantity_to_refund=1,
                    metadata={"reason": str(e)},
                )
            except Exception:
                pass
        print(f"[FACTURE_{issuer.upper()}_ERROR] {e}\n{traceback.format_exc()}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/justificatif/pricing")
async def justificatif_pricing():
    pool = await get_pool()
    cfg = await load_generate_docs_config(pool)
    prices = {}
    for issuer in JUSTIFICATIF_ISSUERS:
        try:
            prices[issuer] = float(cfg["prices"].get(issuer, 1.0))
        except (TypeError, ValueError):
            prices[issuer] = 1.0
    return {
        "service": "generate-docs",
        "subcategory": "justificatif",
        "prices": prices,
        "currency": "EUR",
        "issuers": list(JUSTIFICATIF_ISSUERS),
        "previewCooldownEnabled": cfg["previewCooldownEnabled"],
        "previewCooldownSeconds": cfg["previewCooldownSeconds"],
    }


@router.post("/justificatif/{issuer}/preview")
async def justificatif_preview(
    issuer: str,
    req: JustificatifGenerateRequest,
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data"),
    x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role"),
):
    if issuer not in JUSTIFICATIF_ISSUERS:
        raise _unknown_justificatif(issuer)
    try:
        await _guard_document_access("justificatif", issuer, x_auth_role, is_preview=True)
        jpg_bytes = await asyncio.to_thread(generate_justificatif_preview_jpg_bytes, issuer, _dump(req))
        db_pool = await get_pool()
        dispatch_stat(db_pool, category="justificatif", slug=issuer, action="preview", init_data=x_telegram_init_data)
        return Response(
            content=jpg_bytes,
            media_type="image/jpeg",
            headers={
                **NO_CACHE,
                "Content-Disposition": "inline",
                "X-Content-Type-Options": "nosniff",
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[JUSTIFICATIF_PREVIEW_{issuer.upper()}_ERROR] {e}\n{traceback.format_exc()}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/justificatif/{issuer}/generate")
async def justificatif_generate(
    issuer: str,
    req: JustificatifGenerateRequest,
    x_user_email: Optional[str] = Header(None, alias="X-User-Email"),
    x_telegram_init_data: Optional[str] = Header(None, alias="X-Telegram-Init-Data"),
    x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role"),
):
    if issuer not in JUSTIFICATIF_ISSUERS:
        raise _unknown_justificatif(issuer)
    user_id_str = await _resolve_user_identifier(x_user_email, x_telegram_init_data)
    db_pool = None
    charged = False
    try:
        await _guard_document_access("justificatif", issuer, x_auth_role, is_preview=False)
        db_pool = await get_pool()
        if not db_pool:
            raise HTTPException(status_code=500, detail="Base de données inaccessible")
        pdf_name, _, label = JUSTIFICATIF_FILENAMES[issuer]
        data = _dump(req)
        validate_justificatif_payload(issuer, data)
        await verify_and_deduct_balance(
            db_pool=db_pool,
            email=user_id_str,
            service_slug="generate-docs",
            action_type=issuer,
            quantity=1,
            metadata={"document": "Justificatif", "issuer": label},
            user_role=x_auth_role or "USER",
        )
        charged = True
        pdf_bytes = await asyncio.to_thread(generate_justificatif_pdf_bytes, issuer, data)
        dispatch_stat(db_pool, category="justificatif", slug=issuer, action="generate", init_data=x_telegram_init_data, email=x_user_email)
        output_bytes = await _process_generated_output(pdf_bytes, "application/pdf", db_pool)
        return Response(
            content=output_bytes,
            media_type="application/pdf",
            headers={
                **NO_CACHE,
                "Content-Disposition": f"attachment; filename={pdf_name}",
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        if charged and db_pool:
            try:
                await refund_balance(
                    db_pool=db_pool,
                    email=user_id_str,
                    service_slug="generate-docs",
                    action_type=issuer,
                    quantity_to_refund=1,
                    metadata={"reason": str(e)},
                )
            except Exception:
                pass
        print(f"[JUSTIFICATIF_{issuer.upper()}_ERROR] {e}\n{traceback.format_exc()}", flush=True)
        raise HTTPException(status_code=500, detail=str(e))


class AdminSaveFormRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    category: str
    slug: str
    title: str
    form_schema: dict = Field(default_factory=dict, alias="schema")
    isActive: bool = True
    allowedRoles: str = "USER,ADMIN,RESELLER"


def _require_admin(x_auth_role: Optional[str]) -> None:
    if x_auth_role != "ADMIN":
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")


@router.get("/admin/forms")
async def admin_list_forms(x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role")):
    _require_admin(x_auth_role)
    return await list_forms()


@router.get("/admin/forms/{doc_id}")
async def admin_get_form(doc_id: str, x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role")):
    _require_admin(x_auth_role)
    form = await get_form(doc_id=doc_id)
    if not form:
        raise HTTPException(status_code=404, detail="Formulaire non trouvé")
    return form


@router.put("/admin/forms/{doc_id}")
async def admin_save_form(
    doc_id: str,
    req: AdminSaveFormRequest,
    x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role"),
):
    _require_admin(x_auth_role)
    saved = await save_form(
        doc_id=doc_id,
        category=req.category,
        slug=req.slug,
        title=req.title,
        schema=req.form_schema,
        is_active=req.isActive,
        allowed_roles=req.allowedRoles,
    )
    return saved


@router.delete("/admin/forms/{doc_id}")
async def admin_delete_form(doc_id: str, x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role")):
    _require_admin(x_auth_role)
    success = await delete_form(doc_id=doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Formulaire non trouvé ou non supprimé")
    return {"status": "ok", "deleted": doc_id}


@router.post("/admin/forms/reload-cache")
async def admin_reload_cache(x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role")):
    _require_admin(x_auth_role)
    invalidate_generate_docs_config_cache()
    invalidate_service_cache("generate-docs")
    cache = await load_forms_cache()
    return {"status": "ok", "cachedCount": len(cache)}


@router.get("/forms/{category}/{slug}")
@router.get("/form/{category}/{slug}")
async def public_get_form(
    category: str,
    slug: str,
    response: Response,
    x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role"),
):
    await _guard_document_access(category, slug, x_auth_role, is_preview=False)
    form = await get_form_by_cat_slug(category=category, slug=slug)
    if not form or not form.get("isActive"):
        raise HTTPException(
            status_code=404,
            detail=f"Configuration de formulaire introuvable pour {category}/{slug}.",
        )
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return form


@router.post("/admin/regression-test/{category}")
async def admin_regression_test(
    category: str,
    x_auth_role: Optional[str] = Header(None, alias="X-Auth-Role"),
):
    _require_admin(x_auth_role)
    cat = category.lower().strip()
    valid_cats = {"rib", "facture", "justificatif", "assurance", "releve", "emploi", "all"}
    if cat not in valid_cats:
        raise HTTPException(status_code=400, detail=f"Catégorie invalide. Options: {', '.join(sorted(valid_cats))}")

    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        if cat in ("rib", "all"):
            for bank in BANKS:
                pdf = await asyncio.to_thread(generate_pdf_bytes, bank, None)
                zf.writestr(f"RIB/{FILENAMES[bank][0]}", pdf)

        if cat in ("facture", "all"):
            for issuer in FACTURE_ISSUERS:
                pdf = await asyncio.to_thread(generate_facture_pdf_bytes, issuer, None)
                zf.writestr(f"Factures/{FACTURE_FILENAMES[issuer][0]}", pdf)

        if cat in ("justificatif", "all"):
            for issuer in JUSTIFICATIF_ISSUERS:
                pdf = await asyncio.to_thread(generate_justificatif_pdf_bytes, issuer, None)
                zf.writestr(f"Justificatifs/{JUSTIFICATIF_FILENAMES[issuer][0]}", pdf)

        if cat in ("assurance", "all"):
            for ass_issuer in ISSUERS:
                pdf = await asyncio.to_thread(generate_assurance_pdf_bytes, ass_issuer, None)
                zf.writestr(f"Assurance/Memo_Vehicule_Assure_{ass_issuer.capitalize()}.pdf", pdf)

        if cat in ("releve", "all"):
            rel_bytes, _, _ = await asyncio.to_thread(generate_lbp_releves_bytes, {"duree_mois": 3})
            with zipfile.ZipFile(io.BytesIO(rel_bytes)) as inner_zf:
                for member in inner_zf.namelist():
                    zf.writestr(f"Releves_3_mois/{member}", inner_zf.read(member))

        if cat in ("emploi", "all"):
            emp_bytes, _, _ = await asyncio.to_thread(generate_fiche_de_paie_bytes, {"duree_mois": 3})
            with zipfile.ZipFile(io.BytesIO(emp_bytes)) as inner_zf:
                for member in inner_zf.namelist():
                    zf.writestr(f"Fiches_de_Paie_3_mois/{member}", inner_zf.read(member))

    zip_buf.seek(0)
    zip_bytes = zip_buf.getvalue()
    filename_map = {
        "rib": "Test_Regression_RIB_17_Banques.zip",
        "facture": "Test_Regression_Factures_13_Emetteurs.zip",
        "justificatif": "Test_Regression_Justificatifs_3_Emetteurs.zip",
        "assurance": "Test_Regression_Assurance_Maxance.zip",
        "releve": "Test_Regression_Releves_LBP_3_Mois.zip",
        "emploi": "Test_Regression_Fiches_De_Paie_3_Mois.zip",
        "all": "Test_Regression_Tous_Documents.zip",
    }
    filename = filename_map.get(cat, "Test_Regression_Documents.zip")
    output_bytes = await _process_generated_output(zip_bytes, "application/zip")

    return Response(
        content=output_bytes,
        media_type="application/zip",
        headers={
            **NO_CACHE,
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


