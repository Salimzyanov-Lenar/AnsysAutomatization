import tkinter as tk
from tkinter import ttk


def choice_button_styles(button):
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
        bg='#1729B0',
        fg='white',
    )

def entry_style(widget):
    widget.config(
        font=('Segoe UI', 14),
        bg='white',
        fg='black',
        relief='flat',
        bd=0,
        highlightthickness=2,
        highlightbackground='#cccccc',
        highlightcolor='#007ACC',
        insertbackground='#007ACC',
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

def result_treeview(parent, fields: list, rows: list) -> ttk.Treeview:
    """
    Создаёт таблицу с данными, стилизует её и добавляет скроллбары.
    Возвращает таблицу и ссылку на контейнер для удобного удаления.
    """
    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview",
                    font=('Segoe UI', 16),
                    rowheight=28,
                    background="#f9f9f9",
                    foreground="#333333",
                    fieldbackground="#f9f9f9")

    style.configure("Treeview.Heading",
                    font=('Segoe UI', 16, 'bold'),
                    background="#1729B0",
                    foreground="white")

    style.map("Treeview.Heading", background=[('active', '#005A9E')])
    style.map("Treeview", background=[('selected', '#1729B0')],
                          foreground=[('selected', 'white')])

    # Контейнер для таблицы и скроллбаров
    container = ttk.Frame(parent)
    container.pack(fill='both')

    tree = ttk.Treeview(container, columns=fields, show='headings')
    tree.tag_configure('oddrow', background='#ffffff')
    tree.tag_configure('evenrow', background='#e6f0fa')

    # Скроллбары
    vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    for field in fields:
        tree.heading(field, text=field, anchor='center')
        tree.column(field, anchor='center', width=220)

    for i, row in enumerate(rows):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree.insert('', 'end', values=row, tags=(tag,))

    return container, tree