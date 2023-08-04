# Standard library imports
import os
import random
# Third-party imports
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Loading the environmental variables in the .env file
load_dotenv()

# This cog contains commands that provide general Minecraft information

# Function to activate cog for the bot to use
async def setup(bot):
    await bot.add_cog(Miscellaneous(bot), guild = discord.Object(id = os.getenv("DEV_DISCORD_SERVER_ID")))

# The class for Miscellaneous commands as defined by commands.GroupCog
class Miscellaneous(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command()
    async def hello(self, interaction: discord.Interaction):
        msg = "Hey there!"
        await interaction.response.send_message(msg)

    # Randomly generates a Minecraft seed between the lowest and highest possible seed values
    @app_commands.command()
    async def seed(self, interaction: discord.Interaction):
        seed = str(random.randint(-9223372036854775808, 9223372036854775807))
        await interaction.response.send_message(seed)