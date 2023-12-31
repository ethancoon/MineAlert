# Standard library imports
import os
import logging, logging.handlers
import time
# Third-party imports
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Local application imports
import data.database as db

# Loading the environmental variables in the .env file
load_dotenv()

# Making sure the bot has the right permissions, and then creating the bot with the specified command prefix
intents = discord.Intents.default()
# Setting the bot's activity to "Playing Minecraft"
activity = discord.Game(name = "Minecraft")

class MineAlertBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix = "/",
            intents = intents,
            activity = activity
        )

    async def setup_hook(self) -> None:
        for file in os.listdir("src/cogs"):
            if file.endswith(".py"):
                logging.info(f"Attempting to load file {file}")
                try: 
                    logging.info(f"Successfully loaded file {file}")
                    await self.load_extension(f"cogs.{file[:-3]}")
                except commands.ExtensionAlreadyLoaded: 
                    logging.warning(f"WARNING: Extension \'{file}\ is already loaded")
                    print(f"ERROR: Extension \'{file}\ is already loaded")
                except commands.ExtensionNotFound:
                    logging.warning(f"WARNING: Extension \'{file}\' is not found")
                    print(f"ERROR: Extension \'{file}\' is not found")
                except Exception as e:
                    logging.warning(f"WARNING: Error with loading cogs ({e})")
                    print(f"ERROR: Error with loading cogs ({e})")
        
        

        # Sync the slash commands to the all Discord servers the bot is in
        await bot.tree.sync()

    async def on_guild_join(self, guild: discord.Guild) -> None:
        # Inserting guild general information into the database on guild join
        db.insert_on_guild_join(guild.id, guild.name, guild.member_count)
        # When the bot joins a server, this message will be output into the terminal
        print(f"Joined {guild.name} with {guild.member_count} members (ID:{guild.id})")

    async def on_ready(self) -> None:
        # When the bot is initialized this message will be output into the terminal
        print(f"Logged in as {bot.user} (ID:{bot.user.id})")
        for guild in self.guilds:
            if db.get_alerts_enabled_from_guild_id(guild.id):
                interaction = discord.Interaction
                interaction.guild = guild
                bot.get_cog("Server").start_notify_server_status(interaction)
        

bot = MineAlertBot()


# # Your function to perform the alert actions for a guild
# async def process_alerts(guild):
#     # Implement your logic here to send alerts or perform other actions for the guild
#     print("hi")
    

# from discord.ext import tasks

# @bot.event
# async def on_ready():
#     print(f'Logged in as {bot.user.name}')
#     # Start the task loop when the bot is ready
#     check_alerts.start()

# @tasks.loop(seconds=5)  # Adjust the interval as needed
# async def check_alerts():
#     guilds_with_alerts = db.get_guild_data_for_all_guilds()
#     for guild in guilds_with_alerts:
#         guild_id = guild[0]
#         guild = bot.get_guild(guild_id)
#         if guild:
#             await process_alerts(guild)

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

# Activating the bot
logger.info("Attempting to run bot...")
try:
    bot.run(os.getenv("BOT_TOKEN"), log_handler = None)
except KeyboardInterrupt:
    logging.warning("WARNING: KeyboardInterrupt exception raised")