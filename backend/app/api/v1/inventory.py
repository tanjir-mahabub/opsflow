from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import require_roles
from app.core.database import get_db
from app.models import InventoryItem, User
from app.schemas.domain import InventoryCreate, InventoryOut

router = APIRouter()

def serialize(item: InventoryItem) -> InventoryOut:
    result = InventoryOut.model_validate(item)
    result.low_stock = item.quantity <= item.reorder_level
    return result

@router.get("", response_model=list[InventoryOut])
async def list_inventory(low_stock: bool = False, db: AsyncSession = Depends(get_db), _: User = Depends(require_roles("admin","manager","technician"))):
    statement = select(InventoryItem).order_by(InventoryItem.name)
    if low_stock: statement = statement.where(InventoryItem.quantity <= InventoryItem.reorder_level)
    return [serialize(item) for item in (await db.scalars(statement)).all()]

@router.post("", response_model=InventoryOut, status_code=status.HTTP_201_CREATED)
async def create_item(data: InventoryCreate, db: AsyncSession = Depends(get_db), _: User = Depends(require_roles("admin","manager"))):
    if await db.scalar(select(InventoryItem).where(InventoryItem.sku == data.sku)):
        raise HTTPException(status_code=409, detail="SKU already exists")
    item = InventoryItem(**data.model_dump()); db.add(item); await db.commit(); await db.refresh(item)
    return serialize(item)

@router.patch("/{item_id}/stock", response_model=InventoryOut)
async def adjust_stock(item_id: int, change: int, db: AsyncSession = Depends(get_db), _: User = Depends(require_roles("admin","manager"))):
    item = await db.get(InventoryItem, item_id)
    if not item: raise HTTPException(status_code=404, detail="Inventory item not found")
    if item.quantity + change < 0: raise HTTPException(status_code=422, detail="Insufficient stock")
    item.quantity += change; await db.commit(); await db.refresh(item)
    return serialize(item)
