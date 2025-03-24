import tkinter as tk
from tkinter import ttk


def show_inventory_screen():
    clear_screen()
    header_label.config(text="Merchandise Inventory")
    add_button.config(text="Add", command=show_add_screen)
    back_button.config(command=root.quit)

    # Table Headers
    columns = ["Date", "Day", "Merch Type", "Merch Value", "Total Merch"]
    for i, col in enumerate(columns):
        label = tk.Label(table_frame, text=col, font=("Arial", 10, "bold"), bg="#FFF4A3", borderwidth=1, relief="solid")
        label.grid(row=0, column=i, padx=2, pady=2, sticky="nsew")

    # Table Rows (Empty for now)
    for r in range(1, 6):  # 5 empty rows
        for c in range(5):
            entry = tk.Entry(table_frame, font=("Arial", 10), borderwidth=1, relief="solid", width=13)
            entry.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")


def show_add_screen():
    clear_screen()
    header_label.config(text="Merchandise Inventory")
    add_button.config(text="Confirm", command=show_inventory_screen)
    back_button.config(command=show_inventory_screen)

    tk.Label(table_frame, text="Merch Type:", font=("Arial", 12), bg="#FFF4A3").grid(row=0, column=0, padx=10, pady=5,
                                                                                     sticky="w")
    merch_type_entry = tk.Entry(table_frame, font=("Arial", 12), width=20)
    merch_type_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    tk.Label(table_frame, text="Merch Value:", font=("Arial", 12), bg="#FFF4A3").grid(row=1, column=0, padx=10, pady=5,
                                                                                      sticky="w")
    merch_value_entry = tk.Entry(table_frame, font=("Arial", 12), width=20)
    merch_value_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")


def clear_screen():
    for widget in table_frame.winfo_children():
        widget.destroy()


def create_gui():
    global root, header_label, add_button, back_button, table_frame
    root = tk.Tk()
    root.title("Merchandise Inventory")
    root.geometry("500x300")
    root.configure(bg="#FFF4A3")

    # Header Label
    header_label = tk.Label(root, text="Merchandise Inventory", font=("Arial", 16, "bold"), bg="#FFF4A3", fg="black")
    header_label.pack(pady=10)

    # Buttons Frame
    button_frame = tk.Frame(root, bg="#FFF4A3")
    button_frame.pack()

    back_button = tk.Button(button_frame, text="Back", font=("Arial", 12, "bold"), width=10, height=1,
                            bg="#B0F2C2", fg="black", relief="ridge", command=root.quit)
    back_button.pack(side=tk.LEFT, padx=10)

    add_button = tk.Button(button_frame, text="Add", font=("Arial", 12, "bold"), width=10, height=1,
                           bg="#EECFA3", fg="black", relief="ridge", command=show_add_screen)
    add_button.pack(side=tk.RIGHT, padx=10)

    # Table Frame
    table_frame = tk.Frame(root, bg="#FFF4A3", padx=5, pady=5)
    table_frame.pack(pady=10, fill="both", expand=True)

    show_inventory_screen()
    root.mainloop()


if __name__ == "__main__":
    create_gui()
