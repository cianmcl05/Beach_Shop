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
    """
    Screen for viewing, filtering, adding, editing, and deleting merchandise items.
    Supports role-based back navigation (employee, manager, owner).
    """
    def __init__(self, master, user_role="manager"):
        super().__init__(master, bg="#FFF4A3")
        self.master = master
        self.user_role = user_role

        # Create mappings between store names and IDs
        self.store_map = { name: sid for sid, name in get_all_stores() }
        self.reverse_store_map = { sid: name for name, sid in self.store_map.items() }

        # Header label
        tk.Label(
            self,
            text="Merchandise Inventory",
            font=("Arial", 16, "bold"),
            bg="#FFF4A3"
        ).pack(pady=10)

        # Filter controls: store and date
        filter_frame = tk.Frame(self, bg="#FFF4A3")
        filter_frame.pack(pady=5, fill="x", padx=20)

        tk.Label(
            filter_frame,
            text="Filter by Store:",
            font=("Arial", 11),
            bg="#FFF4A3"
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
            font=("Arial", 11),
            bg="#FFF4A3"
        ).pack(side=tk.LEFT, padx=5)

        self.date_filter_entry = tk.Entry(
            filter_frame,
            font=("Arial", 11),
            width=12
        )
        self.date_filter_entry.pack(side=tk.LEFT, padx=5)

        # Apply and reset filter buttons
        tk.Button(
            filter_frame,
            text="Apply Filter",
            font=("Arial", 11, "bold"),
            bg="#E58A2C",
            command=self.apply_filter
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            filter_frame,
            text="Reset",
            font=("Arial", 11, "bold"),
            bg="#D9D9D9",
            command=self.load_table
        ).pack(side=tk.LEFT, padx=5)

        # Table container: expands vertically and horizontally
        self.table_frame = tk.Frame(self, bg="#FFF4A3")
        self.table_frame.pack(pady=10, fill="both", expand=True, padx=20)

        # Define table columns and widget
        self.columns = ("ID", "Type", "Value", "Date", "Store")
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=self.columns,
            show="headings",
            height=15            # display more rows
        )

        # Set column headings and widths
        widths = {"ID": 50, "Type": 100, "Value": 80, "Date": 90, "Store": 100}
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths[col], anchor="center")

        # Pack the treeview to fill the frame
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.on_double_click)

        # Load data into the table initially
        self.load_table()

        # Action buttons below the table
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=5)

        # Back button (role-based)
        back_command = self.get_back_command()
        tk.Button(
            button_frame,
            text="Back",
            font=("Arial", 12, "bold"),
            width=8,
            bg="#B0F2C2",
            command=back_command
        ).pack(side=tk.LEFT, padx=8)

        # Add new merchandise
        tk.Button(
            button_frame,
            text="Add",
            font=("Arial", 12, "bold"),
            width=8,
            bg="#EECFA3",
            command=self.show_add_form
        ).pack(side=tk.LEFT, padx=8)

        # Delete selected entry
        tk.Button(
            button_frame,
            text="Delete",
            font=("Arial", 12, "bold"),
            width=8,
            bg="#F2B6A0",
            command=self.delete_selected
        ).pack(side=tk.LEFT, padx=8)

    def get_back_command(self):
        """
        Return a lambda that navigates to the correct view based on user_role.
        """
        if self.user_role == "employee":
            return lambda: self.master.show_frame(screens.emp_view.EmployeeView)
        elif self.user_role == "manager":
            return lambda: self.master.show_frame(screens.manager_view.ManagerView)
        else:
            return lambda: self.master.show_frame(screens.owner_view.OwnerView)

    def load_table(self):
        """
        Fetch and display all merchandise records.
        Clears existing rows, then populates from the database.
        """
        self.tree.delete(*self.tree.get_children())
        for merch in get_all_merchandise():
            self.tree.insert("", "end", values=merch)

    def apply_filter(self):
        """
        Filter merchandise by selected store and/or date.
        Fetches fresh data and applies in-memory filtering.
        """
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
        # Refresh table with filtered rows
        self.tree.delete(*self.tree.get_children())
        for row in filtered:
            self.tree.insert("", "end", values=row)

    def show_add_form(self):
        """
        Open a modal window to input new merchandise details.
        """
        add_win = tk.Toplevel(self)
        add_win.title("Add Merchandise")
        add_win.configure(bg="white")

        # Input for merchandise type
        tk.Label(
            add_win,
            text="Merch Type:",
            font=("Arial", 12),
            bg="#FFF4A3"
        ).pack(anchor="w", padx=20, pady=2)
        merch_type_entry = tk.Entry(add_win, font=("Arial", 12))
        merch_type_entry.pack(padx=20)

        # Input for merchandise value
        tk.Label(
            add_win,
            text="Merch Value:",
            font=("Arial", 12),
            bg="#FFF4A3"
        ).pack(anchor="w", padx=20, pady=2)
        merch_value_entry = tk.Entry(add_win, font=("Arial", 12))
        merch_value_entry.pack(padx=20)

        # Confirm button to call confirm_add
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
        """
        Validate and insert the new merchandise into the database,
        then refresh the table and close the modal.
        """
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
        """
        Delete the currently selected merchandise record,
        after user confirmation.
        """
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Delete", "Select a row to delete.")
            return
        merch_id = self.tree.item(sel[0], "values")[0]
        if messagebox.askyesno("Delete", f"Delete item ID {merch_id}?"):
            delete_merchandise(merch_id)
            self.tree.delete(sel[0])

    def on_double_click(self, event):
        """
        Handle double-click on a row to open an edit form.
        Prefill fields with existing data.
        """
        sel = self.tree.selection()
        if not sel:
            return
        merch_id, mtype, mvalue, mdate, mstore = self.tree.item(sel[0], "values")
        # Create edit modal
        edit_win = tk.Toplevel(self)
        edit_win.title("Edit Merchandise")
        edit_win.configure(bg="white")

        # Type field
        tk.Label(edit_win, text="Merch Type:", bg="#FFF4A3").pack()
        merch_type_entry = tk.Entry(edit_win, font=("Arial", 12))
        merch_type_entry.insert(0, mtype)
        merch_type_entry.pack()

        # Value field
        tk.Label(edit_win, text="Merch Value:", bg="#FFF4A3").pack()
        merch_value_entry = tk.Entry(edit_win, font=("Arial", 12))
        merch_value_entry.insert(0, mvalue)
        merch_value_entry.pack()

        # Date field
        tk.Label(
            edit_win,
            text="Purchase Date (YYYY-MM-DD):",
            bg="#FFF4A3"
        ).pack()
        date_entry = tk.Entry(edit_win, font=("Arial", 12))
        date_entry.insert(0, mdate)
        date_entry.pack()

        # Store dropdown
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

        # Save changes button
        tk.Button(
            edit_win,
            text="Save Changes",
            font=("Arial", 12, "bold"),
            bg="#E58A2C",
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
        """
        Save edited merchandise details back to the database,
        then refresh the table and close the edit modal.
        """
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
