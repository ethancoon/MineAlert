# Standard library imports
import datetime
import os
import time
import unittest
from unittest.mock import patch, MagicMock
# Third-party imports
import discord
from discord.ext import commands
import os
# Local application imports
from src.cogs.server import Server

class TestServer(unittest.TestCase):
    def setUp(self) -> None:
        self.server = Server(commands.Bot)
        

    def test_query_server(self):
        dev_guild_id = os.getenv("DEV_DISCORD_SERVER_ID")
        result = self.server.helpers.query_server(dev_guild_id)
        self.assertTrue(isinstance(result, tuple))

    def test_calculate_uptime_or_downtime(self):
        hour_in_seconds = 60 * 60
        start_time = time.time() - hour_in_seconds
        result = self.server.helpers.calculate_uptime_or_downtime(start_time)
        self.assertEqual(result, str(datetime.timedelta(hours=1)))

    # Testing when the server goes from online to offline
    @patch('src.data.database')
    @patch('src.cogs.server.ServerHelpers.query_server', return_value= False)
    def test_check_for_alert(self, mock_db, mock_query_server):
        
        interaction = MagicMock(discord.Interaction)
        interaction.guild.id = os.getenv("DEV_DISCORD_SERVER_ID")
        interaction.guild.get_channel.return_value = 'alerts_channel'

        hour_in_seconds = 60 * 60
        start_time = time.time() - hour_in_seconds
        channel, message = self.server.helpers.check_for_alert(interaction, start_time, time.time(), True)
        siren_emoji = b'\xf0\x9f\x9a\xa8'.decode("utf-8")
        self.assertEqual(message, f"{siren_emoji} ALERT: Server has just gone offline! (Uptime: 1:00:00)")
        self.assertEqual(channel, 'alerts_channel')

        



if __name__ == "__main__":
    unittest.main()
