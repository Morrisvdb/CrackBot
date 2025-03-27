from discord.ext import commands
from __init__ import db, bot
from models import ServerConfig
from googletrans import Translator
from random import choice
from os import path

class SayWhatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def get_response(self):
        if (path.exists("bot/cogs/what.txt") == False):
            with open("bot/cogs/what.txt", "w") as f:
                f.write("Chicken Butt")
        with open("bot/cogs/what.txt", "r") as f:
            lines = f.readlines()
        return choice(lines).strip()
        
    async def translate_what(self, message):
        message = message.lower()
        
        async with Translator() as translator:
            print(f"Translating: {message}")
            translated = await translator.translate(message, dest='en')
            text = translated.text.lower()
            print(f"Translated: {text}")
            if text[-1] == "?":
                text = text[:-1]
            if text[-4:] == 'what':
                return True
            else:
                return False
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return # When a slash command in run
        if message.author == self.bot.user:
            return

        # if message.author.get_role(894922218235113504):
        content : str =  message.content.lower()
        if content[-4:] == "what" or content[-5:] == "what?":
            await message.channel.send(self.get_response())
        else:
            if (await self.translate_what(content)):
                await message.channel.send(self.get_response())
                
    
    
def setup(bot):
    bot.add_cog(SayWhatCog(bot))
