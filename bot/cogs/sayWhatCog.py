from discord.ext import commands
from __init__ import db, bot
from models import ServerConfig

class SayWhatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return # When a slash command in run
        if message.author == self.bot.user:
            return

        if message.author.get_role(894922218235113504):
            content : str =  message.content.lower()
            if content[-4:] == "what" or content[-5:] == "what?":
                await message.channel.send("Chicken Butt!")
    
    
def setup(bot):
    bot.add_cog(SayWhatCog(bot))