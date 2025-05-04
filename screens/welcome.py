import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import os
import screens.signup
import screens.login
import tkinter as tk

class WelcomeScreen(tb.Frame):
    """
    Initial landing screen with background image and two actions:
    Sign Up (success style) and Login (primary style).
    """
    def __init__(self, master):
        super().__init__(master)

        # Load and resize the background image to full screen
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(
            base_dir,
            "City-Highlight--Clearwater-ezgif.com-webp-to-jpg-converter.jpg"
        )
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Background image not found at: {image_path}")

        bg_image = Image.open(image_path)
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)

        # Place the background image label behind all widgets
        self.bg_label = tb.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a fixed-size white container to hold the title and buttons
        white_box = tb.Frame(self, width=700, height=400, bootstyle="light")
        white_box.place(relx=0.5, rely=0.5, anchor="center")
        white_box.pack_propagate(False)  # Prevent auto-resizing

        # Display the welcome title in the white box
        welcome_label = tb.Label(
            white_box,
            text="Welcome",
            font=("Arial", 28, "bold"),
            bootstyle="primary"
        )
        welcome_label.pack(pady=(50, 60))  # Top and bottom padding

        # Frame for action buttons (Sign Up, Login)
        button_frame = tb.Frame(white_box, bootstyle="light")
        button_frame.pack()

        # Sign Up button navigates to SignUpScreen
        tb.Button(
            button_frame,
            text="Sign Up",
            bootstyle="success-outline",
            width=15,
            padding=10,
            command=lambda: master.show_frame(screens.signup.SignUpScreen)
        ).pack(side="left", padx=30)

        # Login button navigates to LoginScreen
        tb.Button(
            button_frame,
            text="Login",
            bootstyle="primary-outline",
            width=15,
            padding=10,
            command=lambda: master.show_frame(screens.login.LoginScreen)
        ).pack(side="left", padx=30)
