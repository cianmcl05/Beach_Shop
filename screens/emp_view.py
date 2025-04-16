import tkinter as tk
import screens.welcome
import screens.end_of_day
import screens.expenses
import sql_connection  # Make sure this is imported
from datetime import datetime
from PIL import Image, ImageTk
import os

class EmployeeView(tk.Frame):
    def __init__(self, master, emp_id=None):
        super().__init__(master)
        self.emp_id = emp_id
        self.clocked_in = False
        self.current_record_id = None

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

        # Employee View title
        tk.Label(self, text="Employee View", font=("Arial", 20, "bold"), bg="#D8D5F2", fg="black").pack(pady=10)

<<<<<<< Updated upstream
        # Buttons
        button_style = {"font": ("Arial", 12, "bold"), "width": 15, "height": 2, "bg": "#D8D5F2", "fg": "black",
                        "relief": "ridge"}
=======
        # Create a frame for buttons (white background)
        button_frame = tk.Frame(self, bg="white")
        button_frame.place(relx=0.5, rely=0.4, anchor="center", width=800, height=500)  # Increased size
>>>>>>> Stashed changes

        # Inner frame to center buttons vertically and horizontally
        inner_frame = tk.Frame(button_frame, bg="white")
        inner_frame.place(relx=0.5, rely=0.5, anchor="center")

<<<<<<< Updated upstream
        tk.Button(self, text="End of Day Sales", **button_style,
                  command=lambda: master.show_frame(screens.end_of_day.EndOfDaySalesScreen, user_role="employee")).place(x=30, y=120)

        tk.Button(self, text="Log Expenses", **button_style,
                  command=lambda: master.show_frame(screens.expenses.Expenses, user_role="employee")).place(x=30, y=180)
=======
        button_style = {"font": ("Arial", 12, "bold"), "width": 20, "height": 2,
                        "bg": "#D8D5F2", "fg": "black", "relief": "ridge"}

        # Buttons list with grid layout
        buttons = [
            ("Clock in / Clock out", self.toggle_clock),
            ("End of Day Sales", lambda: master.show_frame(screens.end_of_day.EndOfDaySalesScreen, user_role="employee", emp_id=self.emp_id)),
            ("Log Expenses", lambda: master.show_frame(screens.expenses.Expenses, user_role="employee", emp_id=self.emp_id)),
            ("Confirm Register Amounts", self.confirm_register_amounts)
        ]

        # Use grid to create a grid layout for buttons inside the inner_frame
        row = 0
        col = 0
        for text, command in buttons:
            button = tk.Button(inner_frame, text=text, **button_style, command=command)
            button.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
>>>>>>> Stashed changes

            col += 1
            if col > 1:  # After 2 buttons, move to next row
                col = 0
                row += 1

        # Register Amount Inputs inside the grid layout
        label_style = {"font": ("Arial", 12, "bold"), "bg": "#FFF4A3", "fg": "black"}
        entry_style = {"font": ("Arial", 12), "width": 20}

<<<<<<< Updated upstream
        tk.Label(self, text="Reg $ in:", **label_style).place(x=230, y=70)
        tk.Entry(self, **entry_style).place(x=320, y=70, height=25)

        tk.Label(self, text="Reg $ out:", **label_style).place(x=230, y=130)
        tk.Entry(self, **entry_style).place(x=320, y=130, height=25)

        tk.Button(self, text="Log out", font=("Arial", 12, "bold"), width=12, height=1, bg="#B0F2C2", fg="black",
                  relief="ridge", command=lambda: master.show_frame(screens.welcome.WelcomeScreen)).place(x=30, y=340)
=======
        tk.Label(inner_frame, text="Reg $ in:", **label_style).grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        self.reg_in_entry = tk.Entry(inner_frame, **entry_style)
        self.reg_in_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")

        row += 1  # Move to the next row
        tk.Label(inner_frame, text="Reg $ out:", **label_style).grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        self.reg_out_entry = tk.Entry(inner_frame, **entry_style)
        self.reg_out_entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")

        # Log out button, placed below the buttons grid
        log_out_button = tk.Button(self, text="Log out", font=("Arial", 12, "bold"), width=12, height=1,
                                   bg="#B0F2C2", fg="black", relief="ridge",
                                   command=lambda: master.show_frame(screens.welcome.WelcomeScreen))
        log_out_button.place(relx=0.5, rely=0.60, anchor="center")
>>>>>>> Stashed changes

    def toggle_clock(self):
        if not self.clocked_in:
            # Clock in
            record_id = sql_connection.clock_in(self.emp_id)
            if record_id:
                self.current_record_id = record_id
                self.clock_button.config(text="Clock out")
                self.clocked_in = True
        else:
            # Clock out
            if self.current_record_id:
                sql_connection.clock_out(self.current_record_id)
                self.clock_button.config(text="Clock in")
                self.clocked_in = False
                self.current_record_id = None
<<<<<<< Updated upstream
=======

    def confirm_register_amounts(self):
        try:
            reg_in_str = self.reg_in_entry.get()
            reg_out_str = self.reg_out_entry.get()

            reg_in = float(reg_in_str) if reg_in_str else 0.00
            reg_out = float(reg_out_str) if reg_out_str else 0.00
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid decimal numbers for register in and out.")
            return

        if not self.current_record_id:
            messagebox.showwarning("Not Clocked In", "You need to be clocked in to save register amounts.")
            return

        success = sql_connection.update_register_amounts(self.current_record_id, reg_in, reg_out)
        if success:
            messagebox.showinfo("Success", "Register amounts saved.")
        else:
            messagebox.showerror("Error", "Failed to update register amounts.")



>>>>>>> Stashed changes
