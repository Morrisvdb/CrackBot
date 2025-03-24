import discord
from discord.ext import commands
from __init__ import bot, db
from models import MessageArchive
import os, json

async def jsonify(message: discord.Message):
    dict = {
        "content": message.content,
        "author": message.author.name,
        "is_bot": message.author.bot,
        "timestamp": str(message.created_at),
        "embeds": [embed.to_dict() for embed in message.embeds]
    }
    return dict

async def saveData(channelData, channel):
    if not os.path.exists(channel.guild.name):
        os.mkdir(channel.guild.name)
    if os.path.exists(f"./{channel.guild.name}/{channel.name}.json"):
        os.remove(f"./{channel.guild.name}/{channel.name}.json")
    with open(f"./{channel.guild.name}/{channel.name}.json", "w") as file:
        file.write(json.dumps(channelData, indent=4))


class ExtractionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="extract", aliases=["e"], guild_ids=[977513866097479760])
    async def extract(self, ctx, lim: int = None):
        if ctx.author.id != 819182608600399872:
            return
        for channel in ctx.guild.text_channels:
            count = 0
            print(f"Extracting channel {channel.name}...")
            channelData = []
            async for msg in channel.history(limit=lim, oldest_first=True):
                count += 1
                if count % 100 == 0:
                    print(f"Progress: {count}", end='\r')
                message = await jsonify(msg)
                channelData.append(message)
                
            await saveData(channelData, channel)
            await ctx.send(f"Data extracted from {channel.name} successfully!")
            print(f"Data extracted from {channel.name} successfully!")
        print(f"------- Extraction of {ctx.guild.name} Complete! -------")
        
def setup(bot):
    bot.add_cog(ExtractionCog(bot))