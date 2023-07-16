from nextcord.ext import commands


class Leet(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def leet(self, ctx, *, text: str):
        leet_dict = {
            "a": "4",
            "b": "b",
            "c": "<",
            "d": "d",
            "e": "3",
            "f": "f",
            "g": "g",
            "h": "h",
            "i": "1",
            "j": "j",
            "k": "k",
            "l": "1",
            "m": "m",
            "n": "n",
            "o": "0",
            "p": "p",
            "q": "q",
            "r": "r",
            "s": "$",
            "t": "7",
            "u": "u",
            "v": "v",
            "w": "w",
            "x": "×",
            "y": "y",
            "z": "z"
        }

        leet_text = "".join(leet_dict.get(c.lower(), c) for c in text)
        await ctx.send(leet_text)


def setup(bot):
    bot.add_cog(Leet(bot))
