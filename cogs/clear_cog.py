import discord
from discord.ext import commands

class Clear(commands.Cog, name="Clear"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cog_name = "Misc"

    @commands.command(brief="clear a given number of messages in the given channel")
    @commands.has_permissions(read_message_history=True, manage_messages=True)
    async def clear(self, ctx: commands.Context, nbr: int, channel: discord.TextChannel, *filters):
        if len(filters) == 0:
            async for msg in ctx.history(limit=int(nbr)):
                ## delete messages
                await msg.delete()
