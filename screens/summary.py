import tkinter as tk
from tkinter import ttk, messagebox
import sql_connection
import screens.manager_view
import screens.owner_view
from datetime import datetime

class SummaryScreen(tk.Frame):
    def __init__(self, master, user_role):
        super().__init__(master, bg="#FFF4A3")
        self.master = master
        self.user_role = user_role

        tk.Label(self, text="Monthly Summary", font=("Arial", 20, "bold"),
                 bg="#D8D5F2", fg="black", pady=10).pack(pady=(20, 5))

        self.filter_frame = tk.Frame(self, bg="#FFF4A3")
        self.filter_frame.pack(pady=10)

        tk.Label(self.filter_frame, text="Select Month:", font=("Arial", 12), bg="#FFF4A3").grid(row=0, column=0, padx=5)
        self.month_var = tk.StringVar()
        self.month_dropdown = ttk.Combobox(self.filter_frame, textvariable=self.month_var, state="readonly",
                                           values=[f"{i:02}" for i in range(1, 13)], width=5, font=("Arial", 12))
        self.month_dropdown.grid(row=0, column=1, padx=5)
        self.month_dropdown.current(datetime.now().month - 1)

        tk.Label(self.filter_frame, text="Select Year:", font=("Arial", 12), bg="#FFF4A3").grid(row=0, column=2, padx=5)
        self.year_var = tk.StringVar()
        self.year_dropdown = ttk.Combobox(self.filter_frame, textvariable=self.year_var, state="readonly",
                                          values=[str(y) for y in range(2020, datetime.now().year + 1)],
                                          width=7, font=("Arial", 12))
        self.year_dropdown.grid(row=0, column=3, padx=5)
        self.year_dropdown.set(str(datetime.now().year))

        tk.Button(self.filter_frame, text="Generate Summary", font=("Arial", 12, "bold"),
                  bg="#A4E4A0", command=self.generate_summary).grid(row=0, column=4, padx=10)

        self.result_box = tk.Text(self, width=60, height=15, font=("Courier New", 12), bg="#FFFFE0")
        self.result_box.pack(pady=15)

        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack()

        tk.Button(button_frame, text="Back", font=("Arial", 12, "bold"), width=12,
                  bg="#B0F2C2", fg="black", relief="ridge",
                  command=self.go_back).pack(pady=10)

    def generate_summary(self):
        try:
            month = int(self.month_var.get())
            year = int(self.year_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please select a valid month and year.")
            return

        # Restrict manager to current month only
        if self.user_role == "manager":
            now = datetime.now()
            if month != now.month or year != now.year:
                messagebox.showwarning(
                    "Access Denied",
                    "Managers are only allowed to view the current month's summary."
                )
                return

        try:
            summary = sql_connection.generate_summary_report(year, month)

            display_text = (
                f"Summary for {month:02}-{year}:\n\n"
                f"{'Net Profit:':<25}${summary['net_profit']:.2f}\n"
                f"{'Current Balance:':<25}${summary['current_balance']:.2f}\n"
                f"{'Withdrawals:':<25}${summary['withdrawals']:.2f}\n"
                f"{'Actual Cash:':<25}${summary['actual_cash']:.2f}\n"
                f"{'Actual Credit:':<25}${summary['actual_credit']:.2f}\n"
                f"{'Actual Total:':<25}${summary['actual_total']:.2f}\n"
                f"{'Sales Tax Report:':<25}${summary['sales_tax']:.2f}"
            )

            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, display_text)

        except Exception as e:
            print("Summary error:", e)
            messagebox.showerror("Error", "Failed to generate summary.")

    def go_back(self):
        if self.user_role == "manager":
            self.master.show_frame(screens.manager_view.ManagerView)
        else:
            self.master.show_frame(screens.owner_view.OwnerView)
