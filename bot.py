import discord
import responses
import json
from discord.ext import commands

# Calls the handle response function, which will then be sent to the user, publicly or privately
async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        # If the bot's response is private, the message will be DMed, with confirmation in public channel
        if is_private:
            await message.author.send(response)
            # If the message is not sent in a public channel, do not sent a confirmation of DM
            if str(message.channel.type) != "private":
                await message.channel.send("DM sent!")
        # If the bot's response is not private, then the message will be sent in the public channel
        else: 
            await message.channel.send(response)
    except Exception as e:
        print(e)

# Getting the bot token from the config.json file
def get_token():
    file = open("config.json")
    data = json.load(file)
    return data["token"]    

# Permissions for the bot are given, and the different events in which the bot will activate are set.
def run_discord_bot():
    TOKEN = get_token()
    intents = discord.Intents.default()  
    intents.message_content = True
    client = discord.Client(intents=intents)

    # When the bot starts up, this message will be printed.
    @client.event
    async def on_ready():
        print(f"{client.user} is now running!")
    
    # When the user sends a message, the bot will send a message back.
    @client.event
    async def on_message(message):
        # Making sure the bot isn't trapped in a loop responding to itself
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said '{user_message}' ({channel})")
        if user_message[0] == "?":
            user_message = user_message[1:]
            await send_message(message, user_message, is_private = True)
        elif user_message[0] == "!":
            user_message = user_message[1:]
            await send_message(message, user_message, is_private = False)

    # The bot will activate using the given token
    client.run(TOKEN)
    