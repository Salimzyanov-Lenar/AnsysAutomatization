import tkinter as tk
from tkinter import filedialog
from services import get_params_from_config, create_new_config


class AppInterface:
    def __init__(self, root):
        # Windows settings
        self.root = root
        self.root.title("AnsysAutomatization")
        self.root.geometry("720x480")
        self.label = tk.Label(root, text="Choose File", font=('Arial', 12))
        self.label.pack(pady=20)
        self.button = tk.Button(root, text="Choose File", command=self.on_button_click)
        self.button.pack()
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=20)

        # Config parameters dict
        self.params = dict | None

    def on_button_click(self):
        """ Saving choosen config file """
        file_path = filedialog.askopenfilename()

        if file_path:
            with open(file_path, mode="r", encoding="utf-8") as file:
                working_config = file.read()

            # Save working_config
            with open("working_config.txt", mode="w", encoding="utf-8") as file:
                file.write(working_config)

            self.label.config(text=f"choosen:\n{file_path}")

            try:
                self.params = get_params_from_config()
                self.create_input_fields()
            except Exception as e:
                tk.messagebox.showerror("Error", str(e))


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

            # Button for saving changes
            save_button = tk.Button(self.input_frame, text="Save", command=self.save_params)
            save_button.grid(row=row, column=0, columnspan=2, pady=10)


    def save_params(self):
        """ Function for updating and creating a new config """
        if isinstance(self.params, dict):
            for key, entry in self.entries.items():
                self.params[key] = entry.get()
        print(self.params)

        # update with the params config
        with open("working_config.txt", "r", encoding="utf-8") as file:
            config = file.read()

        # Update config
        create_new_config(config, self.params)
        tk.messagebox.showinfo("Информация", "Параметры сохранены")
