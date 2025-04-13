import tkinter as tk
from tkinter import ttk, messagebox
import screens.emp_view
import screens.manager_view
import screens.owner_view
import sql_connection
from datetime import date


class Expenses(tk.Frame):
    def __init__(self, master, user_role, emp_id=None):
        super().__init__(master, bg="#FFF4A3")
        self.user_role = user_role
        self.emp_id = emp_id

        # Header
        title = tk.Label(self, text="Expenses", font=("Helvetica", 16, "bold"),
                         bg="#d9d6f2", padx=20, pady=5, relief="raised")
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
        self.add_expense_button = tk.Button(self, text="Add Expense", font=("Helvetica", 12, "bold"),
                                            width=15, height=1, bg="#CFCFCF",
                                            command=self.open_add_expense_window)
        self.add_expense_button.pack(pady=5)

        self.load_expenses()

    def create_buttons(self, master):
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=5)

        # Back Button
        if self.user_role == "employee":
            back_screen = screens.emp_view.EmployeeView
        elif self.user_role == "manager":
            back_screen = screens.manager_view.ManagerView
        else:
            back_screen = screens.owner_view.OwnerView

        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"),
                  width=10, height=1, bg="#A4E4A0", fg="black", relief="ridge",
                  command=lambda: master.show_frame(back_screen)).pack(side="left", padx=10)


    def open_add_expense_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add Expense")
        add_window.configure(bg="#FFF4A3")

        self.value_entry = self.create_label_entry(add_window, "Value:")
        self.type_entry = self.create_label_entry(add_window, "Type:")

        tk.Label(add_window, text="Payment Method:", font=("Helvetica", 12), bg="#FFF4A3").pack(anchor="w", padx=20)
        self.payment_method_combo = ttk.Combobox(add_window, font=("Helvetica", 12), width=28, state="readonly")
        self.payment_method_combo['values'] = ["Cash", "Credit"]
        self.payment_method_combo.pack(anchor="w", padx=20, pady=5)
        self.payment_method_combo.current(0)

        self.create_add_expense_buttons(add_window)

    def create_label_entry(self, parent, text, show=""):
        tk.Label(parent, text=text, font=("Helvetica", 12), bg="#FFF4A3").pack(anchor="w", padx=20)
        entry = tk.Entry(parent, font=("Helvetica", 12), show=show, width=30)
        entry.pack(anchor="w", padx=20, pady=5)
        return entry

    def create_add_expense_buttons(self, add_window):
        button_frame = tk.Frame(add_window, bg="#FFF4A3")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"),
                  width=10, height=1, bg="#A4E4A0", fg="black", relief="ridge",
                  command=add_window.destroy).pack(side="left", padx=10)

        tk.Button(button_frame, text="Confirm", font=("Helvetica", 12, "bold"),
                  width=10, height=1, bg="#E58A2C", fg="black", relief="ridge",
                  command=lambda: self.confirm_add(add_window)).pack(side="left", padx=10)

    def confirm_add(self, window):
        expense_type = self.type_entry.get()
        value_str = self.value_entry.get()
        payment_method = self.payment_method_combo.get()

        if not expense_type or not value_str:
            messagebox.showwarning("Missing Info", "Please fill in all fields.")
            return

        try:
            value = float(value_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return

        if not self.emp_id:
            messagebox.showerror("Error", "Employee ID is missing. Cannot add expense.")
            return

        # Convert payment method to 0 (Cash) or 1 (Credit)
        payment_method_binary = 0 if payment_method == "Cash" else 1

        # Save to DB
        success = sql_connection.insert_expense(expense_type, value, payment_method_binary, self.emp_id)

        if success:
            self.tree.insert("", "end",
                             values=(expense_type, date.today().isoformat(), f"{value:.2f}", "0.00",
                                     payment_method, "N/A"))
            messagebox.showinfo("Success", "Expense added successfully.")
        else:
            messagebox.showerror("Error", "Failed to add expense.")

        window.destroy()


    def load_expenses(self):
        connection = sql_connection.connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT Type, Date, Value, Tax, Cash, Credit, StoreID FROM Expenses ORDER BY Date DESC")
                rows = cursor.fetchall()

                for row in rows:
                    payment_method = "Cash" if row[4] > 0 else "Credit"
                    self.tree.insert("", "end",
                                     values=(row[0], row[1], f"{row[2]:.2f}", f"{row[3]:.2f}", payment_method,
                                             str(row[6] or "N/A")))
            except Exception as e:
                print("Error loading expenses:", e)
            finally:
                cursor.close()
                connection.close()
