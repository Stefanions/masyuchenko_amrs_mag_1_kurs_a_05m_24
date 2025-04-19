import pytest
from fastapi.testclient import TestClient
from app.main import app
from sql_func.sql_func import take_all_emp

# Создаем клиент для тестирования
client = TestClient(app)

# Тест для корневого маршрута "/"
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Масюченко": "Степан"}

# Тест для получения всех сотрудников
def test_get_employees(mocker):
    mock_data = [(1, "Иванов Иван", "Менеджер"), (2, "Петров Петр", "Аналитик")]
    mocker.patch("app.main.take_all_emp", return_value=mock_data)
    response = client.get("/employees")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "FIO": "Иванов Иван", "position": "Менеджер"},
        {"id": 2, "FIO": "Петров Петр", "position": "Аналитик"},
    ]

# Тест для получения сотрудника по ID
def test_get_employee_by_id(mocker):
    mock_data = (1, "Иванов Иван", "Менеджер")
    mocker.patch("app.main.take_one_emp_by_id", return_value=mock_data)
    response = client.get("/employees/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "FIO": "Иванов Иван", "position": "Менеджер"}

# Тест для добавления нового сотрудника
def test_create_employee(mocker):
    mock_data = (3, "Сидоров Сидор", "Разработчик")
    mocker.patch("app.main.write_emp", return_value=mock_data)
    new_employee = {"FIO": "Сидоров Сидор", "position": "Разработчик"}
    response = client.post("/employees", json=new_employee)
    assert response.status_code == 200
    assert response.json() == {"id": 3, "FIO": "Сидоров Сидор", "position": "Разработчик"}

# Тест для обновления данных сотрудника
def test_update_employee(mocker):
    mock_data = (1, "Иванов Иван Иванович", "Старший менеджер")
    mocker.patch("app.main.rewrite_emp", return_value=mock_data)
    updated_employee = {"FIO": "Иванов Иван Иванович", "position": "Старший менеджер"}
    response = client.put("/employees/1", json=updated_employee)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "FIO": "Иванов Иван Иванович", "position": "Старший менеджер"}

# Тест для удаления сотрудника
def test_delete_employee(mocker):
    mock_data = (1, "Иванов Иван", "Менеджер")
    mocker.patch("app.main.delete_emp", return_value=mock_data)
    response = client.delete("/employees/1")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Сотрудник удалён",
        "id": 1,
        "FIO": "Иванов Иван",
        "position": "Менеджер",
    }

# Тест получения всех торгов
def test_get_trades(mocker):
    mock_data = [
        (1, "TRADE001", "Торги 1", "Описание торгов 1", "2025-03-29T06:30:18", "2025-03-30T06:30:18", 1, "applied"),
        (2, "TRADE002", "Торги 2", "Описание торгов 2", "2025-03-09T05:11:06", "2025-03-10T05:11:06", 2, "not purchased"),
    ]
    mocker.patch("app.main.take_all_trades", return_value=mock_data)
    response = client.get("/trades")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "trade_number": "TRADE001",
            "title": "Торги 1",
            "description": "Описание торгов 1",
            "start_date": "2025-03-29T06:30:18",
            "end_date": "2025-03-30T06:30:18",
            "status": "applied",
            "responsible_id": 1,
        },
        {
            "id": 2,
            "trade_number": "TRADE002",
            "title": "Торги 2",
            "description": "Описание торгов 2",
            "start_date": "2025-03-09T05:11:06",
            "end_date": "2025-03-10T05:11:06",
            "status": "not purchased",
            "responsible_id": 2,
        },
    ]

# Тест для получения торгов по статусу
def test_get_trades_by_status(mocker):
    mock_data = [
        (1, "TRADE001", "Торги 1", "Описание торгов 1", "2025-03-29T06:30:18", "2025-03-30T06:30:18", 1, "applied"),
    ]
    mocker.patch("app.main.take_trade_by_status", return_value=mock_data)
    response = client.get("/trades/by_status?status=applied")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "trade_number": "TRADE001",
            "title": "Торги 1",
            "description": "Описание торгов 1",
            "start_date": "2025-03-29T06:30:18",
            "end_date": "2025-03-30T06:30:18",
            "status": "applied",
            "responsible_id": 1,
        }
    ]

# Тест для получения торгов по ФИО ответственного сотрудника
def test_get_trades_by_responsible_fio(mocker):
    # Мокаем функцию take_trade_by_FIO из sql_func.sql_func
    mock_data = [
        (1, "TRADE001", "Торги 1", "Описание торгов 1", "2025-03-29T06:30:18", "2025-03-30T06:30:18", 1, "applied"),
    ]
    mocker.patch("app.main.take_trade_by_FIO", return_value=mock_data)
    response = client.get("/trades/by_responsible_fio?fio=Иванов Иван")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "trade_number": "TRADE001",
            "title": "Торги 1",
            "description": "Описание торгов 1",
            "start_date": "2025-03-29T06:30:18",
            "end_date": "2025-03-30T06:30:18",
            "status": "applied",
            "responsible_id": 1,
        }
    ]

# Тест для добавления новых торгов
def test_create_trade(mocker):
    # Мокаем функцию write_trades из sql_func.sql_func
    mock_data = (1, "TRADE001", "Торги 1", "Описание торгов 1", "2025-03-29T06:30:18", "2025-03-30T06:30:18", 1, "applied")
    mocker.patch("app.main.write_trades", return_value=mock_data)
    new_trade = {
        "trade_number": "TRADE001",
        "title": "Торги 1",
        "description": "Описание торгов 1",
        "start_date": "2025-03-29T06:30:18",
        "end_date": "2025-03-30T06:30:18",
        "status": "applied",
        "responsible_id": 1
    }
    response = client.post("/trades", json=new_trade)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "trade_number": "TRADE001",
        "title": "Торги 1",
        "description": "Описание торгов 1",
        "start_date": "2025-03-29T06:30:18",
        "end_date": "2025-03-30T06:30:18",
        "status": "applied",
        "responsible_id": 1
    }

# Тест для изменения статуса торгов
def test_update_trade_status(mocker):
    mock_data = (1, "TRADE001", "Торги 1", "Описание торгов 1", "2025-03-29T06:30:18", "2025-03-30T06:30:18", 1, "not purchased")
    mocker.patch("app.main.rewrite_trades", return_value=mock_data)
    response = client.patch("/trades/1/new_status?status=not purchased")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "trade_number": "TRADE001",
        "title": "Торги 1",
        "description": "Описание торгов 1",
        "start_date": "2025-03-29T06:30:18",
        "end_date": "2025-03-30T06:30:18",
        "status": "not purchased",
        "responsible_id": 1,
    }

# Тест проверка не корректного id при получении сотрудника
def test_get_employee_by_id_noid(mocker):
    mocker.patch("app.main.take_one_emp_by_id", return_value=None)
    response = client.get("/employees/999")
    assert response.status_code == 500
    assert "detail" in response.json()
    assert "NoneType" in response.json()["detail"]

# Тест некоректного статуса
def test_update_trade_status_invalid_status():
    response = client.patch("/trades/1/new_status?status=not purchasadsed")
    assert response.status_code == 422
