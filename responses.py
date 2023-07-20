import random
import json
from query import query_basic_stats, query_advanced_stats

# Opening the config.json to get the server address
def get_server_address():
    file = open("config.json")
    data = json.load(file)
    return data["server-address"]

# Opening the config.json to get the server  port
def get_server_port():
    file = open("config.json")
    data = json.load(file)
    return data["server-port"]   

# The function that determines the appropriate response for a given command by the user
def handle_response(message: str) -> str:
    # Parsing the string to make sure the command can be interpreted
    p_message = message.lower()
    
    if p_message == "hello":
        return "Hey there!"
    
    if p_message == "seed":
        return str(random.randint(-9223372036854775808, 9223372036854775807)) 
    
    if p_message == "help":
        return "`This is a placeholder for help.`"
    
    if p_message == "about":
        return "`This is a placeholder for about.`"
    
    if p_message == "server" or p_message == "serverbasic":
        return query_basic_stats(get_server_address(), get_server_port())
    
    if p_message == "serveradvanced":
        return query_advanced_stats(get_server_address(), get_server_port())

    # If the user sends an invalid command, this message will be returned.
    return "I didn\'t understand what you wrote. Try typing \"!help\""