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
        font=('Arial', 16),
        bg='#007ACC',
        fg='white')

def entry_style(widget):
    widget.config(
        font=('Arial', 16),
        bg='#f4f4f4',
        fg='black',
        relief='solid',
        bd=1)

def result_treeview(tree: ttk.Treeview, fields: list, rows: list):
    """ 
    Creating and return table with data
    Создаёт и возвращаёт таблицу с данными
    """
    style = ttk.Style()
    style.theme_use("default")

    # Стили для основного отображения
    style.configure("Treeview",
                    font=('Arial', 14),
                    rowheight=25,
                    borderwidth=1,
                    relief="solid")

    # Стили для заголовков
    style.configure("Treeview.Heading",
                    font=('Arial', 13,),
                    background="white",
                    relief="raised")

    # Цвет строк
    style.map("Treeview", background=[('selected', '#007acc')])
    style.configure("EvenRow", background="#ffffff")
    style.configure("OddRow", background="#f2f2f2")

    # Настройка колонок
    tree["columns"] = fields
    tree["show"] = "headings"

    for field in fields:
        tree.heading(field, text=field)
        tree.column(field, anchor="center", width=100)

    for i, row in enumerate(rows):
        tag = "EvenRow" if i % 2 == 0 else "OddRow"
        tree.insert("", "end", values=row, tags=(tag,))
    
    tree.pack(fill="both",)