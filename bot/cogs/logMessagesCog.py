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
        # ignore bot messages
        if message.author.bot:
            return
        new_message = Message.from_discord_message(message)
        db.add(new_message)
        db.commit()
        
    @discord.app_commands.command(name='backlog')
    @discord.app_commands.describe(only_this="Set true to only retrieve this channel.")
    async def backlog(self, interaction: discord.Interaction, only_this: bool = False):
        # permission check
        if interaction.user.id != 819182608600399872:
            await interaction.response.send_message("Nuh Uh", ephemeral=True)
            return

        if interaction.guild is None:
            await interaction.response.send_message("This command must be used in a guild.", ephemeral=True)
            return

        if not only_this:
            channels = interaction.guild.text_channels
        else:
            channels = [interaction.channel]

        # initial response and grab the message object so we can edit it later
        await interaction.response.send_message(f"Aight, we cooking. Found {len(channels)} channels")
        progress_message = await interaction.original_response()

        for channel in channels:
            async for message in channel.history(limit=None):
                # skip bot messages
                if message.author.bot:
                    continue
                new_message = Message.from_discord_message(message)
                db.add(new_message)
                db.commit()
            await progress_message.edit(content=f"Finished extracting {channel.name}")

        await progress_message.edit(content="Success, your secrets are now mine!")
        
    
    

            
        
async def setup(bot):
    await bot.add_cog(LogMessagesCog(bot))
    # await bot.tree.sync()