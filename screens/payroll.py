import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import screens.manager_view
import screens.owner_view
import sql_connection
from sql_connection import (
    get_all_payroll,
    insert_payroll,
    get_all_employees,
    update_payroll_with_bonus,
    delete_payroll
)

class PayrollScreen(tk.Frame):
    def __init__(self, master, user_role="manager"):
        super().__init__(master, bg="#FFF4A3")
        self.master = master
        self.user_role = user_role

        # Employee lookup
        self.emp_map = {name: eid for eid, name in get_all_employees()}

        # Header
        tk.Label(self, text="Payroll Management",
                 font=("Arial", 16, "bold"), bg="#FFF4A3")\
          .pack(pady=10)

        # Filter Area (remains above table)
        filter_frame = tk.Frame(self, bg="#FFF4A3")
        filter_frame.pack(pady=5, fill="x", padx=20)

        tk.Label(filter_frame, text="Filter by Employee:",
                 bg="#FFF4A3", font=("Arial", 11))\
          .pack(side=tk.LEFT)

        self.filter_var = tk.StringVar()
        self.filter_dropdown = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=["All"] + list(self.emp_map.keys()),
            state="readonly",
            width=20
        )
        self.filter_dropdown.pack(side=tk.LEFT, padx=5)
        self.filter_dropdown.set("All")

        tk.Button(filter_frame, text="Apply",
                  bg="#E58A2C", font=("Arial", 11, "bold"),
                  command=self.load_table)\
          .pack(side=tk.LEFT, padx=5)

        # Table
        self.table_frame = tk.Frame(self, bg="#FFF4A3")
        self.table_frame.pack(pady=10, fill="both", expand=True, padx=20)

        self.columns = ("ID", "Date", "Employee", "Amount", "Pay with Bonus")
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=self.columns,
            show="headings",
            height=15
        )
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.double_click_edit)

        # Load data
        self.load_table()

        # Buttons below table
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Back",
                  font=("Arial", 12, "bold"), width=10,
                  bg="#B0F2C2", command=self.get_back_command())\
          .pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="Add Payroll",
                  font=("Arial", 12, "bold"), width=15,
                  bg="#EECFA3", command=self.open_add_window)\
          .pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="Edit Selected",
                  font=("Arial", 12, "bold"), width=15,
                  bg="#F6D860", command=self.edit_selected)\
          .pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="Delete Selected",
                  font=("Arial", 12, "bold"), width=15,
                  bg="#F28B82", command=self.delete_selected)\
          .pack(side=tk.LEFT, padx=10)

    def get_back_command(self):
        return lambda: self.master.show_frame(
            screens.owner_view.OwnerView
            if self.user_role == "owner"
            else screens.manager_view.ManagerView
        )

    def load_table(self):
        selected_emp = self.filter_var.get()
        emp_id_filter = self.emp_map.get(selected_emp)

        today = date.today()
        current_month = today.month
        current_year = today.year

        all_payrolls = get_all_payroll()
        self.tree.delete(*self.tree.get_children())

        for pid, pay_date, name, amount, pay_with_bonus in all_payrolls:
            if self.user_role == "manager":
                pay_date_obj = pay_date if isinstance(pay_date, date) else date.fromisoformat(pay_date)
                if pay_date_obj.month != current_month or pay_date_obj.year != current_year:
                    continue
            if emp_id_filter and name != selected_emp:
                continue
            self.tree.insert("", "end", values=(
                pid,
                pay_date,
                name,
                f"${amount:.2f}",
                f"${pay_with_bonus:.2f}" if pay_with_bonus is not None else "N/A"
            ))

    def open_add_window(self):
        win = tk.Toplevel(self)
        win.title("Add Payroll")
        win.configure(bg="white")

        tk.Label(win, text="Employee:", bg="#FFF4A3").pack(pady=2)
        emp_var = tk.StringVar()
        emp_dropdown = ttk.Combobox(
            win,
            textvariable=emp_var,
            values=list(self.emp_map.keys()),
            state="readonly"
        )
        emp_dropdown.pack()
        emp_dropdown.current(0)

        tk.Label(win, text="Hourly Wage ($):", bg="#FFF4A3").pack(pady=2)
        wage_entry = tk.Entry(win, font=("Arial", 12))
        wage_entry.pack()

        tk.Label(win, text="Hours Worked:", bg="#FFF4A3").pack(pady=2)
        hours_entry = tk.Entry(win, font=("Arial", 12))
        hours_entry.pack()

        tk.Button(win, text="Confirm",
                  font=("Arial", 12, "bold"), bg="#E58A2C",
                  command=lambda: self.confirm_add(
                      win, emp_var.get(), wage_entry.get(), hours_entry.get()
                  )
        ).pack(pady=10)

    def confirm_add(self, win, emp_name, wage_str, hours_str):
        try:
            emp_id = self.emp_map[emp_name]
            store_id = getattr(self.master, "current_store_id", None)
            hourly_wage = float(wage_str)
            hours = float(hours_str)
            base_pay = hourly_wage * hours
            insert_payroll(date.today(), emp_id, base_pay, store_id)
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
        payroll_id, pay_date, emp_name, amount, _ = values
        win = tk.Toplevel(self)
        win.title("Edit Payroll")
        win.configure(bg="#FFF4A3")

        tk.Label(win, text="Employee:", bg="#FFF4A3").pack(pady=2)
        emp_var = tk.StringVar()
        emp_dropdown = ttk.Combobox(
            win,
            textvariable=emp_var,
            values=list(self.emp_map.keys()),
            state="readonly"
        )
        emp_dropdown.pack()
        emp_dropdown.set(emp_name)

        tk.Label(win, text="Hourly Wage ($):", bg="#FFF4A3").pack(pady=2)
        wage_entry = tk.Entry(win, font=("Arial", 12))
        wage_entry.pack()

        tk.Label(win, text="Hours Worked:", bg="#FFF4A3").pack(pady=2)
        hours_entry = tk.Entry(win, font=("Arial", 12))
        hours_entry.pack()

        try:
            raw_amount = float(amount.replace('$', '').strip())
            default_wage = 15.00
            est_hours = raw_amount / default_wage
            wage_entry.insert(0, f"{default_wage:.2f}")
            hours_entry.insert(0, f"{est_hours:.2f}")
        except:
            pass

        tk.Button(win, text="Confirm",
                  font=("Arial", 12, "bold"), bg="#E58A2C",
                  command=lambda: self.confirm_edit(
                      win, payroll_id, emp_var.get(), wage_entry.get(), hours_entry.get()
                  )
        ).pack(pady=10)

    def confirm_edit(self, win, payroll_id, emp_name, wage_str, hours_str):
        try:
            emp_id = self.emp_map[emp_name]
            hourly_wage = float(wage_str)
            hours = float(hours_str)
            base_pay = hourly_wage * hours

            latest_bonus = sql_connection.get_latest_bonus_for_employee(emp_id) or 0
            total_with_bonus = base_pay + latest_bonus

            update_payroll_with_bonus(payroll_id, emp_id, base_pay, total_with_bonus)
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
        if messagebox.askyesno("Delete", f"Delete payroll ID {payroll_id}?"):
            delete_payroll(payroll_id)
            self.load_table()
