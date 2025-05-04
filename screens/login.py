import ttkbootstrap as tb
from ttkbootstrap.constants import END
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
    """
    Login screen using ttkbootstrap for styled widgets.
    Allows user to enter email, password, and select a store.
    Authenticates against the Employee table and routes to the appropriate view.
    """
    def __init__(self, master):
        super().__init__(master, bootstyle="light")
        self.master = master

        # Attempt to load a fullscreen background image
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(
            base_dir,
            "City-Highlight--Clearwater-ezgif.com-webp-to-jpg-converter.jpg"
        )
        if os.path.exists(image_path):
            bg_image = Image.open(image_path)
            screen_w = master.winfo_screenwidth()
            screen_h = master.winfo_screenheight()
            bg_image = bg_image.resize((screen_w, screen_h), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(bg_image)

            # Place the background image behind all widgets
            self.bg_label = tb.Label(self, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            print(f"Warning: Background image not found at {image_path}")

        # Form container in the center
        self.form_frame = tb.Frame(self, padding=20, bootstyle="light")
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title label
        tb.Label(
            self.form_frame,
            text="Welcome back",
            font=("Arial", 16, "bold"),
            bootstyle="light",
            foreground="black"
        ).pack(pady=10)

        # Email and password entry fields
        self.email_entry = self._create_label_entry("Email:")
        self.password_entry = self._create_label_entry("Password:", show="*")

        # Store selection dropdown populated from database
        tb.Label(
            self.form_frame,
            text="Select Store",
            font=("Arial", 12, "bold"),
            bootstyle="light",
            foreground="black"
        ).pack(anchor="w", padx=20, pady=(10, 0))

        try:
            # Fetch store list: (ID, name, ...)
            stores = get_full_store_list()
            # Map store name to ID
            self.store_map = {name: sid for sid, name, _ in stores}
        except Exception as e:
            self.store_map = {}
            print(f"Error loading stores: {e}")

        self.store_var = tb.StringVar()
        self.store_dropdown = tb.Combobox(
            self.form_frame,
            values=list(self.store_map.keys()),
            font=("Arial", 12),
            textvariable=self.store_var,
            state="readonly"
        )
        self.store_dropdown.pack(anchor="w", padx=20)
        if self.store_map:
            self.store_dropdown.current(0)

        # Action buttons: Back and Confirm
        self._create_buttons()

    def _create_label_entry(self, label_text, show=""):
        """
        Helper to create a label and entry in the form_frame.
        Returns the Entry widget.
        """
        tb.Label(
            self.form_frame,
            text=label_text,
            font=("Arial", 12),
            bootstyle="light",
            foreground="black"
        ).pack(anchor="w", padx=20)
        entry = tb.Entry(self.form_frame, font=("Arial", 12), show=show)
        entry.pack(anchor="w", padx=20)
        return entry

    def _create_buttons(self):
        """
        Create the Back and Confirm buttons.
        Back returns to WelcomeScreen; Confirm attempts login.
        """
        button_frame = tb.Frame(self.form_frame, bootstyle="light")
        button_frame.pack(pady=10)

        # Back button navigates to welcome screen
        tb.Button(
            button_frame,
            text="Back",
            width=10,
            bootstyle="primary",
            command=lambda: self.master.show_frame(screens.welcome.WelcomeScreen)
        ).pack(side="left", padx=10)

        # Confirm button triggers login flow
        tb.Button(
            button_frame,
            text="Confirm",
            width=10,
            bootstyle="primary",
            command=self.login
        ).pack(side="left", padx=10)

    def login(self):
        """
        Authenticate the user and route to their dashboard based
        on role: employee, manager, or owner.
        """
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        store_name = self.store_var.get()

        if not store_name:
            messagebox.showerror("Error", "Please select a store.")
            return

        # Validate credentials
        role = self._authenticate_user(email, password)
        if role:
            # Clear sensitive fields
            self.email_entry.delete(0, END)
            self.password_entry.delete(0, END)

            # Store context in master
            self.master.user_role = role
            self.master.emp_id = self.emp_id
            self.master.current_store_id = self.store_map[store_name]

            messagebox.showinfo(
                "Login Success",
                f"Welcome back, {role.capitalize()}!"
            )
            # Reset any existing frames
            self.master.reset_frames_after_login()

            # Navigate based on role
            if role == "employee":
                self.master.show_frame(
                    screens.emp_view.EmployeeView,
                    emp_id=self.emp_id
                )
            elif role == "manager":
                self.master.show_frame(
                    screens.manager_view.ManagerView,
                    emp_id=self.emp_id
                )
            else:
                self.master.show_frame(
                    screens.owner_view.OwnerView,
                    emp_id=self.emp_id
                )
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid email or password."
            )

    def _authenticate_user(self, email, password):
        """
        Hashes the password and checks credentials in the database.
        Returns the user role in lowercase, or None if invalid.
        """
        # SHA-256 hash of the password
        hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                query = (
                    "SELECT ID, Role FROM Employee "
                    "WHERE Email = %s AND Password = %s"
                )
                cursor.execute(query, (email, hashed))
                result = cursor.fetchone()
                if result:
                    emp_id, role = result
                    self.emp_id = emp_id
                    return role.lower()
            except Exception as e:
                print(f"Database error: {e}")
            finally:
                cursor.close()
                conn.close()
        return None

