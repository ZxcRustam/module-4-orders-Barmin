"""Окно списка заказов."""
import tkinter as tk
from tkinter import ttk, messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
import order_manager as om


class OrdersWindow:
    """Окно списка заказов."""

    def __init__(self, parent, current_user=None):
        self.current_user = current_user

        self.window = tk.Toplevel(parent)
        self.window.title("Список заказов")
        self.window.geometry("800x500")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()
        self.load_orders()

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
        tk.Label(header, text="СПИСОК ЗАКАЗОВ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Treeview — ДОПИСАТЬ
        # TODO: columns = ("id", "date", "client")
        # TODO: self.tree = ttk.Treeview(self.window, columns=columns,
        #                                show="headings", height=15)
        # TODO: Настрой заголовки: №, Дата, Клиент
        # TODO: Настрой ширину: id=50, date=120, client=400
        # TODO: self.tree.pack(fill="both", expand=True, padx=20, pady=20)
        # TODO: self.tree.bind("<Double-1>", self.on_order_select)

        # Кнопки — ДОПИСАТЬ
        # TODO: Создай btn_frame
        # TODO: Кнопки:
        #       - "Просмотр состава" (command=self.on_order_select)
        #       - "Обновить" (command=self.load_orders)
        #       - "Назад" (command=self.window.destroy)

    def load_orders(self):
        """Загружает заказы из БД."""
        # TODO: Очисти таблицу: for row in self.tree.get_children(): delete
        # TODO: orders = om.get_all_orders()
        # TODO: Для каждого order — self.tree.insert("", tk.END, values=order)
        pass

    def on_order_select(self, event=None):
        """Обработчик выбора заказа."""
        # TODO: selected = self.tree.selection()
        # TODO: Если пусто — messagebox.showwarning и return
        # TODO: item = self.tree.item(selected[0])
        # TODO: order_id = item["values"][0]
        # TODO: from order_items_window import OrderItemsWindow
        # TODO: OrderItemsWindow(self.window, order_id, self.current_user)
        pass