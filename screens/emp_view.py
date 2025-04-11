import tkinter as tk
import screens.welcome
import screens.end_of_day
import screens.expenses
import sql_connection  # Make sure this is imported
from datetime import datetime


class EmployeeView(tk.Frame):
    def __init__(self, master, emp_id=None):
        super().__init__(master, bg="#FFF4A3")
        self.emp_id = emp_id
        self.clocked_in = False
        self.current_record_id = None

        tk.Label(self, text="Employee View", font=("Arial", 20, "bold"), bg="#D8D5F2", fg="black").pack(pady=10)

        # Buttons
        button_style = {"font": ("Arial", 12, "bold"), "width": 15, "height": 2, "bg": "#D8D5F2", "fg": "black",
                        "relief": "ridge"}

        self.clock_button = tk.Button(self, text="Clock in", **button_style, command=self.toggle_clock)
        self.clock_button.place(x=30, y=60)

        tk.Button(self, text="End of Day Sales", **button_style,
                  command=lambda: master.show_frame(screens.end_of_day.EndOfDaySalesScreen, user_role="employee")).place(x=30, y=120)

        tk.Button(self, text="Log Expenses", **button_style,
                  command=lambda: master.show_frame(screens.expenses.Expenses, user_role="employee")).place(x=30, y=180)

        # Cash Register Entry
        label_style = {"font": ("Arial", 12, "bold"), "bg": "#FFF4A3", "fg": "black"}
        entry_style = {"font": ("Arial", 12), "width": 20}

        tk.Label(self, text="Reg $ in:", **label_style).place(x=230, y=70)
        tk.Entry(self, **entry_style).place(x=320, y=70, height=25)

        tk.Label(self, text="Reg $ out:", **label_style).place(x=230, y=130)
        tk.Entry(self, **entry_style).place(x=320, y=130, height=25)

        tk.Button(self, text="Log out", font=("Arial", 12, "bold"), width=12, height=1, bg="#B0F2C2", fg="black",
                  relief="ridge", command=lambda: master.show_frame(screens.welcome.WelcomeScreen)).place(x=30, y=340)

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
