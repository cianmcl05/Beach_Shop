import tkinter as tk
import screens.welcome
import screens.end_of_day


class EmployeeView(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")

        tk.Label(self, text="Employee View", font=("Arial", 20, "bold"), bg="#D8D5F2", fg="black").pack(pady=10)

        # Buttons
        button_style = {"font": ("Arial", 12, "bold"), "width": 15, "height": 2, "bg": "#D8D5F2", "fg": "black",
                        "relief": "ridge"}

        tk.Button(self, text="Clock in/out", **button_style).place(x=30, y=60)
        tk.Button(self, text="End of Day Sales", **button_style,
                  command=lambda: master.show_frame(screens.end_of_day.EndOfDaySalesScreen)).place(x=30, y=120)
        tk.Button(self, text="Log\nExpenses", **button_style).place(x=30, y=180)

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


