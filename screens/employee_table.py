import tkinter as tk
from tkinter import ttk
import screens.manager_view  # Make sure to import ManagerView class


class EmployeesScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#fff7a8")

        # Header
        title = tk.Label(self, text="Employees", font=("Helvetica", 16, "bold"), bg="#d9d6f2", padx=20, pady=5, relief="raised")
        title.pack(pady=10)

        # Table Frame
        self.table_frame = tk.Frame(self, bg="#fff7a8")
        self.table_frame.pack(pady=10)

        # Treeview (Table)
        columns = ("Name", "Phone", "Email", "Role", "Username", "Password")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack()

        # Buttons
        self.create_buttons(master)

        # Add Employee Button
        self.add_employee_button = tk.Button(self, text="Add Employee", font=("Helvetica", 12, "bold"), width=15, height=1,
                                             bg="#CFCFCF", command=self.open_add_employee_window)
        self.add_employee_button.pack(pady=5)

    def create_buttons(self, master):
        button_frame = tk.Frame(self, bg="#fff7a8")
        button_frame.pack(pady=5)

        # Back Button
        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#A4E4A0",
                  fg="black", relief="ridge", command=lambda: master.show_frame(screens.manager_view.ManagerView)).pack(side="left", padx=10)

        # Save Button
        tk.Button(button_frame, text="Save", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#E58A2C",
                  fg="black", relief="ridge", command=self.save_data).pack(side="left", padx=10)

    def open_add_employee_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add Employee")
        add_window.configure(bg="#fff7a8")

        # Form Labels & Entry Fields
        self.name_entry = self.create_label_entry(add_window, "Name:")
        self.phone_entry = self.create_label_entry(add_window, "Phone:")
        self.email_entry = self.create_label_entry(add_window, "Email:")
        self.role_entry = self.create_label_entry(add_window, "Role:")
        self.username_entry = self.create_label_entry(add_window, "Username:")
        self.password_entry = self.create_label_entry(add_window, "Password:")

        # Buttons for Confirm and Back
        self.create_add_employee_buttons(add_window)

    def create_label_entry(self, parent, text):
        tk.Label(parent, text=text, font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20)
        entry = tk.Entry(parent, font=("Helvetica", 12), width=30)
        entry.pack(anchor="w", padx=20, pady=5)
        return entry

    def create_add_employee_buttons(self, add_window):
        button_frame = tk.Frame(add_window, bg="#fff7a8")
        button_frame.pack(pady=10)

        # Back Button
        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#A4E4A0",
                  fg="black", relief="ridge", command=add_window.destroy).pack(side="left", padx=10)

        # Confirm Button
        tk.Button(button_frame, text="Confirm", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#E58A2C",
                  fg="black", relief="ridge", command=lambda: self.confirm_add(add_window)).pack(side="left", padx=10)

    def confirm_add(self, window):
        # Adding employee data to table (in a real application, you'd save it somewhere)
        employee_data = (self.name_entry.get(), self.phone_entry.get(), self.email_entry.get(),
                         self.role_entry.get(), self.username_entry.get(), self.password_entry.get())
        self.tree.insert("", "end", values=employee_data)
        window.destroy()

    def save_data(self):
        print("Data saved!")  # Placeholder for actual save functionality
