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
import sql_connection

class OwnerView(tk.Frame):
    """
    Dashboard for store owners. Displays a full-screen background image,
    current store name, a grid of navigation buttons for various screens,
    and a logout button.
    """
    def __init__(self, master, emp_id=None):
        super().__init__(master)
        self.emp_id = emp_id
        # Get current store ID from the main application context
        self.store_id = getattr(master, "current_store_id", None)

        # Load and validate background image path
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(
            base_dir,
            "City-Highlight--Clearwater-ezgif.com-webp-to-jpg-converter.jpg"
        )
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Background image not found at: {image_path}")

        # Open and resize image to fill entire screen
        bg_image = Image.open(image_path)
        screen_w = master.winfo_screenwidth()
        screen_h = master.winfo_screenheight()
        bg_image = bg_image.resize((screen_w, screen_h), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)

        # Place the background image behind all other widgets
        self.bg_label = tk.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Display the store name at the top
        store_name = sql_connection.get_store_name_by_id(self.store_id)
        tk.Label(
            self,
            text=store_name,
            font=("Arial", 20, "bold"),
            bg="#D8D5F2",
            fg="black"
        ).pack(pady=10)

        # Common style for all navigation buttons
        button_style = {
            "font": ("Arial", 12, "bold"),
            "width": 20,
            "height": 2,
            "bg": "#D8D5F2",
            "fg": "black",
            "relief": "ridge"
        }

        # Container frame with white background for button grid
        button_frame = tk.Frame(self, bg="white")
        button_frame.place(relx=0.5, rely=0.4, anchor="center", width=600, height=400)

        # Inner frame to center the grid layout of buttons
        inner_frame = tk.Frame(button_frame, bg="white")
        inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Define (label, FrameClass) pairs for each feature
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

        # Place buttons in a two-column grid
        row, col = 0, 0
        for text, ScreenClass in buttons:
            tk.Button(
                inner_frame,
                text=text,
                command=lambda cls=ScreenClass: master.show_frame(cls, user_role="owner"),
                **button_style
            ).grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            # Advance to next grid position
            col += 1
            if col > 1:
                col = 0
                row += 1

        # Logout button placed below the white frame
        tk.Button(
            self,
            text="Log out",
            font=("Arial", 12, "bold"),
            width=12,
            height=1,
            bg="#B0F2C2",
            fg="black",
            relief="ridge",
            command=lambda: master.show_frame(screens.welcome.WelcomeScreen)
        ).place(relx=0.5, rely=0.8, anchor="center")
