import nextcord
import random
import requests
import json
from nextcord.ext import commands


class meme(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meme(self, ctx):
        reddit_api_url = 'https://www.reddit.com/r/memes/top/.json?sort=top&t=day&limit=100'
        try:
            response = requests.get(reddit_api_url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            meme_data = response.json()['data']['children']
            random_meme = random.choice(meme_data)['data']
            meme_title = random_meme['title']
            meme_url = random_meme['url']

            embed = nextcord.Embed(title=meme_title, color=nextcord.Color.green())
            embed.set_image(url=meme_url)

            await ctx.send(embed=embed)

        except requests.RequestException as e:
            await ctx.send(f"Error fetching meme: {e}")


def setup(bot):
    bot.add_cog(meme(bot))
