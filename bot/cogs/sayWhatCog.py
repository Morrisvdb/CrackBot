from discord.ext import commands
from __init__ import db, bot
from models import ServerConfig
from googletrans import Translator

class SayWhatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def translate_what(self, message):
        message = message.lower()
        if message[-1] == "?":
            message = message[:-1]
        async with Translator() as translator:
            translated = await translator.translate(message, dest='en')
            if translated.text.lower() == 'what':
                return True
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return # When a slash command in run
        if message.author == self.bot.user:
            return

        if message.author.get_role(894922218235113504):
            content : str =  message.content.lower()
            if content[-4:] == "what" or content[-5:] == "what?":
                await message.channel.send("Chicken Butt")
            else:
                await self.translate_what(content)
                await message.channel.send("Chicken Butt")
                
    
    
def setup(bot):
    bot.add_cog(SayWhatCog(bot))
