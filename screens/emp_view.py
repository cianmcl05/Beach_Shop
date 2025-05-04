import tkinter as tk
from tkinter import messagebox
import screens.welcome
import screens.end_of_day
import screens.expenses
import sql_connection
from datetime import datetime
from PIL import Image, ImageTk
import os

class EmployeeView(tk.Frame):
    """
    Main interface for store employees: clock in/out, register cash entries, and quick navigation.
    """
    def __init__(self, master, emp_id=None):
        super().__init__(master)
        # Store identification for attendance and register updates
        self.emp_id = emp_id
        self.store_id = getattr(master, "current_store_id", None)
        self.clocked_in = False
        self.current_record_id = None

        # Configure background
        self.config(bg="white")

        # Load and display a full-screen background image
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "City-Highlight--Clearwater-ezgif.com-webp-to-jpg-converter.jpg")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Background image not found: {image_path}")

        bg_image = Image.open(image_path)
        screen_w, screen_h = master.winfo_screenwidth(), master.winfo_screenheight()
        bg_image = bg_image.resize((screen_w, screen_h), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)
        tk.Label(self, image=self.bg_image).place(x=0, y=0, relwidth=1, relheight=1)

        # Display current store name at the top
        store_name = sql_connection.get_store_name_by_id(self.store_id)
        tk.Label(
            self,
            text=store_name,
            font=("Arial", 20, "bold"),
            bg="#D8D5F2",
            fg="black"
        ).pack(pady=10)

        # Container for the main action buttons
        button_frame = tk.Frame(self, bg="white")
        button_frame.place(relx=0.5, rely=0.4, anchor="center", width=800, height=500)
        inner_frame = tk.Frame(button_frame, bg="white")
        inner_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Standard style for all buttons
        button_style = {
            "font": ("Arial", 12, "bold"),
            "width": 20,
            "height": 2,
            "bg": "#D8D5F2",
            "fg": "black",
            "relief": "ridge"
        }

        # Clock in/out button toggles attendance state
        self.clock_button = tk.Button(
            inner_frame,
            text="Clock in / Clock out",
            **button_style,
            command=self.toggle_clock
        )
        self.clock_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Other feature buttons: End-of-day sales, expense logging, and register confirmation
        features = [
            ("End of Day Sales",
             lambda: master.show_frame(
                 screens.end_of_day.EndOfDaySalesScreen,
                 user_role="employee",
                 emp_id=self.emp_id
             )
            ),
            ("Log Expenses",
             lambda: master.show_frame(
                 screens.expenses.Expenses,
                 user_role="employee",
                 emp_id=self.emp_id
             )
            ),
            ("Confirm Register Amounts", self.confirm_register_amounts)
        ]

        # Layout the feature buttons to the right of the clock button
        row, col = 0, 1
        for text, cmd in features:
            btn = tk.Button(inner_frame, text=text, **button_style, command=cmd)
            btn.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            col += 1
            if col > 1:
                col = 0
                row += 1

        # Input fields for opening and closing register cash amounts
        label_style = {"font": ("Arial", 12, "bold"), "bg": "#FFF4A3", "fg": "black"}
        entry_style = {"font": ("Arial", 12), "width": 20}

        # "Reg $ in" field
        tk.Label(inner_frame, text="Reg $ in:", **label_style)\
          .grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        self.reg_in_entry = tk.Entry(inner_frame, **entry_style)
        self.reg_in_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")

        # "Reg $ out" field below
        row += 1
        tk.Label(inner_frame, text="Reg $ out:", **label_style)\
          .grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        self.reg_out_entry = tk.Entry(inner_frame, **entry_style)
        self.reg_out_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")

        # Log out button at the bottom, outside the white box
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
        ).place(relx=0.5, rely=0.80, anchor="center")

    def toggle_clock(self):
        """
        Clock the employee in or out by creating/updating a time record in the database.
        """
        if not self.clocked_in:
            # Clock in: insert new record and switch button text
            record_id = sql_connection.clock_in(self.emp_id, self.store_id)
            if record_id:
                self.current_record_id = record_id
                self.clock_button.config(text="Clock out")
                self.clocked_in = True
        else:
            # Clock out: finalize existing record and reset state
            if self.current_record_id:
                sql_connection.clock_out(self.current_record_id)
                self.clock_button.config(text="Clock in")
                self.clocked_in = False
                self.current_record_id = None

    def confirm_register_amounts(self):
        """
        Save the "Reg $ in" and "Reg $ out" values to the active clock record.
        """
        try:
            # Parse the cash input fields
            reg_in = float(self.reg_in_entry.get() or 0.00)
            reg_out = float(self.reg_out_entry.get() or 0.00)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid decimal numbers for register in and out."
            )
            return

        # Must be clocked in to update register amounts
        if not self.current_record_id:
            messagebox.showwarning(
                "Not Clocked In",
                "You need to be clocked in to save register amounts."
            )
            return

        # Write to database and notify user
        success = sql_connection.update_register_amounts(
            self.current_record_id, reg_in, reg_out
        )
        if success:
            messagebox.showinfo("Success", "Register amounts saved.")
        else:
            messagebox.showerror("Error", "Failed to update register amounts.")
