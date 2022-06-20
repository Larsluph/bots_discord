from datetime import datetime as dt
from typing import Optional

from discord import Role, Message, Member, TextChannel
from discord.ext import commands


class Retardataire(commands.Cog, name="RetardataireCog"):
    role: Optional[Role]

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cog_name = "RetardataireCog"
        self.role = None

    @commands.command(brief="Sets the role to give to the user before spam")
    def set_role(self, role: Role):
        self.role = role

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        channel: TextChannel = message.channel
        message: Message = await channel.history(limit=1).flatten()[-1]
        # if (dt.now() - message.created_at).seconds > 60*20:
        if True:
            if self.role is None:
                await channel.send("role not assigned")
                return

            author: Member = message.author
            await author.add_roles(self.role)
            await channel.send(self.role.mention)
            await author.remove_roles(self.role)
