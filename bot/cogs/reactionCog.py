import discord
from discord.ext import commands
from random import randint

def difference(string1, string2):
        # Split both strings into list items
        string1 = string1.split()
        string2 = string2.split()

        A = set(string1) # Store all string1 list items in set A
        B = set(string2) # Store all string2 list items in set B
        
        str_diff = A.symmetric_difference(B)
        return str_diff

class ReactionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return # When a slash command in run
        if message.author == self.bot.user:
            return
        
        nr = randint(0, 250)
        if nr == 0:
            # if message.author.id in [819182608600399872, 932294125208895539]:
                reactions = ["🇳", "🇮", "🇬", "🇪", "🇷", "🫃"]  
                # await message.add_reaction("🫃")
                for reaction in reactions:
                    await message.add_reaction(reaction)
                    
        
    
        
        
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.guild is None:
            return # When a slash command in run
        if before.author == self.bot.user:
            return
        
        # if before.author.id == 819182608600399872:
        #     return
        
        diff = list(difference(before.content, after.content))
        if len(diff) == 2:
            # if diff[0].lower() != diff[1].lower():
            # print("Just capitalized")
            pass # The message was just capitalised
                
        else:
            safe = True
            for word in diff:
                for char in word:
                    if word not in [".", ",", ":", "?", "!"]:
                        safe = False
                        
            if not safe:
                if before.guild.id == 894905195195150406: # Cuz custom emoji...
                    await after.add_reaction(await after.guild.fetch_emoji(1160854665462829068))
    
def setup(bot):
    bot.add_cog(ReactionCog(bot))