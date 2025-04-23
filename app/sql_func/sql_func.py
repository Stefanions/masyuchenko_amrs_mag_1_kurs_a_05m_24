from contextlib import contextmanager
import psycopg2

# Контекстный менеджер для автоматического подключения/отключения
@contextmanager
def db_conn():
    # conn = psycopg2.connect(
    #     dbname="AMRS",
    #     user="postgres",      
    #     password="cport2003",
    #     host="amrs_postgres",
    #     port="5432"             
    # )
    conn = psycopg2.connect(
        dbname="AMRS",
        user="postgres",      
        password="cport2003",
        host="localhost",
        port="5432"             
    )
    cur = conn.cursor()
    try:
        yield cur, conn
    finally:
        conn.close()

#Получить всех сотрудников
def take_all_emp():
    with db_conn() as (cur, conn):
        cur.execute('SELECT * FROM employees')
        rez = cur.fetchall()

    return rez

#Получить сотрудника по id
def take_one_emp_by_id(id):
    with db_conn() as (cur, conn):
        cur.execute(f'SELECT * FROM employees WHERE id = {id}')
        rez = cur.fetchone()
        if rez is None:
            raise ValueError("Сотрудник с таким id не существует") 
        else:
            return rez
    return None

#Записать сотрудника
def write_emp(emp):
    with db_conn() as (cur, conn):
        cur.execute('SELECT * FROM employees WHERE FIO = %s AND position = %s', (emp.FIO, emp.position))
        rez = cur.fetchone()
        if rez is None:
            cur.execute("INSERT INTO employees (FIO, position) VALUES (%s, %s)", (emp.FIO, emp.position))
            conn.commit()
            cur.execute('SELECT * FROM employees WHERE FIO = %s AND position = %s', (emp.FIO, emp.position))
            rez = cur.fetchone()
            return rez
        else:
            raise ValueError("Сотрудник с таким ФИО уже существует") 
    return None

#Изменить данные о сотруднике
def rewrite_emp(id, new_emp):
    with db_conn() as (cur, conn):
        cur.execute('SELECT * FROM employees WHERE id = %s', (id, ))
        rez = cur.fetchone()
        if rez is None:
            raise ValueError("Сотрудник с таким id не существует") 
        else:
            cur.execute("UPDATE employees SET FIO = %s, position = %s WHERE id = %s", (new_emp.FIO, new_emp.position, id))
            conn.commit()
            cur.execute('SELECT * FROM employees WHERE id=%s', (id, ))
            rez = cur.fetchone()
            return rez
    return None

#Удалить сотрудника
def delete_emp(id):
    with db_conn() as (cur, conn):
        cur.execute('SELECT * FROM employees WHERE id = %s', (id, ))
        rez = cur.fetchone()
        if rez is not None:
            cur.execute("DELETE FROM employees WHERE id = %s", (id, ))
            conn.commit()
            return rez
        else:
            raise ValueError("Сотрудник с таким id не существует") 
    return None

#Получить все торги
def take_all_trades():
    with db_conn() as (cur, conn):
        cur.execute('SELECT * FROM trades')
        rez = cur.fetchall()
    return rez

#Получить торги по статусу
def take_trade_by_status(status):
    with db_conn() as (cur, conn):
        cur.execute('SELECT * FROM trades WHERE status = %s', (status,))
        rez = cur.fetchall()
        if rez is None:
            raise ValueError("Торгов с таким статусом не существует.") 
        else:
            return rez
    return None

#Получить торги по ФИО
def take_trade_by_FIO(FIO):
    with db_conn() as (cur, conn):
        cur.execute('''SELECT id FROM employees WHERE FIO = %s''', (FIO,))
        id = cur.fetchone()
        if id is None:
            raise ValueError("Такого сотрудника не существует") 
        else:
            id = id[0]
            cur.execute('''SELECT * FROM trades WHERE responsible_id = %s''', (id,))
            rez = cur.fetchall()
            if rez is None:
                raise ValueError("У сотрудника нет торгов") 
            return rez
    return None

#Записать новые торги
def write_trades(trd):
    if trd.start_date >= trd.end_date:
        raise ValueError("Даты заполнены не корректно") 
    else:
        with db_conn() as (cur, conn):
            cur.execute('SELECT * FROM trades WHERE trade_number=%s', (trd.trade_number, ))
            rez = cur.fetchone()
            if rez is None:
                cur.execute("INSERT INTO trades (trade_number, title, description, start_date, end_date, responsible_id, status) VALUES (%s, %s, %s, %s, %s, %s, %s)", (trd.trade_number, trd.title, trd.description, trd.start_date, trd.end_date, trd.responsible_id, trd.status))
                conn.commit()
                cur.execute('SELECT * FROM trades WHERE trade_number = %s', (trd.trade_number, ))
                rez = cur.fetchone()
                return rez
            else:
                raise ValueError("Такие торги уже существуют.") 
        return None

#Изменить данные о торгах
def rewrite_trades(id, status):
    with db_conn() as (cur, conn):
        cur.execute('SELECT * FROM trades WHERE id = %s', (id, ))
        rez = cur.fetchone()
        if rez is not None:
            cur.execute('UPDATE trades SET status = %s WHERE id = %s', (status, id))
            conn.commit()
            cur.execute('SELECT * FROM trades WHERE id = %s', (id, ))
            rez = cur.fetchone()
            return rez
        else:
            raise ValueError("Таких торгов не существует.") 
    return None