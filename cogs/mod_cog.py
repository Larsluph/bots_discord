"""\
Cog to implement mod commands:
    - clear
    - purge
    - send
    - kick
    - ban
    - unban
    - lockdown\
"""

from typing import Optional

import discord
from discord.ext import commands

from cogs import utils


class Mod(commands.Cog, name="ModCog"):
    "Mod d.py cog (see module docstring for more info)"

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cog_name = "ModCog"

    @commands.has_permissions(read_message_history=True, manage_messages=True)
    @commands.command(brief="clear a given number of messages in the given channel")
    async def clear(self, ctx: commands.Context, nbr: int, *criterias):
        "add command to clear a given number of messages with filters"

        nbr = int(nbr)+1
        if len(criterias) == 0:
            messages = await ctx.history(limit=nbr).flatten()
            for msg in messages:
                await msg.delete()
        else:
            filters = {
                "user": None,
                "channel": None
            }
            for criteria in criterias:
                obj = await utils.auto_convert_obj(self.bot, ctx, criteria)
                if isinstance(obj, discord.User) and not filters["user"]:
                    filters["user"] = obj
                elif isinstance(obj, discord.TextChannel) and not filters["channel"]:
                    filters["channel"] = obj

            if filters["channel"]:
                ctx = filters["channel"]

            i = 0
            async for msg in ctx.history():
                print("history")
                if i == nbr:
                    break

                if filters["user"] and msg.author == filters["user"]:
                    await msg.delete()
                    i += 1
        await ctx.send("Clear finished! :white_check_mark:", delete_after=1.5)

    @commands.command(brief="Purges a channel")
    async def purge(self, ctx: commands.Context):
        "add a command to purge a channel"

        deleted = await ctx.channel.purge()
        await ctx.send(f"Deleted {deleted} message(s).", delete_after=10)

    @commands.has_permissions(send_messages=True)
    @commands.command(brief="sends a given number of messages")
    async def send(self, ctx: commands.Context, nbr: int, *, msg: str):
        "add a command to send a given number of messages"

        for _ in range(int(nbr)):
            await ctx.send(msg)

    @commands.has_permissions(kick_members=True)
    @commands.command(brief="kick someone from the current guild")
    async def kick(self, ctx: commands.Context, user: discord.Member, *, reason: str):
        "add command to kick someone from the current guild"

        await ctx.guild.kick(user, reason=reason and f"{reason} (on behalf of {ctx.author})")
        await ctx.send(f"user `{user}` kicked!")

    @commands.has_permissions(ban_members=True)
    @commands.command(brief="ban someone from the current guild")
    async def ban(self, ctx: commands.Context, members: commands.Greedy[discord.Member], delete_delay: Optional[int] = 3, *, reason: Optional[str]):
        "add command to ban someone from the current guild"

        for member in members:
            await member.ban(delete_message_days=delete_delay, reason=reason and f"{reason} (on behalf of {ctx.author})")
            await ctx.send(f"user `{member}` banned!")

    @commands.has_permissions(ban_members=True)
    @commands.command(brief="unban someone from the current guild")
    async def unban(self, ctx: commands.Context, users: commands.Greedy[discord.User], *, reason: Optional[str]):
        "add command to unban someone from the current guild"

        for user in users:
            await ctx.guild.unban(user, reason=reason and f"{reason} (on behalf of {ctx.author})")
            await ctx.send(f"user `{user}` unbanned!")

    @commands.has_permissions(manage_roles=True)
    @commands.command(brief="removes send messages rights to specified role")
    async def lockdown(self, ctx: commands.Context, targeted_role: discord.Role):
        "add command to removes send messages rights to specified role"

        perms = targeted_role.permissions

        if perms.send_messages:
            perms.update(send_messages=False)
            msg = "Lockdown mode activated."
        else:
            perms.update(send_messages=True)
            msg = "Lockdown mode deactivated."

        await targeted_role.edit(permissions=perms)
        await ctx.send(msg)
