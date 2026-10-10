"""Главное окно приложения."""
import tkinter as tk
from tkinter import ttk, messagebox
from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
import database as db
from catalog import create_product_card
from resources import load_image_proportional, PATH_LOGO, PATH_ICON
from config import APP_TITLE


class MainWindow:
    """Главное окно приложения."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")
        self.root.configure(bg=COLOR_MAIN_BG)
        
        # Установка иконки приложения, если путь задан
        if PATH_ICON:
            try:
                self.root.iconbitmap(PATH_ICON)
            except Exception:
                pass

        self.current_user = None
        self.user_label = None

        self.build_ui()
        self.load_products()
        self.require_auth()

    def build_ui(self):
        """Строит графический интерфейс главного окна."""
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Отображение логотипа компании
        logo = load_image_proportional(PATH_LOGO, max_size=(60, 60))
        if logo:
            logo_label = tk.Label(header, image=logo, bg=COLOR_SECONDARY_BG)
            logo_label.image = logo
            logo_label.pack(side="left", padx=15)

        # Главное название приложения
        tk.Label(header, text="КАТАЛОГ ЭЛЕКТРОНИКИ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG,
                 fg="white").pack(side="left", padx=10)

        # Информация о пользователе (изначально — не авторизован)
        self.user_label = tk.Label(header, text="Не авторизован",
                                   font=font(FONT_SIZE_NORMAL),
                                   bg=COLOR_SECONDARY_BG,
                                   fg="white")
        self.user_label.pack(side="right", padx=15)

        # Область каталога с прокруткой (Canvas + Скроллбар)
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        
        self.catalog_frame = tk.Frame(self.canvas, bg="white")
        self.catalog_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.catalog_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def require_auth(self):
        """Вызывает модальное окно авторизации при старте."""
        from auth import AuthWindow
        AuthWindow(self.root, self.on_auth_success)

    def on_auth_success(self, user):
        """
        Обработчик успешного входа в систему.
        :param user: Кортеж данных (id, фамилия, имя, отчество, логин, роль)
        """
        self.current_user = user
        
        # user[1] - Фамилия, user[2] - Имя, user[3] - Отчество, user[5] - Роль
        fio = f"{user[1]} {user[2]} {user[3] or ''}".strip()
        self.user_label.config(text=f"{fio} ({user[5]})")
        
        # Динамически добавляем функциональные кнопки в зависимости от привилегий
        self.add_role_buttons(user[5])

    def add_role_buttons(self, role):
        """Добавляет кнопки управления в шапку интерфейса на основе роли."""
        header = self.user_label.master

        # Исправляем видимость текста пользователя (делаем цвет черным)
        self.user_label.config(fg="black")

        # Кнопка «Заказы»
        if role in ("Менеджер", "Администратор"):
            tk.Button(header, text="Заказы",
                      command=self.open_orders,
                      bg=COLOR_ACCENT, fg="white",
                      font=font(FONT_SIZE_NORMAL),
                      padx=15, pady=5).pack(side="right", padx=10, pady=15)

        # Кнопка «Админ» (исправлен текст и увеличены отступы padx)
        if role == "Администратор":
            tk.Button(header, text="Админ",
                      command=self.open_admin,
                      bg="#d9534f", fg="white",
                      font=font(FONT_SIZE_NORMAL),
                      padx=15, pady=5).pack(side="right", padx=10, pady=15)


    def open_orders(self):
        """Открывает окно списка заказов."""
        from orders_window import OrdersWindow
        OrdersWindow(self.root, self.current_user)

    def open_admin(self):
        """Открывает окно администратора."""
        messagebox.showinfo("Админ-панель", "Переход в панель администратора системы.")

    def load_products(self):
        """Загружает товары из базы данных и строит их карточки."""
        try:
            products = db.get_all_products()
            for p in products:
                create_product_card(self.catalog_frame, p, refresh=self.refresh_catalog)
        except AttributeError:
            # Вспомогательное сообщение на случай, если модуль database ещё пустой или не дописан
            print("Ошибка: Метод get_all_products() не найден в модуле database.")

    def refresh_catalog(self):
        """Очищает сетку товаров и загружает их заново."""
        for widget in self.catalog_frame.winfo_children():
            widget.destroy()
        self.load_products()

    def run(self):
        """Запуск главного цикла приложения."""
        self.root.mainloop()


if __name__ == "__main__":
    MainWindow().run()
