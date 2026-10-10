"""Работа с заказами."""
import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection():
    """Соединение с БД."""
    return sqlite3.connect(DB_PATH)


# ============================================
# ЗАДАНИЕ 1.1. get_all_orders
# ============================================
def get_all_orders():
    """
    Возвращает список всех заказов.
    :return: список кортежей (id, дата, клиент)
    """
    # TODO: Открой соединение через get_connection()
    # TODO: Создай курсор
    # TODO: Выполни SQL: SELECT id, дата, клиент FROM Заказ ORDER BY id DESC
    # TODO: Получи все строки через cur.fetchall()
    # TODO: Закрой соединение
    # TODO: Верни список кортежей
    pass


# ============================================
# ЗАДАНИЕ 1.2. get_order_by_id (вспомогательная)
# ============================================
def get_order_by_id(order_id):
    """
    Возвращает заказ по id.
    :param order_id: id заказа
    :return: кортеж (id, дата, клиент) или None
    """
    # TODO: Открой соединение
    # TODO: Выполни SELECT id, дата, клиент FROM Заказ WHERE id = ?
    # TODO: Получи row = cur.fetchone()
    # TODO: Закрой соединение
    # TODO: Верни row
    pass


# ============================================
# ЗАДАНИЕ 1.3. get_order_items (JOIN)
# ============================================
def get_order_items(order_id):
    """
    Возвращает состав заказа через JOIN.
    :param order_id: id заказа
    :return: список кортежей (id, название, производитель,
                              модель, количество, цена)
    """
    # TODO: Открой соединение
    # TODO: Выполни JOIN таблиц Состав_заказа и Товар
    #       ON Состав_заказа.товар_id = Товар.id
    # TODO: Отфильтруй WHERE Состав_заказа.заказ_id = ?
    # TODO: Передай (order_id,) как параметр
    # TODO: Получи строки
    # TODO: Верни результат
    pass


# ============================================
# ЗАДАНИЕ 1.4. get_order_total
# ============================================
def get_order_total(order_id):
    """
    Возвращает итоговую сумму заказа.
    :param order_id: id заказа
    :return: сумма (float)
    """
    # TODO: Открой соединение
    # TODO: Выполни SELECT SUM(количество * цена)
    #       FROM Состав_заказа WHERE заказ_id = ?
    # TODO: Получи row = cur.fetchone()
    # TODO: Верни row[0] если не None, иначе 0.0
    pass


# ============================================
# ЗАДАНИЕ 1.5. create_order
# ============================================
def create_order(client, items):
    """
    Создаёт заказ с несколькими позициями.
    :param client: ФИО клиента
    :param items: список (product_id, model, quantity, price)
    :return: id заказа или None
    """
    # TODO: Открой соединение и курсор
    # TODO: Оберни в try-except-finally
    # TODO: Получи дату: datetime.now().strftime("%Y-%m-%d")
    # TODO: INSERT INTO Заказ (дата, клиент) VALUES (?, ?)
    # TODO: order_id = cur.lastrowid
    # TODO: Для каждой позиции из items:
    #       - SELECT количество FROM Товар WHERE id = ?
    #       - Если row[0] < quantity — raise ValueError
    #       - INSERT INTO Состав_заказа
    #       - UPDATE Товар SET количество = количество - ?
    # TODO: conn.commit()
    # TODO: Верни order_id
    # TODO: В except — conn.rollback() и верни None
    pass


# ============================================
# ЗАДАНИЕ 1.6. delete_order
# ============================================
def delete_order(order_id):
    """
    Удаляет заказ и восстанавливает остатки.
    :param order_id: id заказа
    :return: True или False
    """
    # TODO: Открой соединение
    # TODO: Оберни в try-except
    # TODO: SELECT товар_id, количество FROM Состав_заказа
    #       WHERE заказ_id = ?
    # TODO: items = cur.fetchall()
    # TODO: Для каждой позиции:
    #       - UPDATE Товар SET количество = количество + ?
    #         WHERE id = ?
    # TODO: DELETE FROM Состав_заказа WHERE заказ_id = ?
    # TODO: DELETE FROM Заказ WHERE id = ?
    # TODO: conn.commit() и верни True
    # TODO: В except — rollback и верни False
    pass


# ============================================
# ЗАДАНИЕ 1.7. update_order_date
# ============================================
def update_order_date(order_id, new_date):
    """
    Обновляет дату заказа.
    :param order_id: id заказа
    :param new_date: новая дата (YYYY-MM-DD)
    :return: True
    """
    # TODO: Открой соединение
    # TODO: UPDATE Заказ SET дата = ? WHERE id = ?
    # TODO: conn.commit()
    # TODO: Закрой соединение
    # TODO: Верни True
    pass


# ============================================
# ЗАДАНИЕ 1.8. delete_order_item
# ============================================
def delete_order_item(item_id):
    """
    Удаляет позицию и восстанавливает остаток.
    :param item_id: id позиции в Состав_заказа
    :return: True или False
    """
    # TODO: Открой соединение
    # TODO: Оберни в try-except
    # TODO: SELECT товар_id, количество FROM Состав_заказа
    #       WHERE id = ?
    # TODO: product_id, quantity = cur.fetchone()
    # TODO: DELETE FROM Состав_заказа WHERE id = ?
    # TODO: UPDATE Товар SET количество = количество + ?
    #       WHERE id = ?
    # TODO: conn.commit() и верни True
    # TODO: В except — rollback и верни False
    pass