# Importing module
import mysql.connector
from mysql.connector import Error


def run_query():
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="10.101.226.22",
            user="beach",
            password="beach",
            database="surfshop"
        )

        if connection.is_connected():
            print("Connected to the database")

            # Create a cursor to execute queries
            cursor = connection.cursor()

            # Example query: Retrieve all records from a table
            query = "SHOW TABLES;"
            cursor.execute(query)  # Run the query

            # Fetch all results
            results = cursor.fetchall()

            # Print the results
            for row in results:
                print(row)

    except Error as e:
        print(f"Error: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")


# Run the function
run_query()
