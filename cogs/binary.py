from nextcord.ext import commands

class T2B(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['t2b'])
    async def text2binary(self, ctx, *, text: str):
        binary_text = ' '.join(format(ord(char), '08b') for char in text)
        await ctx.send(binary_text)

    @commands.command(aliases=['b2t'])
    async def binary2text(self, ctx, *, binary_text: str):
        text = ''.join(chr(int(binary, 2)) for binary in binary_text.split())
        await ctx.send(text)

def setup(bot):
    bot.add_cog(T2B(bot))
