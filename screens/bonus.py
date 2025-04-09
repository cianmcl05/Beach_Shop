import tkinter as tk
from tkinter import ttk
import screens.manager_view
import screens.owner_view

class Bonus(tk.Frame):
    def __init__(self, master, user_role):
        super().__init__(master, bg="#FFF4A3")
        self.user_role = user_role  # Set user role

        # Header
        title = tk.Label(self, text="Bonus", font=("Helvetica", 16, "bold"), bg="#d9d6f2", padx=20, pady=5,
                         relief="raised")
        title.pack(pady=10)

        # Table Frame
        self.table_frame = tk.Frame(self, bg="#FFF4A3")
        self.table_frame.pack(pady=10)

        # Treeview (Table)
        columns = ("Employee", "Sales", "Gross", "Bonus %", "Bonus Amount")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack()

        # Buttons
        self.create_buttons(master)

        # Add Bonus Button
        self.add_bonus_button = tk.Button(self, text="Add Bonus", font=("Helvetica", 12, "bold"), width=15, height=1,
                                          bg="#CFCFCF", command=self.open_add_bonus_window)
        self.add_bonus_button.pack(pady=5)

    def create_buttons(self, master):
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=5)

        # Back Button: Navigate based on user role
        if self.user_role == "manager":
            back_command = lambda: master.show_frame(screens.manager_view.ManagerView)
        else:
            back_command = lambda: master.show_frame(screens.owner_view.OwnerView)

        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#A4E4A0",
                  fg="black", relief="ridge", command=back_command).pack(side="left", padx=10)

        # Save Button
        tk.Button(button_frame, text="Save", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#E58A2C",
                  fg="black", relief="ridge", command=self.save_data).pack(side="left", padx=10)

    def open_add_bonus_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add Bonus")
        add_window.configure(bg="#FFF4A3")

        self.employee_entry = self.create_label_entry(add_window, "Employee:")
        self.sales_entry = self.create_label_entry(add_window, "Sales:")
        self.gross_entry = self.create_label_entry(add_window, "Gross:")
        self.bonus_percent_entry = self.create_label_entry(add_window, "Bonus %:")

        self.bonus_amount_label = tk.Label(add_window, text="Bonus Amount:", font=("Helvetica", 12), bg="#FFF4A3")
        self.bonus_amount_label.pack(anchor="w", padx=20, pady=5)

        self.create_add_bonus_buttons(add_window)

    def create_label_entry(self, parent, text, show=""):
        tk.Label(parent, text=text, font=("Helvetica", 12), bg="#FFF4A3").pack(anchor="w", padx=20)
        entry = tk.Entry(parent, font=("Helvetica", 12), show=show, width=30)
        entry.pack(anchor="w", padx=20, pady=5)
        return entry

    def create_add_bonus_buttons(self, add_window):
        button_frame = tk.Frame(add_window, bg="#FFF4A3")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#A4E4A0",
                  fg="black", relief="ridge", command=add_window.destroy).pack(side="left", padx=10)

        tk.Button(button_frame, text="Confirm", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#E58A2C",
                  fg="black", relief="ridge", command=lambda: self.confirm_add(add_window)).pack(side="left", padx=10)

    def confirm_add(self, window):
        sales = float(self.sales_entry.get())
        bonus_percent = float(self.bonus_percent_entry.get())
        bonus_amount = (sales * bonus_percent) / 100
        self.tree.insert("", "end", values=(self.employee_entry.get(), self.sales_entry.get(), self.gross_entry.get(),
                                            self.bonus_percent_entry.get(), f"${bonus_amount:.2f}"))
        window.destroy()

    def save_data(self):
        print("Data saved!")  # Placeholder
