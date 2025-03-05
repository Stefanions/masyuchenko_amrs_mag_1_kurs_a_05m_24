from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from enum import Enum

app = FastAPI()

# Модели данных
class Employee(BaseModel):
    id: int
    FIO: str
    position: str

class Trade(BaseModel):
    id: int
    title: str
    description: str
    start_date: date
    end_date: date
    status: str
    responsible_id: int

class EmployeeCreate(BaseModel):
    FIO: str
    position: str

class TradeCreate(BaseModel):
    title: str
    description: str
    start_date: date
    end_date: date
    status: str
    responsible_id: int

class TradeStatus(str, Enum):
    INTERESTING = "interesting"
    APPLIED = "applied"
    PURCHASED = "purchased"
    NOT_PURCHASED = "not purchased"

class TradeStatusUpdate(BaseModel):
    status: TradeStatus 

# Пример данных (для демонстрации)
employees_db = []
trades_db = []

# Получить всех сотрудников
@app.get("/employees", response_model=List[Employee], summary="Получить всех сотрудников", description="Возвращает список всех сотрудников.")
def get_employees():
    return employees_db

# Получить сотрудника по ID
@app.get("/employees/{employee_id}", response_model=Employee, summary="Получить сотрудника по ID", description="Возвращает данные сотрудника по его ID.")
def get_employee(employee_id: int = Path(..., description="ID сотрудника")):
    return None

# Добавить нового сотрудника
@app.post("/employees", response_model=Employee, summary="Добавить нового сотрудника", description="Создает нового сотрудника и возвращает его данные.")
def create_employee(employee: EmployeeCreate):
    return None

# Обновить данные сотрудника
@app.put("/employees/{employee_id}", response_model=Employee, summary="Обновить данные сотрудника", description="Обновляет данные сотрудника по его ID.")
def update_employee(employee_id: int, employee: EmployeeCreate):
    return None

# Удалить сотрудника
@app.delete("/employees/{employee_id}", summary="Удалить сотрудника", description="Удаляет сотрудника по его ID.")
def delete_employee(employee_id: int):
    return None

# Получить все торги
@app.get("/trades", response_model=List[Trade], summary="Получить все торги", description="Возвращает список всех торгов.")
def get_trades():
    return None

# Получить торги по статусу
@app.get("/trades/by_status", response_model=List[Trade], summary="Получить торги по статусу", description="Возвращает список торгов с указанным статусом.")
def get_trades_by_status(status: TradeStatus = Query(..., description="Статус торгов")):
    return None

# Получить торги, где сотрудник ответственный по его ФИО
@app.get("/trades/by_responsible_fio", response_model=List[Trade], summary="Получить торги по ФИО ответственного", description="Возвращает список торгов, где указанный сотрудник является ответственным.")
def get_trades_by_responsible_fio(fio: str = Query(..., description="ФИО ответственного сотрудника")):
    return None

# Добавить новые торги
@app.post("/trades", response_model=Trade, summary="Добавить новые торги", description="Создает новые торги и возвращает их данные.")
def create_trade(trade: TradeCreate):
    return None

# Изменение статуса торгов
@app.patch("/trades/{trade_id}/status", response_model=Trade, summary="Изменить статус торгов", description="Обновляет статус торгов по их ID.")
def update_trade_status(trade_id: int = Path(..., description="ID торгов", gt=0), status_update: TradeStatusUpdate = None ):
    return None