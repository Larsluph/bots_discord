"""\
Cog to implement spamming commands:
    - start
    - stop\
"""

import asyncio

from discord.ext import commands


class Spam(commands.Cog, name="SpamCog"):
    "Spam d.py cog (see module docstring for more info)"

    def __init__(self, bot):
        self.bot = bot
        self.cog_name = "SpamCog"
        self.spam_status = False

    @commands.command(brief="start spamming given text every second")
    async def start(self, ctx: commands.Context, *text):
        "add a command to start spamming"

        self.spam_status = True

        if text[0] == "dm":
            ctx = self.bot.get_user(int(text[1]))
            print(f"starting spam on user {ctx.display_name}#{ctx.discriminator}")
            text = " ".join(map(str, text[2:]))
        else:
            text = " ".join(map(str, text))

        while self.spam_status:
            await ctx.send(text)
            await asyncio.sleep(1/3)

    @commands.command(brief="stop spamming")
    async def stop(self, ctx: commands.Context):
        "add a command to stop spam user"

        self.spam_status = False
        await ctx.send("Stopped spamming!")
        print("stopped spamming")
