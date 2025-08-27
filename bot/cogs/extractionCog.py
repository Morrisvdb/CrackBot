import discord
from discord.ext import tasks
from discord.ext import commands
from __init__ import bot, db
from models import Message
import os, json
from sqlalchemy import func

class ExtractionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def extract_guilds(self, guilds: list):
        for guild in guilds:
            channels = guild.channels
            for channel in channels:
                oldest = channel.history(limit=1, oldest_first=True)[0]
                if db.query(Message).filter(func.json_extract(Message.json_content, '$.id') == str(oldest.id)):
                    # Oldest message in log matches the channels oldest message, continue with the next channel
                    continue
                else:
                    print("Found unknown channel, extracting...")
                    for message in channel.history(limit=None).flatten():
                        Message.from_discord_message(message)
        
    @commands.Cog.listener()
    async def on_message(self, message):
        Message.from_discord_message(message)
        
    @commands.Cog.listener()
    async def on_ready(self):
        guilds = bot.guilds
        self.extract_guilds(guilds=guilds)
        
    # @discord.slash_command(name)
    # # TODO: Somehow trigger the extract function


# messages = (
#             db.query(Message)
#             .filter(func.json_extract(Message.json_content, '$.author.id') == str(user.id))
#             .order_by(Message.id.desc())
#             .limit(count)
#             .all()
#         )

# async def jsonify(message: discord.Message):
#     dict = {
#         "content": message.content,
#         "author": message.author.name,
#         "is_bot": message.author.bot,
#         "timestamp": str(message.created_at),
#         "embeds": [embed.to_dict() for embed in message.embeds]
#     }
#     return dict

# async def saveData(channelData, channel):
#     if not os.path.exists(channel.guild.name):
#         os.mkdir(channel.guild.name)
#     if os.path.exists(f"./{channel.guild.name}/{channel.name}.json"):
#         os.remove(f"./{channel.guild.name}/{channel.name}.json")
#     with open(f"./{channel.guild.name}/{channel.name}.json", "w") as file:
#         file.write(json.dumps(channelData, indent=4))


# class ExtractionCog(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
        
#     @commands.Cog.listener()
#     async def on_message(self, message):
#         if message.author == self.bot:
#             return
        
#         MessageArchive.save(message.id, message.guild.id, message.channel.id, message.created_at.timestamp(), message.author.name, message.content)

#     @discord.slash_command(name="extract", aliases=["e"], guild_ids=[977513866097479760])
#     async def extract(self, ctx, lim: int = None):
#         if ctx.author.id != 819182608600399872:
#             return
#         for channel in ctx.guild.text_channels:
#             count = 0
#             print(f"Extracting channel {channel.name}...")
#             channelData = []
#             async for msg in channel.history(limit=lim, oldest_first=True):
#                 count += 1
#                 if count % 100 == 0:
#                     print(f"Progress: {count}", end='\r')
#                 message = await jsonify(msg)
#                 channelData.append(message)
                
#             await saveData(channelData, channel)
#             await ctx.send(f"Data extracted from {channel.name} successfully!")
#             print(f"Data extracted from {channel.name} successfully!")
#         print(f"------- Extraction of {ctx.guild.name} Complete! -------")
        
def setup(bot):
    bot.add_cog(ExtractionCog(bot))