import discord
from discord.ext import commands
from collections import Counter


class ServerAnalytics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx):
        guild = ctx.guild
        total_members = guild.member_count
        online_members = len([member for member in guild.members if member.status != discord.Status.offline])
        offline_members = total_members - online_members
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)

        embed = discord.Embed(title="Server Statistics", color=discord.Color.blue())
        embed.add_field(name="Total Members", value=total_members, inline=False)
        embed.add_field(name="Online Members", value=online_members, inline=False)
        embed.add_field(name="Offline Members", value=offline_members, inline=False)
        embed.add_field(name="Text Channels", value=text_channels, inline=False)
        embed.add_field(name="Voice Channels", value=voice_channels, inline=False)
        embed.add_field(name="Categories", value=categories, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def topactive(self, ctx, limit=5):
        members = ctx.guild.members
        member_activity = {str(member): member.activity for member in members if member.activity}
        sorted_members = dict(Counter(member_activity).most_common(limit))

        embed = discord.Embed(title=f"Top {limit} Most Active Members", color=discord.Color.green())
        for index, (member_name, activity) in enumerate(sorted_members.items(), 1):
            embed.add_field(name=f"{index}. {member_name}", value=str(activity), inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def topchannels(self, ctx, limit=5):
        text_channels = ctx.guild.text_channels
        sorted_channels = sorted(text_channels, key=lambda c: c.message_count, reverse=True)[:limit]

        embed = discord.Embed(title=f"Top {limit} Text Channels by Message Count", color=discord.Color.orange())
        for index, channel in enumerate(sorted_channels, 1):
            embed.add_field(name=f"{index}. {channel.name}", value=f"Messages: {channel.message_count}", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def topvoice(self, ctx, limit=5):
        voice_channels = ctx.guild.voice_channels
        sorted_channels = sorted(voice_channels, key=lambda c: len(c.members), reverse=True)[:limit]

        embed = discord.Embed(title=f"Top {limit} Voice Channels by Member Count", color=discord.Color.purple())
        for index, channel in enumerate(sorted_channels, 1):
            embed.add_field(name=f"{index}. {channel.name}", value=f"Members: {len(channel.members)}", inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ServerAnalytics(bot))
