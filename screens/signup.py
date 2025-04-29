import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Button
from PIL import Image, ImageTk
import screens.welcome
import sql_connection
import hashlib
import re
import os

class SignUpScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Background image setup
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "City-Highlight--Clearwater-ezgif.com-webp-to-jpg-converter.jpg")

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Background image not found at: {image_path}")

        self.master.update_idletasks()  # Ensure dimensions are accurate
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Resize and display the background image
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)

        # Canvas for the background image
        self.canvas = tk.Canvas(self, width=screen_width, height=screen_height)
        self.canvas.place(x=0, y=0)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Form frame with transparent background and fixed size
        self.form_frame = tk.Frame(self, bg="", bd=0)
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)  # Consistent size

        # Title Label
        title_label = ttk.Label(self.form_frame, text="Create Account", font=("Arial", 18, "bold"))
        title_label.pack(pady=10)

        # Input Fields Frame
        self.input_fields_frame = tk.Frame(self.form_frame)
        self.input_fields_frame.pack(padx=20, pady=5)

        self.entries = {}

        # Role dropdown
        role_frame = tk.Frame(self.input_fields_frame)
        role_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

        ttk.Label(role_frame, text="Role:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.role_var = tk.StringVar()
        role_dropdown = ttk.Combobox(role_frame, values=["Employee", "Manager", "Owner"], font=("Arial", 12), textvariable=self.role_var, state="readonly")
        role_dropdown.grid(row=0, column=1, padx=5, pady=5)
        role_dropdown.current(0)
        role_dropdown.bind("<<ComboboxSelected>>", self.toggle_role_keys)

        # Manager/Owner Key fields
        self.manager_key_label = ttk.Label(role_frame, text="Manager Key:", font=("Arial", 12))
        self.manager_key_entry = ttk.Entry(role_frame, font=("Arial", 12))
        self.owner_key_label = ttk.Label(role_frame, text="Owner Key:", font=("Arial", 12))
        self.owner_key_entry = ttk.Entry(role_frame, font=("Arial", 12))

        # Other fields
        field_labels = [
            ("First Name:", None),
            ("Last Name:", None),
            ("Phone Number:", None),
            ("Email:", None),
            ("Password:", "*"),
            ("Confirm Password:", "*"),
        ]

        for idx, (label_text, show) in enumerate(field_labels, start=1):
            ttk.Label(self.input_fields_frame, text=label_text, font=("Arial", 12)).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(self.input_fields_frame, font=("Arial", 12), show=show)
            entry.grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            self.entries[label_text] = entry

        # Store dropdown
        store_label_row = len(field_labels) + 1
        ttk.Label(self.input_fields_frame, text="Select Store:", font=("Arial", 12)).grid(row=store_label_row, column=0, padx=5, pady=5, sticky="e")
        self.store_var = tk.StringVar()
        self.store_dropdown = ttk.Combobox(self.input_fields_frame, textvariable=self.store_var, font=("Arial", 12), state="readonly")
        self.store_dropdown.grid(row=store_label_row, column=1, padx=5, pady=5, sticky="w")

        stores = sql_connection.get_all_stores()
        self.store_dropdown["values"] = [store[1] for store in stores]
        self.store_map = {store[1]: store[0] for store in stores}
        if stores:
            self.store_dropdown.current(0)

        # Buttons frame
        button_frame = tk.Frame(self.form_frame)
        button_frame.pack(pady=15)

        Button(button_frame, text="Back", bootstyle="primary", command=lambda: master.show_frame(screens.welcome.WelcomeScreen)).pack(side="left", padx=10)
        Button(button_frame, text="Sign Up", bootstyle="primary", command=self.validate_role_keys).pack(side="left", padx=10)

    def toggle_role_keys(self, event):
        self.manager_key_label.grid_forget()
        self.manager_key_entry.grid_forget()
        self.owner_key_label.grid_forget()
        self.owner_key_entry.grid_forget()

        role = self.role_var.get()
        if role == "Manager":
            self.manager_key_label.grid(row=0, column=2, padx=5, pady=5)
            self.manager_key_entry.grid(row=0, column=3, padx=5, pady=5)
        elif role == "Owner":
            self.owner_key_label.grid(row=0, column=2, padx=5, pady=5)
            self.owner_key_entry.grid(row=0, column=3, padx=5, pady=5)

    def validate_role_keys(self):
        role = self.role_var.get()
        if role == "Manager" and self.manager_key_entry.get() != "manager":
            messagebox.showerror("Error", "Invalid Manager Key!")
            return
        if role == "Owner" and self.owner_key_entry.get() != "owner":
            messagebox.showerror("Error", "Invalid Owner Key!")
            return
        self.register_user()

    def valid_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def valid_phone(self, phone):
        return phone.isdigit() and 10 <= len(phone) <= 15

    def valid_password(self, password):
        return len(password) >= 8

    def register_user(self):
        first_name = self.entries["First Name:"].get().strip()
        last_name = self.entries["Last Name:"].get().strip()
        phone = self.entries["Phone Number:"].get().strip()
        email = self.entries["Email:"].get().strip().lower()
        password = self.entries["Password:"].get().strip()
        confirm_password = self.entries["Confirm Password:"].get().strip()
        role = self.role_var.get()
        store_name = self.store_var.get()
        store_id = self.store_map.get(store_name)

        if not store_id:
            messagebox.showerror("Error", "Please select a store.")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        if not self.valid_password(password):
            messagebox.showerror("Weak Password", "Password must be at least 8 characters.")
            return
        if not self.valid_email(email):
            messagebox.showerror("Invalid Email", "Email must be valid.")
            return
        if not self.valid_phone(phone):
            messagebox.showerror("Invalid Phone", "Phone must be 10–15 digits.")
            return

        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        sql_connection.insert_user(first_name, last_name, phone, email, hashed_password, role, store_id)

        messagebox.showinfo("Sign Up Successful", f"Welcome {role}!")
        self.master.current_store_id = store_id
        self.master.show_frame(screens.welcome.WelcomeScreen)


