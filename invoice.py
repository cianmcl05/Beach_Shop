import tkinter as tk

# Main window
root = tk.Tk()
root.title("Invoices")
root.geometry("750x430")
root.configure(bg="#fff7a8")

# === Helper function to clear and switch screens ===
def show_invoice_list():
    clear_screen()
    build_invoice_list()

def show_invoice_form():
    clear_screen()
    build_invoice_form()

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

# === Invoice list screen ===
def build_invoice_list():
    # Title
    title = tk.Label(root, text="Invoices", font=("Helvetica", 16, "bold"), bg="#d9d6f2", padx=20, pady=5, relief="raised")
    title.place(relx=0.5, y=15, anchor="n")

    # Back button
    back = tk.Button(root, text="Back", font=("Helvetica", 12), bg="#b9f1c0", command=root.quit)
    back.place(x=10, y=15)

    # Add button
    add = tk.Button(root, text="Add", font=("Helvetica", 12), bg="#ffa94d", command=show_invoice_form)
    add.place(x=670, y=15)

    # Table headers
    headers = ["DATE", "Invoice#", "Company", "Amount", "Paid?", "DUE", "Closed?"]
    for col, header in enumerate(headers):
        tk.Label(root, text=header, font=("Helvetica", 11, "bold"), bg="#fff7a8").place(x=20 + col * 100, y=80)

    # Empty rows
    for row in range(7):
        for col in range(len(headers)):
            tk.Entry(root, width=12).place(x=20 + col * 100, y=110 + row * 35)

# === Invoice form screen ===
def build_invoice_form():
    # Title
    title = tk.Label(root, text="Invoices", font=("Helvetica", 16, "bold"), bg="#d9d6f2", padx=20, pady=5, relief="raised")
    title.place(relx=0.5, y=15, anchor="n")

    # Back button
    back = tk.Button(root, text="Back", font=("Helvetica", 12), bg="#b9f1c0", command=show_invoice_list)
    back.place(x=10, y=15)

    # Confirm button
    confirm = tk.Button(root, text="Confirm", font=("Helvetica", 12), bg="#ffa94d")
    confirm.place(x=670, y=15)

    # Labels and entries
    tk.Label(root, text="Invoice #:", bg="#fff7a8", font=("Helvetica", 11)).place(x=50, y=80)
    tk.Entry(root, width=20).place(x=150, y=80)

    tk.Label(root, text="Company:", bg="#fff7a8", font=("Helvetica", 11)).place(x=50, y=120)
    tk.Entry(root, width=20).place(x=150, y=120)

    tk.Label(root, text="Amount:", bg="#fff7a8", font=("Helvetica", 11)).place(x=50, y=160)
    tk.Entry(root, width=20).place(x=150, y=160)

    tk.Label(root, text="DUE:", bg="#fff7a8", font=("Helvetica", 11)).place(x=50, y=200)
    tk.Entry(root, width=20).place(x=150, y=200)

    # Paid? buttons
    tk.Label(root, text="Paid:", bg="#fff7a8", font=("Helvetica", 11)).place(x=420, y=80)
    tk.Button(root, text="Yes", bg="#4CAF50", fg="white", width=5).place(x=470, y=75)
    tk.Button(root, text="No", bg="#f44336", fg="white", width=5).place(x=530, y=75)

    # Closed? buttons
    tk.Label(root, text="Closed:", bg="#fff7a8", font=("Helvetica", 11)).place(x=420, y=120)
    tk.Button(root, text="Yes", bg="#4CAF50", fg="white", width=5).place(x=470, y=115)
    tk.Button(root, text="No", bg="#f44336", fg="white", width=5).place(x=530, y=115)

# Start with invoice list view
build_invoice_list()
root.mainloop()
