import sqlite3
import random


connection = sqlite3.connect("bot_telegram14_4.db")
cursor = connection.cursor()

# Удаление таблицы Users и индекса, если они существуют
cursor.execute("DROP TABLE IF EXISTS Products")
cursor.execute('''
CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL
)
''')
connection.commit()
connection.close()

def initiate_db():
    # """
    # Заполняет таблицу Products тестовыми данными.
    # """
    connection = sqlite3.connect("bot_telegram14_4.db")
    cursor = connection.cursor()
    for i in range(1, 5):
        cursor.execute('''
        INSERT INTO Products (id, title, description, price)
        VALUES (?, ?, ?, ?)
        ''', (i, f"Продукт {i}", f"Описание {i}", i * 100))
    connection.commit()
    connection.close()

def get_all_products():
    """
    Возвращает все записи из таблицы Products.
    """
    connection = sqlite3.connect("bot_telegram14_4.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    connection.close()
    return products

# Пример использования
initiate_db()    # Создание таблицы
products = get_all_products()
for k in products:
    print(k)

# print(get_all_products())  # Получение и вывод всех продуктов