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
        self.master = master
        self.user_role = user_role
        self.emp_id = emp_id
        self.store_id = getattr(master, "current_store_id", None)

        tk.Label(self, text="Expenses", font=("Helvetica", 16, "bold"),
                 bg="#d9d6f2", padx=20, pady=5, relief="raised").pack(pady=10)

        self.table_frame = tk.Frame(self, bg="#FFF4A3")
        self.table_frame.pack(pady=10)

        columns = ("ID", "Type", "Date", "Value", "Tax", "Payment Method", "Store")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack()
        self.tree.bind("<Double-1>", self.edit_selected)

        self.create_buttons(master)

        self.add_expense_button = tk.Button(self, text="Add Expense", font=("Helvetica", 12, "bold"),
                                            width=15, height=1, bg="#CFCFCF",
                                            command=self.open_add_expense_window)
        self.add_expense_button.pack(pady=5)

        self.edit_expense_button = tk.Button(self, text="Edit Selected", font=("Helvetica", 12, "bold"),
                                             width=15, height=1, bg="#F6D860",
                                             command=self.edit_selected)
        self.edit_expense_button.pack(pady=5)

        self.delete_button = tk.Button(self, text="Delete Selected", font=("Helvetica", 12, "bold"),
                                       width=15, height=1, bg="#F28B82",
                                       command=self.delete_selected)
        self.delete_button.pack(pady=5)

        self.load_expenses()

    def create_buttons(self, master):
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=5)

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
        self._open_expense_form("Add Expense", self.confirm_add)

    def edit_selected(self, event=None):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Edit", "Please select an expense to edit.")
            return
        values = self.tree.item(selected[0], "values")
        self._open_expense_form("Edit Expense", self.confirm_edit, values)

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Delete", "Select a row to delete.")
            return
        expense_id = self.tree.item(selected[0], "values")[0]
        confirm = messagebox.askyesno("Delete", f"Delete expense ID {expense_id}?")
        if confirm:
            sql_connection.delete_expense(expense_id)
            self.load_expenses()

    def _open_expense_form(self, title, confirm_callback, values=None):
        win = tk.Toplevel(self)
        win.title(title)
        win.configure(bg="#FFF4A3")

        type_entry = self.create_label_entry(win, "Type:")
        value_entry = self.create_label_entry(win, "Value:")

        tk.Label(win, text="Payment Method:", font=("Helvetica", 12), bg="#FFF4A3").pack(anchor="w", padx=20)
        payment_var = tk.StringVar()
        payment_method_combo = ttk.Combobox(win, textvariable=payment_var,
                                            font=("Helvetica", 12), width=28, state="readonly")
        payment_method_combo['values'] = ["Cash", "Credit"]
        payment_method_combo.pack(anchor="w", padx=20, pady=5)
        payment_method_combo.current(0)

        if values:
            type_entry.insert(0, values[1])
            value_entry.insert(0, values[3])
            payment_var.set(values[5])

        def on_confirm():
            if values:
                confirm_callback(win, values[0], type_entry.get(), value_entry.get(), payment_var.get())
            else:
                confirm_callback(win, type_entry.get(), value_entry.get(), payment_var.get())

        tk.Button(win, text="Confirm", font=("Helvetica", 12, "bold"), bg="#E58A2C",
                  command=on_confirm).pack(pady=10)

    def confirm_add(self, win, expense_type, value_str, payment_method):
        try:
            value = float(value_str)
            method_binary = 0 if payment_method == "Cash" else 1
            success = sql_connection.insert_expense(expense_type, value, method_binary, self.emp_id, self.store_id)
            if success:
                self.load_expenses()
                messagebox.showinfo("Success", "Expense added.")
                win.destroy()
            else:
                messagebox.showerror("Error", "Failed to add expense.")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def confirm_edit(self, win, expense_id, expense_type, value_str, payment_method):
        try:
            value = float(value_str)
            method_binary = 0 if payment_method == "Cash" else 1
            success = sql_connection.update_expense(expense_id, expense_type, value, method_binary)
            if success:
                self.load_expenses()
                messagebox.showinfo("Updated", "Expense updated.")
                win.destroy()
            else:
                messagebox.showerror("Error", "Failed to update expense.")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def create_label_entry(self, parent, text, show=""):
        tk.Label(parent, text=text, font=("Helvetica", 12), bg="#FFF4A3").pack(anchor="w", padx=20)
        entry = tk.Entry(parent, font=("Helvetica", 12), show=show, width=30)
        entry.pack(anchor="w", padx=20, pady=5)
        return entry

    def load_expenses(self):
        self.tree.delete(*self.tree.get_children())
        connection = sql_connection.connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT ID, Type, Date, Value, Tax, Cash, Credit, StoreID FROM Expenses ORDER BY Date DESC")
                rows = cursor.fetchall()
                for row in rows:
                    method = "Cash" if row[5] > 0 else "Credit"
                    self.tree.insert("", "end", values=(row[0], row[1], row[2],
                                                        f"{row[3]:.2f}", f"{row[4]:.2f}", method,
                                                        str(row[7] or "N/A")))
            except Exception as e:
                print("Error loading expenses:", e)
            finally:
                cursor.close()
                connection.close()

        # Summary Section
        if self.store_id:
            summary = sql_connection.get_store_expense_summary(self.store_id)
            if summary:
                total, cash, credit = summary
                summary_text = (
                    f"Store {self.store_id} Summary — "
                    f"Total: ${total or 0:.2f} | "
                    f"Cash: ${cash or 0:.2f} | "
                    f"Credit: ${credit or 0:.2f}"
                )
                if hasattr(self, 'summary_label'):
                    self.summary_label.config(text=summary_text)
                else:
                    self.summary_label = tk.Label(self, text=summary_text,
                                                  font=("Helvetica", 11, "bold"),
                                                  bg="#FFF4A3", fg="#333")
                    self.summary_label.pack(pady=(10, 5))


