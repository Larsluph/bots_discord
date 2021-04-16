import discord
from discord.ext import commands

from typing import Text

class Giveaway(commands.Cog, name="GiveawayCog"):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = "GiveawayCog"

    @commands.command(brief="start a giveaway")
    async def start(self, ctx: commands.Context, duration: Text, prize: Text):
        duration = int(duration)
        await message.channel.send(f"""\
                **NEW GIVEAWAY !**
                ```
                {prize}
                Giveaway Duration: {duration} minutes
                Hosted by: <@{ctx.author.id}>
                ```""")
        # react
        for i in range(duration*2):
            time.sleep(30)
            # edit countdown
        # check reactions
        # chose random winner
        # congrats !
