from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.router import api_router
from app.core.config import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(_: FastAPI):
    yield

app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.exception_handler(Exception)
async def unexpected_error(_: Request, __: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred", "code": "INTERNAL_ERROR"})

app.include_router(api_router, prefix="/api/v1")
