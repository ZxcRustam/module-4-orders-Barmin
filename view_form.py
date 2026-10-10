"""Форма просмотра товара."""
import tkinter as tk
from tkinter import messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
from resources import get_product_image
from database import get_product_quantity
from order_manager import create_order
from error_handler import validate_positive_int


class ViewForm:
    """Форма просмотра товара."""

    def __init__(self, parent, product, on_add_to_order=None):
        self.product = product
        self.on_add_to_order = on_add_to_order

        self.window = tk.Toplevel(parent)
        self.window.title(f"Просмотр — {product[1]}")
        self.window.geometry("700x600")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()

    def build_ui(self):
        """Строит интерфейс формы."""
        # Шапка — ГОТОВО
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="КАРТОЧКА ТОВАРА",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Изображение — ГОТОВО
        img_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        img_frame.pack(side="left", padx=10)
        photo = get_product_image(self.product[7], size=(200, 200))
        if photo:
            img_label = tk.Label(img_frame, image=photo, bg=COLOR_MAIN_BG)
            img_label.image = photo
            img_label.pack()

        # Информация — ДОПИСАТЬ
        info_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=20)

        # TODO: Добавь 6 вызовов _add_field:
        #       - Производитель (product[3])
        #       - Наименование (product[1])
        #       - Категория (product[2])
        #       - Характеристики (product[4])
        #       - Цена (f"{product[5]} руб.")
        #       - Модель (product[8])

        # Поле ввода количества — ДОПИСАТЬ
        qty_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        qty_frame.pack(fill="x", padx=20, pady=10)

        # TODO: Label "Количество:"
        # TODO: Entry с self.qty_var = tk.StringVar(value="1")

        # Кнопки — ДОПИСАТЬ
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)

        # TODO: Кнопка "Добавить в заказ" (command=self.add_to_order)
        # TODO: Кнопка "Назад" (command=self.window.destroy)

    def _add_field(self, parent, label, value):
        """
        Добавляет поле в форму.
        :param parent: родительский фрейм
        :param label: название поля
        :param value: значение
        """
        # TODO: Создай фрейм row с фоном COLOR_MAIN_BG
        # TODO: Создай метку с f"{label}:" — жирно, ширина 15, слева
        # TODO: Создай метку со str(value) — слева
        pass

    def add_to_order(self):
        """Обработчик добавления в заказ."""
        # TODO: Проверь self.product — если пусто, showerror
        # TODO: Валидация через validate_positive_int
        # TODO: Если qty > current_qty — showwarning
        # TODO: Оберни в try-except
        # TODO: items = [(self.product[0], self.product[8], qty, self.product[5])]
        # TODO: order_id = create_order("Клиент", items)
        # TODO: Если order_id — showinfo + on_add_to_order() + destroy
        pass