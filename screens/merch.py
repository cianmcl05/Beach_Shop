import tkinter as tk
from tkinter import ttk
import screens.manager_view  # Import ManagerView screen


class MerchandiseInventoryScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")
        self.master = master

        # Header Label
        self.header_label = tk.Label(self, text="Merchandise Inventory", font=("Arial", 16, "bold"), bg="#FFF4A3", fg="black")
        self.header_label.pack(pady=10)

        # Buttons Frame
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack()

        self.back_button = tk.Button(button_frame, text="Back", font=("Arial", 12, "bold"), width=10, height=1,
                                     bg="#B0F2C2", fg="black", relief="ridge",
                                     command=lambda: self.master.show_frame(screens.manager_view.ManagerView))
        self.back_button.pack(side=tk.LEFT, padx=10)

        self.add_button = tk.Button(button_frame, text="Add", font=("Arial", 12, "bold"), width=10, height=1,
                                    bg="#EECFA3", fg="black", relief="ridge", command=self.show_add_screen)
        self.add_button.pack(side=tk.RIGHT, padx=10)

        # Table Frame
        self.table_frame = tk.Frame(self, bg="#FFF4A3", padx=5, pady=5)
        self.table_frame.pack(pady=10, fill="both", expand=True)

        self.show_inventory_screen()

    def show_inventory_screen(self):
        self.clear_screen()
        self.header_label.config(text="Merchandise Inventory")
        self.add_button.config(text="Add", command=self.show_add_screen)
        self.back_button.config(command=lambda: self.master.show_frame(screens.manager_view.ManagerView))

        # Table Headers
        columns = ["Date", "Day", "Merch Type", "Merch Value", "Total Merch"]
        for i, col in enumerate(columns):
            label = tk.Label(self.table_frame, text=col, font=("Arial", 10, "bold"), bg="#FFF4A3", borderwidth=1, relief="solid")
            label.grid(row=0, column=i, padx=2, pady=2, sticky="nsew")

        # Table Rows (Empty for now)
        for r in range(1, 6):  # 5 empty rows
            for c in range(5):
                entry = tk.Entry(self.table_frame, font=("Arial", 10), borderwidth=1, relief="solid", width=13)
                entry.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

    def show_add_screen(self):
        self.clear_screen()
        self.header_label.config(text="Add Merchandise")
        self.add_button.config(text="Confirm", command=self.show_inventory_screen)
        self.back_button.config(command=self.show_inventory_screen)

        tk.Label(self.table_frame, text="Merch Type:", font=("Arial", 12), bg="#FFF4A3").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        merch_type_entry = tk.Entry(self.table_frame, font=("Arial", 12), width=20)
        merch_type_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(self.table_frame, text="Merch Value:", font=("Arial", 12), bg="#FFF4A3").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        merch_value_entry = tk.Entry(self.table_frame, font=("Arial", 12), width=20)
        merch_value_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    def clear_screen(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

