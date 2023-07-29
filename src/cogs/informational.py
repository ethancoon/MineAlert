# Third-party imports
from discord.ext import commands


# This cog contains commands that provide general Minecraft information

# Function to activate cog for the bot to use
async def setup(bot):
    await bot.add_cog(Informational(bot))

class Informational(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def about(self, ctx):
        about_msg = "`This bot was originally created to help keep my friends updated on the status of our server. If you have any questions or concerns, please reach out to me through Discord (w1f1)`"
        await ctx.send(about_msg)