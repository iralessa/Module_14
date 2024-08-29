import sqlite3
import random
# Подключение к базе данных
connection =sqlite3.connect("not_telegram3.db")
cursor = connection.cursor()

# Удаление таблицы Users и индекса, если они существуют
#cursor.execute("DROP TABLE IF EXISTS Users")
#cursor.execute("DROP INDEX IF EXISTS idx_email")

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
# for i in range(1, 11):
#     cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)",
#                    (f"User{i}", f"example{i}@gmail.com", i*10, 1000))
#     if i % 2 == 1:
#         cursor.execute("UPDATE Users SET balance =  ? WHERE id = ?", (500, i))
#
# for i in range(1, 11):
#     if i % 3 == 1:
#         cursor.execute("DELETE FROM Users WHERE id = ?", (i,))
#
# cursor.execute("SELECT username,email,age,balance FROM Users WHERE age <>? ", (60,))
# users = cursor.fetchall()
# for user in users:
#     print(user)
cursor.execute("DELETE FROM Users WHERE id = ?", (6,))
cursor.execute("SELECT COUNT(*) FROM Users")
total1 = cursor.fetchone()[0]
print("общее количество записей =", total1)
cursor.execute("SELECT SUM(balance) FROM Users")
total2 = cursor.fetchone()[0]
print("сумма всех балансов =", total2)
cursor.execute("SELECT AVG(balance) FROM Users")
total3 = cursor.fetchone()[0]
print("средний баланс всех пользователей =", total3)
print("ДОП. ПРОВЕРКА! средний баланс всех пользователей =", total2/total1)
# Сохранение изменений и закрытие соединения
connection.commit()
connection.close()
