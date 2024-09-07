import sqlite3

def create_products_table():
    connection = sqlite3.connect("bot_telegram14_4.db")
    cursor = connection.cursor()

    # Удаление таблицы Products, если она существует
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

def create_users_table():
    connection = sqlite3.connect("not_telegram3.db")
    cursor = connection.cursor()
    
    # Удаление таблицы Users, если она существует
    cursor.execute("DROP TABLE IF EXISTS Users")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id_user INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER,
        balance INTEGER NOT NULL
    )
    ''')
    connection.commit()
    connection.close()

def initiate_db():
    """
    Заполняет таблицу Products тестовыми данными.
    """
    connection = sqlite3.connect("bot_telegram14_4.db")
    cursor = connection.cursor()
    for i in range(1, 5):
        cursor.execute('''
        INSERT INTO Products (id, title, description, price)
        VALUES (?, ?, ?, ?)
        ''', (i, f"Продукт {i}", f"Описание {i}", i * 100))
    connection.commit()
    connection.close()

def add_user(username, email, age):
    connection = sqlite3.connect('not_telegram3.db')
    cursor = connection.cursor()

    # Выполняем SQL-запрос для добавления данных
    cursor.execute('''
    INSERT INTO Users (username, email, age, balance)
    VALUES (?, ?, ?, ?)
    ''', (username, email, age, 1000))

    # Сохраняем изменения
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

def get_users_count():
    """
    Возвращает количество пользователей в таблице Users.
    """
    connection = sqlite3.connect("not_telegram3.db")
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM Users")
    count = cursor.fetchone()[0]
    connection.close()
    return count

def is_included(username):
    """
    Проверяет, существует ли пользователь с заданным именем в таблице Users.

    :param username: Имя пользователя для проверки.
    :return: True, если пользователь существует, иначе False.
    """
    connection = sqlite3.connect("not_telegram3.db")
    cursor = connection.cursor()
    cursor.execute('''
    SELECT COUNT(*) FROM Users WHERE username = ?
    ''', (username,))
    count = cursor.fetchone()[0]
    connection.close()
    return count > 0