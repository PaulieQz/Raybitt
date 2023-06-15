import sqlite3
import nltk
import configparser
import re
import cursor
from discord.ext import commands
from nltk.corpus import stopwords


class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        config = configparser.ConfigParser()
        config.read('config.ini')
        database_file = config['Database']['File']
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()
        nltk.download("stopwords")
        self.dumbasswords = stopwords.words('english')
        self.symbols = ['+', '×', '÷', '=', '/', '_', '<', '>', '[', ']', '!', '@', '#', '$', '%', '^', '&', '*', '(',
                        ')', '-', ':', ';', ',', '?', '`', '~', '|', '{', '}', '€', '£', '¥', '₩', '°', '•', '○', '●',
                        '□', '■', '♤', '♡', '◇', '♧', '☆', '▪︎', '¤', '《', '¿']


    @staticmethod
    def remove_symbols(text):
        # Remove all non-alphanumeric characters (excluding spaces) from the string
        return re.sub(r'[^a-zA-Z0-9\s]', '', text)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith(self.bot.command_prefix):
            await self.bot.proccess_commands(message)
            return
        words = message.content.split()
        for word in words:
            if word not in self.dumbasswords:
                word = self.remove_symbols(word)
                word = word.lower()
                if len(word) > 2 and word.isalpha():
                    try:
                        self.cursor.execute('SELECT count FROM word_counts WHERE word = ?', [word])
                        result = self.cursor.fetchone()
                    except sqlite3.Error as error:
                        print(f"Failed to read data from SELECT statement. Word: {word} Error: {error}")
                    if result:
                        count = result[0] + 1
                        try:
                            self.cursor.execute('UPDATE word_counts SET count = ? WHERE word = ?', (count, word))
                        except sqlite3.Error as error:
                            print(f"Failed to UPDATE word count for Word: {word}. Error: {error}")
                    else:
                        count = 1
                        try:
                            self.cursor.execute('INSERT INTO word_counts (word, count) VALUES (?, ?)', (word, count))
                        except sqlite3.Error as error:
                            print(f"Failed to Insert word into table. Word: {word}. Error {error}")
                try:
                    self.conn.commit()
                except sqlite3.Error as error:
                    print(f"Failed to commit changes for Word: {word}. Error: {error}")


async def setup(bot):
    await bot.add_cog(Listener(bot))
