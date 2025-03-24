from __init__ import bot, TOKEN

bot.load_extension('cogs.rewindCog')
# bot.load_extension('cogs.extractionCog')


@bot.event
async def on_ready():
    bot.load_extension('cogs.rewindCog')
    print(f'Loaded cog: rewindCog')
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)