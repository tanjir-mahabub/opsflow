from datetime import UTC, datetime
from fastapi import APIRouter

router = APIRouter()

@router.get("/health", summary="Service readiness")
async def health() -> dict[str, str]:
    return {"status": "healthy", "service": "opsflow-api", "timestamp": datetime.now(UTC).isoformat()}
