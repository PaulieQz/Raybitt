import cursor
import configparser
import sqlite3
from discord.ext import commands


class Wc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        config = configparser.ConfigParser()
        config.read('config.ini')
        database_file = config['Database']['File']
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()

    @commands.command()
    async def wc(self, ctx, word):
        word = word.lower()
        self.cursor.execute('SELECT count FROM word_counts WHERE word = ?', (word,))
        result = self.cursor.fetchone()
        if result:
            count = result[0]
            await ctx.send(f'The word "{word}" has been said {count} times.')
        else:
            await ctx.send(f'The word "{word}" has not been said yet.')


async def setup(bot):
    await bot.add_cog(Wc(bot))
