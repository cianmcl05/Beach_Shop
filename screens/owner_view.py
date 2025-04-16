import tkinter as tk
from PIL import Image, ImageTk
import os
import screens.welcome
import screens.end_of_day  # Import EndOfDaySalesScreen
import screens.expenses  # Import Expenses Screen
import screens.bonus  # Import Bonus Screen
import screens.invoices
import screens.employee_table  # Import EmployeesScreen
import screens.merch  # Import MerchandiseInventoryScreen
import screens.payroll  # Import PayrollScreen
import screens.withdraw

class OwnerView(tk.Frame):
<<<<<<< Updated upstream
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")
=======
    def __init__(self, master, emp_id=None):
        super().__init__(master)
        self.emp_id = emp_id
>>>>>>> Stashed changes

        # Set white background for the frame
        self.config(bg="white")

        # Load background image and resize it to fit
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "City-Highlight--Clearwater-ezgif.com-webp-to-jpg-converter.jpg")

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Background image not found at: {image_path}")

        bg_image = Image.open(image_path)
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Resize background image to cover the screen
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)

        # Background label
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Owner View title
        tk.Label(self, text="Owner View", font=("Arial", 20, "bold"), bg="#D8D5F2", fg="black").pack(pady=10)

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
            ("Add Expense", 250, 230),
            ("Withdraw", 50, 230)
        ]

        for text, x, y in buttons:
            if text == "Employees":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.employee_table.EmployeesScreen, user_role="owner")).place(x=x, y=y)
            elif text == "Merchandise":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.merch.MerchandiseInventoryScreen, user_role="owner")).place(x=x, y=y)
            elif text == "Invoices":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.invoices.InvoicesScreen, user_role="owner")).place(x=x, y=y)
            elif text == "End of Day Sales":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.end_of_day.EndOfDaySalesScreen, user_role="owner")).place(x=x, y=y)
            elif text == "Add Expense":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.expenses.Expenses, user_role="owner")).place(x=x, y=y)
            elif text == "Pay":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.payroll.PayrollScreen, user_role="owner")).place(x=x, y=y)
            elif text == "Bonus":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.bonus.Bonus, user_role="owner")).place(x=x, y=y)
            elif text == "Withdraw":
                tk.Button(self, text=text, **button_style,
                          command=lambda: master.show_frame(screens.withdraw.Withdraw)).place(x=x, y=y)
            else:
                tk.Button(self, text=text, **button_style).place(x=x, y=y)

        # Logout Button
        tk.Button(self, text="Log out", font=("Arial", 12, "bold"), width=12, height=1, bg="#B0F2C2", fg="black",
                  relief="ridge", command=lambda: master.show_frame(screens.welcome.WelcomeScreen)).place(x=150, y=280)
=======
        # Create a frame for buttons (white background)
        button_frame = tk.Frame(self, bg="white")
        button_frame.place(relx=0.5, rely=0.4, anchor="center", width=600, height=400)  # Increased size

        # Inner frame to center buttons vertically and horizontally
        inner_frame = tk.Frame(button_frame, bg="white")
        inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        button_style = {"font": ("Arial", 12, "bold"), "width": 20, "height": 2,
                        "bg": "#D8D5F2", "fg": "black", "relief": "ridge"}

        # Buttons list with grid layout
        buttons = [
            ("Employees", screens.employee_table.EmployeesScreen),
            ("Merchandise", screens.merch.MerchandiseInventoryScreen),
            ("Pay", screens.payroll.PayrollScreen),
            ("Manage Stores", screens.store_management.StoreManagementScreen),
            ("Withdraw", screens.withdraw.Withdraw),
            ("Summary", screens.summary.SummaryScreen),
            ("End of Day Sales", screens.end_of_day.EndOfDaySalesScreen),
            ("Bonus", screens.bonus.Bonus),
            ("Invoices", screens.invoices.InvoicesScreen),
            ("Add Expense", screens.expenses.Expenses)
        ]

        # Use grid to create a grid layout for buttons inside the inner_frame
        row = 0
        col = 0
        for text, screen in buttons:
            button = tk.Button(inner_frame, text=text, **button_style,
                               command=lambda screen=screen: master.show_frame(screen, user_role="owner"))
            button.grid(row=row, column=col, padx=10, pady=5, sticky="ew")

            col += 1
            if col > 1:  # After 2 buttons, move to next row
                col = 0
                row += 1

        # Log out button, placed below the buttons grid
        log_out_button = tk.Button(self, text="Log out", font=("Arial", 12, "bold"), width=12, height=1,
                                   bg="#B0F2C2", fg="black", relief="ridge",
                                   command=lambda: master.show_frame(screens.welcome.WelcomeScreen))
        log_out_button.place(relx=0.5, rely=0.62, anchor="center")









>>>>>>> Stashed changes
