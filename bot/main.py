import discord
from __init__ import bot, TOKEN

bot.load_extension('cogs.rewindCog')
bot.load_extension('cogs.sayWhatCog')
bot.load_extension('cogs.reactionCog')
# bot.load_extension('cogs.mirrorChannelCog')



@bot.event
async def on_ready():    
    print(f'{bot.user.name} has connected to Discord!')
    
@bot.event
async def on_application_command_error(ctx, e: Exception):
    if isinstance(e, discord.ext.commands.errors.PrivateMessageOnly):
        await ctx.respond("This command is DM only!", ephemeral=True)
        return
    elif isinstance(e, discord.ext.commands.errors.NoPrivateMessage):
        await ctx.respond("This command is Guild only!", ephemeral=True)
        return
    else:
        await ctx.respond("An error occured. If this keeps happening please contact a developer.")
        raise e

bot.run(TOKEN)