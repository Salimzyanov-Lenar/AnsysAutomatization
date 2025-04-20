import tkinter as tk
from tkinter import ttk
import styles
from PIL import Image, ImageTk


from tkinter import filedialog
from services import get_params_from_config, create_new_config, get_needed_param_value
from executor import execute_with_updated_config
from regex import pattern_for_saving_path
from csv_parse import parse_result


class AppInterface:
    def __init__(self, root):
        """
        App Setup
        Начальная настройка окна и его параметров 
        """
        self.root = root
        self.root.title("AnsysAutomatization")
        self.root.geometry("1920x1080")
        self.root.configure(bg="white")


        # Left Frame
        self.left_frame = tk.Frame(self.root, bg="#1729B0", width=200)
        self.left_frame.pack(side="left", fill="y")

        # Right Frame
        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.pack(side="left", fill="both", expand=True)

        # Frame for input fields
        self.input_frame = tk.Frame(self.right_frame, bg="white")
        self.input_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Picture
        image = Image.open("static/pic.jpg")
        photo = ImageTk.PhotoImage(image)
        self.image_label = tk.Label(self.right_frame, image=photo, bg='white')
        self.image_label.image = photo
        self.image_label.pack(pady=100)

        
        # Welcome page
        self.label = tk.Label(
            self.left_frame,
        text="Добро пожаловать в программу для автоматизации создания и запуска журналов Ansys INC \n\n Для начала потребуется выбрать проект, журнал проекта и путь до исполнителя",
            font=('Arial', 14, 'bold'),
            bg="#1729B0",
            fg="white",
            justify="center",
            pady=100,
            wraplength=600,
            )
        self.label.pack(pady=(0, 200), anchor="w")


        # Path to journal button 
        self.config_button = tk.Button(self.left_frame, text="📄 Выберите файл конфигурации",
                                        command=self.on_button_click)
        # Path to project button
        self.project_button = tk.Button(self.left_frame, text="📁 Выбрать путь до проекта",
                                        command=self.get_project_path)
        # Path to executor button
        self.executor_button = tk.Button(self.left_frame, text="⚙ Выбрать исполнитель Ansys",
                                        command=self.get_executor_path)

        for btn in [self.config_button, self.project_button, self.executor_button]:
            styles.choice_button_styles(btn)
            btn.pack(fill="both", padx=10, pady=5)


        # App Setup parameters
        self.ansys_executor_path = None
        self.ansys_project_path = None
        self.ansys_result_path = None
        self.result_tree = None
        self.safety_factor_label = None
        self.category_label = None

        # Config parameters dict
        self.params = dict | None
        self.strength_limit = None
        self.strength_entry = None

    def on_button_click(self):
        """ 
        Saving choosen config file 
        Сохранение выбранного конфига
        """
        file_path = filedialog.askopenfilename()

        # Desctroying old params
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        if self.result_tree:
            self.result_tree.destroy()
        
        if self.safety_factor_label and self.category_label:
            self.safety_factor_label.destroy()
            self.category_label.destroy()

        # Getting new journal
        if file_path:
            with open(file_path, mode="r", encoding="utf-8") as file:
                working_config = file.read()

            # Save working_config
            with open("working_config.wbjn", mode="w", encoding="utf-8") as file:
                file.write(working_config)

            # Ищем путь к результату и сохраняем в self.ansys_result_path
            print("Trying to get result path...")
            match = pattern_for_saving_path.search(working_config)
            if match:
                self.ansys_result_path = match.group(1)
                print(f"Result path is {self.ansys_result_path}")
            else:
                print("Error, result path was not found")
                self.ansys_result_path = None
            
            if self.image_label:
                self.image_label.destroy()

            self.label.config(text=f"Выбран путь:\n{file_path}")
            try:
                self.params = get_params_from_config()
                self.create_input_fields()
            except Exception as e:
                tk.messagebox.showerror("Ошибка", str(e))
        
    def get_executor_path(self):
        """ 
        Saving path to executor
        Сохранение пути до файла исполнителя
        """
        file_path = filedialog.askopenfilename()
        
        if file_path:
            self.ansys_executor_path = file_path

        else:
            tk.messagebox.showerror("Ошибка, выберите валидный исполнительный файл Ansys")
        print(self.ansys_executor_path)

    def get_project_path(self):
        """ 
        Getting project path
        Сохранение пути до файла проекта
        """
        
        project_path = filedialog.askopenfilename()
        if project_path:
            self.ansys_project_path = project_path
            self.label.config(text=f"Выбран путь:\n{project_path}")
            
        else:
            tk.messagebox.showerror("Ошибка, выбери валидный путь до проекта")


    def create_input_fields(self):
        """ 
        Creating a input fields which depending on config
        Создание полей ввода на основе конфига
        """
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        if not self.params:
            return

        row = 0
        # Links for input fields
        self.entries = {}

        if isinstance(self.params, dict):
            for key, value in self.params.items():
                # label = tk.Label(self.input_frame, text=key)
                label = tk.Label(self.input_frame, text=key)
                styles.label_style(label)
                label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

                entry = tk.Entry(self.input_frame)
                styles.entry_style(entry)
                entry.insert(0, str(value))
                entry.grid(row=row, column=1, padx=10, pady=5, sticky="e")

                self.entries[key] = entry
                row += 1

            # Addind field for input strength limit
            self.strength_label = tk.Label(self.input_frame, text="Предел прочности")
            self.strength_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            styles.label_style(self.strength_label)

            self.strength_entry = tk.Entry(self.input_frame)
            self.strength_entry.grid(row=row, column=1, padx=10, pady=5, sticky="e")
            styles.entry_style(self.strength_entry)
            row += 1

            # Button for saving changes
            save_button = tk.Button(self.input_frame, text="Рассчитать", command=self.save_params)
            save_button.grid(row=row, column=0, columnspan=2, pady=10)
            styles.choice_button_styles(save_button)


    def save_params(self):
        """
        Function for updating and creating a new config
        Обновляет сохраненный конфиг с параметрами введеными пользователем
        """
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
        """
        Show table with data and strength limit
        Выводит таблицу и показания предела прочности
        """
        if not self.ansys_executor_path:
            tk.messagebox.showerror("Ошибка", "Выберите файл испонитель")
            return

        if not self.ansys_project_path:
            tk.messagebox.showerror("Ошибка", "Выберите файл проекта")

        for widget in self.input_frame.winfo_children():
            widget.destroy()

        try:
            execute_with_updated_config(
                self.ansys_executor_path,
                self.ansys_project_path,
                self.ansys_result_path,
            )
        except Exception as e:
            print(f"ERROR: {Exception}")
        
        fields, rows = parse_result(self.ansys_result_path)
        self.result_tree = ttk.Treeview(self.right_frame)
        styles.result_treeview(self.result_tree, fields, rows)

        try:
            stress = float(get_needed_param_value(rows))
            print(stress)
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
            # Создаем и упаковываем метки под таблицей
            self.safety_factor_label = tk.Label(self.right_frame, text=f"Коэффициент запаса: {safety_factor:.2f}")
            styles.label_style(self.safety_factor_label)
            self.safety_factor_label.pack(anchor='center', padx=10, pady=(5, 0))

            self.category_label = tk.Label(self.right_frame, text=f"Категория: {category}")
            styles.label_style(self.category_label)
            self.category_label.pack(anchor='center', padx=10, pady=(0, 10))

            
        except ValueError:
            tk.messagebox.showerror("Ошибка", "Некорректные введеные данные")