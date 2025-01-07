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
        
    @commands.command(name='recall', guild_ids=[977513866097479760])
    async def recall(self, ctx, count: int):
        messages = db.query(Message).order_by(Message.id.desc()).limit(count).all()
        if len(messages) < count:
            await ctx.send("Not enough messages in history.")
            return

        nth_message = messages[-1]
        
        user = self.bot.get_user(nth_message.user_id)
        
        new_webhook = await ctx.channel.create_webhook(name = user.name, avatar = await user.avatar.read(), reason = "Rewind")
        await new_webhook.send(content=nth_message.content)
        await new_webhook.delete()


def setup(bot):
    bot.add_cog(RewindCog(bot))