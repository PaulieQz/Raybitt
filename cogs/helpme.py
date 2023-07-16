import nextcord as discord
from nextcord.ext import commands


class Helpme(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def helpme(self, ctx):
        embed = discord.Embed(title="Raybitt-old Bot - Help", color=discord.Color.blue())
        embed.add_field(name="/top5", value="Display the top 5 most common words.", inline=False)
        embed.add_field(name="/wc <word>", value="Check how many times a word has been said.", inline=False)
        embed.add_field(name="/convert <num> <o/g><in/cm><c/f>", value="Convert either Ounces to Grams or vice versa.",
                        inline=False)
        embed.add_field(name="/binary2text <INTs>", value="Convert binary into text", inline=False)
        embed.add_field(name="/text2binary <String>", value="Convert text into binary")
        embed.add_field(name="/square <num>", value="Calculate the square of a number.", inline=False)
        embed.add_field(name="/cube <num>", value="Calculate the cube of a number.", inline=False)
        embed.add_field(name="/factorial <num>", value="Calculate the factorial of a number.", inline=False)
        embed.add_field(name="/simplify <expression>", value="Simplify a mathematical expression.", inline=False)
        embed.add_field(name="/solve <equation>", value="Solve a mathematical equation.", inline=False)
        embed.add_field(name="/derivative <expression>", value="Calculate the derivative of an expression.",
                        inline=False)
        embed.add_field(name="/integral <expression>", value="Calculate the integral of an expression.", inline=False)
        embed.add_field(name="/random_number <lower> <upper>", value="Generate a random number within a range.",
                        inline=False)
        embed.add_field(name="/quadratic_equation <a> <b> <c>", value="Solve a quadratic equation.", inline=False)
        embed.add_field(name="/pythagorean_theorem <a> <b>",
                        value="Calculate the length of the hypotenuse using the Pythagorean theorem.", inline=False)
        embed.add_field(name="/prime_factorization <num>", value="Find the prime factorization of a number.",
                        inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Helpme(bot))
