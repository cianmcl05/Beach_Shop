import tkinter as tk
from tkinter import ttk, messagebox
import screens.emp_view
import screens.manager_view
import screens.owner_view
import sql_connection
from datetime import datetime

class InvoicesScreen(tk.Frame):
    """
    Screen for viewing, adding, editing, and deleting invoices.
    Navigation varies by user_role: managers and owners.
    """
    def __init__(self, master, user_role):
        super().__init__(master, bg="#fff7a8")
        self.user_role = user_role

        # Title banner
        title = tk.Label(
            self,
            text="Invoices",
            font=("Helvetica", 16, "bold"),
            bg="#d9d6f2",
            padx=20,
            pady=5,
            relief="raised"
        )
        title.pack(pady=10)

        # Container for invoice table
        self.table_frame = tk.Frame(self, bg="#fff7a8")
        self.table_frame.pack(pady=10)

        # Define columns and create the Treeview widget
        columns = (
            "Invoice#", "Company", "Amount",
            "Paid?", "Due", "Status", "Payment Type"
        )
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings"
        )
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack()

        # Double-click an invoice to edit it
        self.tree.bind("<Double-1>", self.open_edit_window)

        # Load existing invoices into the table
        self.load_invoices()

        # Navigation buttons frame
        self.create_buttons(master)

        # Buttons for adding and deleting invoices
        self.add_invoice_button = tk.Button(
            self,
            text="Add Invoice",
            font=("Helvetica", 12, "bold"),
            width=15,
            bg="#CFCFCF",
            command=self.open_add_invoice_window
        )
        self.add_invoice_button.pack(pady=5)

        self.delete_invoice_button = tk.Button(
            self,
            text="Delete Invoice",
            font=("Helvetica", 12, "bold"),
            width=15,
            bg="#F2B6A0",
            command=self.delete_selected_invoice
        )
        self.delete_invoice_button.pack(pady=5)

    def create_buttons(self, master):
        """
        Create Back and Save buttons. 'Back' returns to
        Manager or Owner view based on role.
        """
        button_frame = tk.Frame(self, bg="#fff7a8")
        button_frame.pack(pady=5)

        # Determine back navigation target
        if self.user_role == "manager":
            back_command = lambda: master.show_frame(screens.manager_view.ManagerView)
        else:
            back_command = lambda: master.show_frame(screens.owner_view.OwnerView)

        # Back button
        tk.Button(
            button_frame,
            text="Back",
            font=("Helvetica", 12, "bold"),
            width=10,
            bg="#A4E4A0",
            relief="ridge",
            command=back_command
        ).pack(side="left", padx=10)

        # Save placeholder button
        tk.Button(
            button_frame,
            text="Save",
            font=("Helvetica", 12, "bold"),
            width=10,
            bg="#E58A2C",
            relief="ridge",
            command=self.save_data
        ).pack(side="left", padx=10)

    def load_invoices(self):
        """
        Retrieve all invoices from the database and display them.
        Formats the 'Paid?' column as Yes/No.
        """
        for row in get_all_invoices():
            display = list(row)
            # Convert payment status to human-readable
            display[3] = "Yes" if row[3] == "paid" else "No"
            self.tree.insert("", "end", values=display)

    def open_add_invoice_window(self):
        """
        Open a modal window to enter a new invoice.
        """
        add_window = tk.Toplevel(self)
        add_window.title("Add Invoice")
        add_window.configure(bg="white")

        # Input fields
        self.invoice_number_entry = self.create_label_entry(add_window, "Invoice #:")
        self.company_entry = self.create_label_entry(add_window, "Company:")
        self.amount_entry = self.create_label_entry(add_window, "Amount:")
        self.due_date_entry = self.create_label_entry(add_window, "Due Date (YYYY-MM-DD):")

        # Dropdowns for status and type
        self.payment_status_var = tk.StringVar(value="not")
        self.company_status_var = tk.StringVar(value="Active")
        self.payment_type_var = tk.StringVar(value="check")
        self.create_dropdowns(add_window)

        # Buttons for Add window
        self.create_add_invoice_buttons(add_window)

    def create_dropdowns(self, parent):
        """
        Create Comboboxes for payment status,
        company status, and payment type.
        """
        tk.Label(parent, text="Payment Status:", font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20)
        ttk.Combobox(parent, textvariable=self.payment_status_var,
                     values=["paid", "not"], state="readonly").pack(anchor="w", padx=20, pady=5)

        tk.Label(parent, text="Company Status:", font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20)
        ttk.Combobox(parent, textvariable=self.company_status_var,
                     values=["Active", "Closed", "Vendor", "Client"], state="readonly").pack(anchor="w", padx=20, pady=5)

        tk.Label(parent, text="Payment Type:", font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20)
        ttk.Combobox(parent, textvariable=self.payment_type_var,
                     values=["check", "cash", "card", "withdrawal"], state="readonly").pack(anchor="w", padx=20, pady=5)

    def create_label_entry(self, parent, text):
        """
        Helper to create a label and Entry field.
        Returns the Entry for data capture.
        """
        tk.Label(parent, text=text, font=("Helvetica", 12), bg="#fff7a8").pack(anchor="w", padx=20)
        entry = tk.Entry(parent, font=("Helvetica", 12), width=30)
        entry.pack(anchor="w", padx=20, pady=5)
        return entry

    def create_add_invoice_buttons(self, add_window):
        """
        Create Back and Confirm buttons in the Add Invoice modal.
        """
        frame = tk.Frame(add_window, bg="#fff7a8")
        frame.pack(pady=10)

        # Back (close modal)
        tk.Button(frame, text="Back", font=("Helvetica", 12, "bold"),
                  width=10, bg="#A4E4A0", relief="ridge",
                  command=add_window.destroy).pack(side="left", padx=10)

        # Confirm (save new invoice)
        tk.Button(frame, text="Confirm", font=("Helvetica", 12, "bold"),
                  width=10, bg="#E58A2C", relief="ridge",
                  command=lambda: self.confirm_add(add_window)
        ).pack(side="left", padx=10)

    def confirm_add(self, window):
        """
        Validate and insert a new invoice into the database,
        then update the table and close the modal.
        """
        try:
            invoice_number = self.invoice_number_entry.get()
            company = self.company_entry.get()
            amount = float(self.amount_entry.get())
            due_date = datetime.strptime(
                self.due_date_entry.get(), "%Y-%m-%d"
            ).date()

            insert_invoice(
                invoice_number,
                company,
                amount,
                self.payment_status_var.get(),
                due_date,
                self.company_status_var.get(),
                self.payment_type_var.get()
            )
            # Add new row to table
            self.tree.insert("", "end", values=(
                invoice_number,
                company,
                amount,
                "Yes" if self.payment_status_var.get() == "paid" else "No",
                due_date,
                self.company_status_var.get(),
                self.payment_type_var.get()
            ))
            window.destroy()
        except Exception as e:
            print("Error adding invoice:", e)

    def open_edit_window(self, event):
        """
        Open modal to edit selected invoice. Prefill fields.
        """
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")

        edit_win = tk.Toplevel(self)
        edit_win.title("Edit Invoice")
        edit_win.configure(bg="#fff7a8")

        # Prefilled entries (invoice#, company, amount, due date)
        self.edit_invoice_number = self.create_label_entry(edit_win, "Invoice #:")
        self.edit_invoice_number.insert(0, values[0])
        self.edit_invoice_number.config(state='disabled')

        self.edit_company = self.create_label_entry(edit_win, "Company:")
        self.edit_company.insert(0, values[1])

        self.edit_amount = self.create_label_entry(edit_win, "Amount:")
        self.edit_amount.insert(0, values[2])

        self.edit_due_date = self.create_label_entry(edit_win, "Due Date (YYYY-MM-DD):")
        self.edit_due_date.insert(0, values[4])

        # Dropdowns pre-populated
        self.edit_payment_status = tk.StringVar(value="paid" if values[3] == "Yes" else "not")
        self.edit_company_status = tk.StringVar(value=values[5])
        self.edit_payment_type = tk.StringVar(value=values[6])
        self.create_dropdowns(edit_win)

        # Update button
        tk.Button(
            edit_win,
            text="Update",
            font=("Helvetica", 12, "bold"),
            width=10,
            bg="#E58A2C",
            relief="ridge",
            command=lambda: self.confirm_edit(values[0], selected[0], edit_win)
        ).pack(pady=10)

    def confirm_edit(self, invoice_number, item_id, window):
        """
        Save changes to the selected invoice in the database,
        then update the table row and close the modal.
        """
        try:
            from sql_connection import update_invoice
            update_invoice(
                invoice_number=invoice_number,
                company=self.edit_company.get(),
                amount=float(self.edit_amount.get()),
                payment_status=self.edit_payment_status.get(),
                due_date=datetime.strptime(
                    self.edit_due_date.get(), "%Y-%m-%d"
                ).date(),
                company_status=self.edit_company_status.get(),
                payment_type=self.edit_payment_type.get()
            )
            # Update the row in the table
            self.tree.item(item_id, values=(
                invoice_number,
                self.edit_company.get(),
                self.edit_amount.get(),
                "Yes" if self.edit_payment_status.get() == "paid" else "No",
                self.edit_due_date.get(),
                self.edit_company_status.get(),
                self.edit_payment_type.get()
            ))
            window.destroy()
        except Exception as e:
            print("Error updating invoice:", e)

    def delete_selected_invoice(self):
        """
        Delete the selected invoice from the database and table.
        """
        selected = self.tree.selection()
        if not selected:
            return
        from sql_connection import delete_invoice
        invoice_number = self.tree.item(selected[0], "values")[0]
        delete_invoice(invoice_number)
        self.tree.delete(selected[0])

    def save_data(self):
        # Placeholder for saving bulk changes
        print("Data saved!")
