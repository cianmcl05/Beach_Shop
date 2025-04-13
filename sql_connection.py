import mysql.connector
from mysql.connector import Error
from datetime import datetime, date



# connects to sql database
def connect_db():
    """Establish connection to MySQL database."""
    try:
        # put in correct details
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="cmac2005",
            database="surfshop"
        )
        print("connection")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


# inserts users into database for signing up
def insert_user(first_name, last_name, phone, email, password, role):
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()

            # Hash password (use actual hashing in production)
            hashed_password = password

            query = """INSERT INTO Employee (Name, Phone, Email, role, password) 
                       VALUES (%s, %s, %s, %s, %s)"""
            values = (f'{first_name} {last_name}', phone, email, role, hashed_password)

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


def clock_in(emp_id):
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

            # Insert new clock-in record
            now = datetime.now()
            insert_query = """INSERT INTO Employee_Time (EmpID, ClockIn, ClockOut) VALUES (%s, %s, %s)"""
            cursor.execute(insert_query, (emp_id, now, now))  # initially ClockOut = ClockIn
            connection.commit()
            return cursor.lastrowid  # return the new record's ID

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


def insert_end_of_day_sales(reg, credit, cash_in_envelope, emp_id):
    connection = connect_db()
    if not connection:
        return False

    try:
        cursor = connection.cursor()

        # Check if there's already a row for today
        today_start = datetime.combine(date.today(), datetime.min.time())
        today_end = datetime.combine(date.today(), datetime.max.time())

        select_query = """
            SELECT Date FROM End_of_Day_Sales
            WHERE Date BETWEEN %s AND %s
        """
        cursor.execute(select_query, (today_start, today_end))
        existing = cursor.fetchone()

        if existing:
            # Update existing record
            update_query = """
                UPDATE End_of_Day_Sales
                SET Reg = %s, Credit = %s, Cash_in_Envelope = %s, EmpID = %s
                WHERE Date BETWEEN %s AND %s
            """
            cursor.execute(update_query, (reg, credit, cash_in_envelope, emp_id, today_start, today_end))
        else:
            # Insert new record
            insert_query = """
                INSERT INTO End_of_Day_Sales (Date, Reg, Credit, Cash_in_Envelope, EmpID)
                VALUES (%s, %s, %s, %s, %s)
            """
            now = datetime.now()
            cursor.execute(insert_query, (now, reg, credit, cash_in_envelope, emp_id))

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
        today = date.today()

        # Assign cash/credit value based on binary method
        cash = 1 if payment_method_binary == 0 else 0.00
        credit = 1 if payment_method_binary == 1 else 0.00

        insert_query = """
            INSERT INTO Expenses (Type, Value, Date, EmpID, Tax, Cash, Credit, StoreID)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (expense_type, value, today, emp_id, 0.00, cash, credit, store_id)
        cursor.execute(insert_query, values)
        connection.commit()
        return True

    except Error as e:
        print(f"Error inserting expense: {e}")
        return False

    finally:
        cursor.close()
        connection.close()
