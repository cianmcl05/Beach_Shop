import tkinter as tk
import screens.welcome
'''import screens.employees
import screens.merchandise
import screens.pay
import screens.sales
import screens.bonus
import screens.invoices'''

class OwnerView(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")

        tk.Label(self, text="Manager View", font=("Arial", 20, "bold"), bg="#D8D5F2", fg="black").pack(pady=10)

        # Buttons
        button_style = {"font": ("Arial", 12, "bold"), "width": 15, "height": 2, "bg": "#D8D5F2", "fg": "black",
                        "relief": "ridge"}


        # Buttons for owner actions
        buttons = [
            ("Employees", 50, 80),
            ("Merchandise", 50, 130),
            ("Pay", 50, 180),
            ("End of Day Sales", 250, 80),
            ("Bonus", 250, 130),
            ("Invoices", 250, 180)
        ]

        for text, x, y in buttons:
            tk.Button(self, text=text, **button_style).place(x=x, y=y)

        # Logout Button
        tk.Button(self, text="Log out", font=("Arial", 12, "bold"), width=12, height=1, bg="#B0F2C2", fg="black",
                  relief="ridge", command=lambda: master.show_frame(screens.welcome.WelcomeScreen)).place(x=150, y=260)
