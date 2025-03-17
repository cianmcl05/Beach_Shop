import mysql.connector
from mysql.connector import Error

def connect_db():
    """Establish connection to MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="cmac2005",
            database="surfshop"
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


def insert_user(first_name, last_name, phone, email, password, role):
    """Insert a new user into the database."""
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()

            # Hash password (use actual hashing in production)
            hashed_password = password  # TODO: Use hashlib or bcrypt for real security

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

