from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import require_roles
from app.core.database import get_db
from app.models import Customer, Invoice, User
from app.schemas.domain import InvoiceCreate, InvoiceOut

router = APIRouter()

def serialize(invoice: Invoice) -> InvoiceOut:
    output = InvoiceOut.model_validate(invoice)
    output.total = max(0, invoice.subtotal + invoice.tax - invoice.discount)
    output.balance = max(0, output.total - invoice.paid)
    return output

@router.get("", response_model=list[InvoiceOut])
async def list_invoices(db: AsyncSession = Depends(get_db), _: User = Depends(require_roles("admin","manager"))):
    return [serialize(value) for value in (await db.scalars(select(Invoice).order_by(Invoice.created_at.desc()))).all()]

@router.post("", response_model=InvoiceOut, status_code=status.HTTP_201_CREATED)
async def create_invoice(data: InvoiceCreate, db: AsyncSession = Depends(get_db), _: User = Depends(require_roles("admin","manager"))):
    if not await db.get(Customer, data.customer_id): raise HTTPException(status_code=404, detail="Customer not found")
    count = await db.scalar(select(func.count()).select_from(Invoice))
    total = max(0, data.subtotal + data.tax - data.discount)
    invoice = Invoice(number=f"INV-{2026001 + (count or 0)}", status="paid" if data.paid >= total else "partial" if data.paid > 0 else "unpaid", **data.model_dump())
    db.add(invoice); await db.commit(); await db.refresh(invoice)
    return serialize(invoice)
