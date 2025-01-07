import discord
from discord.ext import commands
from __init__ import bot, db
from models import MessageArchive


class ExtractionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
    @commands.command(name='extract', guild_ids=[977513866097479760])
    async def extract(self, ctx, count: int = 100, all: bool = False):
        if count == 0:
            count = None    
        
        if all:
            all_channels = ctx.guild.text_channels
        else:
            all_channels = [ctx.channel]
        
        statusmsg = await ctx.send(f"Found {len(all_channels)} text channels.")
        
        number = 0
        total_count = 0
        for channel in all_channels:
            await statusmsg.edit(f"Extracting channel {channel.name}.")
            async for message in channel.history(limit=count, oldest_first=True):
                MessageArchive.save(message_id=message.id, guild_id=message.guild.id, channel_id=message.channel.id, timestamp=message.created_at.timestamp(), user=message.author.name, content=message.content)
                number += 1
                total_count += 1
                if number % 100 == 0:
                    await statusmsg.edit(f"Extracted {number} messages from channel {channel.name}. \nTotal messages extracted: {total_count}.")
            await statusmsg.edit(f"Extracted channel {channel.name}.")
            number = 0
            
        await statusmsg.edit(f"Extracted {total_count} messages.")
    
        
def setup(bot):
    bot.add_cog(ExtractionCog(bot))