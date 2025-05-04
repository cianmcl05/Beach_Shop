import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sql_connection
import screens.owner_view

class Withdraw(tk.Frame):
    """
    Screen for viewing and adding withdrawal records.
    Displays current available balance, past withdrawals,
    and allows owner to withdraw funds.
    """
    def __init__(self, master, user_role='owner'):
        super().__init__(master, bg="#FFF4A3")
        self.master = master

        # Header label with raised relief
        tk.Label(
            self,
            text="Withdrawals",
            font=("Helvetica", 16, "bold"),
            bg="#d9d6f2",
            padx=20,
            pady=5,
            relief="raised"
        ).pack(pady=10)

        # Display the current available balance
        balance = sql_connection.get_current_available_balance()
        self.available_label = tk.Label(
            self,
            text=f"Available Balance: ${balance:.2f}",
            font=("Helvetica", 12, "bold"),
            bg="#FFF4A3"
        )
        self.available_label.pack(pady=5)

        # Table frame for listing past withdrawals
        self.table_frame = tk.Frame(self, bg="#FFF4A3")
        self.table_frame.pack(pady=10)

        columns = ("Date", "Amount", "Owner")
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings"
        )
        for col in columns:
            self.tree.heading(col, text=col)  # Set column heading text
            self.tree.column(col, width=150)  # Fixed column width
        self.tree.pack()

        # Create navigation and action buttons
        self.create_buttons()

        # Withdraw button opens a window to enter amount
        tk.Button(
            self,
            text="Withdraw",
            font=("Helvetica", 12, "bold"),
            width=15,
            bg="#CFCFCF",
            command=self.open_add_withdraw_window
        ).pack(pady=5)

        # Load withdrawal data into table
        self.load_data()

    def create_buttons(self):
        """
        Create the Back button to return to OwnerView.
        """
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=5)

        tk.Button(
            button_frame,
            text="Back",
            font=("Helvetica", 12, "bold"),
            width=10,
            bg="#A4E4A0",
            command=lambda: self.master.show_frame(screens.owner_view.OwnerView)
        ).pack(side="left", padx=10)

    def load_data(self):
        """
        Fetch all withdrawals and update the table and balance label.
        """
        # Clear existing rows
        self.tree.delete(*self.tree.get_children())
        rows = sql_connection.get_all_withdrawals()
        for date_val, amount, owner in rows:
            # Format date and amount for display
            date_str = date_val.strftime("%Y-%m-%d")
            amount_str = f"${amount:.2f}"
            self.tree.insert("", "end", values=(date_str, amount_str, owner))

        # Update available balance after adding any new entries
        balance = sql_connection.get_current_available_balance()
        self.available_label.config(text=f"Available Balance: ${balance:.2f}")

    def open_add_withdraw_window(self):
        """
        Open a modal window to input withdrawal amount.
        """
        add_window = tk.Toplevel(self)
        add_window.title("Withdraw")
        add_window.configure(bg="white")

        # Label and entry for amount
        tk.Label(
            add_window,
            text="Amount:",
            font=("Helvetica", 12),
            bg="#FFF4A3"
        ).pack(anchor="w", padx=20, pady=5)
        amount_entry = tk.Entry(add_window, font=("Helvetica", 12), width=30)
        amount_entry.pack(anchor="w", padx=20, pady=5)

        # Confirm button to process withdrawal
        tk.Button(
            add_window,
            text="Confirm",
            font=("Helvetica", 12, "bold"),
            bg="#E58A2C",
            command=lambda: self.confirm_add(add_window, amount_entry)
        ).pack(pady=10)

    def confirm_add(self, window, entry):
        """
        Validate and insert the new withdrawal.
        Ensures amount is positive and does not exceed balance.
        """
        try:
            amount = float(entry.get())
            if amount <= 0:
                messagebox.showwarning("Invalid", "Enter a valid amount.")
                return

            current_balance = sql_connection.get_current_available_balance()
            if amount > current_balance:
                messagebox.showwarning(
                    "Insufficient Funds",
                    "You can't withdraw more than the available balance."
                )
                return

            # Retrieve owner name from current employee ID
            owner_name = sql_connection.get_current_user_name(self.master.emp_id)
            success = sql_connection.insert_withdrawal(amount, owner_name)

            if success:
                # Refresh table and notify user
                self.load_data()
                messagebox.showinfo("Success", f"${amount:.2f} withdrawn successfully.")
                window.destroy()
            else:
                messagebox.showerror("Error", "Could not process withdrawal.")

        except ValueError:
            # Non-numeric input
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
