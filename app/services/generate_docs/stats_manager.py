import asyncio

# --------------------------------------------------------------------------
def dispatch_stat(
    pool,
    category: str,
    slug: str,
    action: str,
    period: str = "default",
) -> None:
    if not pool:
        return
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(record_stat(pool, category, slug, action, period))
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
