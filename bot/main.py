import os
import discord

from __init__ import bot, TOKEN

# bot.load_extension('cogs.rewindCog')
# bot.load_extension('cogs.sayWhatCog')
# bot.load_extension('cogs.reactionCog')
# bot.load_extension('cogs.logMessagesCog')
# bot.load_extension('cogs.randomResponseCog')
# bot.load_extension('cogs.entranceTuneCog')

for file in os.listdir('./bot/cogs'):
    if file.endswith('.py'):
        bot.load_extension("cogs." + file[:-3])

@bot.event
async def on_ready():    
    print(f'{bot.user.name} has connected to Discord!')
    
    # async def setup_hook(self) -> None:
    #     # Wavelink 2.0 has made connecting Nodes easier... Simply create each Node
    #     # and pass it to NodePool.connect with the client/bot.
    #     node: wavelink.Node = wavelink.Node(uri='http://localhost:2333', password='youshallnotpass')
    #     await wavelink.NodePool.connect(client=self, nodes=[node])
    
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