# Standard library imports
import datetime
import os
import time
# Third-party imports
import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from mcipc.query import Client
import os
# Local application imports
from bot_files.bot_global_settings import *

# Loading the environmental variables in the .env file
load_dotenv()

# Function to activate cog for the bot to use
async def setup(bot: commands.Bot):
    await bot.add_cog(Server(bot), guild = discord.Object(id = os.getenv("DEV_DISCORD_SERVER_ID")))

# Command to query the server for information, and check if the server is online
def query_server():
    try:
        # Using the query protocol to communicate with the server through the IP and port
        with Client(config["server_config"]["server_ip"], int(config["server_config"]["server_port"]), timeout = 10) as client:
            full_stats = client.stats(full=True)
            server_online = True
        # Turning the stats into a JSON-ish dictionary
        full_stats = dict(full_stats)
        return full_stats, server_online
    except Exception as e:
        print(f"This is the exception: {e}")
        full_stats = None
        server_online = False
        return full_stats, server_online
    
def uptime(start_or_end):
    return str(datetime.timedelta(seconds=int(round(time.time()-start_or_end))))


# The cog for configuring the bot to correctly interact with the Minecraft server
# as well as which users can use which commands
class Server(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.previous_online_check = None
        global start_time
        global end_time
        start_time = time.time()
        end_time = None

    @app_commands.command(name = "setalertschannel", description = "Set the channel for Minecraft server alerts")
    @app_commands.default_permissions(administrator = True)
    async def setalertschannel(self, interaction: discord.Interaction, channel: str):
        print(f"Alerts channel: {channel}")
        if channel[0] == "#":
            channel = channel[1:]
        try:
            channel = discord.utils.get(interaction.guild.channels, name = str(channel))
            channel_id = channel.id
            update_config("server_config", "alerts_channel_id", channel_id)
            await interaction.response.send_message(f"The server's alerts channel is now #{channel}!")
        except Exception as e:
            print(f"ERROR: Setalertschannel exception: {e}")
            await interaction.response.send_message("I'm having trouble finding that channel, maybe try again?")
    
    @app_commands.command(name = "setip", description = "Set the IP of the Minecraft server")
    @app_commands.default_permissions(administrator = True)
    async def setip(self, interaction: discord.Interaction, server_ip: str):
        print(f"Server IP: {server_ip}")
        update_config("server_config", "server_ip", server_ip)
        await interaction.response.send_message(f"The server's IP is now {server_ip}!")

    @app_commands.command(name = "setport", description = "Set the port of the Minecraft server")
    @app_commands.default_permissions(administrator = True)
    async def setport(self, interaction: discord.Interaction, server_port: int):
        print(f"Server port: {server_port}")
        update_config("server_config", "server_port", server_port)
        await interaction.response.send_message(f"The server's port is now {server_port}!")

    @app_commands.command(name = "setname", description = "Set the name of the Minecraft server")
    @app_commands.default_permissions(administrator = True)
    async def setname(self, interaction: discord.Interaction, server_name: str):
        print(f"Server name: {server_name}")
        update_config("server_config", "server_name", server_name)
        await interaction.response.send_message(f"The server's name is now {server_name}!")

    @app_commands.command(name = "serverinfo", description = "Retrieves live information on the Minecraft server")
    async def serverinfo(self, interaction: discord.Interaction):
        async with interaction.channel.typing():
            full_stats, online = query_server()
            if online:
                if config['server_config']['server_name'] == None:
                    title = "Minecraft Server Info",
                else:
                    title = f"{config['server_config']['server_name']} Server Info"
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

    # Command to begin the task of monitoring the server
    @app_commands.command(name = "servercheck", description = "Activates the background tasks that will monitor the server status")
    @app_commands.default_permissions(administrator = True)
    async def servercheck(self, interaction: discord.Interaction):
        self.check_server_status.start(interaction)
        self.check_for_alert.start(interaction)
        print("Task started!")
        await interaction.response.send_message("Checking now! This may take a few seconds...")

    # The bot will query the server to see if it is online, then change nickname depending on result
    @tasks.loop(seconds = 10)
    async def check_server_status(self, interaction: discord.Interaction):
        await self.bot.wait_until_ready()
        full_stats, server_online = query_server()
        if server_online:
            await interaction.guild.me.edit(nick="[SERVER ONLINE] MineAlertBot")
        else:
            await interaction.guild.me.edit(nick="[SERVER OFFLINE] MineAlertBot")
        print("check_server_status running...")

    # If the bot has gone from being online to offline for any reason, the bot will send an alert in the designated channel
    @tasks.loop(seconds = 10)
    async def check_for_alert(self, interaction: discord.Interaction):
        global start_time
        global end_time
        await self.bot.wait_until_ready()
        print("check_for_alert running...")
        full_stats, current_online_check = query_server()
        if self.previous_online_check == None:
            self.previous_online_check = current_online_check
        elif self.previous_online_check == True and current_online_check == False:
            end_time = time.time()
            try:
                channel_id = config["server_config"]["alerts_channel_id"]
                channel = interaction.guild.get_channel(int(channel_id))
                decoded_siren_emoji = b'\xf0\x9f\x9a\xa8'.decode("utf-8")
                await channel.send(f"{decoded_siren_emoji} ALERT: Server has just gone offline! (Uptime: {uptime(start_time)})") 
            except Exception as e:
                print(f"ERROR: check_for_alert exception: {e}")
        elif self.previous_online_check == False and current_online_check == True:
            start_time = time.time()
            try:
                channel_id = config["server_config"]["alerts_channel_id"]
                channel = interaction.guild.get_channel(int(channel_id))
                checkmark_emoji = b'\xE2\x9C\x85'.decode("utf-8")
                if type(end_time) != None:
                    await channel.send(f"{checkmark_emoji} ALERT: Server is back online! (Downtime: {uptime(end_time)})")
                else:
                    await channel.send(f"{checkmark_emoji} ALERT: Server is back online!")
            except Exception as e:
                print(f"ERROR: check_for_alert exception: {e}")
        self.previous_online_check = current_online_check