import tkinter as tk
from tkinter import ttk
import screens.manager_view
import screens.owner_view
import screens.emp_view
from sql_connection import get_all_invoices, insert_invoice
from datetime import datetime


class InvoicesScreen(tk.Frame):
    def __init__(self, master, user_role):
        super().__init__(master, bg="#fff7a8")
        self.user_role = user_role

        title = tk.Label(self, text="Invoices", font=("Helvetica", 16, "bold"),
                         bg="#d9d6f2", padx=20, pady=5, relief="raised")
        title.pack(pady=10)

        self.table_frame = tk.Frame(self, bg="#fff7a8")
        self.table_frame.pack(pady=10)

        columns = ("Invoice#", "Company", "Amount", "Paid?", "Due", "Status", "Payment Type")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack()
        self.tree.bind("<Double-1>", self.open_edit_window)

        self.load_invoices()
        self.create_buttons(master)

        self.add_invoice_button = tk.Button(self, text="Add Invoice", font=("Helvetica", 12, "bold"), width=15,
                                            height=1, bg="#CFCFCF", command=self.open_add_invoice_window)
        self.add_invoice_button.pack(pady=5)

        self.delete_invoice_button = tk.Button(self, text="Delete Invoice", font=("Helvetica", 12, "bold"), width=15,
                                               height=1, bg="#F2B6A0", command=self.delete_selected_invoice)
        self.delete_invoice_button.pack(pady=5)

    def create_buttons(self, master):
        button_frame = tk.Frame(self, bg="#fff7a8")
        button_frame.pack(pady=5)

        if self.user_role == "manager":
            back_command = lambda: master.show_frame(screens.manager_view.ManagerView)
        else:
            back_command = lambda: master.show_frame(screens.owner_view.OwnerView)

        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10,
                  height=1, bg="#A4E4A0", fg="black", relief="ridge", command=back_command).pack(side="left", padx=10)

        tk.Button(button_frame, text="Save", font=("Helvetica", 12, "bold"), width=10,
                  height=1, bg="#E58A2C", fg="black", relief="ridge", command=self.save_data).pack(side="left", padx=10)

    def load_invoices(self):
        records = get_all_invoices()
        for row in records:
            display_row = list(row)
            display_row[3] = "Yes" if row[3] == "paid" else "No"
            self.tree.insert("", "end", values=display_row)

    def open_add_invoice_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add Invoice")
        add_window.configure(bg="#fff7a8")

        self.invoice_number_entry = self.create_label_entry(add_window, "Invoice #:")
        self.company_entry = self.create_label_entry(add_window, "Company:")
        self.amount_entry = self.create_label_entry(add_window, "Amount:")
        self.due_date_entry = self.create_label_entry(add_window, "Due Date (YYYY-MM-DD):")

        self.payment_status_var = tk.StringVar()
        self.company_status_var = tk.StringVar()
        self.payment_type_var = tk.StringVar()

        self.create_dropdowns(add_window)
        self.create_add_invoice_buttons(add_window)

    def create_dropdowns(self, parent):
        # Payment Status
        tk.Label(parent, text="Payment Status:", font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20)
        ttk.Combobox(parent, textvariable=self.payment_status_var, state="readonly",
                     values=["paid", "not"]).pack(anchor="w", padx=20, pady=5)
        self.payment_status_var.set("not")

        # Company Status
        tk.Label(parent, text="Company Status:", font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20)
        ttk.Combobox(parent, textvariable=self.company_status_var, state="readonly",
                     values=["Active", "Closed", "Vendor", "Client"]).pack(anchor="w", padx=20, pady=5)
        self.company_status_var.set("Active")

        # Payment Type
        tk.Label(parent, text="Payment Type:", font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20)
        ttk.Combobox(parent, textvariable=self.payment_type_var, state="readonly",
                     values=["check", "cash", "card", "withdrawal"]).pack(anchor="w", padx=20, pady=5)
        self.payment_type_var.set("check")

    def create_label_entry(self, parent, text):
        tk.Label(parent, text=text, font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20)
        entry = tk.Entry(parent, font=("Helvetica", 12), width=30)
        entry.pack(anchor="w", padx=20, pady=5)
        return entry

    def create_add_invoice_buttons(self, add_window):
        button_frame = tk.Frame(add_window, bg="#fff7a8")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10, height=1,
                  bg="#A4E4A0", fg="black", relief="ridge", command=add_window.destroy).pack(side="left", padx=10)

        tk.Button(button_frame, text="Confirm", font=("Helvetica", 12, "bold"), width=10, height=1,
                  bg="#E58A2C", fg="black", relief="ridge", command=lambda: self.confirm_add(add_window)).pack(side="left", padx=10)

    def confirm_add(self, window):
        try:
            invoice_number = self.invoice_number_entry.get()
            company = self.company_entry.get()
            amount = float(self.amount_entry.get())
            due_date = datetime.strptime(self.due_date_entry.get(), "%Y-%m-%d").date()

            insert_invoice(invoice_number, company, amount,
                           self.payment_status_var.get(), due_date,
                           self.company_status_var.get(), self.payment_type_var.get())

            self.tree.insert("", "end", values=(
                invoice_number, company, amount,
                "Yes" if self.payment_status_var.get() == "paid" else "No",
                due_date, self.company_status_var.get(), self.payment_type_var.get()
            ))
            window.destroy()
        except Exception as e:
            print("Error adding invoice:", e)

    def open_edit_window(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")

        edit_win = tk.Toplevel(self)
        edit_win.title("Edit Invoice")
        edit_win.configure(bg="#fff7a8")

        self.edit_invoice_number = self.create_label_entry(edit_win, "Invoice #:")
        self.edit_invoice_number.insert(0, values[0])
        self.edit_invoice_number.config(state='disabled')

        self.edit_company = self.create_label_entry(edit_win, "Company:")
        self.edit_company.insert(0, values[1])

        self.edit_amount = self.create_label_entry(edit_win, "Amount:")
        self.edit_amount.insert(0, values[2])

        self.edit_due_date = self.create_label_entry(edit_win, "Due Date (YYYY-MM-DD):")
        self.edit_due_date.insert(0, values[4])

        # Dropdown variables
        self.edit_payment_status = tk.StringVar(value="paid" if values[3] == "Yes" else "not")
        self.edit_company_status = tk.StringVar(value=values[5])
        self.edit_payment_type = tk.StringVar(value=values[6])

        # Payment Status Dropdown
        tk.Label(edit_win, text="Payment Status:", font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20)
        ttk.Combobox(edit_win, textvariable=self.edit_payment_status, state="readonly",
                     values=["paid", "not"]).pack(anchor="w", padx=20, pady=5)

        # Company Status Dropdown
        tk.Label(edit_win, text="Company Status:", font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20)
        ttk.Combobox(edit_win, textvariable=self.edit_company_status, state="readonly",
                     values=["Active", "Closed", "Vendor", "Client"]).pack(anchor="w", padx=20, pady=5)

        # Payment Type Dropdown
        tk.Label(edit_win, text="Payment Type:", font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20)
        ttk.Combobox(edit_win, textvariable=self.edit_payment_type, state="readonly",
                     values=["check", "cash", "card", "withdrawal"]).pack(anchor="w", padx=20, pady=5)

        tk.Button(edit_win, text="Update", font=("Helvetica", 12, "bold"), width=10, height=1,
                  bg="#E58A2C", fg="black", relief="ridge",
                  command=lambda: self.confirm_edit(values[0], selected[0], edit_win)).pack(pady=10)

    def confirm_edit(self, invoice_number, item_id, window):
        try:
            from sql_connection import update_invoice
            update_invoice(
                invoice_number=invoice_number,
                company=self.edit_company.get(),
                amount=float(self.edit_amount.get()),
                payment_status=self.edit_payment_status.get(),
                due_date=datetime.strptime(self.edit_due_date.get(), "%Y-%m-%d").date(),
                company_status=self.edit_company_status.get(),
                payment_type=self.edit_payment_type.get()
            )

            self.tree.item(item_id, values=(
                invoice_number, self.edit_company.get(), self.edit_amount.get(),
                "Yes" if self.edit_payment_status.get() == "paid" else "No",
                self.edit_due_date.get(),
                self.edit_company_status.get(),
                self.edit_payment_type.get()
            ))
            window.destroy()
        except Exception as e:
            print("Error updating invoice:", e)

    def delete_selected_invoice(self):
        selected = self.tree.selection()
        if not selected:
            return
        from sql_connection import delete_invoice
        invoice_number = self.tree.item(selected[0], "values")[0]
        delete_invoice(invoice_number)
        self.tree.delete(selected[0])

    def save_data(self):
        print("Data saved!")  # Placeholder



