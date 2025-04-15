import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from PIL import Image, ImageTk
import screens.welcome
import screens.emp_view
import screens.manager_view
import screens.owner_view
from sql_connection import connect_db
import hashlib
import os

class LoginScreen(tb.Frame):
    def __init__(self, master):
        super().__init__(master)

        # ✅ Load background image
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "City-Highlight--Clearwater-ezgif.com-webp-to-jpg-converter.jpg")

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Background image not found at: {image_path}")
<<<<<<< Updated upstream

        bg_image = Image.open(image_path)
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)

        self.bg_label = tb.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.form_frame = tb.Frame(self, padding=20)
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk = tb

        ttk.Label(self.form_frame, text="Welcome back", font=("Arial", 16, "bold")).pack(pady=10)
        self.email_entry = self.create_label_entry("Email:")
        self.password_entry = self.create_label_entry("Password:", show="*")

        tb.Label(self.form_frame, text="Forgot User/Password?", font=("Arial", 10, "italic"),
                 foreground="black", cursor="hand2").pack(anchor="w", padx=20, pady=5)

        ttk.Label(self.form_frame, text="Select Store", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(10, 0))
        self.store_dropdown = ttk.Combobox(self.form_frame, values=["Store 1", "Store 2", "Store 3"],
                                           font=("Arial", 12), state="readonly")  # 👈 read-only dropdown
        self.store_dropdown.pack(anchor="w", padx=20)
        self.store_dropdown.current(0)

        self.create_buttons(master, screens.welcome.WelcomeScreen, screens.emp_view.EmployeeView)

    def create_label_entry(self, text, show=""):
        tb.Label(self.form_frame, text=text, font=("Arial", 12)).pack(anchor="w", padx=20)
        entry = tb.Entry(self.form_frame, show=show, font=("Arial", 12))
        entry.pack(anchor="w", padx=20, pady=(0, 5))
        return entry

    def create_buttons(self, master, back_screen, confirm_screen):
        button_frame = tb.Frame(self.form_frame)
        button_frame.pack(pady=10)

        tb.Button(button_frame, text="Back", command=lambda: master.show_frame(back_screen)).pack(side="left", padx=10)
        tb.Button(button_frame, text="Confirm", command=lambda: self.login(master, confirm_screen)).pack(side="left", padx=10)

    def login(self, master, confirm_screen):
=======

        bg_image = Image.open(image_path)
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)

        self.bg_label = tb.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # ✅ Form frame
        self.form_frame = tb.Frame(self, padding=20)
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk = tb  # alias

        ttk.Label(self.form_frame, text="Welcome back", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Email and password
        ttk.Label(self.form_frame, text="Email:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.email_entry = tb.Entry(self.form_frame, font=("Arial", 12))
        self.email_entry.grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(self.form_frame, text="Password:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.password_entry = tb.Entry(self.form_frame, font=("Arial", 12), show="*")
        self.password_entry.grid(row=2, column=1, sticky="w", pady=5)

        # Forgot password
        tb.Label(self.form_frame, text="Forgot User/Password?", font=("Arial", 10, "italic"),
                 foreground="black", cursor="hand2").grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 10))

        # Store selection
        ttk.Label(self.form_frame, text="Select Store", font=("Arial", 12)).grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.store_var = tb.StringVar()
        self.store_dropdown = tb.Combobox(self.form_frame, font=("Arial", 12), textvariable=self.store_var, state="readonly")
        self.store_dropdown.grid(row=4, column=1, sticky="w", pady=5)

        # Load stores from DB
        try:
            self.store_map = {name: sid for sid, name, _ in get_full_store_list()}
            self.store_dropdown['values'] = list(self.store_map.keys())
            if self.store_map:
                self.store_dropdown.current(0)
        except Exception as e:
            print(f"Error loading stores: {e}")
            self.store_map = {}

        # Buttons
        self.create_buttons(master, screens.welcome.WelcomeScreen)

    def create_buttons(self, master, back_screen):
        button_frame = tb.Frame(self.form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)

        tb.Button(button_frame, text="Back", width=12,
                  command=lambda: master.show_frame(back_screen)).pack(side="left", padx=10)
        tb.Button(button_frame, text="Confirm", width=12,
                  command=lambda: self.login(master)).pack(side="left", padx=10)

    def login(self, master):
>>>>>>> Stashed changes
        email = self.email_entry.get()
        password = self.password_entry.get()

        user_role = self.authenticate_user(email, password)
<<<<<<< Updated upstream

        if user_role:
            self.email_entry.delete(0, "end")
            self.password_entry.delete(0, "end")

            messagebox.showinfo("Login Success", f"Welcome back, {user_role}!")
            master.user_role = user_role

            master.reset_frames_after_login()
            if user_role == "employee":
                master.show_frame(screens.emp_view.EmployeeView, emp_id=self.emp_id)
            elif user_role == "manager":
                master.show_frame(screens.manager_view.ManagerView)
            elif user_role == "owner":
                master.show_frame(screens.owner_view.OwnerView)
=======
        if user_role:
            self.email_entry.delete(0, "end")
            self.password_entry.delete(0, "end")

            master.user_role = user_role
            master.emp_id = self.emp_id
            master.current_store_id = self.store_map[selected_store]

            messagebox.showinfo("Login Success", f"Welcome back, {user_role.capitalize()}!")

            master.reset_frames_after_login()

            if user_role == "employee":
                master.show_frame(screens.emp_view.EmployeeView, emp_id=self.emp_id)
            elif user_role == "manager":
                master.show_frame(screens.manager_view.ManagerView, emp_id=self.emp_id)
            elif user_role == "owner":
                master.show_frame(screens.owner_view.OwnerView, emp_id=self.emp_id)
>>>>>>> Stashed changes
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






<<<<<<< Updated upstream













=======
>>>>>>> Stashed changes
