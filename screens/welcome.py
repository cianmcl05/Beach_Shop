import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import os
<<<<<<< Updated upstream
=======
import tkinter as tk  # Import tkinter for Canvas usage
>>>>>>> Stashed changes
import screens.signup
import screens.login

class WelcomeScreen(tb.Frame):
    def __init__(self, master):
        super().__init__(master)

        # ✅ Load background image
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "City-Highlight--Clearwater-ezgif.com-webp-to-jpg-converter.jpg")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Background image not found at: {image_path}")

        bg_image = Image.open(image_path)
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)

        # ✅ Background label
        self.bg_label = tb.Label(self, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

<<<<<<< Updated upstream
        # ✅ Transparent content frame (use tk.Frame to support background customization)
=======
        # ✅ Create canvas to simulate rounded frame
        canvas = tk.Canvas(self, width=500, height=300, highlightthickness=0, bg="#f8f9fa")  # use a light color
        canvas.place(relx=0.5, rely=0.5, anchor="center")

        radius = 30
        canvas.create_arc((0, 0, radius*2, radius*2), start=90, extent=90, fill="#ffffff", outline="#ffffff")
        canvas.create_arc((500 - radius*2, 0, 500, radius*2), start=0, extent=90, fill="#ffffff", outline="#ffffff")
        canvas.create_arc((0, 300 - radius*2, radius*2, 300), start=180, extent=90, fill="#ffffff", outline="#ffffff")
        canvas.create_arc((500 - radius*2, 300 - radius*2, 500, 300), start=270, extent=90, fill="#ffffff", outline="#ffffff")
        canvas.create_rectangle((radius, 0, 500 - radius, 300), fill="#ffffff", outline="#ffffff")
        canvas.create_rectangle((0, radius, 500, 300 - radius), fill="#ffffff", outline="#ffffff")

        # ✅ Content Frame over canvas
>>>>>>> Stashed changes
        content_frame = tb.Frame(self, bootstyle="light")
        content_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=300)

        # ✅ Title
        title_label = tb.Label(
            content_frame,
            text="Welcome",
            font=("Arial", 28, "bold"),
            bootstyle="primary",
        )
        title_label.pack(pady=(20, 40))

        # ✅ Button frame
        button_frame = tb.Frame(content_frame)
        button_frame.pack()

        tb.Button(
            button_frame,
            text="Sign Up",
            bootstyle="success-outline",
            width=18,
            padding=12,
            command=lambda: master.show_frame(screens.signup.SignUpScreen)
        ).pack(side="left", padx=25)

        tb.Button(
            button_frame,
            text="Login",
            bootstyle="primary-outline",
            width=18,
            padding=12,
            command=lambda: master.show_frame(screens.login.LoginScreen)
        ).pack(side="left", padx=25)
<<<<<<< Updated upstream








=======
>>>>>>> Stashed changes



