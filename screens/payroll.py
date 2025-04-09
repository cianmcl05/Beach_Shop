import tkinter as tk
from tkinter import ttk
import screens.emp_view
import screens.manager_view
import screens.owner_view

class PayrollScreen(tk.Frame):
    def __init__(self, master, user_role):
        super().__init__(master, bg="#fff7a8")
        self.user_role = user_role
        self.master = master

        # Header
        tk.Label(self, text="Payroll", font=("Helvetica", 16, "bold"), bg="#d9d6f2",
                 padx=20, pady=5, relief="raised").pack(pady=10)

        # Table Frame
        self.table_frame = tk.Frame(self, bg="#fff7a8")
        self.table_frame.pack(pady=10)

        # Treeview (Table)
        columns = ("Date", "Employee", "Pay Amount")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack()

        # Buttons
        self.create_buttons()

        # Add Payroll Entry Button
        tk.Button(self, text="Add Payroll Entry", font=("Helvetica", 12, "bold"), width=18, height=1, bg="#ffa94d",
                  command=self.open_add_payroll_window).pack(pady=5)

    def create_buttons(self):
        button_frame = tk.Frame(self, bg="#fff7a8")
        button_frame.pack(pady=5)

        # Back Button: Go to EmployeeView or ManagerView or OwnerView based on user role
        if self.user_role == "manager":
            back_command = lambda: self.master.show_frame(screens.manager_view.ManagerView)
        else:  # For owners
            back_command = lambda: self.master.show_frame(screens.owner_view.OwnerView)

        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#A4E4A0",
                  fg="black", relief="ridge", command=back_command).pack(side="left", padx=10)

        # Save Button
        tk.Button(button_frame, text="Save", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#E58A2C",
                  fg="black", relief="ridge", command=self.save_data).pack(side="left", padx=10)

    def open_add_payroll_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add Payroll Entry")
        add_window.configure(bg="#fff7a8")

        # Form Labels & Entry Fields
        self.employee_entry = self.create_label_entry(add_window, "Employee:")
        self.amount_entry = self.create_label_entry(add_window, "Amount:")

        # Buttons
        self.create_add_payroll_buttons(add_window)

    def create_label_entry(self, parent, text, show=""):
        tk.Label(parent, text=text, font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20)
        entry = tk.Entry(parent, font=("Helvetica", 12), show=show, width=30)
        entry.pack(anchor="w", padx=20, pady=5)
        return entry

    def create_add_payroll_buttons(self, add_window):
        button_frame = tk.Frame(add_window, bg="#fff7a8")
        button_frame.pack(pady=10)

        # Back Button
        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#A4E4A0",
                  fg="black", relief="ridge", command=add_window.destroy).pack(side="left", padx=10)

        # Confirm Button
        tk.Button(button_frame, text="Confirm", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#E58A2C",
                  fg="black", relief="ridge", command=lambda: self.confirm_add(add_window)).pack(side="left", padx=10)

    def confirm_add(self, window):
        # For now, dummy data added with "N/A" as placeholder for date
        self.tree.insert("", "end", values=("N/A", self.employee_entry.get(), self.amount_entry.get()))
        window.destroy()

    def save_data(self):
        print("Payroll data saved!")  # Placeholder for actual save functionality
