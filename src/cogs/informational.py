# Standard library imports
import os
# Third-party imports
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from mojang import API

# Loading the environmental variables in the .env file
load_dotenv()

# This cog contains commands that provide general Minecraft information

# Function to activate cog for the bot to use
async def setup(bot: commands.Bot):
    await bot.add_cog(Informational(bot))

# The class for Informational commands as defined by commands.GroupCog
class Informational(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # The /profile command, will use the mojang API wrapper to retrieve information on Minecraft players
    # This includes username, UUID, the skin the player uses, and the skin variant, if any
    @app_commands.command(name = "profile", description = "View info on a Minecraft player's profile")
    async def profile(self, interaction: discord.Interaction, name: str):
        # Initializing the API wrapper
        api = API()
        # Retrieving the UUID through the API wrapper
        uuid = api.get_uuid(str(name))
        # If the UUID does not exist, no player profile exists
        if not uuid:
            await interaction.response.send_message(f"{name} is not a taken username")
        else:
            # Returns a profile object
            profile = api.get_profile(uuid)
            print(profile)
            # Get the value of the name in the profile object
            username = getattr(profile, "name")
            # Get the value of the skin variant in the profile object
            skin_variant = getattr(profile, "skin_variant")
            print(profile)
        # Creating an embed for Discord
        embed = discord.Embed(
            title = f"{username}'s Minecraft Profile",
            color = discord.Color.green()
        )

        embed.add_field(name = "UUID", value = f"`{uuid}`", inline = False)
        embed.add_field(name = "Skin Variant", value = f"`{skin_variant}`", inline = False)
        # Using the Mineatar API to retrieve an image of the player's full skin to be displayed through the UUID
        embed.set_image(url = f"https://api.mineatar.io/body/full/{uuid}")
        # Same for the face
        embed.set_thumbnail(url = f"https://api.mineatar.io/face/{uuid}")
        await interaction.response.send_message(embed = embed)

    # Command that gives information on this bot
    @app_commands.command(name = "about", description = "Information about the bot")
    async def about(self, interaction: discord.Interaction):
        about_msg = "`This bot is a Minecraft server-monitoring assistant. For a full command list, use /help. If you have any questions or concerns, please reach out to me through Discord (w1f1)`"
        await interaction.response.send_message(about_msg)