import tkinter as tk

root = tk.Tk()
root.title("Withdraw")
root.geometry("500x300")
root.configure(bg="#fff7a8")

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def show_withdraw_table():
    clear_screen()
    # Title + Buttons
    tk.Label(root, text="Withdraw", font=("Helvetica", 16, "bold"),
             bg="#d9d6f2", padx=20, pady=5, relief="raised").place(relx=0.5, y=10, anchor="n")
    tk.Button(root, text="Back", font=("Helvetica", 11), bg="#b9f1c0", command=root.quit).place(x=10, y=10)
    tk.Button(root, text="Save", font=("Helvetica", 11), bg="#ffa94d", command=show_withdraw_form).place(x=420, y=10)

    # Table headers
    headers = ["Date", "Amount Withdrew", "Owner Name:"]
    for col, header in enumerate(headers):
        tk.Label(root, text=header, font=("Helvetica", 11, "bold"), bg="#fff7a8").place(x=30 + col * 140, y=70)

    # Sample empty rows
    for row in range(3):
        for col in range(len(headers)):
            tk.Entry(root, width=18).place(x=30 + col * 140, y=100 + row * 35)

def show_withdraw_form():
    clear_screen()
    # Title + Buttons
    tk.Label(root, text="Withdraw", font=("Helvetica", 16, "bold"),
             bg="#d9d6f2", padx=20, pady=5, relief="raised").place(relx=0.5, y=10, anchor="n")
    tk.Button(root, text="Back", font=("Helvetica", 11), bg="#b9f1c0", command=show_withdraw_table).place(x=10, y=10)
    tk.Button(root, text="Confirm", font=("Helvetica", 11), bg="#ffa94d").place(x=400, y=10)

    # Amount entry
    tk.Label(root, text="Amount:", font=("Helvetica", 11), bg="#fff7a8").place(x=60, y=100)
    tk.Entry(root, width=25).place(x=140, y=100)

# Start with withdraw table
show_withdraw_table()
root.mainloop()
