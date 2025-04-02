import tkinter as tk
from tkinter import ttk, messagebox
import screens.welcome
import screens.emp_view
import screens.manager_view
import screens.owner_view
import sql_connection
#for password hashing
import hashlib
#for email validation
import re


class SignUpScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")

        tk.Label(self, text="Create Account", font=("Arial", 16, "bold"), bg="#FFF4A3", fg="black").pack(pady=10)
        # Store user inputs
        self.entries = {}

        role_frame = tk.Frame(self, bg="#FFF4A3")
        role_frame.pack(anchor="w", padx=20, pady=5)

        tk.Label(role_frame, text="Role:", font=("Arial", 12), bg="#FFF4A3").grid(row=0, column=0, padx=5)
        self.role_var = tk.StringVar()
        role_dropdown = ttk.Combobox(role_frame, values=["Employee", "Manager", "Owner"], font=("Arial", 12), textvariable=self.role_var)
        role_dropdown.grid(row=0, column=1, padx=5)
        role_dropdown.current(0)
        role_dropdown.bind("<<ComboboxSelected>>", self.toggle_role_keys)

        self.manager_key_label = tk.Label(role_frame, text="Manager Key:", font=("Arial", 12), bg="#FFF4A3")
        self.manager_key_entry = tk.Entry(role_frame, font=("Arial", 12), show="*")

        self.owner_key_label = tk.Label(role_frame, text="Owner Key:", font=("Arial", 12), bg="#FFF4A3")
        self.owner_key_entry = tk.Entry(role_frame, font=("Arial", 12), show="*")

        self.create_label_entry("First Name:")
        self.create_label_entry("Last Name:")
        self.create_label_entry("Phone Number:")
        self.create_label_entry("Email:")
        self.create_label_entry("Password:", show="*")
        self.create_label_entry("Confirm Password:", show="*")

        self.create_buttons(master, screens.welcome.WelcomeScreen, "Sign Up")

    # create input fields
    def create_label_entry(self, label_text, show=""):
        frame = tk.Frame(self, bg="#FFF4A3")
        frame.pack(anchor="w", padx=20, pady=2)

        tk.Label(frame, text=label_text, font=("Arial", 12), bg="#FFF4A3").pack(side="left")
        entry = tk.Entry(frame, font=("Arial", 12), show=show)
        entry.pack(side="left", padx=10)
        self.entries[label_text] = entry  # Store entry field reference

    # back and sign up buttons
    def create_buttons(self, master, back_screen, confirm_text):
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Back", font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#B0F2C2", fg="black", relief="ridge",
                  command=lambda: master.show_frame(back_screen)).pack(side="left", padx=10)

        tk.Button(button_frame, text=confirm_text, font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#EECFA3", fg="black", relief="ridge",
                  command=self.validate_role_keys).pack(side="left", padx=10)

    # used if you are a manager or owner
    def toggle_role_keys(self, event):
        if self.role_var.get() == "Manager":
            self.manager_key_label.grid(row=0, column=2, padx=10)
            self.manager_key_entry.grid(row=0, column=3, padx=10)
            self.owner_key_label.grid_forget()
            self.owner_key_entry.grid_forget()
        elif self.role_var.get() == "Owner":
            self.manager_key_label.grid_forget()
            self.manager_key_entry.grid_forget()
            self.owner_key_label.grid(row=0, column=2, padx=10)
            self.owner_key_entry.grid(row=0, column=3, padx=10)
        else:
            self.manager_key_label.grid_forget()
            self.manager_key_entry.grid_forget()
            self.owner_key_label.grid_forget()
            self.owner_key_entry.grid_forget()

    # checks to see if the key is correct
    def validate_role_keys(self):
        role = self.role_var.get()

        if role == "Manager":
            manager_key = self.manager_key_entry.get()
            if manager_key != "manager":
                messagebox.showerror("Error", "Invalid Manager Key!")
                return
        elif role == "Owner":
            owner_key = self.owner_key_entry.get()
            if owner_key != "owner":
                messagebox.showerror("Error", "Invalid Owner Key!")
                return

        self.register_user()


    #validation functions to ensure clean signups
    #ensures theres an @ symbol in email
    def valid_email(self, email):
        return "@" in email and re.match(r"[^@]+@[^@]+\.[^@]+", email)
    #ensures correct amount of phone digits
    def valid_phone(self, phone):
        return phone.isdigit() and 10 <= len(phone) <= 15
    #ensures passwords are more than or equal to 8 for security purposes
    def valid_password(self, password):
        return len(password) >= 8

    # puts information into database
    def register_user(self):
        first_name = self.entries["First Name:"].get().strip()
        last_name = self.entries["Last Name:"].get().strip()
        phone = self.entries["Phone Number:"].get().strip()
        email = self.entries["Email:"].get().strip().lower()
        password = self.entries["Password:"].get().strip()
        confirm_password = self.entries["Confirm Password:"].get().strip()
        role = self.role_var.get()
        manager_key = self.manager_key_entry.get() if role == "Manager" else ""
        owner_key = self.owner_key_entry.get() if role == "Owner" else ""

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        #validation of password, email, and phone number with error messages
        if not self.valid_password(password):
            messagebox.showerror("Weak Password", "Password must contain at least 8 characters.")
            return

        if not self.valid_email(email):
            messagebox.showerror("Invalid Email", "Email must contain valid email address with '@'.")
            return

        if not self.valid_phone(phone):
            messagebox.showerror("Invalid Phone Number", "Phone number must be between 10-15 digits.")
            return

        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # Insert user info into database
        sql_connection.insert_user(first_name, last_name, phone, email, hashed_password, role)

        # Clear the input fields after successful registration
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.manager_key_entry.delete(0, tk.END)
        self.owner_key_entry.delete(0, tk.END)

        # Navigate to the right page after successful sign-up
        messagebox.showinfo("Sign Up Successful", f"Welcome {role}!")
        if role == "Employee":
            self.master.show_frame(screens.emp_view.EmployeeView)
        elif role == "Manager":
            self.master.show_frame(screens.manager_view.ManagerView)
        elif role == "Owner":
            self.master.show_frame(screens.owner_view.OwnerView)
