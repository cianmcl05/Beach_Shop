import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import screens.manager_view
import screens.owner_view
import screens.emp_view
from sql_connection import get_all_merchandise, insert_merchandise, delete_merchandise, get_all_stores, update_merchandise


class MerchandiseInventoryScreen(tk.Frame):
    def __init__(self, master, user_role="manager"):
        super().__init__(master, bg="#FFF4A3")
        self.master = master
        self.user_role = user_role

        self.store_map = {name: sid for sid, name in get_all_stores()}
        self.reverse_store_map = {sid: name for name, sid in self.store_map.items()}

        self.header_label = tk.Label(self, text="Merchandise Inventory", font=("Arial", 16, "bold"), bg="#FFF4A3")
        self.header_label.pack(pady=10)

        self.button_frame = tk.Frame(self, bg="#FFF4A3")
        self.button_frame.pack()

        back_command = self.get_back_command()
        tk.Button(self.button_frame, text="Back", font=("Arial", 12, "bold"), width=10,
                  bg="#B0F2C2", command=back_command).pack(side=tk.LEFT, padx=10)

        tk.Button(self.button_frame, text="Add", font=("Arial", 12, "bold"), width=10,
                  bg="#EECFA3", command=self.show_add_form).pack(side=tk.LEFT, padx=10)

        tk.Button(self.button_frame, text="Delete", font=("Arial", 12, "bold"), width=10,
                  bg="#F2B6A0", command=self.delete_selected).pack(side=tk.LEFT, padx=10)

        # Filter Area
        filter_frame = tk.Frame(self, bg="#FFF4A3")
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Filter by Store:", bg="#FFF4A3", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        self.filter_store_var = tk.StringVar()
        self.store_filter_dropdown = ttk.Combobox(filter_frame, textvariable=self.filter_store_var, values=list(self.store_map.keys()), state="readonly", width=15)
        self.store_filter_dropdown.pack(side=tk.LEFT, padx=5)

        tk.Label(filter_frame, text="Date (YYYY-MM-DD):", bg="#FFF4A3", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        self.date_filter_entry = tk.Entry(filter_frame, font=("Arial", 11), width=15)
        self.date_filter_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(filter_frame, text="Apply Filter", bg="#E58A2C", font=("Arial", 11, "bold"),
                  command=self.apply_filter).pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="Reset", bg="#D9D9D9", font=("Arial", 11, "bold"),
                  command=self.load_table).pack(side=tk.LEFT, padx=5)

        # Table
        self.table_frame = tk.Frame(self, bg="#FFF4A3")
        self.table_frame.pack(pady=10, fill="both", expand=True)

        self.columns = ("ID", "Merch Type", "Value", "Purchase Date", "Store")
        self.tree = ttk.Treeview(self.table_frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack()

        self.tree.bind("<Double-1>", self.on_double_click)
        self.load_table()

    def get_back_command(self):
        if self.user_role == "employee":
            return lambda: self.master.show_frame(screens.emp_view.EmployeeView)
        elif self.user_role == "manager":
            return lambda: self.master.show_frame(screens.manager_view.ManagerView)
        else:
            return lambda: self.master.show_frame(screens.owner_view.OwnerView)

    def load_table(self):
        self.tree.delete(*self.tree.get_children())
        for merch in get_all_merchandise():
            self.tree.insert("", "end", values=merch)

    def apply_filter(self):
        store_name = self.filter_store_var.get()
        date_str = self.date_filter_entry.get().strip()

        filtered = []
        for merch in get_all_merchandise():
            merch_id, merch_type, merch_value, purchase_date, store = merch

            if store_name and store != store_name:
                continue

            if date_str:
                try:
                    if str(purchase_date) != date_str:
                        continue
                except:
                    continue

            filtered.append(merch)

        self.tree.delete(*self.tree.get_children())
        for row in filtered:
            self.tree.insert("", "end", values=row)

    def show_add_form(self):
        add_win = tk.Toplevel(self)
        add_win.title("Add Merchandise")
        add_win.configure(bg="#FFF4A3")

        tk.Label(add_win, text="Merch Type:", bg="#FFF4A3", font=("Arial", 12)).pack(anchor="w", padx=20, pady=2)
        merch_type_entry = tk.Entry(add_win, font=("Arial", 12))
        merch_type_entry.pack(padx=20)

        tk.Label(add_win, text="Merch Value:", bg="#FFF4A3", font=("Arial", 12)).pack(anchor="w", padx=20, pady=2)
        merch_value_entry = tk.Entry(add_win, font=("Arial", 12))
        merch_value_entry.pack(padx=20)

        tk.Button(add_win, text="Confirm", font=("Arial", 12, "bold"), bg="#E58A2C", width=12,
                  command=lambda: self.confirm_add(add_win, merch_type_entry.get(), merch_value_entry.get())).pack(pady=10)

    def confirm_add(self, win, merch_type, merch_value):
        try:
            purchase_date = date.today()
            store_id = self.master.current_store_id
            merch_value = float(merch_value)

            insert_merchandise(merch_type, merch_value, purchase_date, store_id)
            self.load_table()
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not add merchandise: {e}")

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Delete", "Select a row to delete.")
            return

        merch_id = self.tree.item(selected[0], "values")[0]
        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete item ID {merch_id}?")
        if confirm:
            delete_merchandise(merch_id)
            self.tree.delete(selected[0])

    def on_double_click(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        merch_id, merch_type, merch_value, purchase_date, store_name = values

        edit_win = tk.Toplevel(self)
        edit_win.title("Edit Merchandise")
        edit_win.configure(bg="#FFF4A3")

        tk.Label(edit_win, text="Merch Type:", bg="#FFF4A3").pack()
        merch_type_entry = tk.Entry(edit_win, font=("Arial", 12))
        merch_type_entry.insert(0, merch_type)
        merch_type_entry.pack()

        tk.Label(edit_win, text="Merch Value:", bg="#FFF4A3").pack()
        merch_value_entry = tk.Entry(edit_win, font=("Arial", 12))
        merch_value_entry.insert(0, merch_value)
        merch_value_entry.pack()

        tk.Label(edit_win, text="Purchase Date (YYYY-MM-DD):", bg="#FFF4A3").pack()
        date_entry = tk.Entry(edit_win, font=("Arial", 12))
        date_entry.insert(0, purchase_date)
        date_entry.pack()

        tk.Label(edit_win, text="Store:", bg="#FFF4A3").pack()
        store_var = tk.StringVar()
        store_dropdown = ttk.Combobox(edit_win, textvariable=store_var, values=list(self.store_map.keys()), state="readonly")
        store_dropdown.pack()
        store_dropdown.set(store_name)

        tk.Button(edit_win, text="Save Changes", bg="#E58A2C", font=("Arial", 12, "bold"),
                  command=lambda: self.save_edit(edit_win, merch_id, merch_type_entry.get(),
                                                 merch_value_entry.get(), date_entry.get(), store_var.get())).pack(pady=10)

    def save_edit(self, win, merch_id, merch_type, merch_value, purchase_date, store_name):
        try:
            store_id = self.store_map[store_name]
            update_merchandise(merch_id, merch_type, float(merch_value), purchase_date, store_id)
            self.load_table()
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not update merchandise: {e}")



