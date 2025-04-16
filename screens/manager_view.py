import tkinter as tk
import screens.welcome
import screens.end_of_day  # Import EndOfDaySalesScreen
import screens.expenses  # Import Expenses Screen
import screens.bonus  # Import Bonus Screen
import screens.invoices
<<<<<<< Updated upstream
import screens.employee_table  # Import EmployeesScreen
import screens.merch  # Import MerchandiseInventoryScreen
import screens.payroll  # Import PayrollScreen

class ManagerView(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")
=======
import screens.employee_table
import screens.merch
import screens.payroll
import screens.store_management
import screens.summary
import os
from PIL import Image, ImageTk

class ManagerView(tk.Frame):
    def __init__(self, master, emp_id=None):
        super().__init__(master)
        self.emp_id = emp_id
>>>>>>> Stashed changes

        # Load and set background image
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "City-Highlight--Clearwater-ezgif.com-webp-to-jpg-converter.jpg")

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Background image not found at: {image_path}")

        bg_image = Image.open(image_path)
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)

        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title label
        tk.Label(self, text="Manager View", font=("Arial", 20, "bold"), bg="#D8D5F2", fg="black").pack(pady=10)

<<<<<<< Updated upstream
        # Buttons
        button_style = {"font": ("Arial", 12, "bold"), "width": 15, "height": 2, "bg": "#D8D5F2", "fg": "black",
                        "relief": "ridge"}

        # Buttons for manager actions
        buttons = [
            ("Employees", 50, 80),
            ("Merchandise", 50, 130),
            ("Pay", 50, 180),  # Now links to PayrollScreen
            ("End of Day Sales", 250, 80),
            ("Bonus", 250, 130),
            ("Invoices", 250, 180),
            ("Add Expense", 250, 230)
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
                          command=lambda: master.show_frame(screens.end_of_day.EndOfDaySalesScreen, user_role="manager")).place(x=x, y=y)
            elif text == "Add Expense":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.expenses.Expenses, user_role="manager")).place(x=x, y=y)
            elif text == "Pay":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.payroll.PayrollScreen, user_role="manager")).place(x=x, y=y)
            elif text == "Bonus":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.bonus.Bonus, user_role="manager")).place(x=x, y=y)
            else:
                tk.Button(self, text=text, **button_style).place(x=x, y=y)

        # Logout Button
        tk.Button(self, text="Log out", font=("Arial", 12, "bold"), width=12, height=1, bg="#B0F2C2", fg="black",
                  relief="ridge", command=lambda: master.show_frame(screens.welcome.WelcomeScreen)).place(x=150, y=280)
=======
        # White background button frame
        button_frame = tk.Frame(self, bg="white")
        button_frame.place(relx=0.5, rely=0.5, anchor="center", width=800, height=500)

        # Inner frame for grid layout
        inner_frame = tk.Frame(button_frame, bg="white")
        inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        button_style = {"font": ("Arial", 12, "bold"), "width": 20, "height": 2,
                        "bg": "#D8D5F2", "fg": "black", "relief": "ridge"}

        button_info = [
            ("Employees", lambda: master.show_frame(screens.employee_table.EmployeesScreen, user_role="manager")),
            ("Merchandise", lambda: master.show_frame(screens.merch.MerchandiseInventoryScreen, user_role="manager")),
            ("Pay", lambda: master.show_frame(screens.payroll.PayrollScreen, user_role="manager")),
            ("Manage Stores", lambda: master.show_frame(screens.store_management.StoreManagementScreen)),
            ("Summary", lambda: master.show_frame(screens.summary.SummaryScreen, user_role="manager")),
            ("End of Day Sales", lambda: master.show_frame(screens.end_of_day.EndOfDaySalesScreen, user_role="manager", emp_id=self.emp_id)),
            ("Bonus", lambda: master.show_frame(screens.bonus.Bonus, user_role="manager")),
            ("Invoices", lambda: master.show_frame(screens.invoices.InvoicesScreen, user_role="manager")),
            ("Add Expense", lambda: master.show_frame(screens.expenses.Expenses, user_role="manager", emp_id=self.emp_id)),
        ]

        row = 0
        col = 0
        for text, command in button_info:
            tk.Button(inner_frame, text=text, command=command, **button_style).grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            col += 1
            if col > 1:  # 2 buttons per row
                col = 0
                row += 1

        # Log out button at the bottom center
        tk.Button(self, text="Log out", font=("Arial", 12, "bold"), width=12, height=1,
                  bg="#B0F2C2", fg="black", relief="ridge",
                  command=lambda: master.show_frame(screens.welcome.WelcomeScreen)).place(relx=0.5, rely=0.75, anchor="center")

>>>>>>> Stashed changes
