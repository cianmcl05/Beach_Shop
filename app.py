# use this code to run app
import tkinter as tk
import screens.welcome
import screens.login
import screens.signup


# main app class
class BeachShopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Welcome Screen")
        self.geometry("500x450")
        self.configure(bg="#FFF4A3")

        # Dictionary to store frames
        self.frames = {}

        # Initialize screens
        for F in (screens.welcome.WelcomeScreen, screens.login.LoginScreen, screens.signup.SignUpScreen,
                  screens.emp_view.EmployeeView, screens.manager_view.ManagerView, screens.owner_view.OwnerView):
            frame = F(self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        # Show welcome screen by default
        self.show_frame(screens.welcome.WelcomeScreen)

    # brings specific screen to the front
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()


# runs the app
app = BeachShopApp()
app.mainloop()
