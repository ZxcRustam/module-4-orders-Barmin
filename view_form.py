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
        
        # Делаем форму модальной поверх каталога
        self.window.grab_set()

        self.build_ui()

    def build_ui(self):
        """Строит интерфейс формы."""
        # Шапка — ГОТОВО
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="КАРТОЧКА ТОВАРА",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG,
                 fg="white").pack(pady=15)

        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Изображение — ГОТОВО
        img_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        img_frame.pack(side="left", padx=10, anchor="n")
        photo = get_product_image(self.product[7], size=(200, 200))
        if photo:
            img_label = tk.Label(img_frame, image=photo, bg=COLOR_MAIN_BG)
            img_label.image = photo
            img_label.pack()
        else:
            img_label = tk.Label(img_frame, text="[НЕТ ФОТО]", font=font(FONT_SIZE_TITLE), bg=COLOR_MAIN_BG, fg="gray")
            img_label.pack(pady=80)

        # Информация — ДОПИСАНО
        info_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=20)

        # Заполняем поля по структуре кортежа продукта
        self._add_field(info_frame, "Производитель", self.product[3])
        self._add_field(info_frame, "Наименование", self.product[1])
        self._add_field(info_frame, "Модель", self.product[8])
        self._add_field(info_frame, "Категория", self.product[2])
        self._add_field(info_frame, "Характеристики", self.product[4])
        
        price_val = self.product[5] if self.product[5] is not None else 0
        self._add_field(info_frame, "Цена", f"{price_val:,.2f} руб.")

        # Поле ввода количества — ДОПИСАНО
        qty_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        qty_frame.pack(fill="x", padx=40, pady=10)

        lbl_qty = tk.Label(qty_frame, text="Количество к заказу:", font=font(FONT_SIZE_NORMAL, bold=True), bg=COLOR_MAIN_BG)
        lbl_qty.pack(side="left", padx=5)

        self.qty_var = tk.StringVar(value="1")
        entry_qty = tk.Entry(qty_frame, textvariable=self.qty_var, font=font(FONT_SIZE_NORMAL), width=10)
        entry_qty.pack(side="left", padx=10)

        # Кнопки — ДОПИСАНО
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", side="bottom", padx=40, pady=20)

        btn_add = tk.Button(
            btn_frame, 
            text="Добавить в заказ", 
            font=font(FONT_SIZE_NORMAL),
            bg=COLOR_ACCENT, 
            fg="white",
            padx=15, 
            pady=5,
            command=self.add_to_order
        )
        btn_add.pack(side="left")

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

    def _add_field(self, parent, label, value):
        """Добавляет отформатированную строчку с полем в форму."""
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", pady=4)

        lbl_title = tk.Label(
            row, 
            text=f"{label}:", 
            font=font(FONT_SIZE_NORMAL, bold=True), 
            bg=COLOR_MAIN_BG, 
            width=15, 
            anchor="w"
        )
        lbl_title.pack(side="left")

        val_text = str(value) if value else "[Не указано]"
        lbl_val = tk.Label(
            row, 
            text=val_text, 
            font=font(FONT_SIZE_NORMAL), 
            bg=COLOR_MAIN_BG, 
            anchor="w",
            justify="left",
            wraplength=350  # Перенос текста, если характеристики длинные
        )
        lbl_val.pack(side="left", fill="x", expand=True)

    def add_to_order(self):
        """Обработчик добавления в заказ."""
        if not self.product:
            messagebox.showerror("Ошибка", "Данные о товаре отсутствуют.")
            return

        # 1. Валидация введенного значения через внешнюю функцию проекта
        qty_str = self.qty_var.get().strip()
        qty = validate_positive_int(qty_str)
        
        if qty is None or qty <= 0:
            messagebox.showwarning("Некорректный ввод", "Пожалуйста, введите корректное целое положительное число.")
            return

        # 2. Проверка реальных остатков товара на складе через БД
        current_qty = get_product_quantity(self.product[0])
        if current_qty is None:
            # На случай, если функция базы вернула ошибку, страхуемся значением из карточки
            current_qty = self.product[6]

        if qty > current_qty:
            messagebox.showwarning(
                "Недостаточно товара", 
                f"На складе доступно всего {current_qty} шт.\nВы запросили: {qty} шт."
            )
            return

        # 3. Оформление покупки (Транзакция в БД)
        try:
            # Структура элементов items для create_order: (product_id, model, quantity, price)
            items = [(self.product[0], self.product[8], qty, self.product[5])]
            
            # Фиксируем покупку на имя дефолтного клиента (или вы можете запрашивать ФИО)
            order_id = create_order("Розничный клиент «ЭлектроМир»", items)
            
            if order_id:
                messagebox.showinfo("Успех", f"Заказ №{order_id} успешно оформлен!")
                
                # Если передан callback — обновляем интерфейс витрины каталога
                if self.on_add_to_order:
                    self.on_add_to_order()
                    
                self.window.destroy()
            else:
                messagebox.showerror("Ошибка БД", "Не удалось сохранить заказ в базе данных.")
                
        except Exception as e:
            messagebox.showerror("Критическая ошибка", f"Произошел сбой при создании транзакции: {e}")
