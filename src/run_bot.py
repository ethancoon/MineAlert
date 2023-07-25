# Standard library imports
import random
import json
import os
# Third-party imports
import discord
from discord.ext import commands

# Making sure the bot has the right permissions, and then creating the bot with the specified command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", description = "A simple Discord bot for a Minecraft server", intents = intents)

# When the bot is initialized this message will be output into the terminal
@bot.event
async def on_ready():
    await bot.wait_until_ready()
    await setup(bot)
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

    

# Either using the user-given info or securely loading it from the config file
def get_token():
    file = open("config.json")
    data = json.load(file)
    return data["token"]

# def get_server_address():
#     file = open("config.json")
#     data = json.load(file)
#     return data["server-address"]   

# def get_server_port():
#     file = open("config.json")
#     data = json.load(file)
#     return data["server-port"]

# Function to activate cog for the bot to use
async def setup(bot):
    await bot.load_extension("cogs.bot_server")

    # print(os.listdir("src"))
    # for i in os.listdir("src/cogs"):
    #     if i.endswith(".py"):
    #         try: await bot.load_extension(f"cogs.{i[:-3]}", package = "./cogs")
    #         except commands.ExtensionAlreadyLoaded: pass
    #         except commands.ExtensionNotFound:
    #             print(f"ERROR: Unable to load cog \'{i}\'")
    #         except:
    #             print("ERROR: Error with loading cogs")


# Activating the bot
bot.run(get_token())