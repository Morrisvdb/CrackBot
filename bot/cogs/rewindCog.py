import discord
from discord import app_commands
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
        
    
    @app_commands.command(name="rewind")
    @app_commands.describe(user="The user to rewind", count="The number of messages to rewind")
    async def rewind(self, interaction: discord.Interaction, user: discord.User, count: int):
        messages = (
            db.query(Message)
            .filter(func.json_extract(Message.json_content, '$.author.id') == str(user.id))
            .order_by(Message.id.desc())
            .limit(count)
            .all()
        )
        # messages = db.query(Message).filter(Message.json_content['author']['id']. == str(user.id)).limit(count).all()
        
        if len(messages) == 0:
            await interaction.response.send_message(f"{user} has not deleted any messages recently", ephemeral=True)
            return

        channel = interaction.channel
        # Send rewound messages via webhook(s)
        for message in messages:
            webhook = await channel.create_webhook(name="RewindWebhook")
            try:
                await webhook.send(
                    content=message.json_content.get('content'),
                    username=user.name,
                    avatar_url=user.avatar,
                )
            finally:
                await webhook.delete()

        await interaction.response.send_message(f"Rewound {len(messages)} message(s) from user {user}", ephemeral=True)


            
        
async def setup(bot):
    await bot.add_cog(RewindCog(bot))
    # await bot.tree.sync()