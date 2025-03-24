import tkinter as tk

root = tk.Tk()
root.title("Bonus")
root.geometry("660x400")
root.configure(bg="#fff7a8")

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def show_bonus_table():
    clear_screen()

    # Header
    tk.Button(root, text="Back", font=("Helvetica", 11), bg="#b9f1c0", command=root.quit).place(x=10, y=10)
    tk.Label(root, text="Bonus", font=("Helvetica", 16, "bold"), bg="#d9d6f2",
             padx=20, pady=5, relief="raised").place(relx=0.5, y=10, anchor="n")
    tk.Button(root, text="Add", font=("Helvetica", 11), bg="#ffa94d", command=show_bonus_form).place(x=590, y=10)

    # Headers
    headers = ["Employee:", "Sales:", "Gross:", "Bonus %:", "Bonus Amount:"]
    for col, header in enumerate(headers):
        tk.Label(root, text=header, font=("Helvetica", 11, "bold"), bg="#fff7a8").place(x=20 + col * 120, y=70)

    # Dummy Rows
    for row in range(6):
        for col in range(len(headers)):
            tk.Entry(root, width=14).place(x=20 + col * 120, y=100 + row * 35)

def show_bonus_form():
    clear_screen()

    # Header
    tk.Button(root, text="Back", font=("Helvetica", 11), bg="#b9f1c0", command=show_bonus_table).place(x=10, y=10)
    tk.Label(root, text="Add Bonus", font=("Helvetica", 16, "bold"), bg="#d9d6f2",
             padx=20, pady=5, relief="raised").place(relx=0.5, y=10, anchor="n")
    tk.Button(root, text="Confirm", font=("Helvetica", 11), bg="#ffa94d").place(x=580, y=10)

    # Entry fields
    tk.Label(root, text="Employee:", font=("Helvetica", 11), bg="#fff7a8").place(x=80, y=120)
    tk.Entry(root, width=25).place(x=180, y=120)

    tk.Label(root, text="Bonus %:", font=("Helvetica", 11), bg="#fff7a8").place(x=80, y=170)
    tk.Entry(root, width=25).place(x=180, y=170)

# Start GUI
show_bonus_table()
root.mainloop()
