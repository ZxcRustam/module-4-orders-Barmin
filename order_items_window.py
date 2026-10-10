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
        
        # Делаем окно модальным
        self.window.grab_set()
        
        # Переменная для хранения и редактирования даты
        self.date_var = tk.StringVar()
        
        self.build_ui()
        self.load_order_info()
        self.load_items()

    def is_admin(self):
        """Проверяет роль текущего пользователя."""
        # Предполагается, что структура кортежа пользователя: (id, login, password, name, surname, role)
        if self.current_user and len(self.current_user) > 5:
            return self.current_user[5] == "Администратор"
        return False

    def build_ui(self):
        """Строит интерфейс."""
        # 1. Шапка окна
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        lbl_title = tk.Label(
            header, 
            text=f"СОСТАВ ЗАКАЗА №{self.order_id}", 
            font=font(FONT_SIZE_TITLE, bold=True),
            bg=COLOR_SECONDARY_BG,
            fg="white"
        )
        lbl_title.pack(pady=15)

        # 2. Блок информации о заказе (Дата и Клиент)
        info_frame = tk.LabelFrame(
            self.window, 
            text=" Информация о заказе ", 
            font=font(FONT_SIZE_NORMAL, bold=True),
            bg=COLOR_MAIN_BG, 
            fg=COLOR_SECONDARY_BG,
            padx=15, 
            pady=10
        )
        info_frame.pack(fill="x", padx=20, pady=10)

        # Поле даты
        lbl_date = tk.Label(info_frame, text="Дата (ГГГГ-ММ-ДД):", font=font(FONT_SIZE_NORMAL), bg=COLOR_MAIN_BG)
        lbl_date.grid(row=0, column=0, sticky="w", pady=5)
        
        # Если администратор — разрешаем редактирование, если менеджер — только чтение
        entry_state = "normal" if self.is_admin() else "readonly"
        self.entry_date = tk.Entry(
            info_frame, 
            textvariable=self.date_var, 
            font=font(FONT_SIZE_NORMAL), 
            state=entry_state,
            width=15
        )
        self.entry_date.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Кнопка сохранения даты (только для Администратора)
        if self.is_admin():
            btn_save_date = tk.Button(
                info_frame,
                text="Сохранить дату",
                font=font(FONT_SIZE_NORMAL),
                bg=COLOR_ACCENT,
                fg="white",
                command=self.save_date
            )
            btn_save_date.grid(row=0, column=2, sticky="w", padx=10, pady=5)

        # Поле клиента
        lbl_client_title = tk.Label(info_frame, text="Клиент:", font=font(FONT_SIZE_NORMAL), bg=COLOR_MAIN_BG)
        lbl_client_title.grid(row=1, column=0, sticky="w", pady=5)
        
        self.client_label = tk.Label(info_frame, text="", font=font(FONT_SIZE_NORMAL, bold=True), bg=COLOR_MAIN_BG)
        self.client_label.grid(row=1, column=1, columnspan=2, sticky="w", padx=10, pady=5)

        # 3. Таблица позиций заказа
        table_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("id", "name", "producer", "model", "quantity", "price", "total")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Название")
        self.tree.heading("producer", text="Производитель")
        self.tree.heading("model", text="Модель")
        self.tree.heading("quantity", text="Кол-во")
        self.tree.heading("price", text="Цена (руб.)")
        self.tree.heading("total", text="Всего (руб.)")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=200, anchor="w")
        self.tree.column("producer", width=120, anchor="w")
        self.tree.column("model", width=120, anchor="w")
        self.tree.column("quantity", width=70, anchor="center")
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("total", width=110, anchor="e")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 4. Строка ИТОГО
        self.total_label = tk.Label(
            self.window, 
            text="ИТОГО: 0.00 руб.", 
            font=font(FONT_SIZE_TITLE, bold=True), 
            bg=COLOR_MAIN_BG,
            fg=COLOR_SECONDARY_BG
        )
        self.total_label.pack(anchor="e", padx=20, pady=5)

        # 5. Нижняя панель с кнопками
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", side="bottom", padx=20, pady=15)

        # Кнопка удаления доступна только Администратору
        if self.is_admin():
            self.btn_delete = tk.Button(
                btn_frame,
                text="Удалить позицию",
                font=font(FONT_SIZE_NORMAL),
                bg="#d9534f",  # Красный оттенок для удаления
                fg="white",
                padx=15,
                pady=5,
                command=self.delete_item
            )
            self.btn_delete.pack(side="left", padx=5)

        btn_refresh = tk.Button(
            btn_frame,
            text="Обновить",
            font=font(FONT_SIZE_NORMAL),
            bg=COLOR_ACCENT,
            fg="white",
            padx=15,
            pady=5,
            command=self.refresh_all
        )
        btn_refresh.pack(side="left", padx=5)

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

    def load_order_info(self):
        """Загружает дату и клиента."""
        order = om.get_order_by_id(self.order_id)
        if order:
            self.date_var.set(order[1])
            self.client_label.config(text=order[2])
        else:
            messagebox.showerror("Ошибка", "Не удалось загрузить информацию о заказе.")

    def load_items(self):
        """Загружает позиции заказа в таблицу."""
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        items = om.get_order_items(self.order_id)
        
        for item in items:
            # Считаем стоимость позиции: количество * цена
            # Структура item из БД: (id, название, производитель, модель, количество, цена)
            item_id, name, producer, model, quantity, price = item
            item_total = quantity * price
            
            # Вставляем данные, добавляя итоговую сумму по строке
            self.tree.insert("", tk.END, values=(item_id, name, producer, model, quantity, price, item_total))
            
        # Обновляем общую сумму заказа
        total = om.get_order_total(self.order_id)
        self.total_label.config(text=f"ИТОГО: {total:.2f} руб.")

    def save_date(self):
        """Сохраняет изменённую дату."""
        new_date = self.date_var.get().strip()
        
        # Проверяем корректность формата даты (ГГГГ-ММ-ДД)
        try:
            datetime.strptime(new_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка формата", "Неверный формат даты! Используйте ГГГГ-ММ-ДД (например, 2026-10-03).")
            return
            
        if om.update_order_date(self.order_id, new_date):
            messagebox.showinfo("Успех", "Дата заказа успешно обновлена.")
            self.refresh_all()
        else:
            messagebox.showerror("Ошибка", "Не удалось обновить дату в базе данных.")

    def delete_item(self):
        """Удаляет выбранную позицию."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите позицию для удаления.")
            return
            
        item_id = self.tree.item(selected[0])["values"][0]
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту позицию? Остатки товара вернутся на склад."):
            if om.delete_order_item(item_id):
                messagebox.showinfo("Успех", "Позиция удалена, остатки восстановлены.")
                self.refresh_all()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить позицию.")

    def refresh_all(self):
        """Полное обновление данных в окне."""
        self.load_order_info()
        self.load_items()
