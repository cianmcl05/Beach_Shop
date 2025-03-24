import tkinter as tk
from tkinter import messagebox
import screens.emp_view
import screens.emp_view


class EndOfDaySalesScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")

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

        # Back Button
        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#B0F2C2",
                  fg="black", relief="ridge", command=lambda: master.show_frame(screens.emp_view.EmployeeView)).pack(side="left", padx=10)

        # Confirm Button
        tk.Button(button_frame, text="Confirm", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#EECFA3",
                  fg="black", relief="ridge", command=self.confirm).pack(side="left", padx=10)

    def confirm(self):
        reg = self.reg_entry.get()
        credit = self.credit_entry.get()
        cash_in_envelope = self.cash_in_envelope_entry.get()

        if not reg or not credit or not cash_in_envelope:
            messagebox.showwarning("Missing Information", "Please fill in all fields.")
        else:
            messagebox.showinfo("Sales Recorded", "End of day sales recorded successfully!")

