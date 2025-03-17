import tkinter as tk
from tkinter import ttk
import screens.welcome
import sql_connection  # Import your database functions


class SignUpScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")

        tk.Label(self, text="Create Account", font=("Arial", 16, "bold"), bg="#FFF4A3", fg="black").pack(pady=10)

        self.entries = {}  # Store user inputs

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

    def create_label_entry(self, label_text, show=""):
        """Create labeled entry fields."""
        frame = tk.Frame(self, bg="#FFF4A3")
        frame.pack(anchor="w", padx=20, pady=2)

        tk.Label(frame, text=label_text, font=("Arial", 12), bg="#FFF4A3").pack(side="left")
        entry = tk.Entry(frame, font=("Arial", 12), show=show)
        entry.pack(side="left", padx=10)
        self.entries[label_text] = entry  # Store entry field reference

    def create_buttons(self, master, back_screen, confirm_text):
        """Create Back and Sign Up buttons."""
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Back", font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#B0F2C2", fg="black", relief="ridge",
                  command=lambda: master.show_frame(back_screen)).pack(side="left", padx=10)

        tk.Button(button_frame, text=confirm_text, font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#EECFA3", fg="black", relief="ridge",
                  command=self.validate_manager_key).pack(side="left", padx=10)

    def toggle_manager_key(self, event):
        if self.role_var.get() == "Manager":
            self.manager_key_label.grid(row=0, column=2, padx=10)
            self.manager_key_entry.grid(row=0, column=3, padx=10)
        else:
            self.manager_key_label.grid_forget()
            self.manager_key_entry.grid_forget()

    def validate_manager_key(self):
        """Validate the manager key."""
        # If the role is 'Manager', check if the manager key matches 'chungus'
        if self.role_var.get() == "Manager":
            manager_key = self.manager_key_entry.get()
            if manager_key != "chungus":
                tk.messagebox.showerror("Error", "Invalid Manager Key!")
                return  # Don't proceed with signup if key is incorrect

        self.register_user()

    def register_user(self):
        """Collect user input and insert into the database."""
        first_name = self.entries["First Name:"].get()
        last_name = self.entries["Last Name:"].get()
        phone = self.entries["Phone Number:"].get()
        email = self.entries["Email:"].get()
        password = self.entries["Password:"].get()
        confirm_password = self.entries["Confirm Password:"].get()
        role = self.role_var.get()
        manager_key = self.manager_key_entry.get() if role == "Manager" else ""

        if password != confirm_password:
            print("Passwords do not match!")
            return

        sql_connection.insert_user(first_name, last_name, phone, email, password, role)
