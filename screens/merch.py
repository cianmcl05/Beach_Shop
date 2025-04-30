import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import screens.manager_view
import screens.owner_view
import screens.emp_view
from sql_connection import (
    get_all_merchandise,
    insert_merchandise,
    delete_merchandise,
    get_all_stores,
    update_merchandise
)

class MerchandiseInventoryScreen(tk.Frame):
    def __init__(self, master, user_role="manager"):
        super().__init__(master, bg="#FFF4A3")
        self.master = master
        self.user_role = user_role

        # Store lookup maps
        self.store_map = {name: sid for sid, name in get_all_stores()}
        self.reverse_store_map = {sid: name for name, sid in self.store_map.items()}

        # Header
        tk.Label(
            self,
            text="Merchandise Inventory",
            font=("Arial", 16, "bold"),
            bg="#FFF4A3"
        ).pack(pady=10)

        # Filter Area
        filter_frame = tk.Frame(self, bg="#FFF4A3")
        filter_frame.pack(pady=5, fill="x", padx=20)

        tk.Label(
            filter_frame,
            text="Filter by Store:",
            bg="#FFF4A3",
            font=("Arial", 11)
        ).pack(side=tk.LEFT, padx=5)

        self.filter_store_var = tk.StringVar()
        ttk.Combobox(
            filter_frame,
            textvariable=self.filter_store_var,
            values=list(self.store_map.keys()),
            state="readonly",
            width=12
        ).pack(side=tk.LEFT, padx=5)

        tk.Label(
            filter_frame,
            text="Date (YYYY-MM-DD):",
            bg="#FFF4A3",
            font=("Arial", 11)
        ).pack(side=tk.LEFT, padx=5)

        self.date_filter_entry = tk.Entry(
            filter_frame,
            font=("Arial", 11),
            width=12
        )
        self.date_filter_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(
            filter_frame,
            text="Apply Filter",
            bg="#E58A2C",
            font=("Arial", 11, "bold"),
            command=self.apply_filter
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            filter_frame,
            text="Reset",
            bg="#D9D9D9",
            font=("Arial", 11, "bold"),
            command=self.load_table
        ).pack(side=tk.LEFT, padx=5)

        # Expanded Table Container
        self.table_frame = tk.Frame(self, bg="#FFF4A3")
        self.table_frame.pack(pady=10, fill="both", expand=True, padx=20)

        self.columns = ("ID", "Type", "Value", "Date", "Store")
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=self.columns,
            show="headings",
            height=15  # more visible rows
        )

        # Column widths
        widths = {"ID": 50, "Type": 100, "Value": 80, "Date": 90, "Store": 100}
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths[col], anchor="center")

        # Let the tree expand vertically as well
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.on_double_click)

        # Load initial data
        self.load_table()

        # Buttons below table
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=5)

        back_command = self.get_back_command()
        tk.Button(
            button_frame,
            text="Back",
            font=("Arial", 12, "bold"),
            width=8,
            bg="#B0F2C2",
            command=back_command
        ).pack(side=tk.LEFT, padx=8)

        tk.Button(
            button_frame,
            text="Add",
            font=("Arial", 12, "bold"),
            width=8,
            bg="#EECFA3",
            command=self.show_add_form
        ).pack(side=tk.LEFT, padx=8)

        tk.Button(
            button_frame,
            text="Delete",
            font=("Arial", 12, "bold"),
            width=8,
            bg="#F2B6A0",
            command=self.delete_selected
        ).pack(side=tk.LEFT, padx=8)

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
            # merch is (ID, type, value, date, store)
            self.tree.insert("", "end", values=merch)

    def apply_filter(self):
        store_name = self.filter_store_var.get()
        date_str = self.date_filter_entry.get().strip()

        filtered = []
        for merch in get_all_merchandise():
            merch_id, mtype, mvalue, mdate, mstore = merch
            if store_name and mstore != store_name:
                continue
            if date_str and str(mdate) != date_str:
                continue
            filtered.append(merch)

        # refresh table
        self.tree.delete(*self.tree.get_children())
        for row in filtered:
            self.tree.insert("", "end", values=row)

    def show_add_form(self):
        add_win = tk.Toplevel(self)
        add_win.title("Add Merchandise")
        add_win.configure(bg="white")

        tk.Label(
            add_win,
            text="Merch Type:",
            bg="#FFF4A3",
            font=("Arial", 12)
        ).pack(anchor="w", padx=20, pady=2)
        merch_type_entry = tk.Entry(add_win, font=("Arial", 12))
        merch_type_entry.pack(padx=20)

        tk.Label(
            add_win,
            text="Merch Value:",
            bg="#FFF4A3",
            font=("Arial", 12)
        ).pack(anchor="w", padx=20, pady=2)
        merch_value_entry = tk.Entry(add_win, font=("Arial", 12))
        merch_value_entry.pack(padx=20)

        tk.Button(
            add_win,
            text="Confirm",
            font=("Arial", 12, "bold"),
            bg="#E58A2C",
            width=12,
            command=lambda: self.confirm_add(
                add_win,
                merch_type_entry.get(),
                merch_value_entry.get()
            )
        ).pack(pady=10)

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
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Delete", "Select a row to delete.")
            return

        merch_id = self.tree.item(sel[0], "values")[0]
        if messagebox.askyesno("Delete", f"Delete item ID {merch_id}?"):
            delete_merchandise(merch_id)
            self.tree.delete(sel[0])

    def on_double_click(self, event):
        sel = self.tree.selection()
        if not sel:
            return

        merch_id, mtype, mvalue, mdate, mstore = self.tree.item(sel[0], "values")

        edit_win = tk.Toplevel(self)
        edit_win.title("Edit Merchandise")
        edit_win.configure(bg="#FFF4A3")

        tk.Label(edit_win, text="Merch Type:", bg="#FFF4A3").pack()
        merch_type_entry = tk.Entry(edit_win, font=("Arial", 12))
        merch_type_entry.insert(0, mtype)
        merch_type_entry.pack()

        tk.Label(edit_win, text="Merch Value:", bg="#FFF4A3").pack()
        merch_value_entry = tk.Entry(edit_win, font=("Arial", 12))
        merch_value_entry.insert(0, mvalue)
        merch_value_entry.pack()

        tk.Label(
            edit_win,
            text="Purchase Date (YYYY-MM-DD):",
            bg="#FFF4A3"
        ).pack()
        date_entry = tk.Entry(edit_win, font=("Arial", 12))
        date_entry.insert(0, mdate)
        date_entry.pack()

        tk.Label(edit_win, text="Store:", bg="#FFF4A3").pack()
        store_var = tk.StringVar()
        store_dd = ttk.Combobox(
            edit_win,
            textvariable=store_var,
            values=list(self.store_map.keys()),
            state="readonly"
        )
        store_dd.pack()
        store_dd.set(mstore)

        tk.Button(
            edit_win,
            text="Save Changes",
            bg="#E58A2C",
            font=("Arial", 12, "bold"),
            command=lambda: self.save_edit(
                edit_win,
                merch_id,
                merch_type_entry.get(),
                merch_value_entry.get(),
                date_entry.get(),
                store_var.get()
            )
        ).pack(pady=10)

    def save_edit(self, win, merch_id, merch_type, merch_value, purchase_date, store_name):
        try:
            store_id = self.store_map[store_name]
            update_merchandise(
                merch_id,
                merch_type,
                float(merch_value),
                purchase_date,
                store_id
            )
            self.load_table()
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not update merchandise: {e}")
