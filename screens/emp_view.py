import tkinter as tk
import screens.welcome
import screens.end_of_day
import screens.expenses
import sql_connection
from tkinter import messagebox
from datetime import datetime


class EmployeeView(tk.Frame):
    def __init__(self, master, emp_id=None):
        super().__init__(master, bg="#FFF4A3")
        self.emp_id = emp_id
        self.clocked_in = False
        self.current_record_id = None

        tk.Label(self, text="Employee View", font=("Arial", 20, "bold"), bg="#D8D5F2", fg="black").pack(pady=10)

        # Buttons
        button_style = {
            "font": ("Arial", 12, "bold"), "width": 15, "height": 2,
            "bg": "#D8D5F2", "fg": "black", "relief": "ridge"
        }

        self.clock_button = tk.Button(self, text="Clock in", **button_style, command=self.toggle_clock)
        self.clock_button.place(x=30, y=60)

        # Now that clock_button exists, update its state based on latest clock data
        latest = sql_connection.get_latest_time_record(self.emp_id)
        if latest and latest["clock_in"].date() == datetime.now().date() and latest["clock_in"] == latest["clock_out"]:
            self.clocked_in = True
            self.current_record_id = latest["id"]
            self.clock_button.config(text="Clock out")
        else:
            self.clocked_in = False
            self.current_record_id = None
            self.clock_button.config(text="Clock in")

        tk.Button(self, text="End of Day Sales", **button_style,
                  command=lambda: master.show_frame(screens.end_of_day.EndOfDaySalesScreen, user_role="employee",
                                                    emp_id=self.emp_id)).place(x=30, y=120)

        tk.Button(self, text="Log Expenses", **button_style,
                  command=lambda: master.show_frame(screens.expenses.Expenses, user_role="employee",
                                                    emp_id=self.emp_id)).place(x=30, y=180)

        # Cash Register Entry
        label_style = {"font": ("Arial", 12, "bold"), "bg": "#FFF4A3", "fg": "black"}
        entry_style = {"font": ("Arial", 12), "width": 20}

        tk.Label(self, text="Reg $ in:", **label_style).place(x=230, y=70)
        self.reg_in_entry = tk.Entry(self, **entry_style)
        self.reg_in_entry.place(x=320, y=70, height=25)

        tk.Label(self, text="Reg $ out:", **label_style).place(x=230, y=110)
        self.reg_out_entry = tk.Entry(self, **entry_style)
        self.reg_out_entry.place(x=320, y=110, height=25)

        tk.Button(self, text="Log out", font=("Arial", 12, "bold"), width=12, height=1, bg="#B0F2C2", fg="black",
                  relief="ridge", command=lambda: master.show_frame(screens.welcome.WelcomeScreen)).place(x=30, y=340)

        tk.Button(self, text="Confirm", font=("Arial", 12, "bold"), width=12, height=1, bg="#B0F2C2", fg="black",
                  relief="ridge", command=self.confirm_register_amounts).place(x=320, y=145)

    def toggle_clock(self):
        if not self.clocked_in:
            store_id = getattr(self.master, "current_store_id", None)
            record_id = sql_connection.clock_in(self.emp_id, store_id)  # ✅ Include store
            if record_id:
                self.current_record_id = record_id
                self.clock_button.config(text="Clock out")
                self.clocked_in = True
            else:
                messagebox.showinfo("Clock In", "You have already clocked out for the day.")
        else:
            confirm = messagebox.askyesno("Confirm Clock Out", "Are you sure you want to clock out?")
            if confirm and self.current_record_id:
                sql_connection.clock_out(self.current_record_id)
                self.clock_button.config(text="Clock in")
                self.clocked_in = False
                self.current_record_id = None

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

