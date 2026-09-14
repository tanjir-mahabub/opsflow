from datetime import date, timedelta
from sqlalchemy import func, select
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models import Customer, InventoryItem, Invoice, Ticket, User

async def seed_demo_data() -> None:
    async with SessionLocal() as db:
        demo = await db.scalar(select(User).where(User.email == "demo@opsflow.dev"))
        if not demo:
            db.add(User(name="Portfolio Visitor", email="demo@opsflow.dev", password_hash=hash_password("Demo12345!"), role="demo"))
            await db.commit()
        if await db.scalar(select(func.count()).select_from(Customer)): return
        admin = User(name="Tanjir Mahabub", email="admin@opsflow.dev", password_hash=hash_password("OpsFlow123!"), role="admin")
        tech = User(name="Alex Rivera", email="alex@opsflow.dev", password_hash=hash_password("OpsFlow123!"), role="technician")
        db.add_all([admin, tech]); await db.flush()
        customers = [
            Customer(name="Nadia Rahman", email="nadia@example.com", phone="+880 1700 000001"),
            Customer(name="Marcus Lee", email="marcus@example.com", phone="+1 555 0102"),
            Customer(name="Ayesha Khan", email="ayesha@example.com", phone="+880 1800 000003"),
        ]
        db.add_all(customers); await db.flush()
        db.add_all([
            Ticket(reference="OS-1001",customer_id=customers[0].id,title="Display replacement",device="MacBook Pro 14",status="in_progress",priority="high",assigned_to=tech.id,due_date=date.today(),estimated_cost=650),
            Ticket(reference="OS-1002",customer_id=customers[1].id,title="Battery diagnostics",device="iPhone 15 Pro",status="awaiting_parts",priority="medium",assigned_to=tech.id,due_date=date.today()+timedelta(days=1),estimated_cost=180),
            Ticket(reference="OS-1003",customer_id=customers[2].id,title="System recovery",device="Dell XPS 13",status="ready",priority="low",assigned_to=tech.id,due_date=date.today()+timedelta(days=2),estimated_cost=120),
            InventoryItem(sku="DSP-MBP14",name="MacBook Pro 14 Display",category="Display",quantity=2,reorder_level=3,unit_cost=410),
            InventoryItem(sku="BAT-IP15P",name="iPhone 15 Pro Battery",category="Battery",quantity=8,reorder_level=4,unit_cost=65),
            InventoryItem(sku="SSD-1TB",name="NVMe SSD 1TB",category="Storage",quantity=4,reorder_level=5,unit_cost=72),
            Invoice(number="INV-2026001",customer_id=customers[0].id,subtotal=650,tax=0,discount=25,paid=300,status="partial",due_date=date.today()+timedelta(days=7)),
        ])
        await db.commit()
