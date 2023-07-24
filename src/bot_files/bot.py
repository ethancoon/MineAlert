# Standard library imports
import json
import random
# Third party imports
import discord
from discord.ext import commands
from mcipc.query import Client
import requests
# Local application imports


# Making sure the bot has the right permissions, and then creating the bot with the specified command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", description = "A simple Discord bot for a Minecraft server", intents = intents)

# When the bot is initialized this message will be output into the terminal
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID:{bot.user.id})")

# Whenever a user sends a message, this message will be logged in the terminal
@bot.event
async def on_message(message):
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f"{username} said '{user_message}' (Channel: {channel})")
    # If this is not included, the bot will be unable to respond to a command if it is loggging the message
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send("Hey there!")

# Randomly generates a Minecraft seed between the lowest and highest possible seed values
@bot.command()
async def seed(ctx):
    await ctx.send(str(random.randint(-9223372036854775808, 9223372036854775807)))

@bot.command()
async def about(ctx):
    await ctx.send("`This bot was originally created to help keep my friends updated on the status of our server. If you have any questions or concerns, please reach out to me: https://github.com/ethancoon`")

# Will return information on the Minecraft server
@bot.command()
async def serverinfo(ctx):
    def get_server_address():
        file = open("config.json")
        data = json.load(file)
        return data["server-address"]   
    def get_server_port():
        file = open("config.json")
        data = json.load(file)
        return data["server-port"]
    server_address = get_server_address()
    server_port = get_server_port()
    async with ctx.typing():
        try:
            # Using the query protocol to communicate with the server through the IP and port
            with Client(server_address, int(server_port), timeout = 10) as client:
                full_stats = client.stats(full=True)
            # Turning the stats into a JSON-ish dictionary
            full_stats = dict(full_stats)
            # Creating an embed for Discord
            embed = discord.Embed(
                title = "Minecraft Server Info",
                description = f"""
                IP: {full_stats['host_ip']}
                Description: {full_stats['host_name']} 
                Version: {full_stats['version']} 
                Online Players: {full_stats['players']}
                Max Players: {full_stats['max_players']}
                Plugins: {full_stats['plugins']}
                """,
                color = discord.Color.dark_blue()
            )
            
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft/images/f/fe/GrassNew.png/revision/latest/scale-to-width-down/250?cb=20190903234415")
            await ctx.send(embed = embed)
        except Exception as e:
            print(e)
            await ctx.send("The server is offline or I am searching the wrong address :(")    

# Securely loading the bot token
def get_token():
    file = open("config.json")
    data = json.load(file)
    return data["token"]

# Activating the bot
bot.run(get_token())