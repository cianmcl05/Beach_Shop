import tkinter as tk
import screens.welcome
import screens.login
import screens.signup
import screens.emp_view
import screens.manager_view
import screens.owner_view
from tkinter import messagebox


# main app class
class BeachShopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Welcome Screen")
        self.geometry("500x450")
        self.configure(bg="#FFF4A3")

        # Dictionary to store frames
        self.frames = {}

        # Store user role
        self.user_role = None

        # Show welcome screen by default
        self.show_frame(screens.welcome.WelcomeScreen)

    # Initialize the frame only when it's needed
    def show_frame(self, frame_class, *args, **kwargs):
        """
        Show the given frame and pass additional arguments like user_role if necessary.
        """
        if frame_class not in self.frames:
            frame = frame_class(self, *args, **kwargs)  # Pass the args and kwargs here
            self.frames[frame_class] = frame
            frame.place(relwidth=1, relheight=1)

        frame = self.frames[frame_class]
        frame.tkraise()

    # Method to destroy frames and reinitialize necessary ones
    def reset_frames_after_login(self):
        # Destroy all frames except Welcome, Login, and SignUp
        for frame_class in list(self.frames.keys()):
            if frame_class not in [screens.welcome.WelcomeScreen, screens.login.LoginScreen,
                                   screens.signup.SignUpScreen]:
                frame = self.frames.pop(frame_class)
                frame.destroy()

        # Reinitialize necessary frames
        self.show_frame(screens.welcome.WelcomeScreen)
        self.show_frame(screens.login.LoginScreen)


app = BeachShopApp()
app.mainloop()
