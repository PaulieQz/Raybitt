import discord
from discord.ext import commands
import requests


class Joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joke(self, ctx):
        try:
            response = requests.get("https://official-joke-api.appspot.com/random_joke")
            joke_data = response.json()

            setup = joke_data["setup"]
            punchline = joke_data["punchline"]

            embed = discord.Embed(title="Joke", description=setup, color=discord.Color.blue())
            embed.add_field(name="Punchline", value=punchline, inline=False)

            await ctx.send(embed=embed)
        except requests.RequestException:
            await ctx.send("Failed to fetch a joke. Please try again later.")

    @commands.command()
    async def how2program(self, ctx):
        try:
            response = requests.get("https://official-joke-api.appspot.com/jokes/programming/random")
            joke_data = response.json()[0]

            setup = joke_data["setup"]
            punchline = joke_data["punchline"]

            embed = discord.Embed(title="Programming Joke", description=setup, color=discord.Color.orange())
            embed.add_field(name="Punchline", value=punchline, inline=False)

            await ctx.send(embed=embed)
        except requests.RequestException:
            await ctx.send("Failed to fetch a programming joke. Please try again later.")

    @commands.command()
    async def dad(self, ctx):
        try:
            response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
            joke_data = response.json()

            joke = joke_data["joke"]

            await ctx.send(f"👨 **Dad Joke:** {joke}")
        except requests.RequestException:
            await ctx.send("Failed to fetch a dad joke. Please try again later.")

    @commands.command(aliases=["chucknorris"])
    async def chuck_norris_joke(self, ctx):
        try:
            response = requests.get("https://api.chucknorris.io/jokes/random")
            joke_data = response.json()

            joke = joke_data["value"]

            await ctx.send(f"👊 **Chuck Norris Joke:** {joke}")
        except requests.RequestException:
            await ctx.send("Failed to fetch a Chuck Norris joke. Please try again later.")


def setup(bot):
    bot.add_cog(Joke(bot))
