"""\
Cog to implement audio guard features
"""

import discord

from discord.ext import commands


class AudioGuardCog(commands.Cog):
    is_connected = False
    guard_user = None
    whitelist = None

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self,
                                    member: discord.Member,
                                    before: discord.VoiceState,
                                    after: discord.VoiceState):
        if member == self.bot.user:
            return

        if before.channel is None:
            print(f"'{member}' connected to channel: {after.channel}")
        else:
            print(f"'{member}' disconnected from channel: {before.channel}")

        if member == self.guard_user and after.channel is None:
            await self.force()
            return

        if not self.is_connected or member in self.whitelist:
            print("safe call")
            return

        if (voice := after.channel) is not None and voice == self.guard_user.voice.channel:
            # TODO: disconnect user
            print("disconnect")
            channel: discord.VoiceChannel = await self.guard_user.guild.create_voice_channel(name="to_delete")
            await member.move_to(channel, reason="Disconnect by AudioGuard")
            await channel.delete(reason="Disconnect by AudioGuard")

    @commands.command(brief="Enable Audio Guard mode")
    async def on(self, ctx: commands.Context):
        if self.is_connected:
            await ctx.message.add_reaction("\u274C")
            await ctx.send("Already guarding another channel!")
            return

        voice_status: discord.VoiceState = ctx.author.voice
        if voice_status is not None:
            voice_channel: discord.VoiceChannel = voice_status.channel
            if voice_channel is not None:
                await voice_channel.connect()
                self.is_connected = True
                self.guard_user = ctx.author
                await ctx.message.add_reaction("\u2705")
                self.whitelist = voice_channel.members
                return

        await ctx.message.add_reaction("\u274C")
        await ctx.send("Not in a voice channel")

    @commands.command(brief="Disable Audio Guard mode")
    async def off(self, ctx: commands.Context):
        if not self.is_connected:
            await ctx.send("Not guarding anything!")
            return

        if self.guard_user != ctx.author:
            await ctx.send("Can't stop guarding. Not my master.")
            return

        for voice_client in self.bot.voice_clients:
            await voice_client.disconnect()

        await ctx.message.add_reaction("\u2705")
        self.is_connected = False

    @commands.command(brief="Reset bot status")
    async def force(self, _=None):
        self.is_connected = False
        for voice_client in self.bot.voice_clients:
            await voice_client.disconnect()
