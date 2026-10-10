"""Работа с заказами."""
import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection():
    """Соединение с БД."""
    return sqlite3.connect(DB_PATH)


# ====================================================================
# 1.1. get_all_orders() — список всех заказов
# ====================================================================
def get_all_orders():
    """Возвращает список всех заказов."""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id, дата, клиент FROM Заказ ORDER BY id DESC")
    orders = cur.fetchall()
    
    conn.close()
    return orders


# ====================================================================
# 1.2. get_order_items(order_id) — состав заказа (JOIN)
# ====================================================================
def get_order_items(order_id):
    """
    Возвращает состав заказа.
    :param order_id: id заказа
    :return: список (id, название, производитель, модель, количество, цена)
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Связываем таблицу Состав_заказа и Товар через JOIN
    query = """
        SELECT Состав_заказа.id, Товар.название, Товар.производитель, 
               Товар.модель, Состав_заказа.количество, Состав_заказа.цена
        FROM Состав_заказа
        JOIN Товар ON Состав_заказа.товар_id = Товар.id
        WHERE Состав_заказа.заказ_id = ?
    """
    cur.execute(query, (order_id,))
    items = cur.fetchall()
    
    conn.close()
    return items


# ====================================================================
# 1.3. get_order_total(order_id) — итоговая сумма
# ====================================================================
def get_order_total(order_id):
    """
    Возвращает итоговую сумму заказа.
    :param order_id: id заказа
    :return: сумма (float)
    """
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT SUM(количество * цена) FROM Состав_заказа WHERE заказ_id = ?", (order_id,))
    row = cur.fetchone()
    
    conn.close()
    
    # Если в заказе нет позиций, SUM вернет None, тогда возвращаем 0.0
    if row and row[0] is not None:
        return float(row[0])
    return 0.0


# ====================================================================
# 1.4. create_order(client, items) — создание заказа
# ====================================================================
def create_order(client, items):
    """
    Создаёт заказ с несколькими позициями.
    :param client: ФИО клиента
    :param items: список кортежей (product_id, model, quantity, price)
    :return: id заказа или None
    """
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # 1. Получаем текущую дату
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # 2. Создаем запись в таблице Заказ
        cur.execute("INSERT INTO Заказ (дата, клиент) VALUES (?, ?)", (current_date, client))
        order_id = cur.lastrowid
        
        # 3. Добавляем позиции и уменьшаем остатки на складе
        for product_id, model, quantity, price in items:
            # Проверяем остаток товара на складе
            cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
            row = cur.fetchone()
            
            if not row or row[0] < quantity:
                # Если товара недостаточно, вызываем ошибку для отката транзакции
                raise ValueError(f"Недостаточно товара с id {product_id} на складе.")
            
            # Добавляем в Состав_заказа
            cur.execute(
                "INSERT INTO Состав_заказа (заказ_id, товар_id, количество, цена) VALUES (?, ?, ?, ?)",
                (order_id, product_id, quantity, price)
            )
            
            # Списываем количество со склада
            cur.execute(
                "UPDATE Товар SET количество = количество - ? WHERE id = ?",
                (quantity, product_id)
            )
            
        conn.commit()
        return order_id
        
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при создании заказа: {e}")
        return None
    finally:
        conn.close()


# ====================================================================
# 1.5. delete_order(order_id) — удаление заказа
# ====================================================================
def delete_order(order_id):
    """
    Удаляет заказ и восстанавливает остатки.
    :return: True или False
    """
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # 1. Получаем все товары из этого заказа, чтобы вернуть их на склад
        cur.execute("SELECT товар_id, количество FROM Состав_заказа WHERE заказ_id = ?", (order_id,))
        items = cur.fetchall()
        
        # 2. Возвращаем остатки на склад
        for product_id, quantity in items:
            cur.execute(
                "UPDATE Товар SET количество = количество + ? WHERE id = ?",
                (quantity, product_id)
            )
            
        # 3. Удаляем позиции из Состава_заказа
        cur.execute("DELETE FROM Состав_заказа WHERE заказ_id = ?", (order_id,))
        
        # 4. Удаляем сам заказ
        cur.execute("DELETE FROM Заказ WHERE id = ?", (order_id,))
        
        conn.commit()
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при удалении заказа: {e}")
        return False
    finally:
        conn.close()


# ====================================================================
# 1.6. update_order_date(order_id, new_date) — изменение даты
# ====================================================================
def update_order_date(order_id, new_date):
    """
    Обновляет дату заказа.
    :return: True или False
    """
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("UPDATE Заказ SET дата = ? WHERE id = ?", (new_date, order_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка при изменении даты: {e}")
        return False
    finally:
        conn.close()


# ====================================================================
# 1.7. delete_order_item(item_id) — удаление позиции
# ====================================================================
def delete_order_item(item_id):
    """
    Удаляет позицию из заказа и восстанавливает остаток товара на складе.
    :return: True или False
    """
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # 1. Находим товар_id и количество удаляемой позиции
        cur.execute("SELECT товар_id, количество FROM Состав_заказа WHERE id = ?", (item_id,))
        row = cur.fetchone()
        
        if row:
            product_id, quantity = row
            
            # 2. Удаляем позицию из состава заказа
            cur.execute("DELETE FROM Состав_заказа WHERE id = ?", (item_id,))
            
            # 3. Возвращаем товар на склад
            cur.execute(
                "UPDATE Товар SET количество = количество + ? WHERE id = ?",
                (quantity, product_id)
            )
            
            conn.commit()
            return True
        return False
        
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при удалении позиции заказа: {e}")
        return False
    finally:
        conn.close()

def get_order_by_id(order_id):
    """Возвращает информацию о конкретном заказе по его id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, дата, клиент FROM Заказ WHERE id = ?", (order_id,))
    order = cur.fetchone()
    conn.close()
    return order
