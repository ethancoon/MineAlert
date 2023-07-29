# Standard library imports
import random
# Third-party imports
from discord.ext import commands


# This cog contains commands that provide general Minecraft information

# Function to activate cog for the bot to use
async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))

class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        msg = "Hey there!"
        await ctx.send(msg)

    # Randomly generates a Minecraft seed between the lowest and highest possible seed values
    @commands.command()
    async def seed(self, ctx):
        seed = str(random.randint(-9223372036854775808, 9223372036854775807))
        await ctx.send(seed)