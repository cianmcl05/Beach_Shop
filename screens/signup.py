import tkinter as tk
from tkinter import ttk
import screens.welcome


class SignUpScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")

        tk.Label(self, text="Create Account", font=("Arial", 16, "bold"), bg="#FFF4A3", fg="black").pack(pady=10)

        role_frame = tk.Frame(self, bg="#FFF4A3")
        role_frame.pack(anchor="w", padx=20, pady=5)

        tk.Label(role_frame, text="Role:", font=("Arial", 12), bg="#FFF4A3").grid(row=0, column=0, padx=5)
        self.role_var = tk.StringVar()
        role_dropdown = ttk.Combobox(role_frame, values=["Employee", "Manager"], font=("Arial", 12), textvariable=self.role_var)
        role_dropdown.grid(row=0, column=1, padx=5)
        role_dropdown.current(0)
        role_dropdown.bind("<<ComboboxSelected>>", self.toggle_manager_key)

        self.manager_key_label = tk.Label(role_frame, text="Manager Key:", font=("Arial", 12), bg="#FFF4A3")
        self.manager_key_entry = tk.Entry(role_frame, font=("Arial", 12), show="*")

        self.create_label_entry("First Name:")
        self.create_label_entry("Last Name:")
        self.create_label_entry("Phone Number:")
        self.create_label_entry("Email:")
        self.create_label_entry("Password:", show="*")
        self.create_label_entry("Confirm Password:", show="*")

        self.create_buttons(master, screens.welcome.WelcomeScreen, "Sign Up")

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

    def toggle_manager_key(self, event):
        if self.role_var.get() == "Manager":
            self.manager_key_label.grid(row=0, column=2, padx=10)
            self.manager_key_entry.grid(row=0, column=3, padx=10)
        else:
            self.manager_key_label.grid_forget()
            self.manager_key_entry.grid_forget()
