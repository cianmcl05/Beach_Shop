import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sql_connection
import screens.owner_view

class Withdraw(tk.Frame):
    def __init__(self, master, user_role='owner'):
        super().__init__(master, bg="#FFF4A3")
        self.master = master
        # Header
        tk.Label(self, text="Withdrawals", font=("Helvetica", 16, "bold"), bg="#d9d6f2", padx=20, pady=5, relief="raised").pack(pady=10)

        # Available Amount
        balance = sql_connection.get_current_available_balance()
        self.available_label = tk.Label(self, text=f"Available Balance: ${balance:.2f}", font=("Helvetica", 12, "bold"), bg="#FFF4A3")
        self.available_label.pack(pady=5)

        # Table
        self.table_frame = tk.Frame(self, bg="#FFF4A3")
        self.table_frame.pack(pady=10)

        columns = ("Date", "Amount", "Owner")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack()

        # Buttons
        self.create_buttons()

        tk.Button(self, text="Withdraw", font=("Helvetica", 12, "bold"), width=15, bg="#CFCFCF", command=self.open_add_withdraw_window).pack(pady=5)

        self.load_data()

    def create_buttons(self):
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10, bg="#A4E4A0",
                  command=lambda: self.master.show_frame(screens.owner_view.OwnerView)).pack(side="left", padx=10)

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        rows = sql_connection.get_all_withdrawals()
        for date, amount, owner in rows:
            self.tree.insert("", "end", values=(date.strftime("%Y-%m-%d"), f"${amount:.2f}", owner))

        balance = sql_connection.get_current_available_balance()
        self.available_label.config(text=f"Available Balance: ${balance:.2f}")

    def open_add_withdraw_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Withdraw")
        add_window.configure(bg="white")

        tk.Label(add_window, text="Amount:", font=("Helvetica", 12), bg="#FFF4A3").pack(anchor="w", padx=20, pady=5)
        amount_entry = tk.Entry(add_window, font=("Helvetica", 12), width=30)
        amount_entry.pack(anchor="w", padx=20, pady=5)

        tk.Button(add_window, text="Confirm", font=("Helvetica", 12, "bold"), bg="#E58A2C",
                  command=lambda: self.confirm_add(add_window, amount_entry)).pack(pady=10)

    def confirm_add(self, window, entry):
        try:
            amount = float(entry.get())
            if amount <= 0:
                messagebox.showwarning("Invalid", "Enter a valid amount.")
                return

            current_balance = sql_connection.get_current_available_balance()
            if amount > current_balance:
                messagebox.showwarning("Insufficient Funds", "You can't withdraw more than the available balance.")
                return

            owner_name = sql_connection.get_current_user_name(self.master.emp_id)
            success = sql_connection.insert_withdrawal(amount, owner_name)

            if success:
                self.load_data()
                messagebox.showinfo("Success", f"${amount:.2f} withdrawn successfully.")
                window.destroy()
            else:
                messagebox.showerror("Error", "Could not process withdrawal.")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

