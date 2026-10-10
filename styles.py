"""Стили приложения по руководству КИМ."""
import tkinter as tk

# Цвета
COLOR_MAIN_BG = "#FFFFFF"
COLOR_SECONDARY_BG = "#D2F6E7"
COLOR_ACCENT = "#70B2AF"
COLOR_HIGHLIGHT = "#ff8080"

# Шрифт
FONT_FAMILY = "Calibri"
FONT_SIZE_SMALL = 10
FONT_SIZE_NORMAL = 12
FONT_SIZE_HEADER = 14
FONT_SIZE_TITLE = 18


def font(size=FONT_SIZE_NORMAL, bold=False):
    """Возвращает кортеж шрифта."""
    return (FONT_FAMILY, size, "bold" if bold else "normal")