from discord.ext import commands
from googletrans import Translator
from numpy.random import choice
from os import path
import json

class SayWhatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def get_response(self):
        if (path.exists("bot/cogs/what.json") == False):
            with open("bot/cogs/what.json", "w") as f:
                f.write("""
                {\"responses\": {\"Chicken Butt\": 0.99}")}
                """)
        with open("bot/cogs/what.json", "r") as f:
            json_data = json.load(f)
            
        if sum(list(json_data["responses"].values())) != 1:
            print("0.o; Someone has not set up the what.json file correctly. Defaulting to Chicken Butt.")
            chosen = ["Chicken Butt"]
        else:
            chosen = choice(list(json_data["responses"].keys()), 1, p=list(json_data["responses"].values()))
            
        return chosen[0]
        
    async def translate_what(self, message):
        message = message.lower()

        async with Translator() as translator:
            # print(f"Translating: {message}")
            translated = await translator.translate(message, dest='en')
            text = translated.text.lower()
            # print(f"Translated: {text}")
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
        content =  message.content.lower()
        # print("Message" + content)
        if content[-4:] == "what" or content[-5:] == "what?":
            await message.channel.send(self.get_response())
        else:
            # print("Message" + content)
            if (await self.translate_what(content)):
                await message.channel.send(self.get_response())
                
    
    
def setup(bot):
    bot.add_cog(SayWhatCog(bot))
