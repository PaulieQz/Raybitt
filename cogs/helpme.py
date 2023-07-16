import nextcord as discord
from nextcord.ext import commands

class Helpme(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def helpme(self, ctx):
        embed = discord.Embed(title="Raybitt-old Bot - Help", color=discord.Color.blue())
        embed.add_field(name="/leet <text>", value="Converts text into leetspeak.", inline=False)
        embed.add_field(name="/text2binary <text>", value="Converts text into binary.", inline=False)
        embed.add_field(name="/binary2text <binary>", value="Converts binary into text.", inline=False)
        embed.add_field(name="/bump", value="Sends a message and reminds you to send another after 7200 seconds.", inline=False)
        embed.add_field(name="/convert <value> <unit_from> <unit_to>", value="Converts units.", inline=False)
        embed.add_field(name="/joke", value="Displays a random joke.", inline=False)
        embed.add_field(name="/how2program", value="Displays a random programming joke.", inline=False)
        embed.add_field(name="/dad", value="Displays a random dad joke.", inline=False)
        embed.add_field(name="/chuck_norris_joke", value="Displays a random Chuck Norris joke.", inline=False)
        embed.add_field(name="/solve <equation>", value="Solves mathematical equations.", inline=False)
        embed.add_field(name="/derivative <expression>", value="Calculates the derivative of an expression.", inline=False)
        embed.add_field(name="/integral <expression>", value="Calculates the integral of an expression.", inline=False)
        embed.add_field(name="/quadratic_equation <a> <b> <c>", value="Solves a quadratic equation.", inline=False)
        embed.add_field(name="/pythagorean_theorem <a> <b>", value="Calculates the length of the hypotenuse using the Pythagorean theorem.", inline=False)
        embed.add_field(name="/prime_factorization <num>", value="Finds the prime factorization of a number.", inline=False)
        embed.add_field(name="/random_number <lower> <upper>", value="Generates a random number within a range.", inline=False)
        embed.add_field(name="/ping", value="Checks the latency of the bot.", inline=False)
        embed.add_field(name="/top5", value="Displays the top 5 most common words in the server.", inline=False)
        embed.add_field(name="/wc <word>", value="Checks how many times a word has been said in the server.", inline=False)
        embed.add_field(name="/stats", value="Displays various server analytics.", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Helpme(bot))
