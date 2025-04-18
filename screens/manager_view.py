import tkinter as tk
import screens.welcome
import screens.end_of_day
import screens.expenses
import screens.bonus
import screens.invoices
import screens.employee_table
import screens.merch
import screens.payroll
import screens.store_management
import screens.summary
import screens.employee_activity

class ManagerView(tk.Frame):
    def __init__(self, master, emp_id=None):
        super().__init__(master, bg="#FFF4A3")
        self.emp_id = emp_id

        tk.Label(self, text="Manager View", font=("Arial", 20, "bold"), bg="#D8D5F2", fg="black").pack(pady=10)

        button_style = {"font": ("Arial", 12, "bold"), "width": 15, "height": 2,
                        "bg": "#D8D5F2", "fg": "black", "relief": "ridge"}

        buttons = [
            ("Employees", 50, 80),
            ("Merchandise", 50, 130),
            ("Pay", 50, 180),
            ("Manage Stores", 50, 230),
            ("Summary", 50, 280),
            ("End of Day Sales", 250, 80),
            ("Bonus", 250, 130),
            ("Invoices", 250, 180),
            ("Add Expense", 250, 230),
            ("Activity Log", 250, 280),

        ]

        for text, x, y in buttons:
            if text == "Employees":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.employee_table.EmployeesScreen, user_role="manager")).place(x=x, y=y)
            elif text == "Merchandise":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.merch.MerchandiseInventoryScreen, user_role="manager")).place(x=x, y=y)
            elif text == "Invoices":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.invoices.InvoicesScreen, user_role="manager")).place(x=x, y=y)
            elif text == "End of Day Sales":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.end_of_day.EndOfDaySalesScreen, user_role="manager", emp_id=self.emp_id)).place(x=x, y=y)
            elif text == "Add Expense":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.expenses.Expenses, user_role="manager", emp_id=self.emp_id)).place(x=x, y=y)
            elif text == "Pay":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.payroll.PayrollScreen, user_role="manager")).place(x=x, y=y)
            elif text == "Bonus":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.bonus.Bonus, user_role="manager")).place(x=x, y=y)
            elif text == "Manage Stores":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.store_management.StoreManagementScreen)).place(x=x, y=y)
            elif text == "Summary":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.summary.SummaryScreen, user_role="manager")).place(x=x, y=y)
            elif text == "Activity Log":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.employee_activity.EmployeeActivityScreen,
                                                            user_role="manager")).place(x=x, y=y)

        tk.Button(self, text="Log out", font=("Arial", 12, "bold"), width=12, height=1,
                  bg="#B0F2C2", fg="black", relief="ridge",
                  command=lambda: master.show_frame(screens.welcome.WelcomeScreen)).place(x=150, y=330)
