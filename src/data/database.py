# Standard library imports
import os

# Third-party imports
from dotenv import load_dotenv
import mysql.connector as mysql

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
def insert_on_guild_join(guild_id: int, guild_name: str, num_members: int) -> None:
    try:
        # Establish the connection
        connection = mysql.connect(**connection_parameters)
        # If the connection is established, execute the query
        cursor = connection.cursor()
        query = "SELECT id FROM guilds WHERE id = %s"
        cursor.execute(query, [guild_id])
        guild_info_exists = cursor.fetchall()
        # If the guild info exists, update the guild info, otherwise insert the guild info
        if guild_info_exists:
            query = "UPDATE guilds SET guild_name = %s, num_members = %s WHERE id = %s"
            cursor.execute(query, [guild_name, num_members, guild_id])
        else:
            query = "INSERT INTO guilds (id, guild_name, num_members) VALUES (%s, %s, %s)"
            cursor.execute(query, [guild_id, guild_name, num_members])
            query = "INSERT INTO minecraft_servers (guild_id) VALUES (%s)"
            cursor.execute(query, [guild_id])
        # Commit the changes to the database
        connection.commit()
        print("Executed")
        # Close the connection
        cursor.close()
        connection.close()
        print("Connection closed")
    except mysql.Error as e:
        print(f"Failed to insert data: {e}")


def get_guild_data_for_all_guilds() -> list:
    try:
        # Establish the connection
        connection = mysql.connect(**connection_parameters)
        # If the connection is established, execute the query
        cursor = connection.cursor()
        query = "SELECT id, guild_name FROM guilds"
        cursor.execute(query)
        print("Executed")
        # Fetch the data from the database
        result = cursor.fetchall()
        # Close the connection
        cursor.close()
        connection.close()
        print("Connection closed")
        return result
    except mysql.Error as e:
        print(f"get_guild_data_for_all_guilds failed to read data: {e}")


def get_server_id_from_guild_id(guild_id: int) -> int:
    try:
        # Establish the connection
        connection = mysql.connect(**connection_parameters)
        # If the connection is established, execute the query
        cursor = connection.cursor()
        query = "SELECT id FROM minecraft_servers WHERE guild_id = %s"
        cursor.execute(query, [guild_id])
        print("Executed")
        # Fetch the data from the database
        result = cursor.fetchall()
        # Close the connection
        cursor.close()
        connection.close()
        print("Connection closed")
        return result[0][0]
    except mysql.Error as e:
        print(f"get_server_id_from_guild_id failed to read data: {e}")


def get_coords_from_server_id(server_id: int) -> list:
    try:
        # Establish the connection
        connection = mysql.connect(**connection_parameters)
        # If the connection is established, execute the query
        cursor = connection.cursor()
        query = "SELECT name, x, y, z FROM minecraft_coordinates WHERE server_id = %s"
        cursor.execute(query, [server_id])
        print("Executed")
        # Fetch the data from the database
        result = cursor.fetchall()
        # Close the connection
        cursor.close()
        connection.close()
        print("Connection closed")
        return result
    except mysql.Error as e:
        print(f"get_coords_from_server_id failed to read data: {e}")


def get_server_name_from_guild_id(guild_id: int) -> str:
    try:
        # Establish the connection
        connection = mysql.connect(**connection_parameters)
        # If the connection is established, execute the query
        cursor = connection.cursor()
        query = "SELECT name FROM minecraft_servers WHERE guild_id = %s"
        cursor.execute(query, [guild_id])
        # Fetch the data from the database
        result = cursor.fetchall()
        # Close the connection
        cursor.close()
        connection.close()
        return result[0][0]
    except mysql.Error as e:
        print(f"get_server_name_from_guild_id failed to read data: {e}")

def get_minecraft_server_data_from_guild_id(guild_id: int, column: str) -> str:
    try:
        # Establish the connection
        connection = mysql.connect(**connection_parameters)
        # If the connection is established, execute the query
        cursor = connection.cursor()
        query = f"SELECT {column} FROM minecraft_servers WHERE guild_id = %s"
        cursor.execute(query, [guild_id])
        # Fetch the data from the database
        result = cursor.fetchall()
        # Close the connection
        cursor.close()
        connection.close()
        return result[0][0]
    except mysql.Error as e:
        print(f"get_minecraft_server_settings_from_guild_id failed to read data: {e}")

def get_alerts_enabled_from_guild_id(guild_id: int) -> bool:
    try:
        # Establish the connection
        connection = mysql.connect(**connection_parameters)
        # If the connection is established, execute the query
        cursor = connection.cursor()
        query = "SELECT alerts_enabled FROM minecraft_servers WHERE guild_id = %s"
        cursor.execute(query, [guild_id])
        # Fetch the data from the database
        result = cursor.fetchall()
        # Close the connection
        cursor.close()
        connection.close()
        return result[0][0]
    except mysql.Error as e:
        print(f"get_alerts_enabled_from_guild_id failed to read data: {e}")

def add_coords_to_db(guild_id: int, values: list) -> None:
    try:
        # Establish the connection
        connection = mysql.connect(**connection_parameters)
        # If the connection is established, execute the query
        cursor = connection.cursor()
        server_id = get_server_id_from_guild_id(guild_id)
        if values[2] == None:
            # Remove the y coordinate if it is None
            values.pop(2) 
            query = f"INSERT INTO minecraft_coordinates (server_id, name, x, z, created_by) VALUES (%s, %s, %s, %s, %s)"
        else:
            query = f"INSERT INTO minecraft_coordinates (server_id, name, x, y, z, created_by) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, [server_id] + values)
        # Commit the changes to the database
        connection.commit()
        print("Executed")
        # Close the connection
        cursor.close()
        connection.close()
        print("Connection closed")
    except mysql.Error as e:
        print(f"add_coords_to_db failed to insert data: {e}")

def delete_coords_from_db(guild_id: int, coords_name: str) -> None:
    try:
        # Establish the connection
        connection = mysql.connect(**connection_parameters)
        # If the connection is established, execute the query
        cursor = connection.cursor()
        server_id = get_server_id_from_guild_id(guild_id)
        query = f"DELETE FROM minecraft_coordinates WHERE server_id = %s AND name = %s"
        cursor.execute(query, [server_id, coords_name])
        # Commit the changes to the database
        connection.commit()
        print("Executed")
        # Close the connection
        cursor.close()
        connection.close()
        print("Connection closed")
    except mysql.Error as e:
        print(f"delete_coords_from_db failed to delete data: {e}")


def update_minecraft_server_table(guild_id = int, column = str, value = str) -> None:
    try:
        # Establish the connection
        connection = mysql.connect(**connection_parameters)
        # If the connection is established, execute the query
        cursor = connection.cursor()
        query = f"UPDATE minecraft_servers SET {column} = %s WHERE guild_id = %s"
        cursor.execute(query, [value, guild_id])
        # Commit the changes to the database
        connection.commit()
        print("Executed")
        # Close the connection
        cursor.close()
        connection.close()
        print("Connection closed")
    except mysql.Error as e:
        print(f"update_minecraft_server_table failed to update data: {e}")
    