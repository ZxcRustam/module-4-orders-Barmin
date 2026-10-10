"""Окно состава заказа."""
import tkinter as tk
from tkinter import ttk, messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
import order_manager as om
from datetime import datetime


class OrderItemsWindow:
    """Окно состава заказа."""

    def __init__(self, parent, order_id, current_user=None):
        self.order_id = order_id
        self.current_user = current_user

        self.window = tk.Toplevel(parent)
        self.window.title(f"Состав заказа №{order_id}")
        self.window.geometry("900x600")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()
        self.load_order_info()
        self.load_items()

    def is_admin(self):
        """Проверяет роль Администратора."""
        # TODO: Верни True, если current_user[5] == "Администратор"
        pass

    def build_ui(self):
        """Строит интерфейс."""
        # Шапка — ГОТОВО
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=f"СОСТАВ ЗАКАЗА №{self.order_id}",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Информация — ДОПИСАТЬ
        # TODO: info_frame с Label "Дата заказа:" + Entry (state="readonly")
        # TODO: Если is_admin() — state="normal" + кнопка "Сохранить дату"
        # TODO: Label "Клиент:" + self.client_label

        # Treeview — ДОПИСАТЬ
        # TODO: columns = ("id", "name", "production", "model",
        #                  "quantity", "price", "total")
        # TODO: Заголовки: №, Товар, Производитель, Модель, Кол-во, Цена, Сумма
        # TODO: self.tree.pack(...)

        # Итоговая сумма — ДОПИСАТЬ
        # TODO: self.total_label = tk.Label(...)

        # Кнопки — ДОПИСАТЬ
        # TODO: Если is_admin() — кнопка "Удалить позицию"
        # TODO: Кнопка "Обновить"
        # TODO: Кнопка "Назад"

    def load_order_info(self):
        """Загружает дату и клиента."""
        # TODO: order = om.get_order_by_id(self.order_id)
        # TODO: self.date_var.set(order[1])
        # TODO: self.client_label.config(text=order[2])
        pass

    def load_items(self):
        """Загружает позиции заказа."""
        # TODO: Очисти таблицу
        # TODO: items = om.get_order_items(self.order_id)
        # TODO: Для каждого item:
        #       item_total = quantity * price
        #       self.tree.insert("", tk.END, values=(...))
        # TODO: total = om.get_order_total(self.order_id)
        # TODO: self.total_label.config(text=f"ИТОГО: {total:.2f} руб.")
        pass

    def save_date(self):
        """Сохраняет изменённую дату."""
        # TODO: new_date = self.date_var.get()
        # TODO: Проверь формат через datetime.strptime
        # TODO: Если ошибка — messagebox.showerror и return
        # TODO: om.update_order_date(self.order_id, new_date)
        # TODO: messagebox.showinfo
        pass

    def delete_item(self):
        """Удаляет выбранную позицию."""
        # TODO: selected = self.tree.selection()
        # TODO: Если пусто — return
        # TODO: item_id = self.tree.item(selected[0])["values"][0]
        # TODO: askyesno подтверждение
        # TODO: om.delete_order_item(item_id)
        # TODO: self.refresh_all()
        pass

    def refresh_all(self):
        """Обновляет всё."""
        self.load_order_info()
        self.load_items()