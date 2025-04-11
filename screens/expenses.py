import tkinter as tk
from tkinter import ttk
import screens.emp_view
import screens.manager_view
import screens.owner_view

class Expenses(tk.Frame):
    def __init__(self, master, user_role):
        super().__init__(master, bg="#FFF4A3")
        self.user_role = user_role  # Store the user's role

        # Header
        title = tk.Label(self, text="Expenses", font=("Helvetica", 16, "bold"), bg="#d9d6f2", padx=20, pady=5, relief="raised")
        title.pack(pady=10)

        # Table Frame
        self.table_frame = tk.Frame(self, bg="#FFF4A3")
        self.table_frame.pack(pady=10)

        # Treeview (Table)
        columns = ("Type", "Date", "Value", "Tax", "Payment Method", "Store")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack()

        # Buttons
        self.create_buttons(master)

        # Add Expense Button
        self.add_expense_button = tk.Button(self, text="Add Expense", font=("Helvetica", 12, "bold"), width=15, height=1, bg="#CFCFCF",
                                            command=self.open_add_expense_window)
        self.add_expense_button.pack(pady=5)

    def create_buttons(self, master):
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=5)

        # Corrected back button logic
        if self.user_role == "employee":
            back_command = lambda: master.show_frame(screens.emp_view.EmployeeView)
        elif self.user_role == "manager":
            back_command = lambda: master.show_frame(screens.manager_view.ManagerView)
        else:  # For owners
            back_command = lambda: master.show_frame(screens.owner_view.OwnerView)

        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#A4E4A0",
                  fg="black", relief="ridge", command=back_command).pack(side="left", padx=10)

        # Save Button
        tk.Button(button_frame, text="Save", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#E58A2C",
                  fg="black", relief="ridge", command=self.save_data).pack(side="left", padx=10)

        # Save Button
        tk.Button(button_frame, text="Save", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#E58A2C",
                  fg="black", relief="ridge", command=self.save_data).pack(side="left", padx=10)

    def open_add_expense_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add Expense")
        add_window.configure(bg="#FFF4A3")

        # Form Labels & Entry Fields
        self.value_entry = self.create_label_entry(add_window, "Value:")
        self.type_entry = self.create_label_entry(add_window, "Type:")
        self.payment_entry = self.create_label_entry(add_window, "Payment Method:")

        # Buttons
        self.create_add_expense_buttons(add_window)

    def create_label_entry(self, parent, text, show=""):
        tk.Label(parent, text=text, font=("Helvetica", 12), bg="#FFF4A3").pack(anchor="w", padx=20)
        entry = tk.Entry(parent, font=("Helvetica", 12), show=show, width=30)
        entry.pack(anchor="w", padx=20, pady=5)
        return entry

    def create_add_expense_buttons(self, add_window):
        button_frame = tk.Frame(add_window, bg="#FFF4A3")
        button_frame.pack(pady=10)

        # Back Button
        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#A4E4A0",
                  fg="black", relief="ridge", command=add_window.destroy).pack(side="left", padx=10)

        # Confirm Button
        tk.Button(button_frame, text="Confirm", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#E58A2C",
                  fg="black", relief="ridge", command=lambda: self.confirm_add(add_window)).pack(side="left", padx=10)

    def confirm_add(self, window):
        self.tree.insert("", "end", values=(self.type_entry.get(), "N/A", self.value_entry.get(), "N/A", self.payment_entry.get(), "N/A"))
        window.destroy()

    def save_data(self):
        print("Data saved!")  # Placeholder for actual save functionality
