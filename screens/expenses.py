import tkinter as tk
from tkinter import ttk


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.configure(bg="#FAF3A3")

        # Table Frame
        self.table_frame = tk.Frame(root, bg="#FAF3A3")
        self.table_frame.pack(pady=10)

        # Treeview (Table)
        columns = ("Type", "Date", "Value", "Tax", "Payment Method", "Store")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack()

        # Buttons
        button_frame = tk.Frame(root, bg="#FAF3A3")
        button_frame.pack(pady=5)

        self.back_button = tk.Button(button_frame, text="Back", bg="#A4E4A0", command=root.quit)
        self.back_button.grid(row=0, column=0, padx=5)

        self.expenses_label = tk.Label(button_frame, text="Expenses", bg="#CFCFCF", font=("Arial", 12, "bold"))
        self.expenses_label.grid(row=0, column=1, padx=5)

        self.save_button = tk.Button(button_frame, text="Save", bg="#E58A2C", command=self.save_data)
        self.save_button.grid(row=0, column=2, padx=5)

        self.add_expense_button = tk.Button(root, text="Add Expense", bg="#CFCFCF",
                                            command=self.open_add_expense_window)
        self.add_expense_button.pack(pady=5)

    def open_add_expense_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Expense")
        add_window.configure(bg="#FAF3A3")

        # Form Labels & Entry Fields
        tk.Label(add_window, text="Value:", bg="#FAF3A3").grid(row=0, column=0, padx=5, pady=5)
        value_entry = tk.Entry(add_window)
        value_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Type:", bg="#FAF3A3").grid(row=1, column=0, padx=5, pady=5)
        type_entry = tk.Entry(add_window)
        type_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Payment Method:", bg="#FAF3A3").grid(row=2, column=0, padx=5, pady=5)
        payment_entry = tk.Entry(add_window)
        payment_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(add_window, bg="#FAF3A3")
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        back_button = tk.Button(button_frame, text="Back", bg="#A4E4A0", command=add_window.destroy)
        back_button.grid(row=0, column=0, padx=5)

        add_expense_label = tk.Label(button_frame, text="Add Expense", bg="#CFCFCF", font=("Arial", 12, "bold"))
        add_expense_label.grid(row=0, column=1, padx=5)

        confirm_button = tk.Button(button_frame, text="Confirm", bg="#E58A2C",
                                   command=lambda: self.confirm_add(value_entry, type_entry, payment_entry, add_window))
        confirm_button.grid(row=0, column=2, padx=5)

    def confirm_add(self, value_entry, type_entry, payment_entry, window):
        self.tree.insert("", "end", values=(type_entry.get(), "N/A", value_entry.get(), "N/A", payment_entry.get(), "N/A"))
        window.destroy()

    def save_data(self):
        print("Data saved!")  # Placeholder for actual save functionality


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
