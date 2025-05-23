import mysql.connector
from mysql.connector import Error
from datetime import datetime, date
from decimal import Decimal
from datetime import datetime, timedelta


# connects to sql database
def connect_db():
    """Establish connection to MySQL database."""
    try:
        # put in correct details
        connection = mysql.connector.connect(
            host="localhost",
            user="beach",
            password="beach",
            database="surfshop"
        )
        print("connection")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


# inserts users into database for signing up
def insert_user(first_name, last_name, phone, email, password, role, store_id):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()

            full_name = f'{first_name} {last_name}'
            query = """INSERT INTO Employee (Name, Phone, Email, role, password, StoreID) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            values = (full_name, phone, email, role, password, store_id)

            cursor.execute(query, values)
            connection.commit()
            print("User registered successfully!")

        except Error as e:
            print(f"Database error: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("fail")



def clock_in(emp_id, store_id):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            today = date.today()

            # Check if employee already clocked in today
            check_query = """
                SELECT ID FROM Employee_Time 
                WHERE EmpID = %s AND DATE(ClockIn) = %s
            """
            cursor.execute(check_query, (emp_id, today))
            result = cursor.fetchone()
            if result:
                print("Already clocked in today.")
                return None  # Already clocked in

            # Insert new clock-in record with StoreID
            now = datetime.now()
            insert_query = """
                INSERT INTO Employee_Time (EmpID, ClockIn, ClockOut, StoreID)
                VALUES (%s, %s, %s, %s)
            """
            # initially ClockOut = ClockIn
            cursor.execute(insert_query, (emp_id, now, now, store_id))
            connection.commit()
            return cursor.lastrowid

        except Error as e:
            print(f"Clock-in error: {e}")
        finally:
            cursor.close()
            connection.close()
    return None


def clock_out(record_id):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            now = datetime.now()
            query = """UPDATE Employee_Time SET ClockOut = %s WHERE ID = %s"""
            cursor.execute(query, (now, record_id))
            connection.commit()
        except Error as e:
            print(f"Clock-out error: {e}")
        finally:
            cursor.close()
            connection.close()

def get_latest_time_record(emp_id):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT ID, ClockIn, ClockOut
                FROM Employee_Time
                WHERE EmpID = %s
                ORDER BY ClockIn DESC
                LIMIT 1
            """
            cursor.execute(query, (emp_id,))
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "clock_in": row[1], "clock_out": row[2]}
        except Error as e:
            print(f"Get latest time record error: {e}")
        finally:
            cursor.close()
            connection.close()
    return None

def has_clocked_in_today(emp_id):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            today = datetime.now().date()
            query = """
                SELECT COUNT(*) FROM Employee_Time
                WHERE EmpID = %s AND DATE(ClockIn) = %s
            """
            cursor.execute(query, (emp_id, today))
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            print(f"Clock-in check error: {e}")
        finally:
            cursor.close()
            connection.close()
    return False

def update_register_amounts(record_id, reg_in, reg_out):
    connection = connect_db()
    try:
        cursor = connection.cursor()
        query = """
            UPDATE Employee_Time
            SET Register_In = %s, Register_Out = %s
            WHERE ID = %s
        """
        cursor.execute(query, (reg_in, reg_out, record_id))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print("Error updating register amounts:", e)
        return False


def insert_end_of_day_sales(reg, credit, cash_in_envelope, emp_id, store_id):
    connection = connect_db()
    if not connection:
        return False

    try:
        cursor = connection.cursor()

        # Check if there's already a row for today and store
        today_start = datetime.combine(date.today(), datetime.min.time())
        today_end = datetime.combine(date.today(), datetime.max.time())

        select_query = """
            SELECT Date FROM End_of_Day_Sales
            WHERE Date BETWEEN %s AND %s AND StoreID = %s
        """
        cursor.execute(select_query, (today_start, today_end, store_id))
        existing = cursor.fetchone()

        if existing:
            # Update existing record
            update_query = """
                UPDATE End_of_Day_Sales
                SET Reg = %s, Credit = %s, Cash_in_Envelope = %s, EmpID = %s
                WHERE Date BETWEEN %s AND %s AND StoreID = %s
            """
            cursor.execute(update_query, (reg, credit, cash_in_envelope, emp_id, today_start, today_end, store_id))
        else:
            # Insert new record
            insert_query = """
                INSERT INTO End_of_Day_Sales (Date, Reg, Credit, Cash_in_Envelope, EmpID, StoreID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            now = datetime.now()
            cursor.execute(insert_query, (now, reg, credit, cash_in_envelope, emp_id, store_id))

        connection.commit()
        return True

    except Error as e:
        print(f"Error inserting/updating sales record: {e}")
        return False

    finally:
        cursor.close()
        connection.close()



def insert_expense(expense_type, value, payment_method_binary, emp_id=None, store_id=None):
    connection = connect_db()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        now = datetime.now()

        # Calculate tax (e.g., 7%)
        tax = round(value * 0.07, 2)

        # Determine payment method
        cash = value if payment_method_binary == 0 else 0.00
        credit = value if payment_method_binary == 1 else 0.00

        insert_query = """
            INSERT INTO Expenses (Type, Value, Date, EmpID, Tax, Cash, Credit, StoreID)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (expense_type, value, now, emp_id, tax, cash, credit, store_id)

        cursor.execute(insert_query, values)
        connection.commit()
        return True

    except Error as e:
        print(f"Error inserting expense: {e}")
        return False

    finally:
        cursor.close()
        connection.close()

def get_store_name_by_id(store_id):
    connection = connect_db()
    if not connection:
        return None

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT Store_Name FROM Store WHERE Store_ID = %s", (store_id,))
        result = cursor.fetchone()
        return result[0] if result else None

    except Exception as e:
        print(f"Error fetching store name: {e}")
        return None

    finally:
        cursor.close()
        connection.close()



def update_expense(expense_id, expense_type, value, payment_method_binary):
    connection = connect_db()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        cash = 1 if payment_method_binary == 0 else 0.00
        credit = 1 if payment_method_binary == 1 else 0.00

        query = """
        UPDATE Expenses
        SET Type = %s, Value = %s, Cash = %s, Credit = %s
        WHERE ID = %s
        """
        cursor.execute(query, (expense_type, value, cash, credit, expense_id))
        connection.commit()
        return True
    except Exception as e:
        print("Error updating expense:", e)
        return False
    finally:
        cursor.close()
        connection.close()

def delete_expense(expense_id):
    connection = connect_db()
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Expenses WHERE ID = %s", (expense_id,))
        connection.commit()
    except Exception as e:
        print("Error deleting expense:", e)
    finally:
        cursor.close()
        connection.close()


def get_all_invoices():
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT InvoiceNumber, Company, Amount, Payment_Status, Due_Date, Company_Status, Payment_Type
                FROM Invoice
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print("Error fetching invoices:", e)
        finally:
            cursor.close()
            connection.close()
    return []

def insert_invoice(invoice_number, company, amount, payment_status, due_date, company_status, payment_type, store_id=None):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO Invoice (InvoiceNumber, Company, Amount, Payment_Status, Due_Date, Company_Status, Payment_Type, StoreID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (invoice_number, company, amount, payment_status, due_date, company_status, payment_type, store_id)
            cursor.execute(query, values)
            connection.commit()
        except Error as e:
            print("Error inserting invoice:", e)
        finally:
            cursor.close()
            connection.close()

def update_invoice(invoice_number, company, amount, payment_status, due_date, company_status, payment_type):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                UPDATE Invoice
                SET Company=%s, Amount=%s, Payment_Status=%s, Due_Date=%s,
                    Company_Status=%s, Payment_Type=%s
                WHERE InvoiceNumber=%s
            """
            values = (company, amount, payment_status, due_date, company_status, payment_type, invoice_number)
            cursor.execute(query, values)
            connection.commit()
        except Error as e:
            print("Update error:", e)
        finally:
            cursor.close()
            connection.close()

def delete_invoice(invoice_number):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Invoice WHERE InvoiceNumber = %s", (invoice_number,))
            connection.commit()
        except Error as e:
            print("Delete error:", e)
        finally:
            cursor.close()
            connection.close()

def get_all_employees():
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT Name, Phone, Email, Role, Email, Password FROM Employee")
            return cursor.fetchall()
        except Error as e:
            print("Error fetching employees:", e)
        finally:
            cursor.close()
            connection.close()
    return []

def get_all_employees_with_store():
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT E.Name, E.Phone, E.Email, E.Role, S.Store_Name, E.Password
                FROM Employee E
                LEFT JOIN Store S ON E.StoreID = S.Store_ID
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print("Error fetching employees:", e)
        finally:
            cursor.close()
            connection.close()
    return []

def delete_employee(email):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Employee WHERE Email = %s", (email,))
            connection.commit()
        except Error as e:
            print("Error deleting employee:", e)
        finally:
            cursor.close()
            connection.close()

def update_employee(email, name, phone, role, store_id, password):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                UPDATE Employee
                SET Name=%s, Phone=%s, Role=%s, StoreID=%s, Password=%s
                WHERE Email=%s
            """
            cursor.execute(query, (name, phone, role, store_id, password, email))
            connection.commit()
        except Error as e:
            print("Error updating employee:", e)
        finally:
            cursor.close()
            connection.close()

def get_all_stores():
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT Store_ID, Store_Name FROM Store")
            return cursor.fetchall()
        except Error as e:
            print("Error fetching stores:", e)
        finally:
            cursor.close()
            connection.close()
    return []

def get_all_merchandise():
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT M.ID, M.Merch_Type, M.Merch_Value, M.Purchase_Date, S.Store_Name
                FROM Merchandise M
                LEFT JOIN Store S ON M.StoreID = S.Store_ID
            """)
            return cursor.fetchall()
        except Error as e:
            print("Error fetching merchandise:", e)
        finally:
            cursor.close()
            connection.close()
    return []

def insert_merchandise(merch_type, merch_value, purchase_date, store_id):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO Merchandise (Merch_Type, Merch_Value, Purchase_Date, StoreID)
                VALUES (%s, %s, %s, %s)
            """, (merch_type, merch_value, purchase_date, store_id))
            connection.commit()
        except Error as e:
            print("Error inserting merchandise:", e)
        finally:
            cursor.close()
            connection.close()

def delete_merchandise(merch_id):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Merchandise WHERE ID = %s", (merch_id,))
            connection.commit()
        except Error as e:
            print("Error deleting merchandise:", e)
        finally:
            cursor.close()
            connection.close()

def get_all_stores():
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT Store_ID, Store_Name FROM Store")
            return cursor.fetchall()
        except Error as e:
            print("Error fetching stores:", e)
        finally:
            cursor.close()
            connection.close()
    return []

def insert_store(name, location):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO Store (Store_Name, Location) VALUES (%s, %s)"
            cursor.execute(query, (name, location))
            connection.commit()
        except Error as e:
            print("Error inserting store:", e)
        finally:
            cursor.close()
            connection.close()

def get_all_stores():
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT Store_ID, Store_Name FROM Store")
            return cursor.fetchall()
        except Error as e:
            print("Error fetching stores:", e)
        finally:
            cursor.close()
            connection.close()
    return []

def get_full_store_list():
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT Store_ID, Store_Name, Location FROM Store")
            return cursor.fetchall()
        except Error as e:
            print("Error getting store list:", e)
        finally:
            cursor.close()
            connection.close()
    return []

def update_merchandise(merch_id, merch_type, merch_value, purchase_date, store_id):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE Merchandise
                       SET Merch_Type = %s, Merch_Value = %s, Purchase_Date = %s, StoreID = %s
                       WHERE ID = %s"""
            cursor.execute(query, (merch_type, merch_value, purchase_date, store_id, merch_id))
            connection.commit()
        except Error as e:
            print("Error updating merchandise:", e)
        finally:
            cursor.close()
            connection.close()

def update_store(store_id, name, location):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE Store SET Store_Name = %s, Location = %s WHERE Store_ID = %s",
                           (name, location, store_id))
            connection.commit()
        except Error as e:
            print("Error updating store:", e)
        finally:
            cursor.close()
            connection.close()

def delete_store(store_id):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()

            # Check if any employees, merchandise, or invoices reference this store
            check_query = """
                SELECT EXISTS (
                    SELECT 1 FROM Employee WHERE StoreID = %s
                    UNION
                    SELECT 1 FROM Merchandise WHERE StoreID = %s
                    UNION
                    SELECT 1 FROM Invoice WHERE StoreID = %s
                )
            """
            cursor.execute(check_query, (store_id, store_id, store_id))
            in_use = cursor.fetchone()[0]

            if in_use:
                print(f"Store ID {store_id} is still in use and cannot be deleted.")
                return "in_use"

            cursor.execute("DELETE FROM Store WHERE Store_ID = %s", (store_id,))
            connection.commit()
            return "deleted"

        except Error as e:
            print("Error deleting store:", e)
            return "error"
        finally:
            cursor.close()
            connection.close()

def get_all_employees():
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT ID, Name FROM Employee")
            return cursor.fetchall()
        except:
            return []
        finally:
            cursor.close()
            connection.close()

def get_all_payroll():
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT Payroll.ID, Payroll.Date, Employee.Name, Payroll.Payroll
                FROM Payroll
                JOIN Employee ON Payroll.EmpID = Employee.ID
                ORDER BY Payroll.Date DESC
            """
            cursor.execute(query)
            return cursor.fetchall()
        except:
            return []
        finally:
            cursor.close()
            connection.close()

def insert_payroll(pay_date, emp_id, amount, store_id):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Payroll (Date, EmpID, Payroll, StoreID) VALUES (%s, %s, %s, %s)",
                (pay_date, emp_id, amount, store_id)
            )
            connection.commit()
        except Exception as e:
            print("Payroll insert error:", e)
        finally:
            cursor.close()
            connection.close()


def update_payroll(payroll_id, emp_id, amount):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            query = "UPDATE Payroll SET EmpID = %s, Payroll = %s WHERE ID = %s"
            cursor.execute(query, (emp_id, amount, payroll_id))
            connection.commit()
        except Exception as e:
            print("Error updating payroll:", e)
        finally:
            cursor.close()
            connection.close()

def delete_payroll(payroll_id):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Payroll WHERE ID = %s", (payroll_id,))
            connection.commit()
        except Exception as e:
            print("Error deleting payroll:", e)
        finally:
            cursor.close()
            connection.close()

def get_store_expense_summary(store_id):
    connection = connect_db()
    if not connection:
        return None
    try:
        cursor = connection.cursor()
        query = """
            SELECT
                SUM(Value) AS Total,
                SUM(Cash) AS TotalCash,
                SUM(Credit) AS TotalCredit
            FROM Expenses
            WHERE StoreID = %s
        """
        cursor.execute(query, (store_id,))
        return cursor.fetchone()  # returns (Total, TotalCash, TotalCredit)
    except Exception as e:
        print("Error fetching expense summary:", e)
        return None
    finally:
        cursor.close()
        connection.close()

def get_employee_weekly_gross_summary(start_date, end_date):
    connection = connect_db()
    if not connection:
        return []

    try:
        cursor = connection.cursor()
        query = """
            SELECT e.Name, SUM(et.Register_Out - et.Register_In) AS WeeklySales, e.ID
            FROM Employee_Time et
            JOIN Employee e ON et.EmpID = e.ID
            WHERE DATE(et.ClockIn) BETWEEN %s AND %s
            GROUP BY e.ID
        """
        cursor.execute(query, (start_date, end_date))
        # List of tuples: (Name, Gross, EmpID)
        return cursor.fetchall()
    except Exception as e:
        print("Error getting weekly gross summary:", e)
        return []
    finally:
        cursor.close()
        connection.close()

def get_all_employee_names():
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT ID, Name FROM Employee")
            # Returns list of (ID, Name)
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()
    return []

def get_all_bonuses():
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT Employee.Name, Bonus.Sales, Bonus.Gross, Bonus.Bonus_Percentage, Bonus.Bonus_Amount
                FROM Bonus
                JOIN Employee ON Bonus.EmpID = Employee.ID
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()
    return []

def insert_bonus(emp_id, bonus_amount, sales, gross, bonus_pct):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            insert_query = """
                INSERT INTO Bonus (EmpID, Bonus_Amount, Sales, Gross, Bonus_Percentage, Current_Bonus_Percentage)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (emp_id, bonus_amount, sales, gross, bonus_pct, bonus_pct))
            connection.commit()
            print("Bonus inserted successfully.")
        except Exception as e:
            print("Error inserting bonus:", e)
        finally:
            cursor.close()
            connection.close()
def get_all_bonuses(include_id=False):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            if include_id:
                query = """
                    SELECT BonusID, Employee.Name, Sales, Gross, Bonus_Percentage, Bonus_Amount
                    FROM Bonus
                    JOIN Employee ON Bonus.EmpID = Employee.ID
                    ORDER BY BonusID DESC
                """
            else:
                query = """
                    SELECT Employee.Name, Sales, Gross, Bonus_Percentage, Bonus_Amount
                    FROM Bonus
                    JOIN Employee ON Bonus.EmpID = Employee.ID
                    ORDER BY BonusID DESC
                """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print("Error fetching bonuses:", e)
            return []
        finally:
            cursor.close()
            connection.close()
    return []

def delete_bonus(bonus_id):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Bonus WHERE BonusID = %s", (bonus_id,))
            connection.commit()
            return True
        except Exception as e:
            print("Error deleting bonus:", e)
            return False
        finally:
            cursor.close()
            connection.close()

def get_bonus_history_for_employee(emp_id):
    connection = connect_db()
    if not connection:
        return []

    try:
        cursor = connection.cursor()
        query = """
            SELECT CreatedAt, Sales, Gross, Bonus_Percentage, Bonus_Amount
            FROM Bonus
            WHERE EmpID = %s
            ORDER BY CreatedAt DESC
        """
        cursor.execute(query, (emp_id,))
        return cursor.fetchall()
    except Exception as e:
        print("Error fetching bonus history:", e)
        return []
    finally:
        cursor.close()
        connection.close()

def get_summary_data(month, year):
    connection = connect_db()
    if not connection:
        return None

    try:
        cursor = connection.cursor()

        # Set date range for the given month
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)

        # Opening Balance: pull from previous month net profit if exists
        cursor.execute("""
            SELECT Net_Profit FROM Summary_Balance 
            WHERE Month = %s AND Year = %s
        """, (month - 1 if month > 1 else 12, year if month > 1 else year - 1))
        opening_balance = cursor.fetchone()
        opening_balance = opening_balance[0] if opening_balance else Decimal("0.00")

        # Total End of Day Reg (Cash), Credit
        cursor.execute("""
            SELECT COALESCE(SUM(Reg), 0), COALESCE(SUM(Credit), 0)
            FROM End_of_Day_Sales
            WHERE Date >= %s AND Date < %s
        """, (start_date, end_date))
        total_cash, total_credit = cursor.fetchone()

        # Total Expenses
        cursor.execute("""
            SELECT COALESCE(SUM(Value), 0)
            FROM Expenses
            WHERE Date >= %s AND Date < %s
        """, (start_date, end_date))
        total_expenses = cursor.fetchone()[0]

        # Total Merchandise
        cursor.execute("""
            SELECT COALESCE(SUM(Merch_Value), 0)
            FROM Merchandise
            WHERE Purchase_Date >= %s AND Purchase_Date < %s
        """, (start_date, end_date))
        total_merch = cursor.fetchone()[0]

        # Total Payroll
        cursor.execute("""
            SELECT COALESCE(SUM(Payroll), 0)
            FROM Payroll
            WHERE Date >= %s AND Date < %s
        """, (start_date, end_date))
        total_payroll = cursor.fetchone()[0]

        # Total Withdrawals
        cursor.execute("""
            SELECT COALESCE(SUM(Amount), 0)
            FROM Withdrawals
            WHERE Date >= %s AND Date < %s
        """, (start_date, end_date))
        total_withdrawals = cursor.fetchone()[0]

        # Net Profit = sales - expenses - merch - payroll
        net_profit = total_cash + total_credit - total_expenses - total_merch - total_payroll

        # Current Balance = opening + net - withdrawals
        current_balance = opening_balance + net_profit - total_withdrawals

        # Actual Cash = cash - payroll
        actual_cash = total_cash - total_payroll

        # Actual Credit = credit - merch - expenses
        actual_credit = total_credit - total_merch - total_expenses

        # Actual Total = cash + credit
        actual_total = actual_cash + actual_credit

        # Sales tax report: credit + (cash * 0.2), rounded to nearest 5
        sales_tax = total_credit + (total_cash * Decimal("0.2"))
        sales_tax = round(sales_tax / Decimal("5.0")) * Decimal("5.0")

        return {
            "net_profit": net_profit,
            "opening_balance": opening_balance,
            "current_balance": current_balance,
            "withdrawals": total_withdrawals,
            "actual_cash": actual_cash,
            "actual_credit": actual_credit,
            "actual_total": actual_total,
            "sales_tax": sales_tax
        }

    except Error as e:
        print("Summary error:", e)
        return None
    finally:
        cursor.close()
        connection.close()

def generate_summary_report(year, month):
    summary = get_summary_data(month, year)
    if not summary:
        return None

    # Save result to persistent summary table
    try:
        connection = connect_db()
        if not connection:
            return None

        cursor = connection.cursor()

        insert_query = """
            INSERT INTO Summary_Balance (Month, Year, Opening_Balance, Net_Profit, Current_Balance)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                Opening_Balance = VALUES(Opening_Balance),
                Net_Profit = VALUES(Net_Profit),
                Current_Balance = VALUES(Current_Balance)
        """
        cursor.execute(insert_query, (
            month,
            year,
            summary["opening_balance"],
            summary["net_profit"],
            summary["current_balance"]
        ))
        connection.commit()
        return summary

    except Exception as e:
        print("Error generating summary report:", e)
        return None
    finally:
        cursor.close()
        connection.close()

from datetime import datetime
from decimal import Decimal

def insert_withdrawal(amount, owner_name):
    connection = connect_db()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        today = datetime.now().date()
        query = """
            INSERT INTO Withdrawals (Date, Amount, OwnerName)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (today, amount, owner_name))
        connection.commit()
        return True
    except Exception as e:
        print("Error inserting withdrawal:", e)
        return False
    finally:
        cursor.close()
        connection.close()

def get_all_withdrawals():
    connection = connect_db()
    withdrawals = []
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT Date, Amount, OwnerName FROM Withdrawals ORDER BY Date DESC")
            withdrawals = cursor.fetchall()
        except Exception as e:
            print("Error fetching withdrawals:", e)
        finally:
            cursor.close()
            connection.close()
    return withdrawals

def get_current_available_balance():
    today = datetime.today()
    month, year = today.month, today.year

    connection = connect_db()
    if not connection:
        return Decimal("0.00")

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Current_Balance
            FROM Summary_Balance
            WHERE Month = %s AND Year = %s
        """, (month, year))
        result = cursor.fetchone()
        return result[0] if result else Decimal("0.00")
    except Exception as e:
        print("Error fetching available balance:", e)
        return Decimal("0.00")
    finally:
        cursor.close()
        connection.close()

def get_current_user_name(emp_id):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT Name FROM Employee WHERE ID = %s", (emp_id,))
            result = cursor.fetchone()
            return result[0] if result else "Unknown"
        except Exception as e:
            print("Error fetching user name:", e)
        finally:
            cursor.close()
            connection.close()
    return "Unknown"

def insert_withdrawal(amount, owner_name):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            today = datetime.now().date()

            # Insert the withdrawal
            insert_query = "INSERT INTO Withdrawals (Date, Amount, OwnerName) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (today, amount, owner_name))

            # Get current month/year
            month = today.month
            year = today.year

            # Update the summary table by subtracting the withdrawal from current balance
            update_query = """
                UPDATE Summary_Balance
                SET Current_Balance = Current_Balance - %s
                WHERE Month = %s AND Year = %s
            """
            cursor.execute(update_query, (amount, month, year))

            connection.commit()
            return True
        except Exception as e:
            print("Error inserting withdrawal:", e)
            return False
        finally:
            cursor.close()
            connection.close()
    return False

def get_current_balance():
    connection = connect_db()
    if not connection:
        return 0.00

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Current_Balance
            FROM Summary_Balance
            ORDER BY Year DESC, Month DESC
            LIMIT 1
        """)
        result = cursor.fetchone()
        return float(result[0]) if result else 0.00

    except Exception as e:
        print("Error fetching current balance:", e)
        return 0.00
    finally:
        cursor.close()
        connection.close()

def get_employee_activity_log():
    connection = connect_db()
    if not connection:
        return [], []

    try:
        cursor = connection.cursor()

        # Clock-in/out with register data
        clock_query = """
            SELECT 
                DAYNAME(ClockIn) AS Day,
                DATE(ClockIn) AS Date,
                e.Name AS Employee,
                ClockIn,
                ClockOut,
                Register_In,
                Register_Out
            FROM Employee_Time et
            JOIN Employee e ON et.EmpID = e.ID
            ORDER BY ClockIn DESC
        """

        # Daily entry logs (one per day)
        input_query = """
            SELECT 
                eods.Date AS Timestamp,
                DAYNAME(eods.Date) AS Day,
                DATE(eods.Date) AS Date,
                eods.Reg - eods.Credit AS Cash,
                eods.Credit AS Credit,
                ex.Type AS ExpenseType,
                ex.Value AS ExpenseValue,
                e.Name AS PayrollName,
                pr.Payroll AS PayrollAmount
            FROM End_of_Day_Sales eods
            LEFT JOIN Expenses ex ON DATE(eods.Date) = ex.Date
            LEFT JOIN Payroll pr ON DATE(eods.Date) = pr.Date
            LEFT JOIN Employee e ON pr.EmpID = e.ID
            ORDER BY eods.Date DESC
        """

        cursor.execute(clock_query)
        clock_data = cursor.fetchall()

        cursor.execute(input_query)
        input_data = cursor.fetchall()

        return clock_data, input_data

    except Exception as e:
        print("Error fetching employee activity log:", e)
        return [], []

    finally:
        cursor.close()
        connection.close()

def get_employee_activity_log_filtered(emp_name_filter="All", week_filter="All", user_role="manager"):
    connection = connect_db()
    if not connection:
        return [], [], [], []

    try:
        cursor = connection.cursor()

        # Parse week range if applicable
        week_start = None
        week_end = None
        if week_filter not in ["All", "", None]:
            parts = week_filter.split("to")
            if len(parts) == 2:
                week_start = datetime.strptime(parts[0].strip(), "%Y-%m-%d").strftime("%Y-%m-%d")
                week_end = datetime.strptime(parts[1].strip(), "%Y-%m-%d").strftime("%Y-%m-%d")

        # Restrict to current month for manager role
        if user_role == "manager":
            now = datetime.now()
            first_day = now.replace(day=1).strftime("%Y-%m-%d")
            last_day = (now.replace(month=now.month % 12 + 1, day=1) - timedelta(days=1)).strftime("%Y-%m-%d")
            if not week_start or not week_end:
                week_start, week_end = first_day, last_day

        # CLOCK LOG QUERY
        clock_query = """
            SELECT 
                DAYNAME(et.ClockIn) AS Day,
                DATE(et.ClockIn) AS Date,
                e.Name AS Employee,
                s.Store_Name AS Store,
                et.ClockIn,
                et.ClockOut,
                et.Register_In,
                et.Register_Out
            FROM Employee_Time et
            JOIN Employee e ON et.EmpID = e.ID
            LEFT JOIN Store s ON et.StoreID = s.Store_ID
        """
        clock_filters = []
        clock_params = []

        if emp_name_filter not in ["All", "", None]:
            clock_filters.append("e.Name = %s")
            clock_params.append(emp_name_filter)

        if week_start and week_end:
            clock_filters.append("DATE(et.ClockIn) BETWEEN %s AND %s")
            clock_params.extend([week_start, week_end])

        if clock_filters:
            clock_query += " WHERE " + " AND ".join(clock_filters)
        clock_query += " ORDER BY et.ClockIn DESC"
        cursor.execute(clock_query, tuple(clock_params))
        clock_data = cursor.fetchall()

        # INPUT LOG QUERY
        input_query = """
            SELECT 
                COALESCE(eods.Date, pr.Date, ex.Date) AS Timestamp,
                DAYNAME(COALESCE(eods.Date, pr.Date, ex.Date)) AS Day,
                COALESCE(eods.Date, pr.Date, ex.Date) AS Date,
                e.Name AS Employee,
                COALESCE(s.Store_Name, s2.Store_Name, s3.Store_Name) AS Store,
                IFNULL(eods.Reg - eods.Credit, 0) AS Cash,
                IFNULL(eods.Credit, 0) AS Credit,
                ex.Type AS ExpenseType,
                ex.Value AS ExpenseValue,
                e.Name AS PayrollName,
                pr.Payroll AS PayrollAmount
            FROM Employee e
            LEFT JOIN End_of_Day_Sales eods ON eods.EmpID = e.ID
            LEFT JOIN Store s ON eods.StoreID = s.Store_ID
            LEFT JOIN Payroll pr ON pr.EmpID = e.ID
            LEFT JOIN Store s2 ON s2.Store_ID = (
                SELECT StoreID FROM End_of_Day_Sales 
                WHERE EmpID = e.ID AND DATE(Date) = DATE(pr.Date) LIMIT 1
            )
            LEFT JOIN Expenses ex ON ex.EmpID = e.ID
            LEFT JOIN Store s3 ON ex.StoreID = s3.Store_ID
        """
        input_filters = []
        input_params = []

        if emp_name_filter not in ["All", "", None]:
            input_filters.append("e.Name = %s")
            input_params.append(emp_name_filter)

        if week_start and week_end:
            input_filters.append("DATE(COALESCE(eods.Date, pr.Date, ex.Date)) BETWEEN %s AND %s")
            input_params.extend([week_start, week_end])

        if input_filters:
            input_query += " WHERE " + " AND ".join(input_filters)
        input_query += " ORDER BY Timestamp DESC"
        cursor.execute(input_query, tuple(input_params))
        input_data = cursor.fetchall()

        # Week ranges
        cursor.execute("SELECT DISTINCT DATE(ClockIn) FROM Employee_Time ORDER BY DATE(ClockIn) DESC")
        all_dates = sorted(set(row[0] for row in cursor.fetchall()))
        weeks = []
        seen = set()
        for d in all_dates:
            start = d - timedelta(days=d.weekday())
            end = start + timedelta(days=6)
            label = f"{start} to {end}"
            if label not in seen:
                weeks.append(label)
                seen.add(label)

        # Distinct employees
        cursor.execute("SELECT DISTINCT Name FROM Employee")
        emp_names = [row[0] for row in cursor.fetchall()]

        return clock_data, input_data, emp_names, weeks

    except Exception as e:
        print("Error fetching filtered employee activity logs:", e)
        return [], [], [], []

    finally:
        cursor.close()
        connection.close()




