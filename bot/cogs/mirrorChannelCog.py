import discord
from __init__ import db
from discord.ext import commands
from models import TrackedChannels

class mirrorChannelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
                
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return  # Ignore DMs
        if message.author == self.bot.user:
            return  # Ignore messages from the bot itself

        # Check if the channel is tracked
        tracked_channel = db.query(TrackedChannels).filter_by(channel_id=message.channel.id).first()
        if tracked_channel:
            # If the channel is tracked, mirror the message to the target channel
            target_channel = self.bot.get_channel(tracked_channel.target_channel_id)
            if target_channel:
                webhook = await target_channel.create_webhook(name=f"MirrorWebhook-{message.author.name}")
                await webhook.send(
                    content=message.content,
                    username=message.author.name,
                    avatar_url=message.author.avatar.url if message.author.avatar else None,
                    embeds=message.embeds,
                    files=[await file.to_file() for file in message.attachments]
                )
                await webhook.delete()  # Clean up the webhook after use

    @discord.slash_command(name='list_server_channels', guild_ids=[1380949984673009805])
    @commands.has_permissions(manage_channels=True)
    async def list_server_channels(self, ctx, guild_id):
        """List all channels in the server."""
        guild = self.bot.get_guild(int(guild_id))   # Fetch the guild by ID
        if not guild:
            await ctx.respond("Guild not found.")
            return
        
        channels = guild.text_channels
        channel_list = "\n".join([f"{channel.name} (ID: {channel.id})" for channel in channels])
        if not channel_list:
            await ctx.respond("No text channels found in this server.")
        else:
            await ctx.respond(f"Text channels in {guild.name}:\n{channel_list}")

    @discord.slash_command(name='track_channel', guild_ids=[1380949984673009805])
    @commands.has_permissions(manage_channels=True)
    async def track_channel(self, ctx, target_channel_id,
                            fill_channel: discord.Option(bool, required = False, description="Wether the bot should put the last n messages in this channel so you can catch up.") = False, 
                            depth: discord.Option(int, required = False, description="The amount of messages to go back. ~1s/message. Default is 10 messages") = 10
                            ):
        """Track the current channel and mirror messages to the target channel."""
        try:
            target_channel_id = int(target_channel_id)
        except ValueError:
            target_channel_id = 0
            
        channel = self.bot.get_channel(target_channel_id)
        
        if db.query(TrackedChannels).filter_by(target_channel_id = ctx.channel.id).first() is not None:
            if db.query(TrackedChannels).filter_by(target_channel_id = ctx.channel.id).first().channel_id == target_channel_id:
                await ctx.respond(f"This channel is already mapped to {channel.mention}")
                return
        
        tracked_channel = TrackedChannels(guild_id = channel.guild.id, channel_id = target_channel_id, target_channel_id = ctx.channel.id)
        db.add(tracked_channel)
        db.commit()
        
        if fill_channel:
            messages = await channel.history(limit = depth).flatten()
            messages = messages[::-1]
        
            for message in messages:
                await ctx.send(f"**{message.author.name}: ** {message.content}")
                
                # webhook = await ctx.channel.create_webhook(name=f"MirrorWebhook-{message.author.name}")
                # await webhook.send(
                #     content=message.content,
                #     username=message.author.name,
                #     avatar_url=message.author.avatar.url if message.author.avatar else None,
                #     embeds=message.embeds,
                #     files=[await file.to_file() for file in message.attachments]
                # )
                # await webhook.delete()  # Clean up the webhook after use
        
        
            await ctx.send(f"Tracking channel {channel.mention} into this channel")
            return
        await ctx.respond(f"Tracking channel {channel.mention} into this channel")
        

    @discord.slash_command(name='untrack_channel', guild_ids=[1380949984673009805])
    @commands.has_permissions(manage_channels=True)
    async def untrack_channel(self, ctx):
        """Stop tracking the current channel."""
        tracked_channel = db.query(TrackedChannels).filter_by(target_channel_id = ctx.channel.id).first()
        if tracked_channel:
            db.delete(tracked_channel)
            db.commit()
            await ctx.respond(f"Stopped tracking this channel.")
        else:
            await ctx.respond(f"This channel is not being tracked.")


def setup(bot):
    bot.add_cog(mirrorChannelCog(bot))
