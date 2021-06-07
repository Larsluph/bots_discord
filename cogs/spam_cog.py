"""\
Cog to implement spamming commands:
    - start
    - stop\
"""

from typing import Union, Optional

import discord
from discord.ext import commands, tasks


class Spam(commands.Cog, name="SpamCog"):
    """Spam d.py cog (see module docstring for more info)"""

    is_spamming = False
    contexts = dict()

    def __init__(self, bot):
        self.bot = bot

    def force_stop(self):
        self.is_spamming = False
        self.spam_loop.cancel()
        self.contexts.clear()

    @tasks.loop(seconds=1)
    async def spam_loop(self):
        """sends a message to every registered contexts"""
        to_spam = self.contexts.copy()
        for chan_id, text in to_spam.items():
            if text is None:
                continue

            ctx = self.bot.get_channel(int(chan_id))
            if ctx is None:
                del self.contexts[chan_id]
                continue

            await ctx.send(text)

    @spam_loop.before_loop
    async def wait_for_bot_ready(self):
        """makes sure that bot is ready before spamming"""
        await self.bot.wait_until_ready()

    @spam_loop.after_loop
    async def contexts_check(self):
        """removes contexts that got stopped"""
        if self.spam_loop.is_being_cancelled():
            pass

        for ctx in self.contexts:
            if self.contexts[ctx] is None:
                del self.contexts[ctx]

        if len(self.contexts) == 0:
            self.force_stop()

    @spam_loop.error
    async def on_loop_error(self, error):
        print(f"error: {error}")

        self.force_stop()

    @commands.command(brief="start spamming given text every second")
    async def start(self,
                    ctx: commands.Context,
                    channel: Optional[Union[discord.User, discord.TextChannel]] = None,
                    *, text):
        """add a command to start spamming"""

        if isinstance(channel, discord.User):
            chan_id = (await channel.create_dm()).id
            print(f"Starting spam in dm: {channel}")
        elif isinstance(channel, discord.TextChannel):
            chan_id = channel.id
            print(f"Starting spam in channel: {channel}")
        else:
            chan_id = ctx.channel.id
            print("Starting spam in current context")

        self.contexts[str(chan_id)] = text

        if not self.is_spamming:
            self.is_spamming = True
            self.spam_loop.start()

    @commands.command(brief="stop spamming")
    async def stop(self, ctx: commands.Context, target: Optional[Union[discord.User, discord.TextChannel]] = None):
        """add a command to stop spam user"""

        if target is None:
            chan_id = ctx.channel.id
            print("Stopped spamming in current context")
        else:
            chan_id = target.id
            print(f"Stopped spamming in: {target}")

        self.contexts[str(chan_id)] = None
        await ctx.send(f"Stopped spamming in channel {chan_id}!")

    @commands.command(brief="force stop all spams")
    async def stopall(self, _: commands.Context):
        """add a command to force stop every spam in progress"""
        self.force_stop()
