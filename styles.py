import tkinter as tk
from tkinter import ttk


def choice_button_styles(button):
    """ Стили для кнопок выбора путей """
    button.configure(
        bg='#007ACC',
        fg='white',
        font=('Arial', 13, 'bold'),
        padx=10,
        pady=6,
        bd=0,
        activebackground='#005A9E',
        activeforeground='white',
        cursor='hand2'
    )

def label_style(widget):
    widget.config(
        font=('Segoe UI', 14, 'bold'),
        bg='#1729B0',  # чуть темнее, насыщенный синий
        fg='white',
    )

def entry_style(widget):
    widget.config(
        font=('Segoe UI', 14),
        bg='white',  # светло-серый фон
        fg='black',  # темно-серый текст
        relief='flat',  # более современный вид без рамки
        bd=0,
        highlightthickness=2,
        highlightbackground='#cccccc',  # светлая рамка
        highlightcolor='#007ACC',  # цвет рамки при фокусе
        insertbackground='#007ACC',  # цвет курсора
    )

def calculate_button_styles(button):
    """ Стили для кнопок выбора путей """
    button.configure(
        bg='white',
        fg='black',
        font=('Arial', 13, 'bold'),
        padx=10,
        pady=6,
        bd=0,
        activebackground='#005A9E',
        activeforeground='white',
        cursor='hand2'
    )

def result_treeview(tree: ttk.Treeview, fields: list, rows: list):
    """ 
    Creating and return table with data
    Создаёт и возвращаёт таблицу с данными
    """
    style = ttk.Style()
    style.theme_use("default")

    # Основной стиль таблицы
    style.configure("Treeview",
                    font=('Segoe UI', 16),
                    rowheight=28,
                    borderwidth=0,
                    relief="flat",
                    background="#f9f9f9",
                    foreground="#333333",
                    fieldbackground="#f9f9f9")

    # Стиль заголовков
    style.configure("Treeview.Heading",
                    font=('Segoe UI', 16, 'bold'),
                    background="#1729B0",
                    foreground="white",
                    relief="flat")

    style.map("Treeview.Heading",
              background=[('active', '#005A9E')])  # цвет при наведении на заголовок

    # Цвета для строк (чередование)
    style.configure("OddRow", background="#ffffff")
    style.configure("EvenRow", background="#e6f0fa")

    # Цвет выделенной строки
    style.map("Treeview",
              background=[('selected', '#1729B0')],
              foreground=[('selected', 'white')])

    # Настройка колонок
    tree["columns"] = fields
    tree["show"] = "headings"

    for field in fields:
        tree.heading(field, text=field)
        tree.column(field, anchor="center", width=480)

    for i, row in enumerate(rows):
        tag = "EvenRow" if i % 2 == 0 else "OddRow"
        tree.insert("", "end", values=row, tags=(tag,))
    
    tree.pack(fill="y",)