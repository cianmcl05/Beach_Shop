import tkinter as tk
from tkinter import ttk
import screens.welcome


class LoginScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")

        tk.Label(self, text="Welcome back", font=("Arial", 16, "bold"), bg="#FFF4A3", fg="black").pack(pady=10)

        self.create_label_entry("EmpID:")
        self.create_label_entry("Password:", show="*")

        tk.Label(self, text="Forgot User/Password?", font=("Arial", 10, "italic"),
                 fg="gray", bg="#FFF4A3", cursor="hand2").pack(anchor="w", padx=20, pady=5)

        tk.Label(self, text="Select Store", font=("Arial", 12, "bold"), bg="#FFF4A3").pack(anchor="w", padx=20, pady=(10, 0))
        store_dropdown = ttk.Combobox(self, values=["Store 1", "Store 2", "Store 3"], font=("Arial", 12))
        store_dropdown.pack(anchor="w", padx=20)
        store_dropdown.current(0)

        self.create_buttons(master, screens.welcome.WelcomeScreen, "Go")

    def create_label_entry(self, text, show=""):
        tk.Label(self, text=text, font=("Arial", 12), bg="#FFF4A3").pack(anchor="w", padx=20)
        tk.Entry(self, font=("Arial", 12), show=show).pack(anchor="w", padx=20)

    def create_buttons(self, master, back_screen, confirm_text):
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Back", font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#B0F2C2", fg="black", relief="ridge",
                  command=lambda: master.show_frame(back_screen)).pack(side="left", padx=10)

        tk.Button(button_frame, text=confirm_text, font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#EECFA3", fg="black", relief="ridge").pack(side="left", padx=10)
