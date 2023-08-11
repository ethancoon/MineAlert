# Standard library imports
import os

# Third-party imports
from dotenv import load_dotenv
import mariadb

# Loading the environmental variables in the .env file
load_dotenv()

# Database connection parameters
connection_parameters = {
    "user" : os.getenv("DB_USER"),
    "password" : os.getenv("DB_PASSWORD"),
    "host" : os.getenv("DB_HOST"),
    "database" : os.getenv("DB_NAME"),
}

# Function to insert new data into the database
def insert_to_db(table: str, columns: list, values: list):
    try:
        # Establish the connection
        connection = mariadb.connect(**connection_parameters)
        # If the connection is established, execute the query
        cursor = connection.cursor()
        columns = ", ".join(columns)
        values_placeholder = ", ".join(["%s"] * len(values))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values_placeholder})"
        cursor.execute(query, values)
        # Commit the changes to the database
        connection.commit()
        print("Executed")
        # Close the connection
        cursor.close()
        connection.close()
        print("Connection closed")
    except mariadb.Error as e:
        print(f"Failed to insert data: {e}")
