from fastapi import APIRouter
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.customers import router as customers_router
from app.api.v1.tickets import router as tickets_router
from app.api.v1.inventory import router as inventory_router
from app.api.v1.invoices import router as invoices_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["system"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(customers_router, prefix="/customers", tags=["customers"])
api_router.include_router(tickets_router, prefix="/tickets", tags=["tickets"])
api_router.include_router(inventory_router, prefix="/inventory", tags=["inventory"])
api_router.include_router(invoices_router, prefix="/invoices", tags=["invoices"])
