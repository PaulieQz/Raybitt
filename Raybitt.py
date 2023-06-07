# Raybitt
# short for Raymond Babbitt
# the autistic dude from Rain Man
# since the bot counts words
# and that's why I'm the name guy - Spacecow

import Config
import discord
from discord.ext import commands
import sqlite3
import nltk
from nltk.corpus import stopwords


intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True

nltk.download('stopwords')
stop_words = stopwords.words('english')
dumbasswords = stop_words[:10000]

bot = commands.Bot(command_prefix='!', intents=intents)

conn = sqlite3.connect('primary.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS word_counts (id INTEGER PRIMARY KEY, word TEXT, count INTEGER)')


def is_string_integer(string):
    return not string.isdigit()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')


@bot.event
async def on_message(message):
    if message.author == bot.user:
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

    await bot.process_commands(message)


@bot.command()
async def top5(ctx):
    cursor.execute('SELECT word, count FROM word_counts ORDER BY count DESC LIMIT 5')
    rows = cursor.fetchall()

    for row in rows:
        await ctx.send(f'The word: "{row[0]}" has been said: {row[1]} times')


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


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please provide all the required arguments.')

bot.run(Config.token)

conn.close()
