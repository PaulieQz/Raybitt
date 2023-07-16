# Raybitt-old
# short for Raymond Babbitt
# the autistic dude from Rain Man
# since the bot counts words
# and that's why I'm the name guy - Spacecow
import nextcord as discord
import sqlite3
import configparser
import os
from nextcord.ext import commands
import tracemalloc
import random
tracemalloc.start()

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents)

config = configparser.ConfigParser()
config.read('config.ini')

database_file = config['Database']['File']
token = config['Bot']['Token']


def loadCog(extension):
    try:
        bot.load_extension(extension)
        print(f"Cog {extension} loaded.")
    except commands.ExtensionNotFound:
        print(f"Cog '{extension}' not found.")
    except commands.ExtensionAlreadyLoaded:
        print(f"Cog '{extension}' is already loaded.")
    except commands.ExtensionFailed as e:
        print(f"Cog '{extension}' failed to load. Reason: {e}")


@bot.event
async def on_ready():
    config = configparser.ConfigParser()
    config.read('config.ini')

    database_file = config['Database']['File']
    token = config['Bot']['Token']

    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS word_counts (id INTEGER PRIMARY KEY, word TEXT, count INTEGER)')

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            loadCog(f"cogs.{filename[:-3]}")
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')


bot.run(token)
