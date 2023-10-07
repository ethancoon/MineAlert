# Standard library imports
import datetime
import os
import time
from typing import Literal, Optional
# Third-party imports
import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from mcipc.query import Client
import os
# Local application imports
from data.database import *

# Loading the environmental variables in the .env file
load_dotenv()

# Function to activate cog for the bot to use
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Server(bot))

# Command to query the server for information, and check if the server is online
def query_server(guild_id: int) -> tuple[dict, bool]:
    try:
        # Using the query protocol to communicate with the server through the IP and port
        with Client(get_minecraft_server_data_from_guild_id(guild_id, "ip"), get_minecraft_server_data_from_guild_id(guild_id, "port"), timeout = 10) as client:
            full_stats = client.stats(full=True)
            server_online = True
        # Turning the stats into a JSON-ish dictionary
        full_stats = dict(full_stats)
        return full_stats, server_online
    except Exception as e:
        full_stats = None
        server_online = False
        return full_stats, server_online
    
def uptime(start_or_end: int) -> str:
    return str(datetime.timedelta(seconds=int(round(time.time()-start_or_end))))


# The cog for configuring the bot to correctly interact with the Minecraft server
# as well as which users can use which commands
class Server(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.previous_online_check = None
        global start_time
        global end_time
        start_time = time.time()
        end_time = None
        self.coords = []
    
    @app_commands.command(name = "set", description = "Modify the bot's config for the Minecraft server")
    @app_commands.default_permissions(administrator = True)
    async def set(self, interaction: discord.Interaction, options: Literal["Name", "IP", "Port", "Alerts Channel", "Alerts Enabled"], value: str) -> None:
        await interaction.response.defer() 
        if options == "Name":
                update_minecraft_server_table(interaction.guild.id, "name", value)
                await interaction.followup.send(f"The Minecraft server's name is now {value}!")
        elif options == "IP":
            update_minecraft_server_table(interaction.guild.id, "ip", value)
            await interaction.followup.send(f"The Minecraft server's IP is now {value}!")   
        elif options == "Port":
            update_minecraft_server_table(interaction.guild.id, "port", value)
            await interaction.followup.send(f"The Minecraft server's port is now {value}!")
        elif options == "Alerts Channel":
            if value[0] == "#":
                value = value[1:]
            try:
                channel = discord.utils.get(interaction.guild.channels, name = str(value))
                channel_id = channel.id
                update_minecraft_server_table(interaction.guild.id, "alerts_channel_id", channel_id)
                await interaction.followup.send(f"The Minecraft server's alerts channel is now #{channel}!")
            except Exception as e:
                print(f"ERROR: Setalertschannel exception: {e}")
                await interaction.followup.send("I'm having trouble finding that channel, maybe try again?")
        elif options == "Alerts Enabled":
            if value.lower() in ["true", "yes", "on", "1"]:
                # If the value is true, then the alerts_enabled column will be set to 1
                update_minecraft_server_table(interaction.guild.id, "alerts_enabled", 1)
                self.check_for_alert.start(interaction)
                await interaction.followup.send("Alerts are now enabled!")
            elif value.lower() in ["false", "no", "off", "0"]:
                # If the value is false, then the alerts_enabled column will be set to 0
                update_minecraft_server_table(interaction.guild.id, "alerts_enabled", 0)
                self.check_for_alert.stop()
                await interaction.followup.send("Alerts are now disabled!")

    # Queries the server, then returns an embed containing live info
    @app_commands.command(name = "serverinfo", description = "Retrieves live information on the Minecraft server")
    async def serverinfo(self, interaction: discord.Interaction) -> None:
        # Will make it seem like the bot is typing, 
        # which is needed to give feedback for when the bot is taking a while to query
        async with interaction.channel.typing():
            full_stats, online = query_server(interaction.guild.id)
            # If the server is online, the embed will be created, otherwise an error message
            if online:
                # If the server has a name set, that will be used
                if get_minecraft_server_data_from_guild_id(interaction.guild.id, "name") == None:
                    title = "Minecraft Server Info",
                else:
                    title = f"{get_minecraft_server_data_from_guild_id(interaction.guild.id, 'name')} Info"
                # Creating an embed for Discord
                embed = discord.Embed(
                    title = title,
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
                global start_time
                embed.set_footer(text = f"Server Uptime: {uptime(start_time)}")
                embed.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft/images/f/fe/GrassNew.png/revision/latest/scale-to-width-down/250?cb=20190903234415")
                await interaction.response.send_message(embed = embed)
            else:
                await interaction.response.send_message("The server is offline or I am searching the wrong address :(")

    # Sends an embed of the server's coords
    @app_commands.command(name = "coords", description = "View any marked coordinates in the Minecraft server")
    async def coords(self, interaction: discord.Interaction) -> None:
        # If the server has a name set, that will be used
        if get_server_name_from_guild_id(interaction.guild.id) == None:
            title = "Minecraft Server Info"
        else:
            title = f"{get_server_name_from_guild_id(interaction.guild.id)} Coords"
        # Creating an embed for Discord
        embed = discord.Embed(
            title = title,
            description = "List of coords (Y is None if left blank)",
            color = discord.Color.dark_green()
        )
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft/images/f/fe/GrassNew.png/revision/latest/scale-to-width-down/250?cb=20190903234415")
        # Looping through the list of coords, and for each coord add a field.
        for coord in get_coords_from_server_id(get_server_id_from_guild_id(interaction.guild.id)):
            coord_name = coord[0]
            coord_pos = coord[1:4]
            # Inline means multiple coords can be on the same line
            embed.add_field(name = f"{coord_name}", value = f"`{coord_pos}`", inline = True)
        await interaction.response.send_message(embed = embed)

    # Adding coords to the coords list
    @app_commands.command(name = "addcoords", description = "Add coordinates to the Minecraft server's coords list")
    # y is optional, using the typing module
    async def addcoords(self, interaction: discord.Interaction, name:str, x: int, y: Optional[int], *, z: int) -> None:
        # Adding the coords to the database
        add_coords_to_db(interaction.guild.id, [name, x, y, z, interaction.user.id])
        await interaction.response.send_message(f"Here are the coordinates for {name}: X = {x}, Y = {y}, Z = {z}")

    @app_commands.command(name = "delcoords", description = "Delete coordinates from the Minecraft server's coords list")
    async def delcoords(self, interaction: discord.Interaction, coords_name: str) -> None:
        # Deleting the coords from the database
        delete_coords_from_db(interaction.guild.id, coords_name)
        await interaction.response.send_message(f"All coordinates named {coords_name} deleted!")

    # Command to begin the task of monitoring the server
    @app_commands.command(name = "servercheck", description = "Activates the background tasks that will monitor the server status")
    async def servercheck(self, interaction: discord.Interaction) -> None:
        # self.check_server_status.start(interaction)
        if get_alerts_enabled_from_guild_id(interaction.guild.id) == 0:
            await interaction.response.send_message("Alerts are disabled! Please enable them with '/set Alerts Enabled True'")
        else:
            self.check_for_alert.start(interaction)
        print("Task started!")
        await interaction.response.send_message("Checking now! This may take a few seconds...")

    # If the bot has gone from being online to offline for any reason, the bot will send an alert in the designated channel
    @tasks.loop(seconds = 10)
    async def check_for_alert(self, interaction: discord.Interaction) -> None:
        global start_time
        global end_time
        await self.bot.wait_until_ready()
        full_stats, current_online_check = query_server(interaction.guild.id)
        if self.previous_online_check == None:
            self.previous_online_check = current_online_check
        elif self.previous_online_check == True and current_online_check == False:
            end_time = time.time()
            try:
                channel_id = get_minecraft_server_data_from_guild_id(interaction.guild.id, "alerts_channel_id")
                channel = interaction.guild.get_channel(int(channel_id))
                decoded_siren_emoji = b'\xf0\x9f\x9a\xa8'.decode("utf-8")
                await channel.send(f"{decoded_siren_emoji} ALERT: Server has just gone offline! (Uptime: {uptime(start_time)})") 
            except Exception as e:
                print(f"ERROR: check_for_alert exception: {e}")
        elif self.previous_online_check == False and current_online_check == True:
            start_time = time.time()
            try:
                channel_id = get_minecraft_server_data_from_guild_id(interaction.guild.id, "alerts_channel_id")
                channel = interaction.guild.get_channel(int(channel_id))
                checkmark_emoji = b'\xE2\x9C\x85'.decode("utf-8")
                if type(end_time) != None:
                    await channel.send(f"{checkmark_emoji} ALERT: Server is back online! (Downtime: {uptime(end_time)})")
                else:
                    await channel.send(f"{checkmark_emoji} ALERT: Server is back online!")
            except Exception as e:
                print(f"ERROR: check_for_alert exception: {e}")
        self.previous_online_check = current_online_check