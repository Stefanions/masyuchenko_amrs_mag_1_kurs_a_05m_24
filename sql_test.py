import sqlite3
from datetime import datetime, timedelta
import random
from faker import Faker
import random

if __name__ == "__main__":
    conn = sqlite3.connect("app/sql_func/efrsb.db")
    mas_state = ["active", "applied", "purchased", "not purchased"]
    rez = conn.execute("select * from trades").fetchall()
    for i in rez:
        conn.execute("update trades set status = ? where id = ?", (random.choice(mas_state), i[0]))
        conn.commit()