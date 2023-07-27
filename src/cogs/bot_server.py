# Standard library imports
import json
import random
# Third-party imports
import discord
from discord.ext import commands, tasks
from mcipc.query import Client
import requests
# Local application imports
from bot_files.bot_global_settings import *

# Function to activate cog for the bot to use
async def setup(bot):
    await bot.add_cog(Server(bot))

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
        print(f"This is the error message: {e}")
        full_stats = None
        server_online = False
        return full_stats, server_online
    



# The cog for configuring the bot to correctly interact with the Minecraft server
# as well as which users can use which commands
class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.previous_alert_check = None

    @commands.command()
    async def setalertschannel(self, ctx, channel):
        print(f"Alerts channel: {channel}")
        try:
            channel = discord.utils.get(ctx.guild.channels, name = str(channel))
            channel_id = channel.id
            update_config("server_config", "alerts_channel_id", channel_id)
            await ctx.send(f"The server's alerts channel is now #{channel}!")
        except Exception as e:
            print(f"ERRROR: Setalertschannel exception: {e}")
            await ctx.send("I'm having trouble finding that channel, maybe try again?")
    
    @commands.command()
    async def setip(self, ctx, server_ip):
        print(f"Server IP: {server_ip}")
        update_config("server_config", "server_ip", server_ip)
        await ctx.send(f"The server's IP is now {server_ip}!")

    @commands.command()
    async def setport(self, ctx, server_port):
        print(f"Server port: {server_port}")
        update_config("server_config", "server_port", server_port)
        await ctx.send(f"The server's port is now {server_port}!")

    @commands.command()
    async def setname(self, ctx, *server_name):
        server_name = " ".join(server_name)
        print(f"Server name: {server_name}")
        update_config("server_config", "server_name", server_name)
        await ctx.send(f"The server's name is now {server_name}!")

    @commands.command()
    async def serverinfo(self, ctx):
        async with ctx.typing():
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
                embed.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft/images/f/fe/GrassNew.png/revision/latest/scale-to-width-down/250?cb=20190903234415")
                await ctx.send(embed = embed)
            else:
                await ctx.send("The server is offline or I am searching the wrong address :(")

    # Command to begin the task of monitoring the server
    @commands.command()
    async def servercheck(self, ctx):
        self.check_server_status.start(ctx)
        self.check_for_alert.start(ctx)
        print("Task started!")
        await ctx.send("Checking now! This may take a few seconds...")

    # T bot will query the server to see if it is online, then change nickname depending on result
    @tasks.loop(seconds = 10)
    async def check_server_status(self, ctx: commands.Context):
        await self.bot.wait_until_ready()
        full_stats, server_online = query_server()
        if server_online:
            await ctx.guild.me.edit(nick="[SERVER ONLINE] MineAlertBot")
        else:
            await ctx.guild.me.edit(nick="[SERVER OFFLINE] MineAlertBot")
        print("check_server_status running...")

    # If the bot has gone from being online to offline for any reason, the bot will send an alert in the designated channel
    @tasks.loop(seconds = 10)
    async def check_for_alert(self, ctx: commands.Context):
        await self.bot.wait_until_ready()
        print("check_for_alert running...")
        full_stats, current_alert_check = query_server()
        if self.previous_alert_check == None:
            self.previous_alert_check = current_alert_check
        elif self.previous_alert_check == True and current_alert_check == False:
            try:
                channel_id = config["server_config"]["alerts_channel_id"]
                channel = ctx.guild.get_channel(int(channel_id))
                decoded_siren_emoji = b'\xf0\x9f\x9a\xa8'.decode("utf-8")
                await channel.send(f"{decoded_siren_emoji} ALERT: Server has just gone offline!") 
            except Exception as e:
                print(f"ERROR: check_for_alert exception: {e}")
        elif self.previous_alert_check == False and current_alert_check == True:
            try:
                channel_id = config["server_config"]["alerts_channel_id"]
                channel = ctx.guild.get_channel(int(channel_id))
                checkmark_emoji = b'\xE2\x9C\x85'.decode("utf-8")
                await channel.send(f"{checkmark_emoji} ALERT: Server is back online!")
            except Exception as e:
                print(f"ERROR: check_for_alert exception: {e}")
        self.previous_alert_check = current_alert_check

