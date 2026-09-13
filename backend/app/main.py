from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from app.api.router import api_router
from app.core.config import get_settings
from app.core.database import engine
from app.models import Base
from app.services.seed import seed_demo_data

settings = get_settings()

@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        if connection.dialect.name == "postgresql":
            # The API uses its own JWT/RBAC layer. Block direct access through
            # Supabase's public Data API unless explicit policies are added.
            for table in Base.metadata.sorted_tables:
                quoted_name = connection.dialect.identifier_preparer.quote(table.name)
                await connection.execute(text(f"ALTER TABLE {quoted_name} ENABLE ROW LEVEL SECURITY"))
    if settings.seed_demo_data:
        await seed_demo_data()
    yield

app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_origin_regex=settings.cors_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def unexpected_error(_: Request, __: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred", "code": "INTERNAL_ERROR"})

app.include_router(api_router, prefix="/api/v1")
