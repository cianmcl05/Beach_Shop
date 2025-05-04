import tkinter as tk
from tkinter import messagebox
import screens.emp_view
import screens.manager_view
import screens.owner_view
import sql_connection

class EndOfDaySalesScreen(tk.Frame):
    """
    UI for employees/managers/owners to submit end-of-day sales data:
    register total, credit total, and cash-in-envelope.
    Validates inputs and writes to the database, with overwrite protection.
    """
    def __init__(self, master, user_role, emp_id=None):
        super().__init__(master, bg="#FFF4A3")
        self.user_role = user_role
        self.emp_id = emp_id

        # Title label at top
        tk.Label(
            self,
            text="End of Day\nSales",
            font=("Helvetica", 16, "bold"),
            bg="#d9d6f2",
            padx=20,
            pady=5,
            relief="raised"
        ).pack(pady=10)

        # Input fields for register, credit, and envelope amounts
        self.reg_entry = self._create_label_entry("Reg:")
        self.credit_entry = self._create_label_entry("Credit:")
        self.cash_in_envelope_entry = self._create_label_entry("Cash in Envelope:")

        # Navigation and confirm buttons
        self._create_buttons(master)

    def _create_label_entry(self, label_text):
        """
        Helper to create a labeled Entry widget.
        Returns the Entry for later value retrieval.
        """
        tk.Label(
            self,
            text=label_text,
            font=("Helvetica", 12),
            bg="#FFF4A3"
        ).pack(anchor="w", padx=20)
        entry = tk.Entry(
            self,
            font=("Helvetica", 12),
            width=30
        )
        entry.pack(anchor="w", padx=20, pady=5)
        return entry

    def _create_buttons(self, master):
        """
        Creates 'Back' and 'Confirm' buttons at the bottom.
        'Back' navigates based on user_role; 'Confirm' triggers data validation and submission.
        """
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=10)

        # Determine destination frame for 'Back'
        if self.user_role == "employee":
            back_screen = screens.emp_view.EmployeeView
        elif self.user_role == "manager":
            back_screen = screens.manager_view.ManagerView
        else:
            back_screen = screens.owner_view.OwnerView

        # Back button
        tk.Button(
            button_frame,
            text="Back",
            font=("Helvetica", 12, "bold"),
            width=10,
            bg="#B0F2C2",
            relief="ridge",
            command=lambda: master.show_frame(back_screen)
        ).pack(side="left", padx=10)

        # Confirm button
        tk.Button(
            button_frame,
            text="Confirm",
            font=("Helvetica", 12, "bold"),
            width=10,
            bg="#EECFA3",
            relief="ridge",
            command=self.confirm
        ).pack(side="left", padx=10)

    def confirm(self):
        """
        Validate inputs and submit end-of-day sales to the database.
        Ensures Reg = Credit + Cash in Envelope and prevents duplicate submissions unless confirmed.
        """
        # Retrieve and validate entries
        reg_str = self.reg_entry.get()
        credit_str = self.credit_entry.get()
        envelope_str = self.cash_in_envelope_entry.get()
        if not (reg_str and credit_str and envelope_str):
            messagebox.showwarning("Missing Information", "Please fill in all fields.")
            return

        try:
            reg = float(reg_str)
            credit = float(credit_str)
            envelope = float(envelope_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid decimal numbers.")
            return

        # Check arithmetic consistency
        if round(reg, 2) != round(credit + envelope, 2):
            messagebox.showerror(
                "Mismatch",
                "Reg must equal Credit + Cash in Envelope."
            )
            return

        # Identify store context
        store_id = getattr(self.master, "current_store_id", None)
        if store_id is None:
            messagebox.showerror("Error", "No store selected.")
            return

        from datetime import datetime
        from sql_connection import (
            check_existing_end_of_day_sale,
            insert_end_of_day_sales
        )

        # Prompt before overwriting today's record
        today = datetime.now().date()
        if check_existing_end_of_day_sale(store_id, today):
            overwrite = messagebox.askyesno(
                "Confirm Overwrite",
                "An end-of-day sale has already been submitted for this store today.\n"
                "Submitting again will overwrite the previous one. Continue?"
            )
            if not overwrite:
                return

        # Insert or overwrite record
        success = insert_end_of_day_sales(
            reg, credit, envelope, self.emp_id, store_id
        )
        if success:
            messagebox.showinfo("Sales Recorded", "End of day sales recorded successfully!")
            # Clear inputs after successful save
            self.reg_entry.delete(0, tk.END)
            self.credit_entry.delete(0, tk.END)
            self.cash_in_envelope_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to save sales record.")
