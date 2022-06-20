"""
Cog to implement delay tracking features
"""

from typing import Optional

from discord import Member, User
from discord.ext import commands


class Retard(commands.Cog, name="RetardCog"):
    """Retard d.py cog (see module docstring for info)"""

    cog_name: str = "RetardCog"
    bot: commands.Bot

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(brief="Register user's delay in DB")
    async def add_record(self, ctx: commands.Context,
                    member: Member,
                    *duration):
        """Register user's delay in DB"""
        pass
