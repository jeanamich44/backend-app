from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.db import init_db, close_db
from app.routes.user import router as user_router
from app.routes.payments import router as payments_router
from app.routes.admin import router as admin_router

# =====================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

# =====================================================================

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan
)

# =====================================================================

origins = [
    settings.frontend_url,
    "https://chez-administration.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# =====================================================================

@app.get("/")
async def root():
    return {"status": "online"}

# =====================================================================

@app.get("/health")
async def health():
    return {"status": "online"}

# =====================================================================

app.include_router(user_router)
app.include_router(payments_router)
app.include_router(admin_router)
