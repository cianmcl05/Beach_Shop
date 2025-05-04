import tkinter as tk
from tkinter import ttk, messagebox
import screens.emp_view
import screens.manager_view
import screens.owner_view
import sql_connection
from datetime import datetime, timedelta

class Expenses(tk.Frame):
    """
    UI for viewing, adding, editing, and deleting store expenses.
    Behavior varies based on user_role (employee sees only today's,
    manager sees this month's, owner sees all).
    """
    def __init__(self, master, user_role, emp_id=None):
        super().__init__(master, bg="#FFF4A3")
        self.master = master
        self.user_role = user_role
        self.emp_id = emp_id
        # Identify current store from master (set in app)
        self.store_id = getattr(master, "current_store_id", None)

        # Header label
        tk.Label(
            self,
            text="Expenses",
            font=("Helvetica", 16, "bold"),
            bg="#d9d6f2",
            padx=20,
            pady=5,
            relief="raised"
        ).pack(pady=10)

        # Container for the expenses table
        self.table_frame = tk.Frame(self, bg="#FFF4A3")
        self.table_frame.pack(pady=10)

        # Define table columns and create Treeview
        columns = ("ID", "Type", "Date", "Value", "Payment Method", "Store")
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings"
        )
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack()
        # Double-click to edit an entry
        self.tree.bind("<Double-1>", self.edit_selected)

        # Back navigation button
        self.create_buttons(master)

        # Buttons for adding, editing, and deleting
        self.add_expense_button = tk.Button(
            self,
            text="Add Expense",
            font=("Helvetica", 12, "bold"),
            width=15,
            bg="#CFCFCF",
            command=self.open_add_expense_window
        )
        self.add_expense_button.pack(pady=5)

        self.edit_expense_button = tk.Button(
            self,
            text="Edit Selected",
            font=("Helvetica", 12, "bold"),
            width=15,
            bg="#F6D860",
            command=self.edit_selected
        )
        self.edit_expense_button.pack(pady=5)

        self.delete_button = tk.Button(
            self,
            text="Delete Selected",
            font=("Helvetica", 12, "bold"),
            width=15,
            bg="#F28B82",
            command=self.delete_selected
        )
        self.delete_button.pack(pady=5)

        # Load initial data into the table
        self.load_expenses()

    def create_buttons(self, master):
        """
        Create the Back button to return to the previous view based on role.
        """
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=5)

        # Determine which screen to go back to
        if self.user_role == "employee":
            back_screen = screens.emp_view.EmployeeView
        elif self.user_role == "manager":
            back_screen = screens.manager_view.ManagerView
        else:
            back_screen = screens.owner_view.OwnerView

        # Back button
        tk.Button(
            button_frame,
            text="Back",
            font=("Helvetica", 12, "bold"),
            width=10,
            bg="#A4E4A0",
            command=lambda: master.show_frame(back_screen)
        ).pack(side="left", padx=10)

    def open_add_expense_window(self):
        """
        Open a window to add a new expense entry.
        """
        self._open_expense_form("Add Expense", self.confirm_add)

    def edit_selected(self, event=None):
        """
        Open the edit window for the selected expense.
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Edit", "Please select an expense to edit.")
            return
        values = self.tree.item(selected[0], "values")
        self._open_expense_form("Edit Expense", self.confirm_edit, values)

    def delete_selected(self):
        """
        Delete the selected expense after user confirmation.
        """
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
        """
        Helper to open a modal for Add/Edit with common fields:
        Type, Value, Payment Method.
        """
        win = tk.Toplevel(self)
        win.title(title)
        win.configure(bg="white")

        # Create Type and Value entries
        type_entry = self._create_label_entry(win, "Type:")
        value_entry = self._create_label_entry(win, "Value:")

        # Payment method dropdown
        tk.Label(win, text="Payment Method:", font=("Helvetica", 12), bg="white").pack(anchor="w", padx=20)
        payment_var = tk.StringVar()
        combo = ttk.Combobox(win, textvariable=payment_var, font=("Helvetica", 12), width=28, state="readonly")
        combo['values'] = ["Cash", "Credit"]
        combo.pack(anchor="w", padx=20, pady=5)
        combo.current(0)

        # Pre-fill fields when editing
        if values:
            type_entry.insert(0, values[1])
            value_entry.insert(0, values[3])
            payment_var.set(values[4])

        btn_color = "#CFCFCF" if title.startswith("Add") else "#F6D860"

        # Confirmation button invokes callback with form data
        def on_confirm():
            if values:
                confirm_callback(win, values[0], type_entry.get(), value_entry.get(), payment_var.get())
            else:
                confirm_callback(win, type_entry.get(), value_entry.get(), payment_var.get())

        tk.Button(
            win,
            text="Confirm",
            font=("Helvetica", 12, "bold"),
            bg=btn_color,
            width=15,
            command=on_confirm
        ).pack(pady=10)

    def confirm_add(self, win, expense_type, value_str, payment_method):
        """
        Insert a new expense record into the database.
        """
        try:
            value = float(value_str)
            method_binary = 0 if payment_method == "Cash" else 1
            success = sql_connection.insert_expense(
                expense_type,
                value,
                method_binary,
                self.emp_id,
                self.store_id
            )
            if success:
                self.load_expenses()
                messagebox.showinfo("Success", "Expense added.")
                win.destroy()
            else:
                messagebox.showerror("Error", "Failed to add expense.")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def confirm_edit(self, win, expense_id, expense_type, value_str, payment_method):
        """
        Update an existing expense record in the database.
        """
        try:
            value = float(value_str)
            method_binary = 0 if payment_method == "Cash" else 1
            success = sql_connection.update_expense(
                expense_id,
                expense_type,
                value,
                method_binary
            )
            if success:
                self.load_expenses()
                messagebox.showinfo("Updated", "Expense updated.")
                win.destroy()
            else:
                messagebox.showerror("Error", "Failed to update expense.")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def _create_label_entry(self, parent, label_text):
        """
        Helper to create a labeled text Entry widget.
        Returns the Entry for data retrieval.
        """
        tk.Label(parent, text=label_text, font=("Helvetica", 12), bg="white").pack(anchor="w", padx=20)
        entry = tk.Entry(parent, font=("Helvetica", 12), width=30)
        entry.pack(anchor="w", padx=20, pady=5)
        return entry

    def load_expenses(self):
        """
        Load expenses from the database with filters based on role:
        - Employee: today's only
        - Manager: this month
        - Owner: all
        Then displays summary for non-employees.
        """
        # Clear existing rows
        self.tree.delete(*self.tree.get_children())
        connection = sql_connection.connect_db()
        if connection:
            cursor = connection.cursor()
            today = datetime.today()
            filter_clause, params = "", ()

            # Employee sees only today's expenses
            if self.user_role == "employee":
                filter_clause = "WHERE e.EmpID = %s AND DATE(e.Date) = CURDATE()"
                params = (self.emp_id,)
            # Manager sees current month
            elif self.user_role == "manager":
                first_day = today.replace(day=1).strftime("%Y-%m-%d")
                last_day = (today.replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)
                filter_clause = "WHERE DATE(e.Date) BETWEEN %s AND %s"
                params = (first_day, last_day.strftime("%Y-%m-%d"))

            # Query database
            query = f"""
                SELECT e.ID, e.Type, e.Date, e.Value, e.Cash, e.Credit, s.Store_Name
                FROM Expenses e
                LEFT JOIN Store s ON e.StoreID = s.Store_ID
                {filter_clause}
                ORDER BY e.Date DESC
            """
            cursor.execute(query, params)
            rows = cursor.fetchall()

            # Populate table rows
            for expense_id, expense_type, date_val, value, cash, credit, store_name in rows:
                method = "Cash" if cash > 0 else "Credit"
                formatted_date = date_val.strftime("%Y-%m-%d %H:%M:%S")
                store_display = store_name or "N/A"
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        expense_id,
                        expense_type,
                        formatted_date,
                        f"{value:.2f}",
                        method,
                        store_display
                    )
                )

            cursor.close()
            connection.close()

        # Show summary for managers/owners
        if self.store_id and self.user_role != "employee":
            summary = sql_connection.get_store_expense_summary(self.store_id)
            store_name = sql_connection.get_store_name_by_id(self.store_id)
            if summary:
                total, cash_sum, credit_sum = summary
                summary_text = (
                    f"{store_name or 'Store '+str(self.store_id)} Summary — "
                    f"Total: ${total or 0:.2f} | "
                    f"Cash: ${cash_sum or 0:.2f} | "
                    f"Credit: ${credit_sum or 0:.2f}"
                )
                if hasattr(self, 'summary_label'):
                    self.summary_label.config(text=summary_text)
                else:
                    self.summary_label = tk.Label(
                        self,
                        text=summary_text,
                        font=("Helvetica", 11, "bold"),
                        bg="#FFF4A3",
                        fg="#333"
                    )
                    self.summary_label.pack(pady=(10, 5))
