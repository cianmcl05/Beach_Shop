import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import os
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

        # ✅ Transparent content frame (use tk.Frame to support background customization)
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











