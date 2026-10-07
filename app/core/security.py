from typing import Any
from app.db import get_db_pool

# =====================================================================

async def get_pool() -> Any:
    return await get_db_pool()
