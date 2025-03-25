import tkinter as tk
from tkinter import ttk  # Add this line to import ttk
import screens.manager_view  # Make sure to import ManagerView class

class InvoicesScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#fff7a8")

        # Header
        title = tk.Label(self, text="Invoices", font=("Helvetica", 16, "bold"), bg="#d9d6f2", padx=20, pady=5, relief="raised")
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
        self.add_invoice_button = tk.Button(self, text="Add Invoice", font=("Helvetica", 12, "bold"), width=15, height=1,
                                            bg="#CFCFCF", command=self.open_add_invoice_window)
        self.add_invoice_button.pack(pady=5)

    def create_buttons(self, master):
        button_frame = tk.Frame(self, bg="#fff7a8")
        button_frame.pack(pady=5)

        # Back Button
        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#A4E4A0",
                  fg="black", relief="ridge", command=lambda: master.show_frame(screens.manager_view.ManagerView)).pack(side="left", padx=10)

        # Save Button
        tk.Button(button_frame, text="Save", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#E58A2C",
                  fg="black", relief="ridge", command=self.save_data).pack(side="left", padx=10)

    def open_add_invoice_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add Invoice")
        add_window.configure(bg="#fff7a8")

        # Form Labels & Entry Fields
        self.invoice_number_entry = self.create_label_entry(add_window, "Invoice #:")
        self.company_entry = self.create_label_entry(add_window, "Company:")
        self.amount_entry = self.create_label_entry(add_window, "Amount:")
        self.due_date_entry = self.create_label_entry(add_window, "DUE:")

        # Paid and Closed are buttons, so no entries for these fields
        self.paid_label = tk.Label(add_window, text="Paid:", font=("Helvetica", 12), bg="#fff7a8")
        self.paid_label.pack(anchor="w", padx=20, pady=5)

        self.paid_yes_button = tk.Button(add_window, text="Yes", bg="#4CAF50", fg="white", width=5)
        self.paid_yes_button.pack(side="left", padx=20)

        self.paid_no_button = tk.Button(add_window, text="No", bg="#f44336", fg="white", width=5)
        self.paid_no_button.pack(side="left", padx=20)

        # Buttons for Confirm and Back
        self.create_add_invoice_buttons(add_window)

    def create_label_entry(self, parent, text):
        tk.Label(parent, text=text, font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20)
        entry = tk.Entry(parent, font=("Helvetica", 12), width=30)
        entry.pack(anchor="w", padx=20, pady=5)
        return entry

    def create_add_invoice_buttons(self, add_window):
        button_frame = tk.Frame(add_window, bg="#fff7a8")
        button_frame.pack(pady=10)

        # Back Button
        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#A4E4A0",
                  fg="black", relief="ridge", command=add_window.destroy).pack(side="left", padx=10)

        # Confirm Button
        tk.Button(button_frame, text="Confirm", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#E58A2C",
                  fg="black", relief="ridge", command=lambda: self.confirm_add(add_window)).pack(side="left", padx=10)

    def confirm_add(self, window):
        # Adding invoice data to table (in a real application, you'd save it somewhere)
        invoice_data = (self.invoice_number_entry.get(), self.company_entry.get(), self.amount_entry.get(),
                        self.due_date_entry.get())
        self.tree.insert("", "end", values=invoice_data)
        window.destroy()

    def save_data(self):
        print("Data saved!")  # Placeholder for actual save functionality


# Usage of InvoicesScreen, you would need a master (parent) window like Tk() to initialize

