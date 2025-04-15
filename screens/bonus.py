import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import sql_connection
import screens.manager_view
import screens.owner_view

class Bonus(tk.Frame):
    def __init__(self, master, user_role):
        super().__init__(master, bg="#FFF4A3")
        self.master = master
        self.user_role = user_role
        self.emp_map = {name: eid for eid, name in sql_connection.get_all_employee_names()}
        self.full_data = []

        tk.Label(self, text="Bonus", font=("Helvetica", 16, "bold"),
                 bg="#d9d6f2", padx=20, pady=5, relief="raised").pack(pady=10)



        self.table_frame = tk.Frame(self, bg="#FFF4A3")
        self.table_frame.pack(pady=10)

        columns = ("BonusID", "Employee", "Sales", "Gross", "Bonus %", "Bonus Amount")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=0 if col == "BonusID" else 120)
        self.tree.pack()
        self.tree.bind("<Double-1>", self.on_tree_double_click)

        self.create_buttons(master)

        tk.Button(self, text="Auto-Generate Weekly Gross", font=("Helvetica", 12, "bold"), width=25,
                  bg="#A4E4A0", command=self.auto_generate_weekly_gross).pack(pady=5)

        self.load_bonuses()

    def create_buttons(self, master):
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=5)

        back_command = lambda: master.show_frame(
            screens.manager_view.ManagerView if self.user_role == "manager" else screens.owner_view.OwnerView)

        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10,
                  bg="#A4E4A0", command=back_command).pack(side="left", padx=10)

        tk.Button(button_frame, text="Refresh", font=("Helvetica", 12, "bold"), width=10,
                  bg="#E58A2C", command=self.load_bonuses).pack(side="left", padx=10)

        tk.Button(button_frame, text="Confirm Selected", font=("Helvetica", 12, "bold"), width=15,
                  bg="#CFCFCF", command=self.confirm_selected_bonus).pack(side="left", padx=10)

        tk.Button(button_frame, text="Delete", font=("Helvetica", 12, "bold"), width=10,
                  bg="#F27474", command=self.delete_selected_bonus).pack(side="left", padx=10)


        filter_frame = tk.Frame(self, bg="#FFF4A3")
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Filter by Employee:", font=("Helvetica", 12), bg="#FFF4A3").pack(side="left",
                                                                                                      padx=5)

        self.filter_var = tk.StringVar()
        emp_names = ["All"] + list(self.emp_map.keys())
        self.filter_dropdown = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                            values=emp_names, state="readonly", font=("Helvetica", 12), width=20)
        self.filter_dropdown.pack(side="left", padx=5)
        self.filter_dropdown.current(0)

        tk.Button(filter_frame, text="Apply Filter", font=("Helvetica", 12), bg="#A4E4A0",
                  command=self.apply_filter).pack(side="left", padx=10)

        tk.Button(self, text="View Bonus History", font=("Helvetica", 12, "bold"), width=18, height=1,
                  bg="#D8D5F2", command=self.view_bonus_history).pack(pady=5)

    def auto_generate_weekly_gross(self):
        self.tree.delete(*self.tree.get_children())
        today = datetime.now()
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)

        summaries = sql_connection.get_employee_weekly_gross_summary(monday.date(), sunday.date())
        self.full_data = []
        for emp_name, sales_total, emp_id in summaries:
            row = ("", emp_name, f"{sales_total:.2f}", f"{sales_total:.2f}", "", "")
            self.tree.insert("", "end", values=row)
            self.full_data.append(row)

    def load_bonuses(self):
        self.tree.delete(*self.tree.get_children())
        rows = sql_connection.get_all_bonuses(include_id=True)
        self.full_data = []
        for bonus_id, name, sales, gross, percent, amount in rows:
            row = (bonus_id, name, f"{sales:.2f}", f"{gross:.2f}",
                   f"{percent:.2f}%", f"${amount:.2f}")
            self.tree.insert("", "end", values=row)
            self.full_data.append(row)

    def filter_tree(self, *args):
        query = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        for row in self.full_data:
            if query in row[1].lower():
                self.tree.insert("", "end", values=row)

    def confirm_selected_bonus(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a bonus row to confirm.")
            return

        values = self.tree.item(selected[0])["values"]
        emp_name = values[1]
        sales = float(values[2])
        gross = float(values[3])
        percent_str = self.tree.set(selected[0], "Bonus %").replace('%', '').strip()

        if not percent_str:
            messagebox.showwarning("Missing Bonus %", "Please enter a bonus percentage.")
            return

        try:
            bonus_pct = float(percent_str)
            bonus_amount = round((gross * bonus_pct) / 100 / 5) * 5
            emp_id = self.emp_map.get(emp_name)

            sql_connection.insert_bonus(emp_id, bonus_amount, sales, gross, bonus_pct)
            self.tree.set(selected[0], "Bonus Amount", f"${bonus_amount:.2f}")
            self.tree.set(selected[0], "Bonus %", f"{bonus_pct:.2f}%")
            messagebox.showinfo("Saved", f"Bonus for {emp_name} saved.")
        except Exception as e:
            print("Error confirming bonus:", e)
            messagebox.showerror("Error", "Invalid input. Please check the values.")

    def delete_selected_bonus(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a bonus to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this bonus?")
        if not confirm:
            return

        bonus_id = self.tree.set(selected[0], "BonusID")
        if sql_connection.delete_bonus(bonus_id):
            self.tree.delete(selected[0])
            messagebox.showinfo("Deleted", "Bonus successfully deleted.")
        else:
            messagebox.showerror("Error", "Failed to delete bonus.")

    def view_bonus_history(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Employee", "Please select a row from the table first.")
            return

        emp_name = self.tree.item(selected[0])["values"][1]
        emp_id = self.emp_map.get(emp_name)

        if not emp_id:
            messagebox.showerror("Error", "Employee ID not found.")
            return

        history_win = tk.Toplevel(self)
        history_win.title(f"{emp_name} - Bonus History")
        history_win.configure(bg="#FFF4A3")

        columns = ("Date", "Sales", "Gross", "Bonus %", "Amount")
        tree = ttk.Treeview(history_win, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(padx=10, pady=10)

        history = sql_connection.get_bonus_history_for_employee(emp_id)
        for row in history:
            date_val, sales, gross, percent, amount = row
            tree.insert("", "end", values=(
                date_val.strftime("%Y-%m-%d"), f"{sales:.2f}",
                f"{gross:.2f}", f"{percent:.2f}%", f"${amount:.2f}"
            ))

        tk.Button(history_win, text="Close", command=history_win.destroy,
                  font=("Helvetica", 12), bg="#B0F2C2").pack(pady=10)

    def on_tree_double_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = self.tree.identify_column(event.x)
        row_id = self.tree.identify_row(event.y)
        if not row_id or column != "#5":  # Bonus % column
            return

        x, y, width, height = self.tree.bbox(row_id, column)
        value = self.tree.set(row_id, column)

        entry = tk.Entry(self.tree, font=("Helvetica", 12), width=10)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value.replace('%', '').strip())
        entry.focus()

        def save_value(event):
            new_val = entry.get()
            try:
                pct = float(new_val)
                self.tree.set(row_id, column, f"{pct:.2f}%")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number.")
            entry.destroy()

        entry.bind("<Return>", save_value)
        entry.bind("<FocusOut>", save_value)

    def apply_filter(self):
        selected_name = self.filter_var.get()
        self.tree.delete(*self.tree.get_children())

        rows = sql_connection.get_all_bonuses(include_id=True)
        for r in rows:
            bonus_id, name, sales, gross, percent, amount = r
            if selected_name == "All" or selected_name == name:
                self.tree.insert("", "end", values=(
                    bonus_id, name, f"{sales:.2f}", f"{gross:.2f}",
                    f"{percent:.2f}%", f"${amount:.2f}"
                ))



