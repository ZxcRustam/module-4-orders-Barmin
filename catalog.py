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
    # TODO: Получи количество товара: qty = product[6]
    # TODO: Определи цвет фона: bg_color = _get_card_color(qty)
    # TODO: Создай Frame с рамкой:
    #       card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    # TODO: Размести через card.pack(fill="x", padx=10, pady=5)
    # TODO: Добавь изображение: _add_image(card, product, bg_color)
    # TODO: Добавь текст: _add_text_info(card, product, bg_color, qty)
    # TODO: Привяжи клик на card:
    #       card.bind("<Button-1>", lambda e: _open_view(parent, product, refresh))
    # TODO: Привяжи клик на все дочерние элементы:
    #       for child in card.winfo_children():
    #           child.bind("<Button-1>", lambda e: _open_view(parent, product, refresh))
    # TODO: Верни card
    pass


def _get_card_color(qty):
    """
    Возвращает цвет фона карточки.
    Если количество ≤ 3 — подсветка #ff8080, иначе белый.
    :param qty: количество товара
    :return: HEX-цвет
    """
    # TODO: Верни COLOR_HIGHLIGHT, если qty <= 3, иначе COLOR_MAIN_BG
    pass


def _add_image(card, product, bg_color):
    """
    Добавляет изображение товара (или заглушку).
    :param card: карточка товара
    :param product: кортеж с данными товара
    :param bg_color: цвет фона
    """
    # TODO: Создай Frame для изображения (side="left", padx=10, pady=10)
    # TODO: Получи фото: photo = get_product_image(product[7], size=(100, 100))
    # TODO: Если photo:
    #       - Создай Label с image=photo, bg=bg_color
    #       - Сохрани ссылку: img_label.image = photo
    #       - Упакуй через pack()
    # TODO: Иначе:
    #       - Создай Label с текстом "[НЕТ ФОТО]"
    pass


def _add_text_info(card, product, bg_color, qty):
    """
    Добавляет текстовую информацию о товаре.
    :param card: карточка товара
    :param product: кортеж с данными товара
    :param bg_color: цвет фона
    :param qty: количество
    """
    # TODO: Создай Frame для текста (side="left", fill="both",
    #       expand=True, padx=10, pady=10)
    # TODO: Получи значения с проверкой на пустоту:
    #       name = product[1] if product[1] else "[Без названия]"
    #       production = product[3] if product[3] else "[Без производителя]"
    #       category = product[2] if product[2] else "[Без категории]"
    #       characteristics = product[4] if product[4] else "[Не указаны]"
    #       price = product[5] if product[5] is not None else 0
    # TODO: Добавь метки через _add_label:
    #       - f"{production} | {name}" — bold=True, size=FONT_SIZE_HEADER
    #       - f"Категория: {category}"
    #       - f"Количество: {_indicator(qty)} ({qty})"
    #       - f"Характеристики: {characteristics}"
    #       - f"{price} руб." — bold=True, size=FONT_SIZE_HEADER, align="e"
    pass


def _add_label(parent, text, bg_color, bold=False,
               size=FONT_SIZE_NORMAL, align="w"):
    """
    Добавляет метку с текстом.
    :param parent: родительский фрейм
    :param text: текст метки
    :param bg_color: цвет фона
    :param bold: жирный шрифт
    :param size: размер шрифта
    :param align: выравнивание ("w" — слева, "e" — справа)
    """
    # TODO: Создай tk.Label с text, font=font(size, bold=bold),
    #       bg=bg_color, anchor=align
    # TODO: Упакуй через .pack(fill="x")
    pass


def _indicator(qty):
    """
    Индикатор «много/мало» (порог 5).
    :param qty: количество
    :return: «много» или «мало»
    """
    # TODO: Верни "много" если qty > 5, иначе "мало"
    pass


def _open_view(parent, product, refresh=None):
    """
    Открывает форму просмотра товара.
    :param parent: родительское окно
    :param product: кортеж с данными товара
    :param refresh: callback для обновления каталога
    """
    # TODO: Импортируй ViewForm из view_form
    # TODO: Создай ViewForm(parent, product, on_add_to_order=refresh)
    pass