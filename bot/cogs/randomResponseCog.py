from discord.ext import commands
import discord
from discord import app_commands
from __init__ import db
from models import Message, ServerConfig
from sqlalchemy import func
from random import choice
from string import punctuation, whitespace
import requests

class randomResponseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def pick_random_word(self, guild):
        # return db.query(Message).first().json_content["guild_id"]
        messages = (db.query(Message)
                    # .filter(Message.json_content['guild_id'] == guild.id)
                    # .filter(str(func.json_extract(Message.json_content, '$.guild_id')) == str(guild.id))
                    .all())
        words = []
        for message in messages:
            if message.json_content["guild_id"] == guild.id:
                for word in message.json_content['content'].lower().split():
                    pop_characters = list(punctuation)
                    for character in pop_characters:
                        word = word.replace(character, "")
                    if word in words:
                        pass
                    else:
                        words.append(word)
            
        real_words = []
        with open("./words.txt", 'r') as file:
            real_words = file.read().split("\n")
            real_words = [item.lower() for item in real_words]
                
        # print(real_words)    
        
        while True:
            picked = choice(words)
            # print(picked)
            if picked in real_words:
                break
            
        return picked
                    

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return
        if message.author == self.bot.user:
            return
        
        response = "https://tenor.com/view/tesla-and-einstein-luma-ai-gif-14475294631445060178"
        current_word = db.query(ServerConfig).filter_by(guild_id = message.guild.id, key = "random_word").first()
        if not current_word:
            return
        if current_word.value in message.content.split():
            await message.channel.send(response)
            await message.channel.send(f"Correct, the word was `{current_word.value}`! Picking a new word")
            current_word.value = self.pick_random_word(message.guild)
            db.add(current_word)
            db.commit()
            
    @app_commands.command(name="reset_word")
    async def reset_word(self, interaction: discord.Interaction):
        """Pick and set a new random word for this guild."""
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("This command must be used in a guild.", ephemeral=True)
            return

        word = self.pick_random_word(guild)

        config = db.query(ServerConfig).filter_by(guild_id=guild.id, key="random_word").first()
        if config:
            await interaction.response.send_message(f"The chosen word was `{config.value}`, selecting a new word")
            config.value = word
            db.add(config)
            db.commit()
            return

        await interaction.response.send_message("No word was chosen before, setting word.")
        new_config = ServerConfig(guild_id=guild.id, key="random_word", value=word)
        db.add(new_config)
        db.commit()
            
        
        
                
    
    
async def setup(bot):
    await bot.add_cog(randomResponseCog(bot))
    # await bot.tree.sync()
