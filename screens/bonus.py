import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import sql_connection
import screens.manager_view
import screens.owner_view

class Bonus(tk.Frame):
    """Frame for managing employee bonuses."""
    def __init__(self, master, user_role):
        super().__init__(master, bg="#FFF4A3")
        self.master = master
        self.user_role = user_role

        # Map employee names to their IDs for dropdowns and lookups
        self.emp_map = {
            name: eid
            for eid, name in sql_connection.get_all_employee_names()
        }
        # Will hold the current table data for filtering
        self.full_data = []

        # Title label
        tk.Label(
            self,
            text="Bonus",
            font=("Helvetica", 16, "bold"),
            bg="#d9d6f2",
            padx=20,
            pady=5,
            relief="raised"
        ).pack(pady=10)

        # Table container
        self.table_frame = tk.Frame(self, bg="#FFF4A3")
        self.table_frame.pack(pady=10)

        # Define and populate the bonus table
        columns = ("BonusID", "Employee", "Sales", "Gross", "Bonus %", "Bonus Amount")
        self.tree = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings"
        )
        for col in columns:
            # Hide the ID column from view by setting width to zero
            width = 0 if col == "BonusID" else 120
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        self.tree.pack()

        # Double-click to edit the Bonus % cell
        self.tree.bind("<Double-1>", self.on_tree_double_click)

        # Create the action buttons and filter controls
        self.create_buttons(master)

        # Auto-generate button below the table
        tk.Button(
            self,
            text="Auto-Generate Weekly Gross",
            font=("Helvetica", 12, "bold"),
            width=25,
            bg="#A4E4A0",
            command=self.auto_generate_weekly_gross
        ).pack(pady=5)

        # Initially load all bonuses
        self.load_bonuses()

    def create_buttons(self, master):
        """Set up the Back, Refresh, Confirm, Delete, and filter controls."""
        button_frame = tk.Frame(self, bg="#FFF4A3")
        button_frame.pack(pady=5)

        # Decide which view to return to based on role
        back_cmd = lambda: master.show_frame(
            screens.manager_view.ManagerView
            if self.user_role == "manager"
            else screens.owner_view.OwnerView
        )

        # Navigation and table actions
        tk.Button(
            button_frame,
            text="Back",
            font=("Helvetica", 12, "bold"),
            width=10,
            bg="#A4E4A0",
            command=back_cmd
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Refresh",
            font=("Helvetica", 12, "bold"),
            width=10,
            bg="#E58A2C",
            command=self.load_bonuses
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Confirm Selected",
            font=("Helvetica", 12, "bold"),
            width=15,
            bg="#CFCFCF",
            command=self.confirm_selected_bonus
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Delete",
            font=("Helvetica", 12, "bold"),
            width=10,
            bg="#F27474",
            command=self.delete_selected_bonus
        ).pack(side="left", padx=10)

        # Filter controls
        filter_frame = tk.Frame(self, bg="#FFF4A3")
        filter_frame.pack(pady=5)

        tk.Label(
            filter_frame,
            text="Filter by Employee:",
            font=("Helvetica", 12),
            bg="#FFF4A3"
        ).pack(side="left", padx=5)

        # Dropdown to select a specific employee or "All"
        self.filter_var = tk.StringVar()
        emp_names = ["All"] + list(self.emp_map.keys())
        self.filter_dropdown = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=emp_names,
            state="readonly",
            font=("Helvetica", 12),
            width=20
        )
        self.filter_dropdown.pack(side="left", padx=5)
        self.filter_dropdown.current(0)

        tk.Button(
            filter_frame,
            text="Apply Filter",
            font=("Helvetica", 12),
            bg="#A4E4A0",
            command=self.apply_filter
        ).pack(side="left", padx=10)

    def auto_generate_weekly_gross(self):
        """
        Calculate and display each employee’s gross sales
        for the current week (Monday–Sunday).
        """
        # Clear existing rows
        self.tree.delete(*self.tree.get_children())

        # Determine this week’s date range
        today = datetime.now()
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)

        # Get weekly summaries from the database
        summaries = sql_connection.get_employee_weekly_gross_summary(
            monday.date(),
            sunday.date()
        )
        self.full_data = []

        # Insert a row per employee
        for emp_name, sales_total, emp_id in summaries:
            row = (
                "",  # placeholder for BonusID
                emp_name,
                f"{sales_total:.2f}",
                f"{sales_total:.2f}",
                "",  # placeholder for Bonus %
                ""   # placeholder for Bonus Amount
            )
            self.tree.insert("", "end", values=row)
            self.full_data.append(row)

    def load_bonuses(self):
        """Fetch all bonuses and display them in the table."""
        self.tree.delete(*self.tree.get_children())
        rows = sql_connection.get_all_bonuses(include_id=True)
        self.full_data = []

        # Format each database row for display
        for bonus_id, name, sales, gross, percent, amount in rows:
            row = (
                bonus_id,
                name,
                f"{sales:.2f}",
                f"{gross:.2f}",
                f"{percent:.2f}%",
                f"${amount:.2f}"
            )
            self.tree.insert("", "end", values=row)
            self.full_data.append(row)

    def confirm_selected_bonus(self):
        """Save the entered bonus % and calculate final bonus amount."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a bonus row to confirm.")
            return

        values = self.tree.item(selected[0])["values"]
        emp_name = values[1]
        sales = float(values[2])
        gross = float(values[3])
        percent_str = self.tree.set(selected[0], "Bonus %").replace('%', '').strip()

        if not percent_str:
            messagebox.showwarning("Missing Bonus %", "Please enter a bonus percentage.")
            return

        try:
            bonus_pct = float(percent_str)
            # Round bonus amount to nearest multiple of 5
            bonus_amount = round((gross * bonus_pct) / 100 / 5) * 5
            emp_id = self.emp_map.get(emp_name)

            # Insert into database with today’s date
            bonus_date = datetime.now().date()
            sql_connection.insert_bonus(
                emp_id,
                bonus_amount,
                sales,
                gross,
                bonus_pct,
                bonus_date
            )

            # Update table display
            self.tree.set(selected[0], "Bonus Amount", f"${bonus_amount:.2f}")
            self.tree.set(selected[0], "Bonus %", f"{bonus_pct:.2f}%")
            messagebox.showinfo("Saved", f"Bonus for {emp_name} saved.")
        except Exception:
            messagebox.showerror("Error", "Invalid input. Please check the values.")

    def delete_selected_bonus(self):
        """Delete the selected bonus from the database and table."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a bonus to delete.")
            return

        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this bonus?"):
            return

        bonus_id = self.tree.set(selected[0], "BonusID")
        success = sql_connection.delete_bonus(bonus_id)
        if success:
            self.tree.delete(selected[0])
            messagebox.showinfo("Deleted", "Bonus successfully deleted.")
        else:
            messagebox.showerror("Error", "Failed to delete bonus.")

    def on_tree_double_click(self, event):
        """
        Allow inline editing of the 'Bonus %' cell on double-click.
        Opens an Entry widget over that cell.
        """
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = self.tree.identify_column(event.x)
        row_id = self.tree.identify_row(event.y)
        # Only allow editing in the Bonus % column (#5)
        if not row_id or column != "#5":
            return

        x, y, width, height = self.tree.bbox(row_id, column)
        value = self.tree.set(row_id, column)

        # Create an entry overlay
        entry = tk.Entry(self.tree, font=("Helvetica", 12), width=10)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value.replace('%', '').strip())
        entry.focus()

        def save_value(event):
            new_val = entry.get()
            try:
                pct = float(new_val)
                self.tree.set(row_id, column, f"{pct:.2f}%")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number.")
            entry.destroy()

        entry.bind("<Return>", save_value)
        entry.bind("<FocusOut>", save_value)

    def apply_filter(self):
        """Refresh the table to show only bonuses for the chosen employee."""
        selected_name = self.filter_var.get()
        self.tree.delete(*self.tree.get_children())

        rows = sql_connection.get_all_bonuses(include_id=True)
        for bonus_id, name, sales, gross, percent, amount in rows:
            if selected_name == "All" or selected_name == name:
                self.tree.insert("", "end", values=(
                    bonus_id,
                    name,
                    f"{sales:.2f}",
                    f"{gross:.2f}",
                    f"{percent:.2f}%",
                    f"${amount:.2f}"
                ))
