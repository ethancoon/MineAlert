# Standard library imports
import json
import random
# Third party imports
import discord
from discord.ext import commands, tasks
from mcipc.query import Client
import requests
# Local application imports


# Making sure the bot has the right permissions, and then creating the bot with the specified command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", description = "A simple Discord bot for a Minecraft server", intents = intents)

# Config options for the bot. Location will be updated
server_address = "ip"
server_port = 25565

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
    async with ctx.typing():
        full_stats, online = query_server(server_address, server_port())
        if online:
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
        else:
            await ctx.send("The server is offline or I am searching the wrong address :(")    

# Command to begin the task of monitoring the server
@bot.command()
async def serverstatus(ctx):
    check_server_status.start(ctx)
    print("Task started!")
    await ctx.send("Checking now! This may take a few seconds...")

@bot.command()
async def setip(ctx, ip):
    global server_address
    server_address = str(ip).lower()
    await ctx.send(f"The Minecraft server IP address is now {server_address}")

@bot.command()
async def setport(ctx, port):
    global server_port
    server_port = int(port)
    await ctx.send(f"The Minecraft server port is now {server_port}")

# Every 15 seconds the bot will query the server to see if it is online, then change nickname depending on result
@tasks.loop(seconds=15)
async def check_server_status(ctx):
    await bot.wait_until_ready()
    print("Running...")
    full_stats, server_online = query_server()
    if server_online:
        await ctx.guild.me.edit(nick="[ONLINE] MineAlertBot")
    else:
        await ctx.guild.me.edit(nick="[OFFLINE] MineAlertBot")
    
# Command to query the server for information, and check if the server is online
def query_server():
    try:
        # Using the query protocol to communicate with the server through the IP and port
        with Client(server_address, int(server_port), timeout = 10) as client:
            full_stats = client.stats(full=True)
            server_online = True
        # Turning the stats into a JSON-ish dictionary
        full_stats = dict(full_stats)
        return full_stats, server_online
    except Exception as e:
        print(server_address, server_port)
        print(f"This is the error message: {e}")
        full_stats = None
        server_online = False
        return full_stats, server_online

# Either using the user-given info or securely loading it from the config file
def get_token(token = "1"):
    file = open("config.json")
    data = json.load(file)
    return data["token"]

def get_server_address():
    file = open("config.json")
    data = json.load(file)
    return data["server-address"]   

def get_server_port():
    file = open("config.json")
    data = json.load(file)
    return data["server-port"]

# Activating the bot
bot.run(get_token())