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
from mcipc.query import Client as mcipcClient
import os
# Local application imports
import src.data.database as db

# Loading the environmental variables in the .env file
load_dotenv()

# Function to activate cog for the bot to use
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Server(bot))

# The cog for configuring the bot to correctly interact with the Minecraft server
# as well as which users can use which commands
class Server(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.previous_online_check = None
        self.start_time = time.time()
        self.end_time = -1
        self.coords = []
        self.helpers = ServerHelpers()
    
    @app_commands.command(name = "set", description = "Modify the bot's config for the Minecraft server")
    @app_commands.default_permissions(administrator = True)
    async def set(self, interaction: discord.Interaction, options: Literal["Name", "IP", "Port", "Alerts Channel", "Alerts Enabled"], value: str) -> None:
        await interaction.response.defer() 
        if options == "Name":
                db.update_minecraft_server_table(interaction.guild.id, "name", value)
                await interaction.followup.send(f"The Minecraft server's name is now {value}!")
        elif options == "IP":
            db.update_minecraft_server_table(interaction.guild.id, "ip", value)
            await interaction.followup.send(f"The Minecraft server's IP is now {value}!")   
        elif options == "Port":
            db.update_minecraft_server_table(interaction.guild.id, "port", value)
            await interaction.followup.send(f"The Minecraft server's port is now {value}!")
        elif options == "Alerts Channel":
            if value[0] == "#":
                value = value[1:]
            try:
                channel = discord.utils.get(interaction.guild.channels, name = str(value))
                channel_id = channel.id
                db.update_minecraft_server_table(interaction.guild.id, "alerts_channel_id", channel_id)
                await interaction.followup.send(f"The Minecraft server's alerts channel is now #{channel}!")
            except Exception as e:
                print(f"ERROR: Setalertschannel exception: {e}")
                await interaction.followup.send("I'm having trouble finding that channel, maybe try again?")
        elif options == "Alerts Enabled":
            if value.lower() in ["true", "yes", "on", "1"]:
                # If the value is true, then the alerts_enabled column will be set to 1
                db.update_minecraft_server_table(interaction.guild.id, "alerts_enabled", 1)
                self.servercheck().start(interaction)
                await interaction.followup.send("Alerts are now enabled!")
            elif value.lower() in ["false", "no", "off", "0"]:
                # If the value is false, then the alerts_enabled column will be set to 0
                db.update_minecraft_server_table(interaction.guild.id, "alerts_enabled", 0)
                self.servercheck().stop()
                await interaction.followup.send("Alerts are now disabled!")

    # Queries the server, then returns an embed containing live info
    @app_commands.command(name = "serverinfo", description = "Retrieves live information on the Minecraft server")
    async def serverinfo(self, interaction: discord.Interaction) -> None:
        # Will make it seem like the bot is typing, 
        # which is needed to give feedback for when the bot is taking a while to query
        async with interaction.channel.typing():
            full_stats, online = self.helpers.query_server(interaction.guild.id)
            # If the server is online, the embed will be created, otherwise an error message
            if online:
                # If the server has a name set, that will be used
                if db.get_minecraft_server_data_from_guild_id(interaction.guild.id, "name") == None:
                    title = "Minecraft Server Info",
                else:
                    title = f"{db.get_minecraft_server_data_from_guild_id(interaction.guild.id, 'name')} Info"
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
                embed.set_footer(text = f"Server Uptime: {self.helpers.uptime(start_time)}")
                embed.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft/images/f/fe/GrassNew.png/revision/latest/scale-to-width-down/250?cb=20190903234415")
                await interaction.response.send_message(embed = embed)
            else:
                await interaction.response.send_message("The server is offline or I am searching the wrong address :(")

    # Sends an embed of the server's coords
    @app_commands.command(name = "coords", description = "View any marked coordinates in the Minecraft server")
    async def coords(self, interaction: discord.Interaction) -> None:
        # If the server has a name set, that will be used
        if db.get_server_name_from_guild_id(interaction.guild.id) == None:
            title = "Minecraft Server Info"
        else:
            title = f"{db.get_server_name_from_guild_id(interaction.guild.id)} Coords"
        # Creating an embed for Discord
        embed = discord.Embed(
            title = title,
            description = "List of coords (Y is None if left blank)",
            color = discord.Color.dark_green()
        )
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft/images/f/fe/GrassNew.png/revision/latest/scale-to-width-down/250?cb=20190903234415")
        # Looping through the list of coords, and for each coord add a field.
        for coord in db.get_coords_from_server_id(db.get_server_id_from_guild_id(interaction.guild.id)):
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
        db.add_coords_to_db(interaction.guild.id, [name, x, y, z, interaction.user.id])
        await interaction.response.send_message(f"Here are the coordinates for {name}: X = {x}, Y = {y}, Z = {z}")

    @app_commands.command(name = "delcoords", description = "Delete coordinates from the Minecraft server's coords list")
    async def delcoords(self, interaction: discord.Interaction, coords_name: str) -> None:
        # Deleting the coords from the database
        db.delete_coords_from_db(interaction.guild.id, coords_name)
        await interaction.response.send_message(f"All coordinates named {coords_name} deleted!")

    # Command to begin the task of monitoring the server
    @app_commands.command(name = "servercheck", description = "Activates the background tasks that will monitor the server status")
    async def servercheck(self, interaction: discord.Interaction) -> None:
        # self.check_server_status.start(interaction)
        if db.get_alerts_enabled_from_guild_id(interaction.guild.id) == 0:
            await interaction.response.send_message("Alerts are disabled! Please enable them with '/set Alerts Enabled True'")
        else:
            self.notify_server_status.start(interaction)
        print("Task started!")
        await interaction.response.send_message("Checking now! This may take a few seconds...")

    # If the bot has gone from being online to offline for any reason, the bot will send an alert in the designated channel
    @tasks.loop(seconds = 10)
    async def notify_server_status(self, interaction: discord.Interaction) -> None:
        await self.bot.wait_until_ready()
        channel, message = self.helpers.check_for_alert(interaction, self.start_time, self.end_time, self.previous_online_check)
        if channel != None and message != None:
            await channel.send(message)


class ServerHelpers():
    def __init__(self) -> None:
        pass

    # Function to query the server for information, and/or check if the server is online
    def query_server(self, guild_id: int, only_check_status: bool = False) -> tuple[dict, bool]:
        try:
            # Using the query protocol to communicate with the server through the IP and port
            with mcipcClient(db.get_minecraft_server_data_from_guild_id(guild_id, "ip"), db.get_minecraft_server_data_from_guild_id(guild_id, "port"), timeout = 10) as client:
                full_stats = client.stats(full=True)
                server_online = True
            # Turning the stats into a JSON-ish dictionary
            full_stats = dict(full_stats)
            if only_check_status:
                return server_online
            else:
                return full_stats, server_online
        except Exception as e:
            full_stats = None
            server_online = False
            if only_check_status:
                return server_online
            else:
                return full_stats, server_online
        
    # Function to calculate the uptime of the server
    def calculate_uptime_or_downtime(self, start_or_end: int) -> str:
        return str(datetime.timedelta(seconds=int(time.time()-start_or_end)))
    
    # Function to find if an alert message needs to be sent, and if so, what the message should be
    def check_for_alert(self, interaction: discord.Interaction, start_time: float, end_time: float, previous_online_check: bool) -> None:
        current_online_check = self.query_server(interaction.guild.id, only_check_status = True)
        if previous_online_check == None:
            previous_online_check = current_online_check
        elif previous_online_check == True and current_online_check == False:
            end_time = time.time()
            try:
                channel_id = db.get_minecraft_server_data_from_guild_id(interaction.guild.id, "alerts_channel_id")
                channel = interaction.guild.get_channel(int(channel_id))
                siren_emoji = b'\xf0\x9f\x9a\xa8'.decode("utf-8")
                return channel, f"{siren_emoji} ALERT: Server has just gone offline! (Uptime: {self.calculate_uptime_or_downtime(start_time)})"
            except Exception as e:
                print(f"ERROR: check_for_alert exception: {e}")
        elif previous_online_check == False and current_online_check == True:
            start_time = time.time()
            try:
                channel_id = db.get_minecraft_server_data_from_guild_id(interaction.guild.id, "alerts_channel_id")
                channel = interaction.guild.get_channel(int(channel_id))
                checkmark_emoji = b'\xE2\x9C\x85'.decode("utf-8")
                if end_time is not None:
                    return channel, f"{checkmark_emoji} ALERT: Server is back online! (Downtime: {self.calculate_uptime_or_downtime(end_time)})"
                else:
                    return channel, f"{checkmark_emoji} ALERT: Server is back online!"
            except Exception as e:
                print(f"ERROR: check_for_alert exception: {e}")
        else:
            return None, None
        previous_online_check = current_online_check

    def handle_setting():
        pass