# Standard library imports
import json
import os
import random
import logging, logging.handlers

# Third-party imports
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Making sure the bot has the right permissions, and then creating the bot with the specified command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", description = "A simple Discord bot for a Minecraft server", intents = intents)

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

    logging.info(f"{username} said '{user_message}' (Channel: {channel})")
    print(f"{username} said '{user_message}' (Channel: {channel})")
    # If this is not included, the bot will be unable to respond to a command if it is loggging the message
    await bot.process_commands(message)

# Function to activate cog for the bot to use
async def setup(bot):
    # print(os.listdir("src/cogs"))
    for file in os.listdir("src/cogs"):
        if file.endswith(".py"):
            logging.info(f"Attempting to load file {file}")
            try: 
                logging.info(f"Successfully loaded file {file}")
                await bot.load_extension(f"cogs.{file[:-3]}")
            except commands.ExtensionAlreadyLoaded: 
                logging.warning(f"WARNING: Extension \'{file}\ is already loaded")
                print(f"ERROR: Extension \'{file}\ is already loaded")
            except commands.ExtensionNotFound:
                logging.warning(f"WARNING: Extension \'{file}\' is not found")
                print(f"ERROR: Extension \'{file}\' is not found")
            except Exception as e:
                logging.warning(f"WARNING: Error with loading cogs ({e})")
                print(f"ERROR: Error with loading cogs ({e})")


# Logging and debugging
# Creating logger
logger = logging.getLogger("run_bot.py")
logger.setLevel(logging.DEBUG)

# Creating handler for logger
handler = logging.handlers.RotatingFileHandler(
    # The file where the log will be output
    filename = "./logs/discord.log",
    encoding = "utf-8",
    # 32 MiB
    maxBytes = 32 * 1024 * 1024,
    # Rotating through 5 files
    backupCount = 5
)
dt_format = "%Y-%m-%d %H:%M:%S"

# Configuring the handler's output so it is more easily readible
formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", dt_format, style = "{")
handler.setFormatter(formatter)

# Adding the handler as the logger's method of storing the logs
logger.addHandler(handler)


# Loading the environmental variables in the .env file
load_dotenv()

# Activating the bot
logger.info("Attempting to run bot...")
try:
    bot.run(os.getenv("BOT_TOKEN"), log_handler = None)
except KeyboardInterrupt:
    bot.logout()
    logging.warning("WARNING: KeyboardInterrupt exception raised")
