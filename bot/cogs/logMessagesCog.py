import discord
from discord.ext import commands
from __init__ import bot, db
from models import Message, MessageType
from sqlalchemy import func

class LogMessagesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        new_message = Message.from_discord_message(message)
        db.add(new_message)
        db.commit()
        
    @discord.slash_command(name='backlog')
    @discord.option("only_this", "Set true to only retrieve this channel.", type = bool)
    async def backlog(self, ctx, only_this):
        if not only_this:
            channels = ctx.guild.text_channels
        else:
            channels = [ctx.channel]
        
        await ctx.respond(f"Aight, we cooking. Found {len(channels)} channels")
        for channel in channels:
            history = await channel.history(limit = None).flatten()
            for message in history:
                new_message = Message.from_discord_message(message)
                db.add(new_message)
                db.commit()
        await ctx.send("Success")
        
    
    

            
        
def setup(bot):
    bot.add_cog(LogMessagesCog(bot))