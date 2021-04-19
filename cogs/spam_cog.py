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

    delay = 1
    # spam_status = False
    contexts = dict()

    def __init__(self, bot):
        self.bot = bot
        self.cog_name = "SpamCog"

        self.spam_loop.start()

    @tasks.loop(seconds=1)
    async def spam_loop(self):
        "sends a message to every registered contexts"
        for ctx in self.contexts:
            await ctx.send(self.contexts[ctx])

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

    # async def spam_loop(self):
    #     "sends a message to every registered contexts"
    #     if self.spam_status:
    #         return

    #     self.spam_status = True
    #     while self.contexts.keys():
    #         for ctx in self.contexts:
    #             if self.contexts[ctx] is None:
    #                 del self.contexts[ctx]
    #                 continue

    #             await ctx.send(self.contexts[ctx])

    #         await asyncio.sleep(self.delay)

    #     self.spam_status = False

    @commands.command(brief="start spamming given text every second")
    async def start(self, ctx: commands.Context, *text):
        "add a command to start spamming"

        if text[0] == "dm":
            ctx = await utils.auto_convert_obj(self.bot, ctx, text[1])
            print(f"Starting spam in dm: {ctx}")
            text = " ".join(map(str, text[2:]))
        else:
            print("Starting spam in current context")
            text = " ".join(map(str, text))

        self.contexts[ctx] = text
        await self.spam_loop()

    @commands.command(brief="stop spamming")
    async def stop(self, ctx: commands.Context, target: Union[discord.User, discord.TextChannel, int] = None):
        "add a command to stop spam user"

        if target is None:
            chan_id = ctx.channel.id
        elif isinstance(target, int):
            chan_id = target
        else:
            chan_id = target.id

        self.contexts[chan_id] = None
        await ctx.send("Stopped spamming!")
        print("Stopped spamming")

    @commands.command(brief="force stop spams", pass_context=False)
    async def stopall(self):
        "add a command to force stop every spam in progress"
        self.spam_loop.cancel()
        self.contexts = dict()
