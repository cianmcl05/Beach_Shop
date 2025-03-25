import tkinter as tk
import screens.manager_view

class PayrollScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#fff7a8")
        self.master = master
        self.build_payroll_list()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_payroll_list(self):
        self.clear_screen()
        self.build_payroll_list()

    def show_payroll_form(self):
        self.clear_screen()
        self.build_payroll_form()

    def build_payroll_list(self):
        # Top buttons and title
        button_frame = tk.Frame(self, bg="#fff7a8")
        button_frame.place(x=10, y=10)

        tk.Button(button_frame, text="Back", font=("Helvetica", 12, "bold"), width=10, height=1, bg="#A4E4A0",
                  fg="black", relief="ridge",
                  command=lambda: self.master.show_frame(screens.manager_view.ManagerView)).pack(side="left", padx=10)

        tk.Label(self, text="Pay", font=("Helvetica", 16, "bold"), bg="#d9d6f2",
                 padx=20, pady=5, relief="raised").place(relx=0.5, y=10, anchor="n")
        tk.Button(self, text="Add", font=("Helvetica", 11), bg="#ffa94d",
                  command=self.show_payroll_form).place(x=430, y=10)

        # Table headers
        headers = ["Date:", "Employee:", "Pay Amount:"]
        for col, header in enumerate(headers):
            tk.Label(self, text=header, font=("Helvetica", 11, "bold"), bg="#fff7a8").place(x=30 + col * 140, y=60)

        # Dummy rows
        for row in range(3):
            for col in range(len(headers)):
                tk.Entry(self, width=18).place(x=30 + col * 140, y=90 + row * 35)

    def build_payroll_form(self):
        tk.Button(self, text="Back", font=("Helvetica", 11), bg="#b9f1c0",
                  command=self.show_payroll_list).place(x=10, y=10)
        tk.Label(self, text="Pay", font=("Helvetica", 16, "bold"), bg="#d9d6f2",
                 padx=20, pady=5, relief="raised").place(relx=0.5, y=10, anchor="n")
        tk.Button(self, text="Confirm", font=("Helvetica", 11), bg="#ffa94d").place(x=410, y=10)

        # Form labels + entries
        tk.Label(self, text="Employee:", bg="#fff7a8", font=("Helvetica", 11)).place(x=50, y=80)
        tk.Entry(self, width=25).place(x=140, y=80)

        tk.Label(self, text="Amount:", bg="#fff7a8", font=("Helvetica", 11)).place(x=50, y=120)
        tk.Entry(self, width=25).place(x=140, y=120)
