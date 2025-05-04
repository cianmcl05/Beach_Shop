import tkinter as tk
from tkinter import ttk, messagebox
from sql_connection import insert_store, get_full_store_list, update_store, delete_store
import screens.manager_view
import screens.owner_view
import screens.emp_view

class StoreManagementScreen(tk.Frame):
    """
    Screen for managing store records: view, add, edit, delete.
    Navigation back to Manager or Owner view based on user_role.
    """
    def __init__(self, master, user_role):
        super().__init__(master, bg="#FFF4A3")
        self.master = master
        self.user_role = user_role

        # Header label
        tk.Label(
            self,
            text="Store Management",
            font=("Arial", 16, "bold"),
            bg="#FFF4A3"
        ).pack(pady=10)

        # Table container for displaying existing stores
        self.table_frame = tk.Frame(self, bg="#FFF4A3")
        self.table_frame.pack(pady=10)

        # Define columns and create Treeview widget
        columns = ("Store ID", "Store Name", "Location")
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings"
        )
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack()

        # Load initial store data
        self.load_stores()

        # Form for adding a new store
        form_frame = tk.Frame(self, bg="#FFF4A3")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Store Name:", font=("Arial", 12), bg="#FFF4A3").grid(row=0, column=0, padx=5)
        self.store_name_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        self.store_name_entry.grid(row=0, column=1, padx=5)

        tk.Label(form_frame, text="Location:", font=("Arial", 12), bg="#FFF4A3").grid(row=1, column=0, padx=5)
        self.location_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        self.location_entry.grid(row=1, column=1, padx=5)

        # Button to add new store record
        tk.Button(
            form_frame,
            text="Add Store",
            font=("Arial", 12, "bold"),
            bg="#A4E4A0",
            command=self.add_store
        ).grid(row=2, column=0, columnspan=2, pady=10)

        # Action buttons for editing and deleting
        action_frame = tk.Frame(self, bg="#FFF4A3")
        action_frame.pack(pady=5)

        tk.Button(
            action_frame,
            text="Edit Selected",
            font=("Arial", 12, "bold"),
            bg="#F6D860",
            command=self.edit_selected
        ).pack(side="left", padx=10)

        tk.Button(
            action_frame,
            text="Delete Selected",
            font=("Arial", 12, "bold"),
            bg="#F28B82",
            command=self.delete_selected
        ).pack(side="left", padx=10)

        # Refresh and Back buttons
        tk.Button(
            self,
            text="Refresh List",
            font=("Arial", 12, "bold"),
            bg="#E58A2C",
            command=self.load_stores
        ).pack(pady=5)

        tk.Button(
            self,
            text="Back",
            font=("Arial", 12, "bold"),
            bg="#B0F2C2",
            command=self.go_back
        ).pack(pady=5)

    def load_stores(self):
        """
        Fetch all stores from the database and populate the table.
        Clears existing rows before inserting new ones.
        """
        self.tree.delete(*self.tree.get_children())
        stores = get_full_store_list()
        for store in stores:
            self.tree.insert("", "end", values=store)

    def add_store(self):
        """
        Add a new store using inputs from the form.
        Validates that both name and location are provided.
        """
        name = self.store_name_entry.get().strip()
        location = self.location_entry.get().strip()

        if not name or not location:
            messagebox.showwarning("Input Error", "Please fill in both fields.")
            return

        insert_store(name, location)
        messagebox.showinfo("Success", f"Store '{name}' added.")
        # Clear form and refresh table
        self.store_name_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.load_stores()

    def edit_selected(self):
        """
        Open a dialog to edit the currently selected store.
        Prefills fields with existing store data.
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Edit", "Please select a store to edit.")
            return

        store_id, name, location = self.tree.item(selected[0], "values")

        edit_win = tk.Toplevel(self)
        edit_win.title("Edit Store")
        edit_win.configure(bg="#FFF4A3")

        tk.Label(edit_win, text="Store Name:", bg="#FFF4A3").pack(pady=2)
        name_entry = tk.Entry(edit_win, font=("Arial", 12))
        name_entry.insert(0, name)
        name_entry.pack(pady=2)

        tk.Label(edit_win, text="Location:", bg="#FFF4A3").pack(pady=2)
        location_entry = tk.Entry(edit_win, font=("Arial", 12))
        location_entry.insert(0, location)
        location_entry.pack(pady=2)

        tk.Button(
            edit_win,
            text="Save",
            bg="#E58A2C",
            font=("Arial", 12, "bold"),
            command=lambda: self.save_edit(
                edit_win, store_id, name_entry.get(), location_entry.get()
            )
        ).pack(pady=10)

    def save_edit(self, win, store_id, name, location):
        """
        Save updates to a store after editing.
        Validates inputs and updates database record.
        """
        if not name or not location:
            messagebox.showerror("Error", "Both fields are required.")
            return

        update_store(store_id, name, location)
        win.destroy()
        self.load_stores()

    def delete_selected(self):
        """
        Delete the selected store after user confirmation.
        Handles cases where deletion is not allowed.
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Delete", "Please select a store to delete.")
            return

        store_id = self.tree.item(selected[0], "values")[0]
        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete store ID {store_id}?")

        if confirm:
            result = delete_store(store_id)
            # Provide feedback based on result status
            if result == "in_use":
                messagebox.showerror(
                    "Cannot Delete",
                    "This store is still in use by employees, merchandise, or invoices."
                )
            elif result == "deleted":
                messagebox.showinfo("Success", "Store deleted.")
            else:
                messagebox.showerror("Error", "An error occurred while trying to delete the store.")
            self.load_stores()

    def go_back(self):
        """
        Navigate back to ManagerView or OwnerView depending on user_role.
        """
        role = getattr(self.master, "user_role", "manager")

        if role == "owner":
            from screens.owner_view import OwnerView
            self.master.show_frame(OwnerView)
        else:
            from screens.manager_view import ManagerView
            self.master.show_frame(ManagerView)
