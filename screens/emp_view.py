import tkinter as tk
import screens.welcome
import screens.end_of_day
import screens.expenses


class EmployeeView(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")

        tk.Label(self, text="Employee View", font=("Arial", 20, "bold"), bg="#D8D5F2", fg="black").pack(pady=10)

        # Button styles
        button_style = {"font": ("Arial", 12, "bold"), "width": 15, "height": 2, "bg": "#D8D5F2", "fg": "black",
                        "relief": "ridge"}

        # Clock In/Out Button with toggle
        self.clocked_in = False
        self.clock_button = tk.Button(self, text="Clock In", **button_style, command=self.toggle_clock)
        self.clock_button.place(x=30, y=60)

        # End of Day Sales Button
        tk.Button(self, text="End of Day Sales", **button_style,
                  command=lambda: master.show_frame(screens.end_of_day.EndOfDaySalesScreen, user_role="employee")).place(x=30, y=120)

        # Log Expenses Button
        tk.Button(self, text="Log Expenses", **button_style,
                  command=lambda: master.show_frame(screens.expenses.Expenses, user_role="employee")).place(x=30, y=180)

        # Labels and Entry fields
        label_style = {"font": ("Arial", 12, "bold"), "bg": "#FFF4A3", "fg": "black"}
        entry_style = {"font": ("Arial", 12), "width": 20}

        tk.Label(self, text="Reg $ in:", **label_style).place(x=230, y=70)
        tk.Entry(self, **entry_style).place(x=320, y=70, height=25)

        tk.Label(self, text="Reg $ out:", **label_style).place(x=230, y=130)
        tk.Entry(self, **entry_style).place(x=320, y=130, height=25)

        # Logout Button
        tk.Button(self, text="Log out", font=("Arial", 12, "bold"), width=12, height=1, bg="#B0F2C2", fg="black",
                  relief="ridge", command=lambda: master.show_frame(screens.welcome.WelcomeScreen)).place(x=30, y=340)

    def toggle_clock(self):
        self.clocked_in = not self.clocked_in
        new_text = "Clock Out" if self.clocked_in else "Clock In"
        self.clock_button.config(text=new_text)
