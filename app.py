import tkinter as tk
import screens.welcome
import screens.login
import screens.signup


class BeachShopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Welcome Screen")
        self.geometry("500x450")
        self.configure(bg="#FFF4A3")

        self.frames = {}  # Dictionary to store frames

        # Initialize screens
        for F in (screens.welcome.WelcomeScreen, screens.login.LoginScreen, screens.signup.SignUpScreen):
            frame = F(self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(screens.welcome.WelcomeScreen)  # Show welcome screen by default

    def show_frame(self, frame_class):
        """Raise a given frame to the front."""
        frame = self.frames[frame_class]
        frame.tkraise()


app = BeachShopApp()
app.mainloop()
