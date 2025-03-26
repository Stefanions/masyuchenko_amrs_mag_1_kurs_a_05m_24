from pydantic import BaseModel
from datetime import datetime
from enum import Enum

# Модели данных
class Employee(BaseModel):
    id: int
    FIO: str
    position: str

class Trade(BaseModel):
    id: int
    trade_number : str
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    status: str
    responsible_id: int

class EmployeeCreate(BaseModel):
    FIO: str
    position: str

class TradeCreate(BaseModel):
    title: str
    trade_number : str
    description: str
    start_date: datetime
    end_date: datetime
    status: str
    responsible_id: int

class TradeStatus(str, Enum):
    INTERESTING = "active"
    APPLIED = "applied"
    PURCHASED = "purchased"
    NOT_PURCHASED = "not purchased"

class TradeStatusUpdate(BaseModel):
    status: TradeStatus 