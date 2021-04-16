import time

import discord
from discord.ext import commands


class Spam(commands.Cog, name="SpamCog"):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = "SpamCog"
        self.spam_status = False

    @commands.command(brief="start spamming given text every second")
    async def start(self, ctx: commands.Context, *text):
        self.spam_status = True

        if text[0] == "dm":
            ctx = self.bot.get_user(int(text[1]))
            print(f"starting spam on user {ctx.display_name}#{ctx.discriminator}")
            text = " ".join(map(str, text[2:]))
        else:
            text = " ".join(map(str, text))

        while self.spam_status:
            await ctx.send(text)
            time.sleep(1/3)
        else:
            await ctx.send("Stopped spamming!")
            print("stopped spamming")

    @commands.command(brief="stop spamming")
    async def stop(self, ctx: commands.Context):
        self.spam_status = False
