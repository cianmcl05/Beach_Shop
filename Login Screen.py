import tkinter as tk
from PIL import Image, ImageTk

# Create main window
root = tk.Tk()
root.title("Welcome Screen")
root.geometry("500x300")
root.configure(bg="#FFF4A3")  # Light yellow background

# Load palm tree image
try:
    palm_img = Image.open("/mnt/data/palm_tree.jpg")  # Use the correct file path
    palm_img = palm_img.resize((80, 100))  # Resize to fit UI
    palm_img = ImageTk.PhotoImage(palm_img)
except Exception as e:
    print("Error loading image:", e)
    palm_img = None  # Fallback if the image fails to load

# Display palm trees
if palm_img:
    left_tree = tk.Label(root, image=palm_img, bg="#FFF4A3")
    left_tree.place(x=30, y=120)

    right_tree = tk.Label(root, image=palm_img, bg="#FFF4A3")
    right_tree.place(x=390, y=120)

# Welcome Label
welcome_label = tk.Label(
    root, text="Welcome", font=("Arial", 20, "bold"), bg="#FFF4A3", fg="black"
)
welcome_label.pack(pady=40)

# Button styles
button_style = {"font": ("Arial", 12, "bold"), "width": 10, "height": 1, "bd": 3}

# Sign-up Button
signup_button = tk.Button(
    root, text="Sign up", **button_style, bg="#B0F2C2", fg="black", relief="ridge"
)
signup_button.place(x=150, y=180)

# Login Button
login_button = tk.Button(
    root, text="Login", **button_style, bg="#EECFA3", fg="black", relief="ridge"
)
login_button.place(x=280, y=180)

# Keep reference to prevent garbage collection
root.palm_img = palm_img

# Run the GUI
root.mainloop()
