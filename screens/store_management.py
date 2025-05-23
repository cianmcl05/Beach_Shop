import tkinter as tk
from tkinter import ttk, messagebox
from sql_connection import insert_store, get_full_store_list, update_store, delete_store


class StoreManagementScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")
        self.master = master

        tk.Label(self, text="Store Management", font=("Arial", 16, "bold"), bg="#FFF4A3").pack(pady=10)

        self.table_frame = tk.Frame(self, bg="#FFF4A3")
        self.table_frame.pack(pady=10)

        columns = ("Store ID", "Store Name", "Location")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack()

        self.load_stores()

        # Add Store Form
        form_frame = tk.Frame(self, bg="#FFF4A3")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Store Name:", font=("Arial", 12), bg="#FFF4A3").grid(row=0, column=0, padx=5)
        self.store_name_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        self.store_name_entry.grid(row=0, column=1, padx=5)

        tk.Label(form_frame, text="Location:", font=("Arial", 12), bg="#FFF4A3").grid(row=1, column=0, padx=5)
        self.location_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        self.location_entry.grid(row=1, column=1, padx=5)

        tk.Button(form_frame, text="Add Store", font=("Arial", 12, "bold"), bg="#A4E4A0",
                  command=self.add_store).grid(row=2, column=0, columnspan=2, pady=10)

        # Edit/Delete Buttons
        action_frame = tk.Frame(self, bg="#FFF4A3")
        action_frame.pack(pady=5)

        tk.Button(action_frame, text="Edit Selected", font=("Arial", 12, "bold"), bg="#F6D860",
                  command=self.edit_selected).pack(side="left", padx=10)

        tk.Button(action_frame, text="Delete Selected", font=("Arial", 12, "bold"), bg="#F28B82",
                  command=self.delete_selected).pack(side="left", padx=10)

        tk.Button(self, text="Refresh List", font=("Arial", 12, "bold"), bg="#E58A2C",
                  command=self.load_stores).pack(pady=5)

        tk.Button(self, text="Back", font=("Arial", 12, "bold"), bg="#B0F2C2",
                  command=self.go_back).pack(pady=5)

    def load_stores(self):
        self.tree.delete(*self.tree.get_children())
        stores = get_full_store_list()
        for store in stores:
            self.tree.insert("", "end", values=store)

    def add_store(self):
        name = self.store_name_entry.get().strip()
        location = self.location_entry.get().strip()

        if not name or not location:
            messagebox.showwarning("Input Error", "Please fill in both fields.")
            return

        insert_store(name, location)
        messagebox.showinfo("Success", f"Store '{name}' added.")
        self.store_name_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.load_stores()

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Edit", "Please select a store to edit.")
            return

        values = self.tree.item(selected[0], "values")
        store_id, name, location = values

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

        tk.Button(edit_win, text="Save", bg="#E58A2C", font=("Arial", 12, "bold"),
                  command=lambda: self.save_edit(edit_win, store_id, name_entry.get(), location_entry.get())).pack(pady=10)

    def save_edit(self, win, store_id, name, location):
        if not name or not location:
            messagebox.showerror("Error", "Both fields are required.")
            return

        update_store(store_id, name, location)
        win.destroy()
        self.load_stores()

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Delete", "Please select a store to delete.")
            return

        store_id = self.tree.item(selected[0], "values")[0]
        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete store ID {store_id}?")

        if confirm:
            result = delete_store(store_id)
            if result == "in_use":
                messagebox.showerror("Cannot Delete",
                                     "This store is still in use by employees, merchandise, or invoices.")
            elif result == "deleted":
                messagebox.showinfo("Success", "Store deleted.")
            else:
                messagebox.showerror("Error", "An error occurred while trying to delete the store.")
            self.load_stores()

    def go_back(self):
        role = getattr(self.master, "user_role", "manager")

        if role == "owner":
            from screens.owner_view import OwnerView
            self.master.show_frame(OwnerView)
        else:
            from screens.manager_view import ManagerView
            self.master.show_frame(ManagerView)


