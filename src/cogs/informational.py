# Third-party imports
import discord
from discord.ext import commands
from mojang import API

# This cog contains commands that provide general Minecraft information

# Function to activate cog for the bot to use
async def setup(bot):
    await bot.add_cog(Informational(bot))

class Informational(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx, name):
        api = API()
        uuid = api.get_uuid(str(name))
        if not uuid:
            await ctx.send(f"{name} is not a taken username")
        else:
            profile = api.get_profile(uuid)
            print(profile)
            username = getattr(profile, "name")
            skin_variant = getattr(profile, "skin_variant")
            print(profile)
        # Creating an embed for Discord
        embed = discord.Embed(
            title = f"{username}'s Minecraft Profile",

            color = discord.Color.green()
        )

        embed.add_field(name = "UUID", value = f"`{uuid}`", inline = False)
        embed.add_field(name = "Skin Variant", value = f"`{skin_variant}`", inline = False)
        embed.set_image(url = f"https://api.mineatar.io/body/full/{uuid}")
        embed.set_thumbnail(url = f"https://api.mineatar.io/face/{uuid}")
        await ctx.send(embed = embed)


            


    @commands.command()
    async def about(self, ctx):
        about_msg = "`This bot was originally created to help keep my friends updated on the status of our server. If you have any questions or concerns, please reach out to me through Discord (w1f1)`"
        await ctx.send(about_msg)