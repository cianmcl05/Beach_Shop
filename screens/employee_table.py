import tkinter as tk
from tkinter import ttk, messagebox
import screens.manager_view
import screens.owner_view
from sql_connection import get_all_employees_with_store, delete_employee, update_employee, get_all_stores

class EmployeesScreen(tk.Frame):
    def __init__(self, master, user_role="manager"):
        super().__init__(master, bg="#fff7a8")
        self.user_role = user_role

        tk.Label(self, text="Employees", font=("Helvetica", 16, "bold"),
                 bg="#d9d6f2", padx=20, pady=5, relief="raised").pack(pady=10)

        # Filter Frame
        filter_frame = tk.Frame(self, bg="#fff7a8")
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Filter by Role:", bg="#fff7a8", font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
        self.role_filter = ttk.Combobox(filter_frame, values=["All", "employee", "manager", "owner"], state="readonly")
        self.role_filter.grid(row=0, column=1, padx=5)
        self.role_filter.set("All")

        tk.Label(filter_frame, text="Filter by Store:", bg="#fff7a8", font=("Helvetica", 12)).grid(row=0, column=2, padx=5)
        self.store_filter = ttk.Combobox(filter_frame, state="readonly")
        self.store_filter.grid(row=0, column=3, padx=5)
        self.store_filter.set("All")

        self.store_filter["values"] = ["All"] + [store[1] for store in get_all_stores()]
        self.store_map = {store[1]: store[0] for store in get_all_stores()}

        filter_btn = tk.Button(filter_frame, text="Apply Filters", font=("Helvetica", 10, "bold"),
                               bg="#A4E4A0", command=self.load_employees)
        filter_btn.grid(row=0, column=4, padx=10)

        # Table Frame
        self.table_frame = tk.Frame(self, bg="#fff7a8")
        self.table_frame.pack(pady=10)

        columns = ("Name", "Phone", "Email", "Role", "Store", "Password")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack()

        self.tree.bind("<Double-1>", self.open_edit_window)

        self.load_employees()
        self.create_buttons(master)

    def load_employees(self):
        self.tree.delete(*self.tree.get_children())
        role_filter = self.role_filter.get()
        store_filter = self.store_filter.get()

        employees = get_all_employees_with_store()

        for emp in employees:
            name, phone, email, role, store_name, password = emp
            if role_filter != "All" and role != role_filter:
                continue
            if store_filter != "All" and store_name != store_filter:
                continue
            self.tree.insert("", "end", values=(name, phone, email, role, store_name, password))

    def create_buttons(self, master):
        button_frame = tk.Frame(self, bg="#fff7a8")
        button_frame.pack(pady=5)

        if self.user_role == "manager":
            back_command = lambda: master.show_frame(screens.manager_view.ManagerView)
        else:
            back_command = lambda: master.show_frame(screens.owner_view.OwnerView)

        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10, bg="#A4E4A0",
                  command=back_command).pack(side="left", padx=10)

        tk.Button(button_frame, text="Delete", font=("Helvetica", 12, "bold"), width=10, bg="#F2B6A0",
                  command=self.delete_selected).pack(side="left", padx=10)

        tk.Button(button_frame, text="Refresh", font=("Helvetica", 12, "bold"), width=10, bg="#E58A2C",
                  command=self.load_employees).pack(side="left", padx=10)

    def open_edit_window(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        self.edit_win = tk.Toplevel(self)
        self.edit_win.title("Edit Employee")
        self.edit_win.configure(bg="#fff7a8")

        self.edit_name = self.create_label_entry(self.edit_win, "Name:", values[0])
        self.edit_phone = self.create_label_entry(self.edit_win, "Phone:", values[1])
        self.edit_email = self.create_label_entry(self.edit_win, "Email (unchanged):", values[2], state="disabled")
        self.edit_role = self.create_dropdown(self.edit_win, "Role:", ["employee", "manager", "owner"], values[3])
        self.edit_store = self.create_dropdown(self.edit_win, "Store:", list(self.store_map.keys()), values[4])
        self.edit_password = self.create_label_entry(self.edit_win, "Password:", values[5])

        tk.Button(self.edit_win, text="Save Changes", font=("Helvetica", 12, "bold"), width=12,
                  bg="#E58A2C", command=lambda: self.confirm_edit(values[2], selected[0])).pack(pady=10)

    def create_label_entry(self, parent, label, default="", state="normal"):
        tk.Label(parent, text=label, font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20)
        entry = tk.Entry(parent, font=("Helvetica", 12), width=30)
        entry.insert(0, default)
        entry.config(state=state)
        entry.pack(anchor="w", padx=20, pady=5)
        return entry

    def create_dropdown(self, parent, label, options, default):
        tk.Label(parent, text=label, font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20)
        var = tk.StringVar()
        var.set(default)
        combo = ttk.Combobox(parent, textvariable=var, values=options, state="readonly", width=28)
        combo.pack(anchor="w", padx=20, pady=5)
        return var

    def confirm_edit(self, email, item_id):
        name = self.edit_name.get()
        phone = self.edit_phone.get()
        role = self.edit_role.get()
        store_id = self.store_map.get(self.edit_store.get())
        password = self.edit_password.get()

        update_employee(email, name, phone, role, store_id, password)

        self.tree.item(item_id, values=(name, phone, email, role, self.edit_store.get(), password))
        self.edit_win.destroy()

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            return

        email = self.tree.item(selected[0], "values")[2]
        confirm = messagebox.askyesno("Delete", f"Delete employee with email: {email}?")
        if confirm:
            delete_employee(email)
            self.tree.delete(selected[0])


