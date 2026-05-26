from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.api.routes import health
from app.api.v1 import ai, billing, classes, deadlines, oppositions, search, trademarks, watchlist
from app.services.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)

_cors_origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()] or ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(trademarks.router, prefix="/api/v1/trademarks", tags=["trademarks"])
app.include_router(watchlist.router, prefix="/api/v1", tags=["watchlist"])
app.include_router(deadlines.router, prefix="/api/v1", tags=["deadlines"])
app.include_router(oppositions.router, prefix="/api/v1", tags=["oppositions"])
app.include_router(classes.router, prefix="/api/v1/classes", tags=["nice-classes"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])
app.include_router(billing.router, prefix="/api/v1/billing", tags=["billing"])
