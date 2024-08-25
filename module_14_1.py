import sqlite3
import random
# Подключение к базе данных
connection =sqlite3.connect("not_telegram3.db")
cursor = connection.cursor()

# Удаление таблицы Users и индекса, если они существуют
cursor.execute("DROP TABLE IF EXISTS Users")
cursor.execute("DROP INDEX IF EXISTS idx_email")

# Создание таблицы Users заново
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)

''')
# Создание индекса на поле email
cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")
#cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)",(User1,example1@gmail.com,10,1000))
# Заполнение таблицы новыми записями
for i in range(1, 11):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)",
                   (f"User{i}", f"example{i}@gmail.com", i*10, 1000))
    if i % 2 == 1:
        cursor.execute("UPDATE Users SET balance =  ? WHERE id = ?", (500, i))

for i in range(1, 11):
    if i % 3 == 1:
        cursor.execute("DELETE FROM Users WHERE id = ?", (i,))

cursor.execute("SELECT username,email,age,balance FROM Users WHERE age <>? ", (60,))
users = cursor.fetchall()
for user in users:
    print(user)
# Сохранение изменений и закрытие соединения
connection.commit()
connection.close()

