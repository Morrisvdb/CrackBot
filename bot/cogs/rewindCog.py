import discord
from discord.ext import commands
from __init__ import bot, db
from models import Message, MessageType
from sqlalchemy import func

class RewindCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        new_message = Message.from_discord_message(message)
        db.add(new_message)
        db.commit()
        
    
    @discord.slash_command(name="rewind")
    @discord.option("user", "The user to rewind", type=discord.User)
    @discord.option('count', 'The number of messages to rewind', type=int)
    async def rewind(self, ctx, count, user):
        messages = (
            db.query(Message)
            .filter(func.json_extract(Message.json_content, '$.author.id') == str(user.id))
            .order_by(Message.id.desc())
            .limit(count)
            .all()
        )
        # messages = db.query(Message).filter(Message.json_content['author']['id']. == str(user.id)).limit(count).all()
        
        if len(messages) == 0:
            await ctx.respond(f"{user} has not deleted any messages recently")

        for message in messages:
            webhook = await ctx.channel.create_webhook(name="RewindWebhook")
            
            await webhook.send(
                content = message.json_content.get('content'),
                username = user.name,
                avatar_url = user.avatar,
            )
            
            await webhook.delete()

            await ctx.respond(f"Rewound {len(messages)} message(s) from user {user}", ephemeral = True)


            
        
def setup(bot):
    bot.add_cog(RewindCog(bot))