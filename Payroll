import tkinter as tk

root = tk.Tk()
root.title("Pay")
root.geometry("500x300")
root.configure(bg="#fff7a8")

# Switch helper
def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def show_payroll_list():
    clear_screen()
    build_payroll_list()

def show_payroll_form():
    clear_screen()
    build_payroll_form()

# === Payroll List View ===
def build_payroll_list():
    # Top buttons and title
    tk.Button(root, text="Back", font=("Helvetica", 11), bg="#b9f1c0", command=root.quit).place(x=10, y=10)
    tk.Label(root, text="Pay", font=("Helvetica", 16, "bold"), bg="#d9d6f2", padx=20, pady=5, relief="raised").place(relx=0.5, y=10, anchor="n")
    tk.Button(root, text="Add", font=("Helvetica", 11), bg="#ffa94d", command=show_payroll_form).place(x=430, y=10)

    # Table headers
    headers = ["Date:", "Employee:", "Pay Amount:"]
    for col, header in enumerate(headers):
        tk.Label(root, text=header, font=("Helvetica", 11, "bold"), bg="#fff7a8").place(x=30 + col * 140, y=60)

    # Dummy rows
    for row in range(3):
        for col in range(len(headers)):
            tk.Entry(root, width=18).place(x=30 + col * 140, y=90 + row * 35)

# === Payroll Form View ===
def build_payroll_form():
    tk.Button(root, text="Back", font=("Helvetica", 11), bg="#b9f1c0", command=show_payroll_list).place(x=10, y=10)
    tk.Label(root, text="Pay", font=("Helvetica", 16, "bold"), bg="#d9d6f2", padx=20, pady=5, relief="raised").place(relx=0.5, y=10, anchor="n")
    tk.Button(root, text="Confirm", font=("Helvetica", 11), bg="#ffa94d").place(x=410, y=10)

    # Form labels + entries
    tk.Label(root, text="Employee:", bg="#fff7a8", font=("Helvetica", 11)).place(x=50, y=80)
    tk.Entry(root, width=25).place(x=140, y=80)

    tk.Label(root, text="Amount:", bg="#fff7a8", font=("Helvetica", 11)).place(x=50, y=120)
    tk.Entry(root, width=25).place(x=140, y=120)

# Launch app with payroll list view
build_payroll_list()
root.mainloop()
