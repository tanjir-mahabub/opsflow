from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import require_roles
from app.core.database import get_db
from app.models import Ticket, User
from app.schemas.domain import UserOut

router = APIRouter()

@router.get("", response_model=list[UserOut])
async def list_team(db: AsyncSession = Depends(get_db), _: User = Depends(require_roles("admin", "manager", "technician"))):
    return list((await db.scalars(select(User).where(User.active.is_(True), User.role != "customer").order_by(User.name))).all())

@router.get("/workload")
async def workload(db: AsyncSession = Depends(get_db), _: User = Depends(require_roles("admin", "manager", "technician"))):
    rows = await db.execute(select(User.id, User.name, User.role, func.count(Ticket.id)).outerjoin(Ticket, (Ticket.assigned_to == User.id) & Ticket.status.not_in(("completed", "cancelled"))).where(User.active.is_(True), User.role != "customer").group_by(User.id).order_by(User.name))
    return [{"id": row[0], "name": row[1], "role": row[2], "active_tickets": row[3]} for row in rows]
