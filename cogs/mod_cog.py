"""\
Cog to implement mod commands:
    - clear
    - send
    - kick
    - ban
    - unban
    - lockdown\
"""

from typing import Optional

from discord import Member, Message, TextChannel, User
from discord.ext import commands


class Mod(commands.Cog, name="ModCog"):
    """Mod d.py cog (see module docstring for more info)"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cog_name = "ModCog"

    @commands.has_permissions(read_message_history=True, manage_messages=True)
    @commands.command(brief="clear a given number of messages in the given channel")
    async def clear(self, ctx: commands.Context,
                    nbr: int,
                    person: commands.Greedy[Member],
                    channel: Optional[TextChannel]):
        """clear a given number of messages in the given channel"""

        target = channel if channel else ctx.channel

        deleted = await target.purge(limit=min(100, nbr + 1),
                                     check=lambda msg: msg.author in person if person else True)

        await ctx.send(f"{len(deleted)} messages deleted! :white_check_mark:", delete_after=2)

    @commands.has_permissions(read_message_history=True, manage_messages=True)
    @commands.command(brief="Clears all messages between 2 specified messages (bound included)")
    async def clear_timeframe(self, ctx: commands.Context,
                              msg1: Message,
                              msg2: Message,
                              channel: Optional[TextChannel]):
        """Clears all messages between 2 specified messages (bound included)"""

        target = channel if channel else ctx.channel

        if msg1.id > msg2.id:
            msg2, msg1 = msg1, msg2

        deleted = await target.purge(check=lambda msg: msg1.id <= msg.id <= msg2.id)
        await ctx.message.delete()

        await ctx.send(f"{len(deleted)} messages deleted! :white_check_mark:", delete_after=2)

    @commands.has_permissions(send_messages=True)
    @commands.command(brief="sends a given number of messages")
    async def send(self, ctx: commands.Context, nbr: int, *, content: str):
        """sends a given number of messages"""

        for _ in range(int(nbr)):
            await ctx.send(content)

    @commands.has_permissions(kick_members=True)
    @commands.command(brief="kick someone from the current guild")
    async def kick(self, ctx: commands.Context, user: Member, *, reason: str):
        """kick someone from the current guild"""

        await ctx.guild.kick(user, reason=reason and f"{reason} (on behalf of {ctx.author})")
        await ctx.send(f"user `{user}` kicked!")

    @commands.has_permissions(ban_members=True)
    @commands.command(brief="ban someone from the current guild")
    async def ban(self, ctx: commands.Context,
                  members: commands.Greedy[Member],
                  delete_delay: Optional[int] = 3, *,
                  reason: Optional[str]):
        """ban someone from the current guild"""

        for member in members:
            await member.ban(
                delete_message_days=delete_delay,
                reason=reason and f"{reason} (on behalf of {ctx.author})"
            )
            await ctx.send(f"user `{member}` banned!")

    @commands.has_permissions(ban_members=True)
    @commands.command(brief="unban someone from the current guild")
    async def unban(self, ctx: commands.Context,
                    users: commands.Greedy[User], *,
                    reason: Optional[str]):
        """unban someone from the current guild"""

        for user in users:
            await ctx.guild.unban(user, reason=reason and f"{reason} (on behalf of {ctx.author})")
            await ctx.send(f"user `{user}` unbanned!")

    # @commands.has_permissions(manage_roles=True)
    # @commands.command(brief="removes send messages rights to specified role")
    # async def lockdown(self, ctx: commands.Context, targeted_role: Role):
    #     "removes send messages rights to specified role"

    #     perms = targeted_role.permissions

    #     if perms.send_messages:
    #         perms.update(send_messages=False)
    #         msg = "Lockdown mode activated."
    #     else:
    #         perms.update(send_messages=True)
    #         msg = "Lockdown mode deactivated."

    #     await targeted_role.edit(permissions=perms)
    #     await ctx.send(msg)
