import psycopg2

connection = psycopg2.connect(
    dbname="AMRS",
    user="postgres",      
    password="cport2003",
    host="localhost",      
    port="5432"             
)
# Создание курсора для выполнения запросов
cursor = connection.cursor()

cursor.execute("SELECT * FROM trades;")
rows = cursor.fetchall()
for row in rows:
    print(row)
