from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UserOut(ORMModel):
    id: int; name: str; email: str; role: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class CustomerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(min_length=5, max_length=40)
    company: str | None = None

class CustomerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, min_length=5, max_length=40)
    company: str | None = None

class CustomerOut(CustomerCreate, ORMModel):
    id: int
    created_at: datetime

class TicketCreate(BaseModel):
    customer_id: int
    title: str = Field(min_length=3, max_length=180)
    device: str = Field(min_length=2, max_length=160)
    description: str = ""
    priority: str = Field(pattern="^(low|medium|high|urgent)$")
    due_date: date | None = None
    assigned_to: int | None = None
    estimated_cost: float = Field(default=0, ge=0)

class TicketUpdate(BaseModel):
    status: str | None = Field(default=None, pattern="^(new|in_progress|awaiting_parts|ready|completed|cancelled)$")
    priority: str | None = Field(default=None, pattern="^(low|medium|high|urgent)$")
    assigned_to: int | None = None
    due_date: date | None = None

class TicketOut(ORMModel):
    id: int; reference: str; customer_id: int; title: str; device: str; description: str
    status: str; priority: str; due_date: date | None; assigned_to: int | None; estimated_cost: float; created_at: datetime

class InventoryCreate(BaseModel):
    sku: str; name: str; category: str
    quantity: int = Field(ge=0)
    reorder_level: int = Field(default=5, ge=0)
    unit_cost: float = Field(default=0, ge=0)

class InventoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=160)
    category: str | None = Field(default=None, min_length=2, max_length=100)
    reorder_level: int | None = Field(default=None, ge=0)
    unit_cost: float | None = Field(default=None, ge=0)

class InventoryOut(InventoryCreate, ORMModel):
    id: int
    low_stock: bool = False

class InvoiceCreate(BaseModel):
    customer_id: int; ticket_id: int | None = None
    subtotal: float = Field(gt=0); tax: float = Field(default=0, ge=0); discount: float = Field(default=0, ge=0)
    paid: float = Field(default=0, ge=0); due_date: date | None = None

class InvoiceOut(InvoiceCreate, ORMModel):
    id: int; number: str; status: str
    total: float = 0; balance: float = 0

class PaymentIn(BaseModel):
    amount: float = Field(gt=0)

class DashboardSummary(BaseModel):
    active_tickets: int
    completed_tickets: int
    customers: int
    low_stock_items: int
    revenue: float
    outstanding: float
