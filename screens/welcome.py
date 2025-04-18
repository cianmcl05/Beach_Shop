import tkinter as tk
import screens.signup
import screens.login


# basic welcome screen
class WelcomeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")

        tk.Label(self, text="Welcome", font=("Arial", 20, "bold"), bg="#FFF4A3", fg="black").pack(pady=40)

        # button for sign up screen
        tk.Button(self, text="Sign up", font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#B0F2C2", fg="black", relief="ridge",
                  command=lambda: master.show_frame(screens.signup.SignUpScreen)).place(x=150, y=180)

        # button for login screen
        tk.Button(self, text="Login", font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#EECFA3", fg="black", relief="ridge",
                  command=lambda: master.show_frame(screens.login.LoginScreen)).place(x=280, y=180)
