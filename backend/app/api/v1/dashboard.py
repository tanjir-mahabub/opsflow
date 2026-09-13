from fastapi import APIRouter
from pydantic import BaseModel

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
