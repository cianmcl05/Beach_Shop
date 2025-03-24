import tkinter as tk
from tkinter import ttk, messagebox
import screens.welcome
import screens.emp_view
import screens.manager_view
import screens.owner_view
from sql_connection import connect_db  # Importing the database connection function
import hashlib

class LoginScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")

        tk.Label(self, text="Welcome back", font=("Arial", 16, "bold"), bg="#FFF4A3", fg="black").pack(pady=10)

        # Create Entry fields for Email and Password
        self.email_entry = self.create_label_entry("Email:")
        self.password_entry = self.create_label_entry("Password:", show="*")

        tk.Label(self, text="Forgot User/Password?", font=("Arial", 10, "italic"),
                 fg="gray", bg="#FFF4A3", cursor="hand2").pack(anchor="w", padx=20, pady=5)

        # Store Dropdown
        tk.Label(self, text="Select Store", font=("Arial", 12, "bold"), bg="#FFF4A3").pack(anchor="w", padx=20, pady=(10, 0))
        store_dropdown = ttk.Combobox(self, values=["Store 1", "Store 2", "Store 3"], font=("Arial", 12))
        store_dropdown.pack(anchor="w", padx=20)
        store_dropdown.current(0)

        self.create_buttons(master, screens.welcome.WelcomeScreen, screens.emp_view.EmployeeView)

# input fields
    def create_label_entry(self, text, show=""):
        tk.Label(self, text=text, font=("Arial", 12), bg="#FFF4A3").pack(anchor="w", padx=20)
        entry = tk.Entry(self, font=("Arial", 12), show=show)
        entry.pack(anchor="w", padx=20)
        return entry

# back and confirm buttons
    def create_buttons(self, master, back_screen, confirm_screen):
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Back", font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#B0F2C2", fg="black", relief="ridge",
                  command=lambda: master.show_frame(back_screen)).pack(side="left", padx=10)

        tk.Button(button_frame, text="Confirm", font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#EECFA3", fg="black", relief="ridge",
                  command=lambda: self.login(master, confirm_screen)).pack(side="left", padx=10)

    # used to identify user and log them in
    def login(self, master, confirm_screen):
        email = self.email_entry.get()
        password = self.password_entry.get()

        user_role = self.authenticate_user(email, password)

        if user_role:
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

            messagebox.showinfo("Login Success", f"Welcome back, {user_role}!")
            if user_role == "employee":
                master.show_frame(screens.emp_view.EmployeeView)
            elif user_role == "manager":
                master.show_frame(screens.manager_view.ManagerView)
            else:
                master.show_frame(screens.owner_view.OwnerView)
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")

    # checks if credentials are in the database
    def authenticate_user(self, email, password):
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        connection = connect_db()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT Role FROM Employee WHERE Email = %s AND Password = %s"
                cursor.execute(query, (email, hashed_password))
                result = cursor.fetchone()
                if result:
                    return result[0].lower()
            except Exception as e:
                print(f"Database error: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
        return None  # Return None if authentication fails

