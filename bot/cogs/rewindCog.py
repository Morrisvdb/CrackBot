import discord
from discord.ext import commands
from __init__ import bot, db
from models import Message

class RewindCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return

        new_message = Message(message_id=message.id, content=message.content, user_id=message.author.id)
        db.add(new_message)
        db.commit()
        
    
    @discord.slash_command(name="rewind")
    @discord.option('count', 'The number of messages to rewind', type=int)
    @discord.option("user", "The user to rewind", type=discord.User, required=False)
    async def rewind(self, ctx, count, user):
        if user:
            messages = db.query(Message).filter(Message.user_id == user.id).limit(count).all()
        else:
            messages = db.query(Message).limit(count).all()
        

        for message in messages:
            user = await self.bot.fetch_user(message.user_id)
            await ctx.respond(f"**{user.name}:** {message.content}")

            
        
def setup(bot):
    bot.add_cog(RewindCog(bot))