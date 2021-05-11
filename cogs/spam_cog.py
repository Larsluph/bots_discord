"""\
Cog to implement spamming commands:
    - start
    - stop\
"""

import asyncio
from typing import Union

import discord
from discord.ext import commands, tasks

from cogs import utils


class Spam(commands.Cog, name="SpamCog"):
    "Spam d.py cog (see module docstring for more info)"

    is_spamming = False
    contexts = dict()

    def __init__(self, bot):
        self.bot = bot
        self.spam_loop.start()

    @tasks.loop(seconds=1)
    async def spam_loop(self):
        "sends a message to every registered contexts"
        for id, text in self.contexts.items():
            if text is None:
               continue
            ctx = self.bot.get_channel(int(id))
            await ctx.send(text)

    @spam_loop.before_loop
    async def wait_for_bot_ready(self):
        "makes sure that bot is ready before spamming"
        await self.bot.wait_until_ready()

    @spam_loop.after_loop
    async def contexts_check(self):
        "removes contexts that got stopped"
        for ctx in self.contexts:
            if self.contexts[ctx] is None:
                del self.contexts[ctx]

        if len(self.contexts) == 0:
            self.is_spamming = False

    @commands.command(brief="start spamming given text every second")
    async def start(self, ctx: commands.Context, *text):
        "add a command to start spamming"

        if text[0] == "dm":
            user = await utils.auto_convert_obj(self.bot, ctx, text[1])
            if (channel := user.dm_channel) is None:
                id = user.create_dm().id
            else:
                id = channel.id
            print(f"Starting spam in dm: {ctx}")
            text = text[2:]
        else:
            id = ctx.channel.id
            print("Starting spam in current context")

        self.contexts[str(id)] = " ".join(map(str, text))

        if not self.is_spamming:
           self.is_spamming = True
           self.spam_loop.start()

    @commands.command(brief="stop spamming")
    async def stop(self, ctx: commands.Context, target: Union[discord.User, discord.TextChannel, int] = None):
        "add a command to stop spam user"

        if target is None:
            chan_id = ctx.channel.id
        elif isinstance(target, int):
            chan_id = target
        else:
            chan_id = target.id

        self.contexts[str(chan_id)] = None
        await ctx.send(f"Stopped spamming in channel {chan_id}!")
        print("Stopped spamming")

    @commands.command(brief="force stop spams")
    async def stopall(self, ctx: commands.Context):
        "add a command to force stop every spam in progress"
        self.is_spamming = False
        self.spam_loop.cancel()
        self.contexts = dict()
