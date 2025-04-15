import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import screens.manager_view
import screens.owner_view
from sql_connection import get_all_payroll, insert_payroll, get_all_employees, update_payroll, delete_payroll

class PayrollScreen(tk.Frame):
    def __init__(self, master, user_role="manager"):
        super().__init__(master, bg="#FFF4A3")
        self.master = master
        self.user_role = user_role

        # Build a mapping of employee names to IDs for filtering and selection
        self.emp_map = {name: eid for eid, name in get_all_employees()}
        self.reverse_emp_map = {eid: name for name, eid in self.emp_map.items()}

        tk.Label(self, text="Payroll Management", font=("Arial", 16, "bold"), bg="#FFF4A3").pack(pady=10)

        self.button_frame = tk.Frame(self, bg="#FFF4A3")
        self.button_frame.pack()

        tk.Button(self.button_frame, text="Back", font=("Arial", 12, "bold"), width=10,
                  bg="#B0F2C2", command=self.get_back_command()).pack(side=tk.LEFT, padx=10)

        tk.Button(self.button_frame, text="Add Payroll", font=("Arial", 12, "bold"), width=15,
                  bg="#EECFA3", command=self.open_add_window).pack(side=tk.LEFT, padx=10)

        tk.Button(self.button_frame, text="Edit Selected", font=("Arial", 12, "bold"), width=15,
                  bg="#F6D860", command=self.edit_selected).pack(side=tk.LEFT, padx=10)

        tk.Button(self.button_frame, text="Delete Selected", font=("Arial", 12, "bold"), width=15,
                  bg="#F28B82", command=self.delete_selected).pack(side=tk.LEFT, padx=10)

        # Filter Section
        filter_frame = tk.Frame(self, bg="#FFF4A3")
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Filter by Employee:", bg="#FFF4A3", font=("Arial", 11)).pack(side=tk.LEFT)
        self.filter_var = tk.StringVar()
        self.filter_dropdown = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                            values=["All"] + list(self.emp_map.keys()), state="readonly", width=20)
        self.filter_dropdown.pack(side=tk.LEFT, padx=5)
        self.filter_dropdown.set("All")

        tk.Button(filter_frame, text="Apply", bg="#E58A2C", font=("Arial", 11, "bold"),
                  command=self.load_table).pack(side=tk.LEFT, padx=5)

        # Table Section
        self.table_frame = tk.Frame(self, bg="#FFF4A3")
        self.table_frame.pack(pady=10, fill="both", expand=True)

        self.columns = ("ID", "Date", "Employee", "Amount")
        self.tree = ttk.Treeview(self.table_frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack()

        # Bind double-click to edit
        self.tree.bind("<Double-1>", self.double_click_edit)

        self.load_table()

    def get_back_command(self):
        if self.user_role == "owner":
            return lambda: self.master.show_frame(screens.owner_view.OwnerView)
        else:
            return lambda: self.master.show_frame(screens.manager_view.ManagerView)

    def load_table(self):
        selected_emp = self.filter_var.get()
        emp_id_filter = self.emp_map[selected_emp] if selected_emp in self.emp_map else None

        self.tree.delete(*self.tree.get_children())
        for pid, pay_date, name, amount in get_all_payroll():
            # If filtering by employee is enabled, only show matching entry
            if emp_id_filter and name != selected_emp:
                continue
            self.tree.insert("", "end", values=(pid, pay_date, name, f"${amount:.2f}"))

    def open_add_window(self):
        win = tk.Toplevel(self)
        win.title("Add Payroll")
        win.configure(bg="#FFF4A3")

        tk.Label(win, text="Employee:", bg="#FFF4A3").pack(pady=2)
        emp_var = tk.StringVar()
        emp_dropdown = ttk.Combobox(win, textvariable=emp_var, values=list(self.emp_map.keys()), state="readonly")
        emp_dropdown.pack()
        emp_dropdown.current(0)

        tk.Label(win, text="Amount:", bg="#FFF4A3").pack(pady=2)
        amount_entry = tk.Entry(win, font=("Arial", 12))
        amount_entry.pack()

        tk.Button(win, text="Confirm", font=("Arial", 12, "bold"), bg="#E58A2C",
                  command=lambda: self.confirm_add(win, emp_var.get(), amount_entry.get())).pack(pady=10)

    def confirm_add(self, win, emp_name, amount):
        try:
            emp_id = self.emp_map[emp_name]
            insert_payroll(date.today(), emp_id, float(amount))
            win.destroy()
            self.load_table()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add payroll: {e}")

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Edit", "Please select a payroll entry.")
            return
        values = self.tree.item(selected[0], "values")
        self._open_edit_form(values)

    def double_click_edit(self, event):
        self.edit_selected()

    def _open_edit_form(self, values):
        payroll_id, pay_date, emp_name, amount = values
        win = tk.Toplevel(self)
        win.title("Edit Payroll")
        win.configure(bg="#FFF4A3")

        tk.Label(win, text="Employee:", bg="#FFF4A3").pack(pady=2)
        emp_var = tk.StringVar()
        emp_dropdown = ttk.Combobox(win, textvariable=emp_var, values=list(self.emp_map.keys()), state="readonly")
        emp_dropdown.pack()
        emp_dropdown.set(emp_name)

        tk.Label(win, text="Amount:", bg="#FFF4A3").pack(pady=2)
        amount_entry = tk.Entry(win, font=("Arial", 12))
        # Remove the "$" symbol and extra spaces
        amount_value = amount.replace('$', '').strip()
        amount_entry.insert(0, amount_value)
        amount_entry.pack()

        tk.Button(win, text="Confirm", font=("Arial", 12, "bold"), bg="#E58A2C",
                  command=lambda: self.confirm_edit(win, payroll_id, emp_var.get(), amount_entry.get())).pack(pady=10)

    def confirm_edit(self, win, payroll_id, emp_name, amount):
        try:
            emp_id = self.emp_map[emp_name]
            update_payroll(payroll_id, emp_id, float(amount))
            win.destroy()
            self.load_table()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update payroll: {e}")

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Delete", "Please select a payroll entry.")
            return

        payroll_id = self.tree.item(selected[0], "values")[0]
        confirm = messagebox.askyesno("Delete", f"Delete payroll ID {payroll_id}?")
        if confirm:
            delete_payroll(payroll_id)
            self.load_table()
