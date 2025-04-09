import tkinter as tk
from tkinter import ttk
import screens.manager_view
import screens.owner_view
import screens.emp_view  # Optional: if you expect employee users too


class InvoicesScreen(tk.Frame):
    def __init__(self, master, user_role):
        super().__init__(master, bg="#fff7a8")
        self.user_role = user_role

        # Header
        title = tk.Label(self, text="Invoices", font=("Helvetica", 16, "bold"),
                         bg="#d9d6f2", padx=20, pady=5, relief="raised")
        title.pack(pady=10)

        # Table Frame
        self.table_frame = tk.Frame(self, bg="#fff7a8")
        self.table_frame.pack(pady=10)

        # Treeview (Table)
        columns = ("Date", "Invoice#", "Company", "Amount", "Paid?", "DUE", "Closed?")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack()

        # Buttons
        self.create_buttons(master)

        # Add Invoice Button
        self.add_invoice_button = tk.Button(self, text="Add Invoice", font=("Helvetica", 12, "bold"), width=15,
                                            height=1, bg="#CFCFCF", command=self.open_add_invoice_window)
        self.add_invoice_button.pack(pady=5)

    def create_buttons(self, master):
        button_frame = tk.Frame(self, bg="#fff7a8")
        button_frame.pack(pady=5)

        # Back Button based on role
        if self.user_role == "manager":
            back_command = lambda: master.show_frame(screens.manager_view.ManagerView)
        else:
            back_command = lambda: master.show_frame(screens.owner_view.OwnerView)

        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10,
                  height=1, bg="#A4E4A0", fg="black", relief="ridge", command=back_command).pack(side="left", padx=10)

        # Save Button
        tk.Button(button_frame, text="Save", font=("Helvetica", 12, "bold"), width=10,
                  height=1, bg="#E58A2C", fg="black", relief="ridge", command=self.save_data).pack(side="left", padx=10)

    def open_add_invoice_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add Invoice")
        add_window.configure(bg="#fff7a8")

        self.date_entry = self.create_label_entry(add_window, "Date:")
        self.invoice_number_entry = self.create_label_entry(add_window, "Invoice #:")
        self.company_entry = self.create_label_entry(add_window, "Company:")
        self.amount_entry = self.create_label_entry(add_window, "Amount:")
        self.due_date_entry = self.create_label_entry(add_window, "DUE:")

        # Paid and Closed buttons
        self.paid_var = tk.StringVar(value="No")
        self.closed_var = tk.StringVar(value="No")

        self.create_toggle_buttons(add_window, "Paid:", self.paid_var)
        self.create_toggle_buttons(add_window, "Closed:", self.closed_var)

        self.create_add_invoice_buttons(add_window)

    def create_label_entry(self, parent, text):
        tk.Label(parent, text=text, font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20)
        entry = tk.Entry(parent, font=("Helvetica", 12), width=30)
        entry.pack(anchor="w", padx=20, pady=5)
        return entry

    def create_toggle_buttons(self, parent, label_text, variable):
        tk.Label(parent, text=label_text, font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20, pady=5)
        frame = tk.Frame(parent, bg="#fff7a8")
        frame.pack(anchor="w", padx=20)

        tk.Radiobutton(frame, text="Yes", variable=variable, value="Yes", bg="#fff7a8").pack(side="left")
        tk.Radiobutton(frame, text="No", variable=variable, value="No", bg="#fff7a8").pack(side="left")

    def create_add_invoice_buttons(self, add_window):
        button_frame = tk.Frame(add_window, bg="#fff7a8")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10, height=1,
                  bg="#A4E4A0", fg="black", relief="ridge", command=add_window.destroy).pack(side="left", padx=10)

        tk.Button(button_frame, text="Confirm", font=("Helvetica", 12, "bold"), width=10, height=1,
                  bg="#E58A2C", fg="black", relief="ridge", command=lambda: self.confirm_add(add_window)).pack(side="left", padx=10)

    def confirm_add(self, window):
        invoice_data = (
            self.date_entry.get(),
            self.invoice_number_entry.get(),
            self.company_entry.get(),
            self.amount_entry.get(),
            self.paid_var.get(),
            self.due_date_entry.get(),
            self.closed_var.get()
        )
        self.tree.insert("", "end", values=invoice_data)
        window.destroy()

    def save_data(self):
        print("Data saved!")  # Placeholder


# Usage of InvoicesScreen, you would need a master (parent) window like Tk() to initialize

