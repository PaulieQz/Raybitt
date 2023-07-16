import sqlite3
import configparser
import nextcord as discord
import cursor
from nextcord.ext import commands


class Top5(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        config = configparser.ConfigParser()
        config.read('config.ini')
        database_file = config['Database']['File']
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()

    @commands.command()
    async def top5(self, ctx):
        self.cursor.execute('SELECT word, count FROM word_counts ORDER BY count DESC LIMIT 5')
        rows = self.cursor.fetchall()
        if len(rows) > 0:
            page = 1
            items_per_page = 5
            total_pages = -(-len(rows) // items_per_page)  # ceil(len(rows) / items_per_page)
            start_index = (page - 1) * items_per_page
            end_index = page * items_per_page

            embed = discord.Embed(title="Top 5 Most Common Words", color=discord.Color.green())

            for row in rows[start_index:end_index]:
                embed.add_field(name=row[0], value=f"Count: {row[1]}", inline=False)

            embed.set_footer(text=f"Page {page}/{total_pages}")

            message = await ctx.send(embed=embed)

            if total_pages > 1:
                await message.add_reaction("⬅️")
                await message.add_reaction("➡️")

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ["⬅️", "➡️"]

                while True:
                    try:
                        reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)

                        if str(reaction.emoji) == "➡️" and page < total_pages:
                            page += 1
                        elif str(reaction.emoji) == "⬅️" and page > 1:
                            page -= 1

                        start_index = (page - 1) * items_per_page
                        end_index = page * items_per_page

                        embed.clear_fields()
                        for row in rows[start_index:end_index]:
                            embed.add_field(name=row[0], value=f"Count: {row[1]}", inline=False)

                        embed.set_footer(text=f"Page {page}/{total_pages}")

                        await message.edit(embed=embed)
                        await message.remove_reaction(reaction, user)
                    except TimeoutError:
                        await message.clear_reactions()
                        break
        else:
            await ctx.send("No word counts found.")


def setup(bot):
    bot.add_cog(Top5(bot))
