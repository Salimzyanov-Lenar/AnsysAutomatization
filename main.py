# Main file for start application
# Главный файл для запуска приложения
import tkinter as tk
from components import AppInterface


root = tk.Tk()
app = AppInterface(root)

root.mainloop()
