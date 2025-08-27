import discord
from discord.ext import commands
from random import randint

class ReactionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return # When a slash command in run
        if message.author == self.bot.user:
            return
        
        nr = randint(0, 100)
        if nr == 0:
            if message.author.id in [819182608600399872, 932294125208895539]:
                await message.add_reaction("🫃")
    
def setup(bot):
    bot.add_cog(ReactionCog(bot))