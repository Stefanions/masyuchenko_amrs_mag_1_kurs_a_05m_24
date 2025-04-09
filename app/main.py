from fastapi import FastAPI, HTTPException, Path, Query
from typing import List, Optional
from schemas.sc_all import *
from sql_func.sql_func import *
import uvicorn

# Пример данных (для демонстрации)
employees_db = []
trades_db = []

app = FastAPI()

@app.get("/")
def read_root():
    return {"Масюченко": "Степан"}

# Получить всех сотрудников
@app.get("/employees", response_model=List[Employee], summary="Получить всех сотрудников", description="Возвращает список всех сотрудников.")
def get_employees():
    try:
        empls = take_all_emp()
        return [{"id":e[0], "FIO":e[1], "position":e[2]} for e in empls]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Получить сотрудника по ID
@app.get("/employees/{employee_id}", response_model=Employee, summary="Получить сотрудника по ID", description="Возвращает данные сотрудника по его ID.")
def get_employee(employee_id: int = Path(..., description="ID сотрудника")):
    try:
        empl = take_one_emp_by_id(employee_id)
        return {"id":empl[0], "FIO":empl[1], "position":empl[2]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Добавить нового сотрудника
@app.post("/employees", response_model=Employee, summary="Добавить нового сотрудника", description="Создает нового сотрудника и возвращает его данные.")
def create_employee(employee: EmployeeCreate):
    try:
        empl = write_emp(employee)
        return {"id":empl[0], "FIO":empl[1], "position":empl[2]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Обновить данные сотрудника
@app.put("/employees/{employee_id}", response_model=Employee, summary="Обновить данные сотрудника", description="Обновляет данные сотрудника по его ID.")
def update_employee(employee_id: int, employee: EmployeeCreate):
    try:
        empl = rewrite_emp(employee_id, employee)
        return {"id":empl[0], "FIO":empl[1], "position":empl[2]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Удалить сотрудника
@app.delete("/employees/{employee_id}", summary="Удалить сотрудника", description="Удаляет сотрудника по его ID.")
def delete_employee(employee_id: int):
    try:
        empl = delete_emp(employee_id)
        return {"message":"Сотрудник удалён", "id":empl[0], "FIO":empl[1], "position":empl[2]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Получить все торги
@app.get("/trades", response_model=List[Trade], summary="Получить все торги", description="Возвращает список всех торгов.")
def get_trades():
    try:
        trds = take_all_trades()
        return [{"id":t[0], "trade_number":t[1], "title":t[2], "description":t[3], "start_date":t[4], "end_date":t[5], "status":t[7], "responsible_id":t[6]} for t in trds]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Получить торги по статусу
@app.get("/trades/by_status", response_model=List[Trade], summary="Получить торги по статусу", description="Возвращает список торгов с указанным статусом.")
def get_trades_by_status(status: TradeStatus = Query(..., description="Статус торгов")):
    try:
        trds = take_trade_by_status(status)
        return [{"id":t[0], "trade_number":t[1], "title":t[2], "description":t[3], "start_date":t[4], "end_date":t[5], "status":t[7], "responsible_id":t[6]} for t in trds]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Получить торги, где сотрудник ответственный по его ФИО
@app.get("/trades/by_responsible_fio", response_model=List[Trade], summary="Получить торги по ФИО ответственного", description="Возвращает список торгов, где указанный сотрудник является ответственным.")
def get_trades_by_responsible_fio(fio: str = Query(..., description="ФИО ответственного сотрудника")):
    try:
        trds = take_trade_by_FIO(fio)
        print(trds)
        return [{"id":t[0], "trade_number":t[1], "title":t[2], "description":t[3], "start_date":t[4], "end_date":t[5], "status":t[7], "responsible_id":t[6]} for t in trds]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Добавить новые торги
@app.post("/trades", response_model=Trade, summary="Добавить новые торги", description="Создает новые торги и возвращает их данные.")
def create_trade(trade: TradeCreate):
    try:
        t = write_trades(trade)
        return {"id":t[0], "trade_number":t[1], "title":t[2], "description":t[3], "start_date":t[4], "end_date":t[5], "status":t[7], "responsible_id":t[6]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Изменение статуса торгов
@app.patch("/trades/{trade_id}/new_status", response_model=Trade, summary="Изменить статус торгов", description="Обновляет статус торгов по их ID.")
def update_trade_status(trade_id: int = Path(..., description="ID торгов", gt=0), status: TradeStatus = Query(..., description="Статус торгов")):
    try:
        t = rewrite_trades(trade_id, status)
        return {"id":t[0], "trade_number":t[1], "title":t[2], "description":t[3], "start_date":t[4], "end_date":t[5], "status":t[7], "responsible_id":t[6]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)