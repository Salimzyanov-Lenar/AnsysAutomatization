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
