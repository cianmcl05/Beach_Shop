import tkinter as tk
from tkinter import ttk, messagebox
import screens.welcome
import screens.emp_view
import screens.manager_view
import screens.owner_view
from sql_connection import connect_db, get_full_store_list
import hashlib

class LoginScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")
        self.master = master

        tk.Label(self, text="Welcome back", font=("Arial", 16, "bold"), bg="#FFF4A3", fg="black").pack(pady=10)

        self.email_entry = self.create_label_entry("Email:")
        self.password_entry = self.create_label_entry("Password:", show="*")

        tk.Label(self, text="Forgot User/Password?", font=("Arial", 10, "italic"),
                 fg="gray", bg="#FFF4A3", cursor="hand2").pack(anchor="w", padx=20, pady=5)

        # Load Stores from DB safely
        tk.Label(self, text="Select Store", font=("Arial", 12, "bold"), bg="#FFF4A3").pack(anchor="w", padx=20, pady=(10, 0))

        try:
            self.store_map = {name: sid for sid, name, _ in get_full_store_list()}
        except Exception as e:
            self.store_map = {}
            print(f"Error loading stores: {e}")

        self.store_var = tk.StringVar()
        self.store_dropdown = ttk.Combobox(self, values=list(self.store_map.keys()), font=("Arial", 12),
                                           textvariable=self.store_var, state="readonly")
        self.store_dropdown.pack(anchor="w", padx=20)

        if self.store_map:
            self.store_dropdown.current(0)

        self.create_buttons(master, screens.welcome.WelcomeScreen)

    def create_label_entry(self, text, show=""):
        tk.Label(self, text=text, font=("Arial", 12), bg="#FFF4A3").pack(anchor="w", padx=20)
        entry = tk.Entry(self, font=("Arial", 12), show=show)
        entry.pack(anchor="w", padx=20)
        return entry

    def create_buttons(self, master, back_screen):
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Back", font=("Arial", 12, "bold"), width=10,
                  bg="#B0F2C2", command=lambda: master.show_frame(back_screen)).pack(side="left", padx=10)

        tk.Button(button_frame, text="Confirm", font=("Arial", 12, "bold"), width=10,
                  bg="#EECFA3", command=self.login).pack(side="left", padx=10)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        selected_store = self.store_var.get()

        if not selected_store:
            messagebox.showerror("Error", "Please select a store.")
            return

        user_role = self.authenticate_user(email, password)
        if user_role:
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

            self.master.user_role = user_role
            self.master.emp_id = self.emp_id
            self.master.current_store_id = self.store_map[selected_store]  # ✅ Save StoreID globally

            messagebox.showinfo("Login Success", f"Welcome back, {user_role}!")

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
                    self.emp_id, role = result
                    return role.lower()
            except Exception as e:
                print(f"Database error: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
        return None




