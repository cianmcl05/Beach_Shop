import tkinter as tk
from tkinter import ttk, messagebox
import screens.manager_view
import screens.owner_view
from sql_connection import (
    get_all_employees_with_store,
    delete_employee,
    update_employee,
    get_all_stores
)

class EmployeesScreen(tk.Frame):
    """
    Screen for viewing, filtering, editing, and deleting employees.
    Managers and owners can filter by role or store, edit selected entries, and delete employees.
    """
    def __init__(self, master, user_role="manager"):
        super().__init__(master, bg="#fff7a8")
        self.user_role = user_role

        # Title label
        tk.Label(
            self,
            text="Employees",
            font=("Helvetica", 16, "bold"),
            bg="#d9d6f2",
            padx=20,
            pady=5,
            relief="raised"
        ).pack(pady=10)

        # Create filter controls
        filter_frame = tk.Frame(self, bg="#fff7a8")
        filter_frame.pack(pady=5)

        # Role filter dropdown
        tk.Label(
            filter_frame,
            text="Filter by Role:",
            bg="#fff7a8",
            font=("Helvetica", 12)
        ).grid(row=0, column=0, padx=5)
        self.role_filter = ttk.Combobox(
            filter_frame,
            values=["All", "employee", "manager", "owner"],
            state="readonly"
        )
        self.role_filter.grid(row=0, column=1, padx=5)
        self.role_filter.set("All")

        # Store filter dropdown
        tk.Label(
            filter_frame,
            text="Filter by Store:",
            bg="#fff7a8",
            font=("Helvetica", 12)
        ).grid(row=0, column=2, padx=5)
        stores = get_all_stores()
        store_names = [store[1] for store in stores]
        self.store_filter = ttk.Combobox(
            filter_frame,
            values=["All"] + store_names,
            state="readonly"
        )
        self.store_filter.grid(row=0, column=3, padx=5)
        self.store_filter.set("All")

        # Map store names to IDs for updates
        self.store_map = {name: sid for sid, name in stores}

        # Button to apply filters
        tk.Button(
            filter_frame,
            text="Apply Filters",
            font=("Helvetica", 10, "bold"),
            bg="#A4E4A0",
            command=self.load_employees
        ).grid(row=0, column=4, padx=10)

        # Table container
        self.table_frame = tk.Frame(self, bg="#fff7a8")
        self.table_frame.pack(pady=10)

        # Define and configure columns
        columns = ("Name", "Phone", "Email", "Role", "Store", "Password")
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings"
        )
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack()

        # Double-click to open edit window
        self.tree.bind("<Double-1>", self.open_edit_window)

        # Initial data load and button creation
        self.load_employees()
        self.create_buttons(master)

    def load_employees(self):
        """
        Fetch and display employees, applying role and store filters.
        """
        # Clear existing rows
        self.tree.delete(*self.tree.get_children())

        # Get current filter selections
        role = self.role_filter.get()
        store = self.store_filter.get()

        # Retrieve all employees with store names
        employees = get_all_employees_with_store()
        for name, phone, email, role_val, store_name, password in employees:
            # Skip if role filter is active
            if role != "All" and role_val != role:
                continue
            # Skip if store filter is active
            if store != "All" and store_name != store:
                continue
            # Insert row into table
            self.tree.insert(
                "", "end",
                values=(name, phone, email, role_val, store_name, password)
            )

    def create_buttons(self, master):
        """
        Create Back, Delete, and Refresh buttons.
        """
        button_frame = tk.Frame(self, bg="#fff7a8")
        button_frame.pack(pady=5)

        # Determine back navigation based on user role
        if self.user_role == "manager":
            back_cmd = lambda: master.show_frame(screens.manager_view.ManagerView)
        else:
            back_cmd = lambda: master.show_frame(screens.owner_view.OwnerView)

        # Back button
        tk.Button(
            button_frame,
            text="Back",
            font=("Helvetica", 12, "bold"),
            width=10,
            bg="#A4E4A0",
            command=back_cmd
        ).pack(side="left", padx=10)

        # Delete selected employee
        tk.Button(
            button_frame,
            text="Delete",
            font=("Helvetica", 12, "bold"),
            width=10,
            bg="#F2B6A0",
            command=self.delete_selected
        ).pack(side="left", padx=10)

        # Refresh table data
        tk.Button(
            button_frame,
            text="Refresh",
            font=("Helvetica", 12, "bold"),
            width=10,
            bg="#E58A2C",
            command=self.load_employees
        ).pack(side="left", padx=10)

    def open_edit_window(self, event):
        """
        Open a popup window to edit the selected employee's details.
        """
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")

        # Create and configure the edit window
        self.edit_win = tk.Toplevel(self)
        self.edit_win.title("Edit Employee")
        self.edit_win.configure(bg="white")

        # Fields: Name, Phone, Email (disabled), Role, Store, Password
        self.edit_name = self.create_label_entry(self.edit_win, "Name:", values[0])
        self.edit_phone = self.create_label_entry(self.edit_win, "Phone:", values[1])
        self.edit_email = self.create_label_entry(
            self.edit_win,
            "Email (unchanged):",
            values[2],
            state="disabled"
        )
        self.edit_role = self.create_dropdown(
            self.edit_win,
            "Role:",
            ["employee", "manager", "owner"],
            values[3]
        )
        self.edit_store = self.create_dropdown(
            self.edit_win,
            "Store:",
            list(self.store_map.keys()),
            values[4]
        )
        self.edit_password = self.create_label_entry(
            self.edit_win,
            "Password:",
            values[5]
        )

        # Save changes button
        tk.Button(
            self.edit_win,
            text="Save Changes",
            font=("Helvetica", 12, "bold"),
            width=12,
            bg="#E58A2C",
            command=lambda: self.confirm_edit(values[2], selected[0])
        ).pack(pady=10)

    def create_label_entry(self, parent, label, default, state="normal"):
        """
        Helper: create a labeled Entry widget.
        Returns the Entry widget for later value retrieval.
        """
        tk.Label(
            parent,
            text=label,
            font=("Helvetica", 12),
            bg="#fff7a8"
        ).pack(anchor="w", padx=20)
        entry = tk.Entry(parent, font=("Helvetica", 12), width=30)
        entry.insert(0, default)
        entry.config(state=state)
        entry.pack(anchor="w", padx=20, pady=5)
        return entry

    def create_dropdown(self, parent, label, options, default):
        """
        Helper: create a labeled Combobox for selection.
        Returns the StringVar tied to the Combobox.
        """
        tk.Label(
            parent,
            text=label,
            font=("Helvetica", 12),
            bg="#fff7a8"
        ).pack(anchor="w", padx=20)
        var = tk.StringVar()
        var.set(default)
        combo = ttk.Combobox(
            parent,
            textvariable=var,
            values=options,
            state="readonly",
            width=28
        )
        combo.pack(anchor="w", padx=20, pady=5)
        return var

    def confirm_edit(self, email, item_id):
        """
        Update the employee record in the database and refresh the table row.
        """
        name = self.edit_name.get()
        phone = self.edit_phone.get()
        role = self.edit_role.get()
        store_id = self.store_map[self.edit_store.get()]
        password = self.edit_password.get()

        # Update database entry
        update_employee(email, name, phone, role, store_id, password)

        # Update table display
        self.tree.item(item_id, values=(
            name, phone, email, role, self.edit_store.get(), password
        ))
        self.edit_win.destroy()

    def delete_selected(self):
        """
        Delete the selected employee after confirmation.
        """
        selected = self.tree.selection()
        if not selected:
            return

        email = self.tree.item(selected[0], "values")[2]
        confirm = messagebox.askyesno(
            "Delete",
            f"Delete employee with email: {email}?"
        )
        if confirm:
            delete_employee(email)
            self.tree.delete(selected[0])
