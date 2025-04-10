import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.sc_all import TradeStatus
from datetime import datetime, timedelta

client = TestClient(app)

# Тестовые данные
TEST_EMPLOYEE = {
    "FIO": "Иванов Иван Иванович",
    "position": "Инженер"
}

TEST_TRADE = {
    "title": "Тестовые торги",
    "trade_number": "TEST-001",
    "description": "Описание тестовых торгов",
    "start_date": datetime.now().isoformat(),
    "end_date": (datetime.now() + timedelta(days=7)).isoformat(),
    "status": TradeStatus.INTERESTING,
    "responsible_id": 1
}

# Фикстуры для тестовых данных
@pytest.fixture
def test_employee():
    return TEST_EMPLOYEE.copy()

@pytest.fixture
def test_trade():
    return TEST_TRADE.copy()

# Тесты для сотрудников
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Масюченко": "Степан"}

def test_create_and_get_employee(test_employee):
    # Создание сотрудника
    response = client.post("/employees", json=test_employee)
    assert response.status_code == 200
    employee_data = response.json()
    assert employee_data["FIO"] == test_employee["FIO"]
    assert employee_data["position"] == test_employee["position"]
    employee_id = employee_data["id"]
    
    # Получение сотрудника по ID
    response = client.get(f"/employees/{employee_id}")
    assert response.status_code == 200
    assert response.json() == employee_data
    
    # Получение всех сотрудников
    response = client.get("/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(emp["id"] == employee_id for emp in response.json())

def test_update_employee(test_employee):
    # Создание сотрудника
    response = client.post("/employees", json=test_employee)
    employee_id = response.json()["id"]
    
    # Обновление данных
    updated_data = {
        "FIO": "Петров Петр Петрович",
        "position": "Менеджер"
    }
    response = client.put(f"/employees/{employee_id}", json=updated_data)
    assert response.status_code == 200
    updated_employee = response.json()
    assert updated_employee["FIO"] == updated_data["FIO"]
    assert updated_employee["position"] == updated_data["position"]
    
    # Проверка обновления
    response = client.get(f"/employees/{employee_id}")
    assert response.json()["FIO"] == updated_data["FIO"]

def test_delete_employee(test_employee):
    # Создание сотрудника
    response = client.post("/employees", json=test_employee)
    employee_id = response.json()["id"]
    
    # Удаление
    response = client.delete(f"/employees/{employee_id}")
    assert response.status_code == 200
    assert "Сотрудник удалён" in response.json()["message"]
    
    # Проверка удаления
    response = client.get(f"/employees/{employee_id}")
    assert response.status_code == 500  # Так как у вас в коде при ошибке возвращается 500

# Тесты для торгов
def test_create_and_get_trade(test_trade, test_employee):
    # Сначала создаем сотрудника, так как торги требуют responsible_id
    emp_response = client.post("/employees", json=test_employee)
    emp_id = emp_response.json()["id"]
    test_trade["responsible_id"] = emp_id
    
    # Создание торгов
    response = client.post("/trades", json=test_trade)
    assert response.status_code == 200
    trade_data = response.json()
    assert trade_data["title"] == test_trade["title"]
    trade_id = trade_data["id"]
    
    # Получение торгов по ID
    response = client.get(f"/trades/{trade_id}")
    assert response.status_code == 200
    assert response.json() == trade_data
    
    # Получение всех торгов
    response = client.get("/trades")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert any(trade["id"] == trade_id for trade in response.json())

def test_get_trades_by_status(test_trade, test_employee):
    # Создаем сотрудника и торги
    emp_response = client.post("/employees", json=test_employee)
    emp_id = emp_response.json()["id"]
    test_trade["responsible_id"] = emp_id
    
    trade_response = client.post("/trades", json=test_trade)
    trade_id = trade_response.json()["id"]
    
    # Получаем торги по статусу
    response = client.get("/trades/by_status", params={"status": TradeStatus.INTERESTING})
    assert response.status_code == 200
    trades = response.json()
    assert isinstance(trades, list)
    assert any(trade["id"] == trade_id for trade in trades)

def test_get_trades_by_responsible_fio(test_trade, test_employee):
    # Создаем сотрудника и торги
    emp_response = client.post("/employees", json=test_employee)
    emp_id = emp_response.json()["id"]
    test_trade["responsible_id"] = emp_id
    
    trade_response = client.post("/trades", json=test_trade)
    trade_id = trade_response.json()["id"]
    
    # Получаем торги по ФИО ответственного
    response = client.get("/trades/by_responsible_fio", params={"fio": test_employee["FIO"]})
    assert response.status_code == 200
    trades = response.json()
    assert isinstance(trades, list)
    assert any(trade["id"] == trade_id for trade in trades)

def test_update_trade_status(test_trade, test_employee):
    # Создаем сотрудника и торги
    emp_response = client.post("/employees", json=test_employee)
    emp_id = emp_response.json()["id"]
    test_trade["responsible_id"] = emp_id
    
    trade_response = client.post("/trades", json=test_trade)
    trade_id = trade_response.json()["id"]
    
    # Обновляем статус
    new_status = TradeStatus.APPLIED
    response = client.patch(
        f"/trades/{trade_id}/new_status",
        params={"status": new_status}
    )
    assert response.status_code == 200
    assert response.json()["status"] == new_status
    
    # Проверяем обновление
    response = client.get(f"/trades/{trade_id}")
    assert response.json()["status"] == new_status

# Тесты обработки ошибок
def test_get_nonexistent_employee():
    response = client.get("/employees/999999")
    assert response.status_code == 500  # Опять же, у вас 500 при ошибке

def test_create_trade_with_invalid_responsible_id(test_trade):
    invalid_data = test_trade.copy()
    invalid_data["responsible_id"] = 999999
    response = client.post("/trades", json=invalid_data)
    assert response.status_code == 500