import tkinter as tk
from tkinter import ttk

def go_back():
    print("Back button clicked")

# Create the main window
root = tk.Tk()
root.title("Employees")
root.configure(bg="lightyellow")

# Header label
header_label = tk.Label(root, text="Employees", bg="lightyellow", font=("Arial", 14, "bold"), relief="ridge", padx=10, pady=5)
header_label.grid(row=0, column=1, columnspan=6, pady=5)

# Back button
back_button = tk.Button(root, text="Back", bg="lightgreen", font=("Arial", 10, "bold"), command=go_back)
back_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

# Column headers
columns = ["Name", "Phone", "Email", "Role", "Username", "Password"]
for i, col in enumerate(columns):
    label = tk.Label(root, text=col + ":", bg="lightyellow", font=("Arial", 10, "bold"))
    label.grid(row=1, column=i, padx=5, pady=5)

# Create empty rows for employee data
num_rows = 5  # Change this to add more rows
entries = []
for row in range(num_rows):
    row_entries = []
    for col in range(len(columns)):
        entry = ttk.Entry(root, width=18)
        entry.grid(row=row+2, column=col, padx=5, pady=5)
        row_entries.append(entry)
    entries.append(row_entries)

# Run the Tkinter event loop
root.mainloop()
