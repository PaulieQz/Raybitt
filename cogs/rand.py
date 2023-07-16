import random

from nextcord.ext import commands


class rand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def random_number(self, ctx, lower: int, upper: int):
        result = random.randint(lower, upper)
        await ctx.send(f"Random number between {lower} and {upper}: {result}")


def setup(bot):
    bot.add_cog(rand(bot))
