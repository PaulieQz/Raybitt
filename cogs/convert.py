from nextcord.ext import commands


class converter(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def convert(self, ctx, value: float, unit_from, unit_to):
        conversions = {
            'cm_to_in': value * 0.393701,
            'in_to_cm': value * 2.54,
            'c_to_f': (value * 9 / 5) + 32,
            'f_to_c': (value - 32) * 5 / 9,
            'g_to_o': (value * 0.035274),
            'o_to_g': (value * 28.3495)
        }

        conversion_key = f"{unit_from.lower()}_to_{unit_to.lower()}"
        if conversion_key in conversions:
            converted_value = conversions[conversion_key]
            await ctx.send(f"{value} {unit_from} is equal to {converted_value} {unit_to}")
        else:
            await ctx.send("Invalid conversion!")


def setup(bot):
    bot.add_cog(converter(bot))
