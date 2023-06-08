# Raybitt
# short for Raymond Babbitt
# the autistic dude from Rain Man
# since the bot counts words
# and that's why I'm the name guy - Spacecow

import discord
from discord.ext import commands
import sqlite3
import configparser
import nltk
from nltk.corpus import stopwords

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True

nltk.download("stopwords")
nltk_stopwords = stopwords.words('english')
additional_words = ['hello', 'with', 'this', 'here', "didn't", 'about', 'again', "can't", 'well', 'that', 'back', 'then', 'only', 'have', "i've"]
dumbasswords = set(nltk_stopwords).union(additional_words)

bot = commands.Bot(command_prefix='!', intents=intents)

config = configparser.ConfigParser()
config.read('config.ini')

database_file = config['Database']['File']
token = config['Bot']['Token']

conn = sqlite3.connect(database_file)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS word_counts (id INTEGER PRIMARY KEY, word TEXT, count INTEGER)')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    words = message.content.split()
    if words[0][0] != "!" and words[0] not in dumbasswords:
        for word in words:
            try:
                word += 1
            except:
                word = word.lower()
                if word[0] != "!" and len(word) > 3 and words[0] != "!":
                    cursor.execute('SELECT count FROM word_counts WHERE word = ?', (word,))
                    result = cursor.fetchone()

                    if result:
                        count = result[0] + 1
                        cursor.execute('UPDATE word_counts SET count = ? WHERE word = ?', (count, word))
                    else:
                        count = 1
                        cursor.execute('INSERT INTO word_counts (word, count) VALUES (?, ?)', (word, count))

    conn.commit()


@bot.command()
async def top5(ctx):
    cursor.execute('SELECT word, count FROM word_counts ORDER BY count DESC LIMIT 5')
    rows = cursor.fetchall()

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
                    reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)

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


@bot.command()
async def wc(ctx, word):
    word = word.lower()

    cursor.execute('SELECT count FROM word_counts WHERE word = ?', (word,))
    result = cursor.fetchone()

    if result:
        count = result[0]
        await ctx.send(f'The word "{word}" has been said {count} times.')
    else:
        await ctx.send(f'The word "{word}" has not been said yet.')


@bot.command()
async def ping(ctx):
    latency = bot.latency
    latency_ms = round(latency * 1000)

    await ctx.send(f"Pong! Latency: {latency_ms}ms")


@bot.command()
async def helpme(ctx):
    embed = discord.Embed(title="Raybitt Bot - Help", color=discord.Color.blue())
    embed.add_field(name="!top5", value="Display the top 5 most common words.", inline=False)
    embed.add_field(name="!wc <word>", value="Check how many times a word has been said.", inline=False)
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please provide all the required arguments.')

bot.run(token)

conn.close()
