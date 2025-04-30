import tkinter as tk
from PIL import Image, ImageTk
import os
import screens.welcome
import screens.end_of_day
import screens.expenses
import screens.bonus
import screens.invoices
import screens.employee_table
import screens.merch
import screens.payroll
import screens.withdraw
import screens.store_management
import screens.summary
import screens.employee_activity

class OwnerView(tk.Frame):
    def __init__(self, master, emp_id=None):
        super().__init__(master)
        self.emp_id = emp_id

        # Load background image (Beach image)
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

        # Background label to display the image
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title Label
        tk.Label(self, text="Owner View", font=("Arial", 20, "bold"), bg="#D8D5F2", fg="black").pack(pady=10)

        # Button style
        button_style = {"font": ("Arial", 12, "bold"), "width": 20, "height": 2,
                        "bg": "#D8D5F2", "fg": "black", "relief": "ridge"}

        # Create a frame for buttons (with white background to stand out from the image)
        button_frame = tk.Frame(self, bg="white")
        button_frame.place(relx=0.5, rely=0.4, anchor="center", width=600, height=400)

        # Inner frame to center buttons
        inner_frame = tk.Frame(button_frame, bg="white")
        inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        # List of buttons with associated actions
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
            ("Add Expense", screens.expenses.Expenses),
            ("Activity Log", screens.employee_activity.EmployeeActivityScreen),
        ]

        # Grid layout for buttons
        row = 0
        col = 0
        for text, screen in buttons:
            button = tk.Button(inner_frame, text=text, **button_style,
                               command=lambda screen=screen: master.show_frame(screen, user_role="owner"))
            button.grid(row=row, column=col, padx=10, pady=5, sticky="ew")

            col += 1
            if col > 1:  # After 2 buttons, move to the next row
                col = 0
                row += 1

        # Log out button, placed below the grid of buttons
        log_out_button = tk.Button(self, text="Log out", font=("Arial", 12, "bold"), width=12, height=1,
                                   bg="#B0F2C2", fg="black", relief="ridge",
                                   command=lambda: master.show_frame(screens.welcome.WelcomeScreen))
        log_out_button.place(relx=0.5, rely=0.8, anchor="center")



