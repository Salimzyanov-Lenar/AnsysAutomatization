import tkinter as tk
from tkinter import filedialog
from services import get_params_from_config, create_new_config
from executor import execute_with_updated_config


class AppInterface:
    def __init__(self, root):
        # Windows settings
        self.root = root
        self.root.title("AnsysAutomatization")
        self.root.geometry("720x480")
        self.label = tk.Label(root, text="Выберите файл", font=('Arial', 12))
        self.label.pack(pady=20)
        self.button = tk.Button(root, text="Выберите файл", command=self.on_button_click)
        self.button.pack()
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=20)

        # Config parameters dict
        self.params = dict | None
        self.strength_limit = None
        self.strength_entry = None

    def on_button_click(self):
        """ Saving choosen config file """
        file_path = filedialog.askopenfilename()

        if file_path:
            with open(file_path, mode="r", encoding="utf-8") as file:
                working_config = file.read()

            # Save working_config
            with open("working_config.wbjn", mode="w", encoding="utf-8") as file:
                file.write(working_config)

            self.label.config(text=f"Выбран путь:\n{file_path}")

            try:
                self.params = get_params_from_config()
                self.create_input_fields()
            except Exception as e:
                tk.messagebox.showerror("Ошибка", str(e))


    def create_input_fields(self):
        """ Creating a input fields which depending on config """
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        if not self.params:
            return

        row = 0
        # Links for input fields
        self.entries = {}

        if isinstance(self.params, dict):
            for key, value in self.params.items():
                label = tk.Label(self.input_frame, text=key)
                label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

                entry = tk.Entry(self.input_frame)
                entry.insert(0, str(value))
                entry.grid(row=row, column=1, padx=10, pady=5, sticky="e")

                self.entries[key] = entry
                row += 1

            self.strength_label = tk.Label(self.input_frame, text="Предел прочности")
            self.strength_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

            self.strength_entry = tk.Entry(self.input_frame)
            self.strength_entry.grid(row=row, column=1, padx=10, pady=5, sticky="e")
            row += 1

            # Button for saving changes
            save_button = tk.Button(self.input_frame, text="Рассчитать", command=self.save_params)
            save_button.grid(row=row, column=0, columnspan=2, pady=10)


    def save_params(self):
        """ Function for updating and creating a new config """
        if isinstance(self.params, dict):
            for key, entry in self.entries.items():
                self.params[key] = entry.get()
        print(self.params)

        try:
            self.strength_limit = float(self.strength_entry.get())
        except ValueError:
            tk.messagebox.showerror("Ошибка", "Введите корректное число для предела прочности")
            return

        # update with the params config
        with open("working_config.wbjn", "r", encoding="utf-8") as file:
            config = file.read()

        # Update config
        create_new_config(config, self.params)
        tk.messagebox.showinfo("Информация", "Параметры сохранены")
        self.show_results()
    
    def show_results(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        print(self.strength_limit)

        results = execute_with_updated_config()

        print(results)
        
        if isinstance(results, dict) and "P2" in results:
           
            row = 0
            for key, value in results.items():
                label = tk.Label(self.input_frame, text=f"{key}: {value}")
                label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
                row += 1
            try:
                stress = float(results["P2"])
                safety_factor = self.strength_limit / stress if stress != 0 else float('inf')

                # Определяем категорию
                if safety_factor < 1:
                    category = "Гарантированное разрушение"
                elif 1 <= safety_factor < 1.5:
                    category = "Локальные повреждения, усталостные трещины"
                elif 1.5 <= safety_factor < 2:
                    category = "Допустимо для неответственных деталей"
                elif 2 <= safety_factor < 3:
                    category = "Оптимальный запас прочности"
                elif 3 <= safety_factor <= 5:
                    category = "Повышенный запас прочности"
                else:
                    category = "Перерасход материала"

                # Вывод коэффициента запаса
                label = tk.Label(self.input_frame, text=f"Коэффициент запаса: {safety_factor:.2f}")
                label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
                row += 1

                # Вывод категории
                category_label = tk.Label(self.input_frame, text=f"Категория: {category}")
                category_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
                row += 1
                
            except ValueError:
                tk.messagebox.showerror("Ошибка", "Некорректные введеные данные")
            
        else:
            tk.messagebox.showerror("Ошибка", "Результаты не получены или имеют некорректный формат")