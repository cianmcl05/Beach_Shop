import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import hashlib
import screens.welcome
import screens.emp_view
import screens.manager_view
import screens.owner_view
from sql_connection import connect_db, get_full_store_list

class LoginScreen(tb.Frame):
    def __init__(self, master):
        super().__init__(master, bootstyle="light")

        self.master = master

        # Load background image (optional)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "City-Highlight--Clearwater-ezgif.com-webp-to-jpg-converter.jpg")
        if os.path.exists(image_path):
            bg_image = Image.open(image_path)
            screen_width = master.winfo_screenwidth()
            screen_height = master.winfo_screenheight()
            bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(bg_image)

            self.bg_label = tb.Label(self, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            print(f"Warning: Background image not found at {image_path}")

        # Form frame
        self.form_frame = tb.Frame(self, padding=20, bootstyle="light")
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tb.Label(self.form_frame, text="Welcome back", font=("Arial", 16, "bold"),
                 bootstyle="light", foreground="black").pack(pady=10)

        # Email and password
        self.email_entry = self.create_label_entry("Email:")
        self.password_entry = self.create_label_entry("Password:", show="*")

        # Forgot Password
        tb.Label(self.form_frame, text="Forgot User/Password?", font=("Arial", 10, "italic"),
                 bootstyle="light", foreground="gray30").pack(anchor="w", padx=20, pady=5)

        # Store selection
        tb.Label(self.form_frame, text="Select Store", font=("Arial", 12, "bold"),
                 bootstyle="light", foreground="black").pack(anchor="w", padx=20, pady=(10, 0))

        try:
            self.store_map = {name: sid for sid, name, _ in get_full_store_list()}
        except Exception as e:
            self.store_map = {}
            print(f"Error loading stores: {e}")

        self.store_var = tb.StringVar()
        self.store_dropdown = tb.Combobox(self.form_frame, values=list(self.store_map.keys()),
                                          font=("Arial", 12), textvariable=self.store_var, state="readonly")
        self.store_dropdown.pack(anchor="w", padx=20)

        if self.store_map:
            self.store_dropdown.current(0)

        # Buttons
        self.create_buttons()

    def create_label_entry(self, text, show=""):
        tb.Label(self.form_frame, text=text, font=("Arial", 12), bootstyle="light",
                 foreground="black").pack(anchor="w", padx=20)
        entry = tb.Entry(self.form_frame, font=("Arial", 12), show=show)
        entry.pack(anchor="w", padx=20)
        return entry

    def create_buttons(self):
        button_frame = tb.Frame(self.form_frame, bootstyle="light")
        button_frame.pack(pady=10)

        # CHANGED: Make both buttons blue (bootstyle="primary")
        tb.Button(button_frame, text="Back", width=10, bootstyle="primary",
                  command=lambda: self.master.show_frame(screens.welcome.WelcomeScreen)).pack(side="left", padx=10)

        tb.Button(button_frame, text="Confirm", width=10, bootstyle="primary",
                  command=self.login).pack(side="left", padx=10)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        selected_store = self.store_var.get()

        if not selected_store:
            messagebox.showerror("Error", "Please select a store.")
            return

        user_role = self.authenticate_user(email, password)
        if user_role:
            self.email_entry.delete(0, tb.END)
            self.password_entry.delete(0, tb.END)

            self.master.user_role = user_role
            self.master.emp_id = self.emp_id
            self.master.current_store_id = self.store_map[selected_store]

            messagebox.showinfo("Login Success", f"Welcome back, {user_role.capitalize()}!")
            self.master.reset_frames_after_login()

            if user_role == "employee":
                self.master.show_frame(screens.emp_view.EmployeeView, emp_id=self.emp_id)
            elif user_role == "manager":
                self.master.show_frame(screens.manager_view.ManagerView, emp_id=self.emp_id)
            elif user_role == "owner":
                self.master.show_frame(screens.owner_view.OwnerView, emp_id=self.emp_id)
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")

    def authenticate_user(self, email, password):
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        connection = connect_db()

        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT ID, Role FROM Employee WHERE Email = %s AND Password = %s"
                cursor.execute(query, (email, hashed_password))
                result = cursor.fetchone()
                if result:
                    emp_id, role = result
                    self.emp_id = emp_id
                    return role.lower()
            except Exception as e:
                print(f"Database error: {e}")
            finally:
                cursor.close()
                connection.close()
        return None








