from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import require_roles
from app.core.database import get_db
from app.models import Customer, User
from app.schemas.domain import CustomerCreate, CustomerOut

router = APIRouter()

@router.get("", response_model=list[CustomerOut])
async def list_customers(q: str = "", limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), db: AsyncSession = Depends(get_db), _: User = Depends(require_roles("admin","manager","technician"))):
    statement = select(Customer).order_by(Customer.created_at.desc()).limit(limit).offset(offset)
    if q:
        statement = statement.where(or_(Customer.name.ilike(f"%{q}%"), Customer.email.ilike(f"%{q}%"), Customer.phone.ilike(f"%{q}%")))
    return list((await db.scalars(statement)).all())

@router.post("", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
async def create_customer(data: CustomerCreate, db: AsyncSession = Depends(get_db), _: User = Depends(require_roles("admin","manager"))):
    if await db.scalar(select(func.count()).select_from(Customer).where(Customer.email == data.email)):
        raise HTTPException(status_code=409, detail="Customer email already exists")
    customer = Customer(**data.model_dump())
    db.add(customer); await db.commit(); await db.refresh(customer)
    return customer

@router.get("/{customer_id}", response_model=CustomerOut)
async def get_customer(customer_id: int, db: AsyncSession = Depends(get_db), _: User = Depends(require_roles("admin","manager","technician"))):
    customer = await db.get(Customer, customer_id)
    if not customer: raise HTTPException(status_code=404, detail="Customer not found")
    return customer
