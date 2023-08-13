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

# Function to insert info to the database on server join
def insert_on_guild_join(guild_id: int, guild_name: str, num_members: int):
    try:
        # Establish the connection
        connection = mariadb.connect(**connection_parameters)
        # If the connection is established, execute the query
        cursor = connection.cursor()
        query = "SELECT guild_id FROM guilds WHERE guild_id = ?"
        guild_info_exists = cursor.execute(query, [guild_id])
        if guild_info_exists:
            query = "UPDATE guilds SET guild_name = ?, num_members = ? WHERE guild_id = ?"
            cursor.execute(query, [guild_name, num_members, guild_id])
        else:
            query = "INSERT INTO guilds (guild_id, guild_name, num_members) VALUES (?, ?, ?)"
            cursor.execute(query, [guild_id, guild_name, num_members])
            query = "INSERT INTO minecraft_servers (guild_id) VALUES (?)"
            cursor.execute(query, [guild_id])
        # Commit the changes to the database
        connection.commit()
        print("Executed")
        # Close the connection
        cursor.close()
        connection.close()
        print("Connection closed")
    except mariadb.Error as e:
        print(f"Failed to insert data: {e}")


def get_server_id_from_guild_id(guild_id: int):
    try:
        # Establish the connection
        connection = mariadb.connect(**connection_parameters)
        # If the connection is established, execute the query
        cursor = connection.cursor()
        query = "SELECT id FROM minecraft_servers WHERE guild_id = ?"
        cursor.execute(query, [guild_id])
        # Fetch the data from the database
        result = cursor.fetchall()
        # Close the connection
        cursor.close()
        connection.close()
        
        print(result[0][0])
        return result[0][0]
    except mariadb.Error as e:
        print(f"get_server_id_from_guild_id failed to read data: {e}")


def get_coords_from_server_id(server_id: int):
    try:
        # Establish the connection
        connection = mariadb.connect(**connection_parameters)
        # If the connection is established, execute the query
        cursor = connection.cursor()
        query = "SELECT name, x, y, z FROM minecraft_coordinates WHERE server_id = ?"
        cursor.execute(query, [server_id])
        # Fetch the data from the database
        result = cursor.fetchall()
        # Close the connection
        cursor.close()
        connection.close()
        return result
    except mariadb.Error as e:
        print(f"get_coords_from_server_id failed to read data: {e}")


def add_coords_to_db(guild_id: int, values: list):
    try:
        # Establish the connection
        connection = mariadb.connect(**connection_parameters)
        # If the connection is established, execute the query
        cursor = connection.cursor()
        server_id = get_server_id_from_guild_id(guild_id)
        query = f"INSERT INTO minecraft_coordinates (server_id, name, x, y, z, created_by) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(query, [server_id] + values)
        # Commit the changes to the database
        connection.commit()
        print("Executed")
        # Close the connection
        cursor.close()
        connection.close()
        print("Connection closed")
    except mariadb.Error as e:
        print(f"add_coords_to_db failed to insert data: {e}")

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