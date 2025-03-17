import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class BeachShopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Welcome Screen")
        self.geometry("500x450")
        self.configure(bg="#FFF4A3")

        self.frames = {}  # Dictionary to store frames

        # Initialize screens
        for F in (WelcomeScreen, LoginScreen, SignUpScreen):
            frame = F(self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(WelcomeScreen)  # Show welcome screen by default

    def show_frame(self, frame_class):
        """Raise a given frame to the front."""
        frame = self.frames[frame_class]
        frame.tkraise()

class WelcomeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")

        tk.Label(self, text="Welcome", font=("Arial", 20, "bold"), bg="#FFF4A3", fg="black").pack(pady=40)

        tk.Button(self, text="Sign up", font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#B0F2C2", fg="black", relief="ridge",
                  command=lambda: master.show_frame(SignUpScreen)).place(x=150, y=180)

        tk.Button(self, text="Login", font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#EECFA3", fg="black", relief="ridge",
                  command=lambda: master.show_frame(LoginScreen)).place(x=280, y=180)

class LoginScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")

        tk.Label(self, text="Welcome back", font=("Arial", 16, "bold"), bg="#FFF4A3", fg="black").pack(pady=10)

        self.create_label_entry("EmpID:")
        self.create_label_entry("Password:", show="*")

        # Forgot Password
        tk.Label(self, text="Forgot User/Password?", font=("Arial", 10, "italic"),
                 fg="gray", bg="#FFF4A3", cursor="hand2").pack(anchor="w", padx=20, pady=5)

        # Store Dropdown
        tk.Label(self, text="Select Store", font=("Arial", 12, "bold"), bg="#FFF4A3").pack(anchor="w", padx=20, pady=(10, 0))
        store_dropdown = ttk.Combobox(self, values=["Store 1", "Store 2", "Store 3"], font=("Arial", 12))
        store_dropdown.pack(anchor="w", padx=20)
        store_dropdown.current(0)

        # Buttons
        self.create_buttons(master, WelcomeScreen, "Go")

    def create_label_entry(self, text, show=""):
        """Helper function to create a label and entry field."""
        tk.Label(self, text=text, font=("Arial", 12), bg="#FFF4A3").pack(anchor="w", padx=20)
        tk.Entry(self, font=("Arial", 12), show=show).pack(anchor="w", padx=20)

    def create_buttons(self, master, back_screen, confirm_text):
        """Helper function to create Back and Confirm buttons."""
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Back", font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#B0F2C2", fg="black", relief="ridge",
                  command=lambda: master.show_frame(back_screen)).pack(side="left", padx=10)

        tk.Button(button_frame, text=confirm_text, font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#EECFA3", fg="black", relief="ridge").pack(side="left", padx=10)

class SignUpScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFF4A3")

        tk.Label(self, text="Create Account", font=("Arial", 16, "bold"), bg="#FFF4A3", fg="black").pack(pady=10)

        # Role Selection
        role_frame = tk.Frame(self, bg="#FFF4A3")
        role_frame.pack(anchor="w", padx=20, pady=5)

        tk.Label(role_frame, text="Role:", font=("Arial", 12), bg="#FFF4A3").grid(row=0, column=0, padx=5)
        self.role_var = tk.StringVar()
        role_dropdown = ttk.Combobox(role_frame, values=["Employee", "Manager"], font=("Arial", 12), textvariable=self.role_var)
        role_dropdown.grid(row=0, column=1, padx=5)
        role_dropdown.current(0)
        role_dropdown.bind("<<ComboboxSelected>>", self.toggle_manager_key)

        # Manager Key (Initially Hidden)
        self.manager_key_label = tk.Label(role_frame, text="Manager Key:", font=("Arial", 12), bg="#FFF4A3")
        self.manager_key_entry = tk.Entry(role_frame, font=("Arial", 12), show="*")

        # Other Fields
        self.create_label_entry("First Name:")
        self.create_label_entry("Last Name:")
        self.create_label_entry("Phone Number:")
        self.create_label_entry("Email:")
        self.create_label_entry("Password:", show="*")
        self.create_label_entry("Confirm Password:", show="*")

        # Buttons
        self.create_buttons(master, WelcomeScreen, "Sign Up")

    def create_label_entry(self, text, show=""):
        """Helper function to create a label and entry field."""
        tk.Label(self, text=text, font=("Arial", 12), bg="#FFF4A3").pack(anchor="w", padx=20)
        tk.Entry(self, font=("Arial", 12), show=show).pack(anchor="w", padx=20)

    def create_buttons(self, master, back_screen, confirm_text):
        """Helper function to create Back and Confirm buttons."""
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Back", font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#B0F2C2", fg="black", relief="ridge",
                  command=lambda: master.show_frame(back_screen)).pack(side="left", padx=10)

        tk.Button(button_frame, text=confirm_text, font=("Arial", 12, "bold"), width=10, height=1,
                  bg="#EECFA3", fg="black", relief="ridge").pack(side="left", padx=10)

    def toggle_manager_key(self, event):
        """Show/hide manager key field based on role selection."""
        if self.role_var.get() == "Manager":
            self.manager_key_label.grid(row=0, column=2, padx=10)
            self.manager_key_entry.grid(row=0, column=3, padx=10)
        else:
            self.manager_key_label.grid_forget()
            self.manager_key_entry.grid_forget()

# Run the application
if __name__ == "__main__":
    app = BeachShopApp()
    app.mainloop()
