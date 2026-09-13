from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import current_user
from app.core.database import get_db
from app.models import Customer, InventoryItem, Invoice, Ticket, User
from app.schemas.domain import DashboardSummary

router = APIRouter()

class Metric(BaseModel):
    label: str
    value: str
    change: float
    helper: str

@router.get("/summary", response_model=list[Metric])
async def summary() -> list[Metric]:
    return [
        Metric(label="Active tickets", value="48", change=12.5, helper="6 require attention"),
        Metric(label="Average resolution", value="2.4 days", change=-4.2, helper="Target: under 3 days"),
        Metric(label="Monthly revenue", value="$28,450", change=18.2, helper="$6,840 pending"),
        Metric(label="Customer satisfaction", value="94.8%", change=2.8, helper="From 126 responses"),
    ]

@router.get("/stats", response_model=DashboardSummary)
async def stats(db: AsyncSession = Depends(get_db), _: User = Depends(current_user)) -> DashboardSummary:
    active = await db.scalar(select(func.count()).select_from(Ticket).where(Ticket.status.not_in(("completed", "cancelled")))) or 0
    completed = await db.scalar(select(func.count()).select_from(Ticket).where(Ticket.status == "completed")) or 0
    customers = await db.scalar(select(func.count()).select_from(Customer)) or 0
    low_stock = await db.scalar(select(func.count()).select_from(InventoryItem).where(InventoryItem.quantity <= InventoryItem.reorder_level)) or 0
    invoices = (await db.scalars(select(Invoice))).all()
    revenue = sum(value.paid for value in invoices)
    outstanding = sum(max(0, value.subtotal + value.tax - value.discount - value.paid) for value in invoices)
    return DashboardSummary(active_tickets=active, completed_tickets=completed, customers=customers, low_stock_items=low_stock, revenue=revenue, outstanding=outstanding)
