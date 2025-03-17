import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import screens.welcome


class LoginScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")

        tk.Label(self, text="Welcome back", font=("Arial", 16, "bold"), bg="#FFF4A3", fg="black").pack(pady=10)

        # Create Entry fields for EmpID and Password
        self.empid_entry = self.create_label_entry("EmpID:")
        self.password_entry = self.create_label_entry("Password:", show="*")

        tk.Label(self, text="Forgot User/Password?", font=("Arial", 10, "italic"),
                 fg="gray", bg="#FFF4A3", cursor="hand2").pack(anchor="w", padx=20, pady=5)

        # Store Dropdown
        tk.Label(self, text="Select Store", font=("Arial", 12, "bold"), bg="#FFF4A3").pack(anchor="w", padx=20, pady=(10, 0))
        store_dropdown = ttk.Combobox(self, values=["Store 1", "Store 2", "Store 3"], font=("Arial", 12))
        store_dropdown.pack(anchor="w", padx=20)
        store_dropdown.current(0)

        self.create_buttons(master, screens.welcome.WelcomeScreen, "Login")

    def create_label_entry(self, text, show=""):
        """Helper function to create a label and entry field."""
        tk.Label(self, text=text, font=("Arial", 12), bg="#FFF4A3").pack(anchor="w", padx=20)
        entry = tk.Entry(self, font=("Arial", 12), show=show)
        entry.pack(anchor="w", padx=20)
        return entry

    def create_buttons(self, master, back_screen, confirm_text):
        """Helper function to create Back and Confirm buttons."""
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Back", font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#B0F2C2", fg="black", relief="ridge",
                  command=lambda: master.show_frame(back_screen)).pack(side="left", padx=10)

        tk.Button(button_frame, text=confirm_text, font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#EECFA3", fg="black", relief="ridge", command=self.login).pack(side="left", padx=10)

    def login(self):
        empid = self.empid_entry.get()
        password = self.password_entry.get()

        if self.authenticate_user(empid, password):
            # If authentication is successful, show the next screen (e.g., go to dashboard)
            messagebox.showinfo("Login Success", "Welcome back!")
            # Here you can call the method to switch to the next screen
            # For example: master.show_frame(DashboardScreen)
        else:
            messagebox.showerror("Login Failed", "Invalid EmpID or Password.")

    def authenticate_user(self, empid, password):
        """Authenticate user by checking the credentials in the MySQL database."""
        try:
            # Establish connection to the database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="cmac2005",
                database="surfshop"
            )

            if connection.is_connected():
                cursor = connection.cursor()

                # Query to check if user exists with the entered EmpID and Password
                query = "SELECT * FROM Employee WHERE Email = %s AND Password = %s"
                cursor.execute(query, (empid, password))

                result = cursor.fetchone()  # Fetch one record

                if result:
                    # If result is not None, the user is found
                    return True
                else:
                    return False

        except Error as e:
            print(f"Error: {e}")
            return False

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

