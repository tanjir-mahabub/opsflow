from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import current_user, require_roles
from app.core.database import get_db
from app.models import Customer, Ticket, User
from app.schemas.domain import TicketCreate, TicketOut, TicketUpdate

router = APIRouter()

@router.get("", response_model=list[TicketOut])
async def list_tickets(status_value: str | None = Query(None, alias="status"), priority: str | None = None, limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), db: AsyncSession = Depends(get_db), _: User = Depends(current_user)):
    statement = select(Ticket).order_by(Ticket.created_at.desc()).limit(limit).offset(offset)
    if status_value: statement = statement.where(Ticket.status == status_value)
    if priority: statement = statement.where(Ticket.priority == priority)
    return list((await db.scalars(statement)).all())

@router.post("", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
async def create_ticket(data: TicketCreate, db: AsyncSession = Depends(get_db), _: User = Depends(require_roles("admin","manager"))):
    if not await db.get(Customer, data.customer_id): raise HTTPException(status_code=404, detail="Customer not found")
    if data.assigned_to and not await db.get(User, data.assigned_to): raise HTTPException(status_code=404, detail="Assigned technician not found")
    count = await db.scalar(select(func.count()).select_from(Ticket))
    ticket = Ticket(reference=f"OS-{1001 + (count or 0)}", **data.model_dump())
    db.add(ticket); await db.commit(); await db.refresh(ticket)
    return ticket

@router.patch("/{ticket_id}", response_model=TicketOut)
async def update_ticket(ticket_id: int, data: TicketUpdate, db: AsyncSession = Depends(get_db), _: User = Depends(require_roles("admin","manager","technician"))):
    ticket = await db.get(Ticket, ticket_id)
    if not ticket: raise HTTPException(status_code=404, detail="Ticket not found")
    for key, value in data.model_dump(exclude_unset=True).items(): setattr(ticket, key, value)
    await db.commit(); await db.refresh(ticket)
    return ticket
