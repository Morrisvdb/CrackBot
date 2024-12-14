from __init__ import bot, TOKEN

@bot.event
async def on_ready():
    bot.load_extension('cogs.rewindCog')
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)