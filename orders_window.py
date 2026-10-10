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
        
        # Делаем окно модальным (поверх главного)
        self.window.grab_set()
        
        self.build_ui()
        self.load_orders()

    def build_ui(self):
        """Строит интерфейс."""
        # 1. Шапка окна
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        lbl_title = tk.Label(
            header, 
            text="СПИСОК ЗАКАЗОВ", 
            font=font(FONT_SIZE_TITLE, bold=True),
            bg=COLOR_SECONDARY_BG,
            fg="white"
        )
        lbl_title.pack(pady=15)

        # 2. Основная рабочая область для таблицы
        main_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Создаем Treeview
        self.tree = ttk.Treeview(
            main_frame, 
            columns=("id", "date", "client"), 
            show="headings",
            selectmode="browse"
        )
        
        # Настраиваем заголовки
        self.tree.heading("id", text="№")
        self.tree.heading("date", text="Дата")
        self.tree.heading("client", text="Клиент")
        
        # Настраиваем ширину колонок и выравнивание
        self.tree.column("id", width=50, minwidth=50, anchor="center")
        self.tree.column("date", width=120, minwidth=120, anchor="center")
        self.tree.column("client", width=400, minwidth=250, anchor="w")
        
        # Добавляем вертикальный скроллбар для таблицы
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Упаковываем таблицу и скроллбар
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Привязываем двойной клик мыши
        self.tree.bind("<Double-1>", self.on_order_select)

        # 3. Нижняя панель с кнопками управления
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", side="bottom", padx=20, pady=15)

        btn_view = tk.Button(
            btn_frame,
            text="Просмотр состава",
            font=font(FONT_SIZE_NORMAL),
            bg=COLOR_ACCENT,
            fg="white",
            padx=15,
            pady=5,
            command=self.on_order_select
        )
        btn_view.pack(side="left")

        btn_back = tk.Button(
            btn_frame,
            text="Назад",
            font=font(FONT_SIZE_NORMAL),
            bg=COLOR_SECONDARY_BG,
            fg="white",
            padx=15,
            pady=5,
            command=self.window.destroy
        )
        btn_back.pack(side="right")

    def load_orders(self):
        """Загружает заказы."""
        # Очищаем таблицу от старых данных
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        # Получаем актуальный список из базы данных
        orders = om.get_all_orders()
        
        # Заполняем таблицу строками
        for order in orders:
            self.tree.insert("", tk.END, values=order)

    def on_order_select(self, event=None):
        """Обработчик выбора заказа."""
        # Получаем выделенную строку
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Пожалуйста, выберите заказ из списка.")
            return
            
        # Извлекаем id выбранного заказа (первый элемент в values)
        order_id = self.tree.item(selected[0])["values"][0]
        
        # Импортируем окно состава заказа внутри метода, чтобы избежать циклического импорта
        from order_items_window import OrderItemsWindow
        
        # Открываем окно состава для выбранного заказа
        OrderItemsWindow(self.window, order_id, self.current_user)
