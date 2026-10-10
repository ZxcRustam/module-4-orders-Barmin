"""Каталог товаров."""
import tkinter as tk
from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)
from resources import get_product_image


def create_product_card(parent, product, refresh=None):
    """
    Создаёт карточку товара.
    :param parent: родительский контейнер
    :param product: кортеж (id, название, категория, производитель,
                            характеристики, цена, количество,
                            изображение, модель)
    :param refresh: callback для обновления каталога после заказа
    :return: созданный Frame
    """
    # 1. Получаем количество товара
    qty = product[6]
    
    # 2. Определяем цвет фона в зависимости от остатка
    bg_color = _get_card_color(qty)
    
    # 3. Создаем Frame с рамкой
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    
    # 4. Размещаем карточку в контейнере
    card.pack(fill="x", padx=10, pady=5)
    
    # 5. Добавляем изображение
    _add_image(card, product, bg_color)
    
    # 6. Добавляем текстовую информацию
    _add_text_info(card, product, bg_color, qty)
    
    # 7. Привязываем клик на саму карточку
    card.bind("<Button-1>", lambda e: _open_view(parent, product, refresh))
    
    # 8. Привязываем клик на все дочерние элементы, чтобы клик в любое место открывал форму
    for child in card.winfo_children():
        child.bind("<Button-1>", lambda e: _open_view(parent, product, refresh))
        # Если у дочернего элемента есть свои вложенные элементы (например, фреймы под картинку/текст)
        for sub_child in child.winfo_children():
            sub_child.bind("<Button-1>", lambda e: _open_view(parent, product, refresh))
            
    # 9. Возвращаем созданный Frame карточки
    return card


def _get_card_color(qty):
    """
    Возвращает цвет фона карточки.
    Если количество ≤ 3 — подсветка #ff8080, иначе белый.
    :param qty: количество товара
    :return: HEX-цвет
    """
    # Если товара 3 или меньше, подсвечиваем его цветом предупреждения
    if qty <= 3:
        return COLOR_HIGHLIGHT
    return COLOR_MAIN_BG


def _add_image(card, product, bg_color):
    """
    Добавляет изображение товара (или заглушку).
    :param card: карточка товара
    :param product: кортеж с данными товара
    :param bg_color: цвет фона
    """
    # Создаем Frame для изображения слева
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)
    
    # Получаем фото через функцию ресурсов
    photo = get_product_image(product[7], size=(100, 100))
    
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo  # Сохраняем ссылку на объект изображения, чтобы сборщик мусора его не удалил
        img_label.pack()
    else:
        img_label = tk.Label(
            img_frame, 
            text="[НЕТ ФОТО]", 
            font=font(FONT_SIZE_NORMAL, bold=True), 
            bg=bg_color, 
            fg="gray"
        )
        img_label.pack(pady=40)  # Центрируем заглушку по высоте


def _add_text_info(card, product, bg_color, qty):
    """
    Добавляет текстовую информацию о товаре.
    :param card: карточка товара
    :param product: кортеж с данными товара
    :param bg_color: цвет фона
    :param qty: количество
    """
    # Создаем Frame для текста, который растягивается на всю оставшуюся область чека
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    
    # Получаем значения из кортежа с проверкой на пустые поля (None)
    name = product[1] if product[1] else "[Без названия]"
    category = product[2] if product[2] else "[Без категории]"
    production = product[3] if product[3] else "[Без производителя]"
    characteristics = product[4] if product[4] else "[Не указаны]"
    price = product[5] if product[5] is not None else 0
    
    # Добавляем текстовые метки на карточку по порядку
    _add_label(text_frame, text=f"{production} | {name}", bg_color=bg_color, bold=True, size=FONT_SIZE_HEADER)
    _add_label(text_frame, text=f"Категория: {category}", bg_color=bg_color)
    _add_label(text_frame, text=f"Количество: {_indicator(qty)} ({qty})", bg_color=bg_color)
    _add_label(text_frame, text=f"Характеристики: {characteristics}", bg_color=bg_color)
    
    # Вывод цены справа
    _add_label(text_frame, text=f"{price:,.2f} руб.", bg_color=bg_color, bold=True, size=FONT_SIZE_HEADER, align="e")


def _add_label(parent, text, bg_color, bold=False, size=FONT_SIZE_NORMAL, align="w"):
    """
    Добавляет метку с текстом.
    :param parent: родительский фрейм
    :param text: текст метки
    :param bg_color: цвет фона
    :param bold: жирный шрифт
    :param size: размер шрифта
    :param align: выравнивание ("w" — слева, "e" — справа)
    """
    # Создаем tk.Label с заданными параметрами форматирования
    lbl = tk.Label(
        parent, 
        text=text, 
        font=font(size, bold=bold), 
        bg=bg_color, 
        anchor=align
    )
    # Упаковываем во весь доступный по горизонтали размер фрейма
    lbl.pack(fill="x")


def _indicator(qty):
    """
    Индикатор «много/мало» (порог 5).
    :param qty: количество
    :return: «много» или «мало»
    """
    if qty > 5:
        return "много"
    return "мало"


def _open_view(parent, product, refresh=None):
    """
    Открывает форму просмотра товара.
    :param parent: родительское окно
    :param product: кортеж с данными товара
    :param refresh: callback для обновления каталога
    """
    # Импортируем ViewForm внутри метода, чтобы избежать циклической зависимости при импорте
    from view_form import ViewForm
    # Открываем форму детального просмотра товара
    ViewForm(parent, product, on_add_to_order=refresh)
