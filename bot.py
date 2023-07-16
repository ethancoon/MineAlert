import discord
import responses
import json

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
    
def run_discord_bot():
    TOKEN = get_token()

def get_token():
    file = open("config.json")
    data = json.load(file)
    return data["token"]
    