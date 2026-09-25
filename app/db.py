import ssl
import asyncpg
from typing import Optional
from app.config import settings

# =====================================================================

db_pool: Optional[asyncpg.Pool] = None

# =====================================================================

def _get_ssl_context() -> Optional[ssl.SSLContext]:
    if "railway" in settings.database_url or "proxy.rlwy.net" in settings.database_url:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
    return None

# =====================================================================

async def init_db() -> asyncpg.Pool:
    global db_pool
    if db_pool is None:
        ssl_ctx = _get_ssl_context()
        db_pool = await asyncpg.create_pool(
            settings.database_url,
            min_size=1,
            max_size=5,
            ssl=ssl_ctx,
            command_timeout=60
        )
        async with db_pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS stock (
                    id SERIAL PRIMARY KEY,
                    brand TEXT NOT NULL DEFAULT 'carr',
                    code TEXT NOT NULL,
                    pin TEXT DEFAULT '0000',
                    value NUMERIC DEFAULT 0,
                    price NUMERIC DEFAULT 0,
                    is_sold BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
            """)
    return db_pool

# =====================================================================

async def get_db_pool() -> asyncpg.Pool:
    global db_pool
    if db_pool is None:
        return await init_db()
    return db_pool

# =====================================================================

async def close_db() -> None:
    global db_pool
    if db_pool is not None:
        await db_pool.close()
        db_pool = None

# =====================================================================

async def check_db_health() -> bool:
    try:
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            val = await conn.fetchval("SELECT 1")
            return val == 1
    except Exception:
        return False
