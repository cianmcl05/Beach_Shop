import tkinter as tk
from tkinter import messagebox
import screens.emp_view
import screens.manager_view  # Assuming you have the manager view
import screens.owner_view  # Assuming you might need owner view too
import screens.emp_view
import sql_connection


class EndOfDaySalesScreen(tk.Frame):
    def __init__(self, master, user_role, emp_id=None):
        super().__init__(master, bg="#FFF4A3")
        self.user_role = user_role
        self.emp_id = emp_id
        # Header
        title = tk.Label(self, text="End of Day\nSales", font=("Helvetica", 16, "bold"), bg="#d9d6f2", padx=20, pady=5, relief="raised")
        title.pack(pady=10)

        # Input Fields
        self.reg_entry = self.create_label_entry("Reg:")
        self.credit_entry = self.create_label_entry("Credit:")
        self.cash_in_envelope_entry = self.create_label_entry("Cash in Envelope:")

        # Buttons
        self.create_buttons(master)

    def create_label_entry(self, text, show=""):
        tk.Label(self, text=text, font=("Helvetica", 12), bg="#FFF4A3").pack(anchor="w", padx=20)
        entry = tk.Entry(self, font=("Helvetica", 12), show=show, width=30)
        entry.pack(anchor="w", padx=20, pady=5)
        return entry

    def create_buttons(self, master):
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=10)

        user_role = self.user_role  # Use the role already passed to this screen

        # Back Button: Adjust based on user role
        if user_role == "employee":
            back_screen = screens.emp_view.EmployeeView
        elif user_role == "manager":
            back_screen = screens.manager_view.ManagerView
        else:
            back_screen = screens.owner_view.OwnerView

        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#B0F2C2",
                  fg="black", relief="ridge", command=lambda: master.show_frame(back_screen)).pack(side="left", padx=10)

        # Confirm Button
        tk.Button(button_frame, text="Confirm", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#EECFA3",
                  fg="black", relief="ridge", command=self.confirm).pack(side="left", padx=10)

    def confirm(self):
        reg = self.reg_entry.get()
        credit = self.credit_entry.get()
        cash_in_envelope = self.cash_in_envelope_entry.get()

        if not reg or not credit or not cash_in_envelope:
            messagebox.showwarning("Missing Information", "Please fill in all fields.")
            return

        try:
            reg = float(reg)
            credit = float(credit)
            cash_in_envelope = float(cash_in_envelope)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid decimal numbers.")
            return

        # Check that Reg == Credit + Cash
        if round(reg, 2) != round(credit + cash_in_envelope, 2):
            messagebox.showerror("Mismatch", "Reg must equal Credit + Cash in Envelope.")
            return

        from sql_connection import insert_end_of_day_sales
        success = insert_end_of_day_sales(reg, credit, cash_in_envelope, self.emp_id)

        if success:
            messagebox.showinfo("Sales Recorded", "End of day sales recorded successfully!")
            self.reg_entry.delete(0, tk.END)
            self.credit_entry.delete(0, tk.END)
            self.cash_in_envelope_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to save sales record.")

