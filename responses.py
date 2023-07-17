import random
import json
from query import get_basic_stats

def get_server_address():
    file = open("config.json")
    data = json.load(file)
    return data["server-address"]   

def handle_response(message: str) -> str:
    p_message = message.lower()
    
    if p_message == "hello":
        return "Hey there!"
    
    if p_message == "seed":
        return str(random.randint(-9223372036854775809, 9223372036854775807)) 
    
    if p_message == "help":
        return "`This is a placeholder for help.`"
    
    if p_message == "about":
        return "`This is a placeholder for about.`"
    
    if p_message == "server":
        return get_basic_stats(get_server_address())

    return "I didn\'t understand what you wrote. Try typing \"!help\""