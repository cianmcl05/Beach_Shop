import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import sql_connection
import screens.manager_view
import screens.owner_view

class EmployeeActivityScreen(tk.Frame):
    """
    Displays logs of employee clock-ins/outs, register activity, sales, expenses, and payroll.
    Allows filtering by employee and week, and refreshing data.
    """
    def __init__(self, master, user_role="manager"):
        super().__init__(master, bg="#FFF4A3")
        self.master = master
        self.user_role = user_role

        # Title label
        tk.Label(
            self,
            text="Employee Activity Log",
            font=("Helvetica", 16, "bold"),
            bg="#d9d6f2",
            padx=20,
            pady=5,
            relief="raised"
        ).pack(pady=10)

        # Create filtering controls
        self.create_filter_section()

        # Section for clock-in/out and register logs
        tk.Label(
            self,
            text="Clock-In/Out and Register Activity",
            font=("Helvetica", 14, "bold"),
            bg="#FFF4A3"
        ).pack(pady=(10, 5))
        self.tree1 = self.create_table([
            "Day", "Date", "Employee", "Store",
            "Clock-in", "Clock-out", "In-Balance", "Out-Balance"
        ])

        # Section for sales, expenses, and payroll logs
        tk.Label(
            self,
            text="Daily Sales, Expense, and Payroll Activity",
            font=("Helvetica", 14, "bold"),
            bg="#FFF4A3"
        ).pack(pady=(20, 5))
        self.tree2 = self.create_table([
            "Timestamp", "Day", "Date", "Employee", "Store",
            "Cash", "Credit", "Expense Type", "Expense Value",
            "Payroll Name", "Payroll Amount"
        ])

        # Navigation buttons below tables
        self.create_buttons()

        # Load initial data into tables
        self.load_data()

    def create_filter_section(self):
        """
        Build the filter controls for selecting an employee and a week.
        """
        filter_frame = tk.Frame(self, bg="#FFF4A3")
        filter_frame.pack(pady=5)

        # Employee filter dropdown
        tk.Label(
            filter_frame,
            text="Filter by Employee:",
            font=("Helvetica", 12),
            bg="#FFF4A3"
        ).grid(row=0, column=0, padx=5)
        self.emp_var = tk.StringVar()
        self.emp_dropdown = ttk.Combobox(
            filter_frame,
            textvariable=self.emp_var,
            state="readonly",
            width=20
        )
        self.emp_dropdown.grid(row=0, column=1, padx=5)

        # Week filter dropdown
        tk.Label(
            filter_frame,
            text="Filter by Week:",
            font=("Helvetica", 12),
            bg="#FFF4A3"
        ).grid(row=0, column=2, padx=5)
        self.week_var = tk.StringVar()
        self.week_dropdown = ttk.Combobox(
            filter_frame,
            textvariable=self.week_var,
            state="readonly",
            width=25
        )
        self.week_dropdown.grid(row=0, column=3, padx=5)

        # Apply filter button
        tk.Button(
            filter_frame,
            text="Apply Filters",
            font=("Helvetica", 11, "bold"),
            bg="#A4E4A0",
            command=self.load_data
        ).grid(row=0, column=4, padx=10)

    def create_table(self, columns):
        """
        Create a Treeview table with the given column headings.
        Returns the Treeview widget.
        """
        frame = tk.Frame(self, bg="#FFF4A3")
        frame.pack(pady=5)
        tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )
        # Configure each column width and heading
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130)
        tree.pack()
        return tree

    def load_data(self):
        """
        Fetch filtered data from the database and populate both tables.
        Updates employee and week dropdown values.
        """
        # Clear existing rows
        self.tree1.delete(*self.tree1.get_children())
        self.tree2.delete(*self.tree2.get_children())

        emp_filter = self.emp_var.get()
        week_filter = self.week_var.get()

        try:
            # Fetch data and dropdown options from SQL layer
            clock_data, input_data, emp_names, week_labels = \
                sql_connection.get_employee_activity_log_filtered(
                    emp_name_filter=emp_filter,
                    week_filter=week_filter,
                    user_role=self.user_role
                )

            # Populate employee filter dropdown
            self.emp_dropdown["values"] = ["All"] + emp_names
            if not self.emp_var.get():
                self.emp_dropdown.set("All")

            # Populate week filter dropdown
            self.week_dropdown["values"] = ["All"] + week_labels
            if not self.week_var.get():
                self.week_dropdown.set("All")

            # Insert clock-in/out records
            for day, date_raw, emp, store, clock_in_raw, clock_out_raw, reg_in, reg_out in clock_data:
                clock_in = datetime.strptime(str(clock_in_raw), "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S")
                clock_out = datetime.strptime(str(clock_out_raw), "%Y-%m-%d %H:%M:%S").strftime("%H:%M:%S")
                self.tree1.insert(
                    "", "end",
                    values=(day, date_raw, emp, store, clock_in, clock_out, reg_in, reg_out)
                )

            # Insert sales, expense, and payroll records
            for (timestamp_raw, day, date_raw, emp, store,
                 cash, credit, ex_type, ex_value,
                 pay_name, pay_amt) in input_data:

                # Format timestamp and date
                try:
                    timestamp_fmt = datetime.strptime(str(timestamp_raw),
                        "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    timestamp_fmt = str(timestamp_raw)
                try:
                    date_fmt = str(date_raw).split(" ")[0]
                except Exception:
                    date_fmt = str(date_raw)

                # Only show rows with meaningful values
                if (cash != 0 or credit != 0
                    or ex_type not in (None, '', 'None')
                    or ex_value not in (None, '', 'None')
                    or pay_amt not in (None, '', 'None', 0)):
                    self.tree2.insert(
                        "", "end",
                        values=(
                            timestamp_fmt, day, date_fmt, emp, store,
                            cash, credit, ex_type, ex_value, pay_name, pay_amt
                        )
                    )

        except Exception as e:
            # Log error and inform the user
            print("Error loading activity data:", e)
            messagebox.showerror(
                "Error",
                "Could not load employee activity data."
            )

    def create_buttons(self):
        """
        Create Back and Refresh buttons below the tables.
        """
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=10)

        # Determine destination frame based on user role
        back_cmd = lambda: self.master.show_frame(
            screens.manager_view.ManagerView
            if self.user_role == "manager"
            else screens.owner_view.OwnerView
        )

        # Back button
        tk.Button(
            button_frame,
            text="Back",
            font=("Helvetica", 12, "bold"),
            width=10,
            bg="#A4E4A0",
            command=back_cmd
        ).pack(side="left", padx=10)

        # Refresh button reloads the data
        tk.Button(
            button_frame,
            text="Refresh",
            font=("Helvetica", 12, "bold"),
            width=10,
            bg="#E58A2C",
            command=self.load_data
        ).pack(side="left", padx=10)
