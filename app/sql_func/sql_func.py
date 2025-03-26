import sqlite3
from contextlib import contextmanager

# Контекстный менеджер для автоматического подключения/отключения
@contextmanager
def db_conn():
    conn = sqlite3.connect('app/sql_func/efrsb.db')
    try:
        yield conn
    finally:
        conn.close()

#Получить всех сотрудников
def take_all_emp():
    with db_conn() as conn:
        rez = conn.execute('SELECT * FROM employees').fetchall()

    return rez

#Получить сотрудника по id
def take_one_emp_by_id(id):
    with db_conn() as conn:
        rez = conn.execute(f'SELECT * FROM employees WHERE id = {id}').fetchone()
        if rez is None:
            raise ValueError("Сотрудник с таким id не существует") 
        else:
            return rez
    return None

#Записать сотрудника
def write_emp(emp):
    with db_conn() as conn:
        rez = conn.execute('SELECT * FROM employees WHERE FIO = ? AND position = ?', (emp.FIO, emp.position)).fetchone()
        if rez is None:
            conn.execute("INSERT INTO employees (FIO, position) VALUES (?, ?)", (emp.FIO, emp.position))
            conn.commit()
            rez = conn.execute('SELECT * FROM employees WHERE FIO = ? AND position = ?', (emp.FIO, emp.position)).fetchone()
            return rez
        else:
            raise ValueError("Сотрудник с таким ФИО уже существует") 
    return None

#Изменить данные о сотруднике
def rewrite_emp(id, new_emp):
    with db_conn() as conn:
        rez = conn.execute('SELECT * FROM employees WHERE id = ?', (id, )).fetchone()
        if rez is None:
            raise ValueError("Сотрудник с таким id не существует") 
        else:
            conn.execute("UPDATE employees SET FIO = ?, position = ? WHERE id = ?", (new_emp.FIO, new_emp.position, id))
            conn.commit()
            rez = conn.execute('SELECT * FROM employees WHERE id=?', (id, )).fetchone()
            return rez
    return None

#Удалить сотрудника
def delete_emp(id):
    with db_conn() as conn:
        rez = conn.execute('SELECT * FROM employees WHERE id = ?', (id, )).fetchone()
        if rez is not None:
            conn.execute("DELETE FROM employees WHERE id = ?", (id, ))
            conn.commit()
            return rez
        else:
            raise ValueError("Сотрудник с таким id не существует") 
    return None

#Получить все торги
def take_all_trades():
    with db_conn() as conn:
        rez = conn.execute('SELECT * FROM trades').fetchall()
    return rez

#Получить торги по статусу
def take_trade_by_status(status):
    with db_conn() as conn:
        rez = conn.execute(f'SELECT * FROM trades WHERE status = ?', (status,)).fetchall()
        if rez is None:
            raise ValueError("Торгов с таким статусом не существует.") 
        else:
            return rez
    return None

#Получить торги по ФИО
def take_trade_by_FIO(FIO):
    with db_conn() as conn:
        id = (conn.execute('''SELECT id FROM employees WHERE FIO = ?''', (FIO,)).fetchone())[0]
        if id is None:
            raise ValueError("Такого сотрудника не существует") 
        else:
            rez = conn.execute('''
                                SELECT * 
                                FROM trades
                                WHERE responsible_id = ?
                            ''', (id,)).fetchall()
            if rez is None:
                raise ValueError("У сотрудника нет торгов") 
            return rez
    return None

#Записать новые торги
def write_trades(trd):
    with db_conn() as conn:
        rez = conn.execute('SELECT * FROM trades WHERE trade_number=?', (trd.trade_number, )).fetchone()
        if rez is None:
            conn.execute("INSERT INTO trades (trade_number, title, description, start_date, end_date, responsible_id, status) VALUES (?, ?, ?, ?, ?, ?, ?)", (trd.trade_number, trd.title, trd.description, trd.start_date, trd.end_date, trd.responsible_id, trd.status))
            conn.commit()
            rez = conn.execute('SELECT * FROM trades WHERE trade_number = ?', (trd.trade_number, )).fetchone()
            return rez
        else:
            raise ValueError("Такие торги уже существуют.") 
    return None

#Изменить данные о торгах
def rewrite_trades(id, status):
    with db_conn() as conn:
        rez = conn.execute('SELECT * FROM trades WHERE id=?', (id, )).fetchone()
        if rez is not None:
            conn.execute('UPDATE trades SET status = ? WHERE id = ?', (status, id))
            conn.commit()
            rez = conn.execute('SELECT * FROM trades WHERE id = ?', (id, )).fetchone()
            return rez
        else:
            raise ValueError("Таких торгов не существует.") 
    return None