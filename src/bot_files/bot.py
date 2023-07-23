import discord
import json
import random
from mctools import QUERYClient
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", description = "A simple Discord bot for a Minecraft server", intents = intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID:{bot.user.id})")

@bot.event
async def on_message(message):
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f"{username} said '{user_message}' (Channel: {channel})")
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send("Hey there!")

@bot.command()
async def seed(ctx):
    await ctx.send(str(random.randint(-9223372036854775808, 9223372036854775807)))

@bot.command()
async def mahelp(ctx):
    await ctx.send("`This is a placeholder for help.`")

@bot.command()
async def about(ctx):
    await ctx.send("`This is a placeholder for about.`")

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
    try:
        query = QUERYClient(server_address, server_port, timeout = 10)
        await ctx.send(query.get_full_stats())
    except Exception as e:
        print(e)
        await ctx.send("The server is offline or I am searching the wrong address :(")    

def get_token():
    file = open("config.json")
    data = json.load(file)
    return data["token"]

bot.run(get_token())