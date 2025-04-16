import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from PIL import Image, ImageTk
import screens.welcome
import sql_connection
import hashlib
import re
import os


class SignUpScreen(tb.Frame):
    def __init__(self, master):
        super().__init__(master)
<<<<<<< Updated upstream

        # ✅ Background setup
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "City-Highlight--Clearwater-ezgif.com-webp-to-jpg-converter.jpg")
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Background image not found at: {image_path}")

        bg_image = Image.open(image_path)
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
        self.bg_label = tb.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # ✅ Form frame
        self.form_frame = tb.Frame(self, padding=20)
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center")
<<<<<<< Updated upstream

        ttk = tb  # Alias for widgets

=======
>>>>>>> Stashed changes
        tb.Label(self.form_frame, text="Create Account", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self.entries = {}
        self.store_map = {}

        current_row = 1

        # Role dropdown
        tb.Label(self.form_frame, text="Role:", font=("Arial", 12)).grid(row=current_row, column=0, sticky="e", padx=10, pady=5)
        self.role_var = tb.StringVar()
<<<<<<< Updated upstream
        self.role_dropdown = tb.Combobox(
            self.form_frame,
            values=["Employee", "Manager", "Owner"],
            textvariable=self.role_var,
            font=("Arial", 12),
            state="readonly"
        )
=======
        self.role_dropdown = tb.Combobox(self.form_frame, values=["Employee", "Manager", "Owner"],
                                         textvariable=self.role_var, font=("Arial", 12), state="readonly")
>>>>>>> Stashed changes
        self.role_dropdown.grid(row=current_row, column=1, sticky="w", padx=10, pady=5)
        self.role_dropdown.current(0)
        self.role_dropdown.bind("<<ComboboxSelected>>", self.toggle_role_keys)

        self.manager_key_label = tb.Label(self.form_frame, text="Manager Key:", font=("Arial", 12))
        self.manager_key_entry = tb.Entry(self.form_frame, show="*", font=("Arial", 12))
<<<<<<< Updated upstream

        self.owner_key_label = tb.Label(self.form_frame, text="Owner Key:", font=("Arial", 12))
        self.owner_key_entry = tb.Entry(self.form_frame, show="*", font=("Arial", 12))

        # Entry fields
        fields = [
            ("First Name:", ""),
            ("Last Name:", ""),
            ("Phone Number:", ""),
            ("Email:", ""),
            ("Password:", "*"),
            ("Confirm Password:", "*"),
        ]

        for label, show in fields:
            current_row += 1
            tb.Label(self.form_frame, text=label, font=("Arial", 12)).grid(row=current_row, column=0, sticky="e", padx=10, pady=5)
            entry = tb.Entry(self.form_frame, font=("Arial", 12), show=show)
            entry.grid(row=current_row, column=1, sticky="w", padx=10, pady=5)
            self.entries[label] = entry
=======
        self.owner_key_label = tb.Label(self.form_frame, text="Owner Key:", font=("Arial", 12))
        self.owner_key_entry = tb.Entry(self.form_frame, show="*", font=("Arial", 12))

        # Entry fields
        fields = [
            ("First Name:", ""), ("Last Name:", ""), ("Phone Number:", ""), ("Email:", ""),
            ("Password:", "*"), ("Confirm Password:", "*")
        ]
        for label, show in fields:
            current_row += 1
            tb.Label(self.form_frame, text=label, font=("Arial", 12)).grid(row=current_row, column=0, sticky="e", padx=10, pady=5)
            entry = tb.Entry(self.form_frame, font=("Arial", 12), show=show)
            entry.grid(row=current_row, column=1, sticky="w", padx=10, pady=5)
            self.entries[label] = entry
=======
        self.master = master

        # Background setup
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "City-Highlight--Clearwater-ezgif.com-webp-to-jpg-converter.jpg")

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Background image not found at: {image_path}")

        bg_image = Image.open(image_path)
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)

        self.bg_label = tb.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Main form frame
        self.form_frame = tb.Frame(self, padding=20)
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center")

        tb.Label(self.form_frame, text="Create Account", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self.entries = {}
        current_row = 1

        # Role dropdown
        tb.Label(self.form_frame, text="Role:", font=("Arial", 12)).grid(row=current_row, column=0, sticky="e", padx=10, pady=5)
        self.role_var = tb.StringVar()
        self.role_dropdown = tb.Combobox(self.form_frame, values=["Employee", "Manager", "Owner"],
                                         textvariable=self.role_var, font=("Arial", 12), state="readonly")
        self.role_dropdown.grid(row=current_row, column=1, sticky="w", padx=10, pady=5)
        self.role_dropdown.current(0)
        self.role_dropdown.bind("<<ComboboxSelected>>", self.toggle_role_keys)

        self.manager_key_label = tb.Label(self.form_frame, text="Manager Key:", font=("Arial", 12))
        self.manager_key_entry = tb.Entry(self.form_frame, show="*", font=("Arial", 12))
        self.owner_key_label = tb.Label(self.form_frame, text="Owner Key:", font=("Arial", 12))
        self.owner_key_entry = tb.Entry(self.form_frame, show="*", font=("Arial", 12))

        # Entry fields
        fields = [
            ("First Name:", ""),
            ("Last Name:", ""),
            ("Phone Number:", ""),
            ("Email:", ""),
            ("Password:", "*"),
            ("Confirm Password:", "*"),
        ]

        for label, show in fields:
            current_row += 1
            tb.Label(self.form_frame, text=label, font=("Arial", 12)).grid(row=current_row, column=0, sticky="e", padx=10, pady=5)
            entry = tb.Entry(self.form_frame, font=("Arial", 12), show=show)
            entry.grid(row=current_row, column=1, sticky="w", padx=10, pady=5)
            self.entries[label] = entry

        # Store selection
        current_row += 1
        tb.Label(self.form_frame, text="Select Store:", font=("Arial", 12)).grid(row=current_row, column=0, sticky="e", padx=10, pady=5)
        self.store_var = tb.StringVar()
        self.store_dropdown = tb.Combobox(self.form_frame, textvariable=self.store_var, font=("Arial", 12), state="readonly")
        self.store_dropdown.grid(row=current_row, column=1, sticky="w", padx=10, pady=5)
>>>>>>> Stashed changes

        # Store dropdown
        current_row += 1
        tb.Label(self.form_frame, text="Select Store:", font=("Arial", 12)).grid(row=current_row, column=0, sticky="e", padx=10, pady=5)
        self.store_var = tb.StringVar()
        self.store_dropdown = tb.Combobox(self.form_frame, textvariable=self.store_var, font=("Arial", 12), state="readonly")
        self.store_dropdown.grid(row=current_row, column=1, sticky="w", padx=10, pady=5)

        stores = sql_connection.get_all_stores()
        self.store_dropdown["values"] = [store[1] for store in stores]
        self.store_map = {store[1]: store[0] for store in stores}
        if stores:
            self.store_dropdown.current(0)
>>>>>>> Stashed changes

        # Buttons
        current_row += 1
        button_frame = tb.Frame(self.form_frame)
        button_frame.grid(row=current_row, column=0, columnspan=2, pady=20)
<<<<<<< Updated upstream
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
        tb.Button(button_frame, text="Back", bootstyle="primary", command=lambda: master.show_frame(screens.welcome.WelcomeScreen)).pack(side="left", padx=10)
        tb.Button(button_frame, text="Sign Up", bootstyle="primary", command=self.validate_role_keys).pack(side="left", padx=10)

    def toggle_role_keys(self, event):
<<<<<<< Updated upstream
        # Remove both first
=======
>>>>>>> Stashed changes
=======

        tb.Button(button_frame, text="Back", bootstyle="primary",
                  command=lambda: master.show_frame(screens.welcome.WelcomeScreen)).pack(side="left", padx=10)
        tb.Button(button_frame, text="Sign Up", bootstyle="primary", command=self.validate_role_keys).pack(side="left", padx=10)

    def toggle_role_keys(self, event):
        # Remove both first
>>>>>>> Stashed changes
        self.manager_key_label.grid_forget()
        self.manager_key_entry.grid_forget()
        self.owner_key_label.grid_forget()
        self.owner_key_entry.grid_forget()

<<<<<<< Updated upstream
<<<<<<< Updated upstream
        row = 1  # same row as role dropdown

=======
        row = 1
>>>>>>> Stashed changes
=======
        row = 1  # same row as role dropdown

>>>>>>> Stashed changes
        if self.role_var.get() == "Manager":
            self.manager_key_label.grid(row=row, column=2, sticky="e", padx=10)
            self.manager_key_entry.grid(row=row, column=3, sticky="w", padx=10)
        elif self.role_var.get() == "Owner":
            self.owner_key_label.grid(row=row, column=2, sticky="e", padx=10)
            self.owner_key_entry.grid(row=row, column=3, sticky="w", padx=10)

    def validate_role_keys(self):
        role = self.role_var.get()
<<<<<<< Updated upstream

<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        if role == "Manager" and self.manager_key_entry.get() != "manager":
            messagebox.showerror("Error", "Invalid Manager Key!")
            return
        if role == "Owner" and self.owner_key_entry.get() != "owner":
            messagebox.showerror("Error", "Invalid Owner Key!")
            return
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes

=======
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
=======
        store_name = self.store_var.get()
        store_id = self.store_map.get(store_name)

        if not store_id:
            messagebox.showerror("Error", "Please select a store.")
            return
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        sql_connection.insert_user(first_name, last_name, phone, email, hashed_password, role)
=======
=======
>>>>>>> Stashed changes
        sql_connection.insert_user(first_name, last_name, phone, email, hashed_password, role, store_id)
>>>>>>> Stashed changes

<<<<<<< Updated upstream
=======
        self.master.current_store_id = store_id

        # Clear all inputs
>>>>>>> Stashed changes
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.manager_key_entry.delete(0, "end")
        self.owner_key_entry.delete(0, "end")

        messagebox.showinfo("Sign Up Successful", f"Welcome {role}!")
        self.master.current_store_id = store_id
        self.master.show_frame(screens.welcome.WelcomeScreen)



<<<<<<< Updated upstream
<<<<<<< Updated upstream






=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
