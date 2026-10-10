"""Работа с БД."""
import sqlite3
from config import DB_PATH


def get_connection():
    """Соединение с БД."""
    return sqlite3.connect(DB_PATH)


def get_all_products():
    """Возвращает список всех товаров."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_product_quantity(product_id):
    """Возвращает количество товара по id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0


def get_product_sizes(product_id):
    """Возвращает список моделей для товара."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT модель FROM Товар WHERE id = ?", (product_id,))
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows if row[0]]


def get_user_by_login(login):
    """Ищет пользователя по логину."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT Пользователь.id, Пользователь.фамилия,
               Пользователь.имя, Пользователь.отчество,
               Пользователь.логин, Роль.название
        FROM Пользователь
        JOIN Роль ON Пользователь.роль_id = Роль.id
        WHERE Пользователь.логин = ?
    """, (login,))
    row = cur.fetchone()
    conn.close()
    return row