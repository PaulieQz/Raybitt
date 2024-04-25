import asyncio
import datetime

from nextcord.ext import commands, tasks


class Bump(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bump(self, ctx):
        print("Starting bumper")
        channel = self.bot.get_channel(795724806225920001)
        print(ctx.message.author)
        await channel.send("Disboard bump available")
        print("starting timer")
        await asyncio.sleep(7200)
        await ctx.send("ACK Disboard API Request")


def setup(bot):
    bot.add_cog(Bump(bot))
