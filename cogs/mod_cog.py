"""\
Cog to implement mod commands:
    - clear
    - send
    - kick
    - ban
    - unban
    - lockdown\
"""

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

    @commands.has_permissions(send_messages=True)
    @commands.command(brief="sends a given number of messages")
    async def send(self, ctx: commands.Context, nbr: int, *msg):
        "add a command to send a given number of messages"

        for _ in range(int(nbr)):
            await ctx.send(" ".join(msg))

    @commands.has_permissions(kick_members=True)
    @commands.command(brief="kick someone from the current guild")
    async def kick(self, ctx: commands.Context, user_id, *reason):
        "add command to kick someone from the current guild"

        user = await utils.auto_convert_obj(self.bot, ctx, user_id)
        await ctx.guild.kick(user, reason=" ".join(reason)+f" (on behalf of {ctx.author})")
        await ctx.send(f"user `{user}` kicked!")

    @commands.has_permissions(ban_members=True)
    @commands.command(brief="ban someone from the current guild")
    async def ban(self, ctx: commands.Context, user_id, delete_delay="", *, reason):
        "add command to ban someone from the current guild"

        user = await utils.auto_convert_obj(self.bot, ctx, user_id)
        if delete_delay.isdigit():
            if 0 <= int(delete_delay) <= 7:
                # await ctx.send(f"banned {user} ({delete_delay} days worth of messages\
                #     to delete) with reason: {' '.join(reason)}")
                await ctx.guild.ban(user,
                                    reason=" ".join(reason) + f" (on behalf of {ctx.author})",
                                    delete_message_days=int(delete_delay))
            else:
                await ctx.send("Only able to delete messages between 0 and 7 days ago")
                return
        else:
            reason = [delete_delay] + list(reason)
            # await ctx.send(f"banned {user} with reason: `{' '.join(reason)}`")
            await ctx.guild.ban(user, reason=" ".join(reason)+f" (on behalf of {ctx.author})")

        await ctx.send(f"user `{user}` banned!")

    @commands.has_permissions(ban_members=True)
    @commands.command(brief="unban someone from the current guild")
    async def unban(self, ctx: commands.Context, user_id, *, reason):
        "add command to unban someone from the current guild"

        user = await self.bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=" ".join(reason)+f" (on behalf of {ctx.author})")

    @commands.has_permissions(manage_roles=True)
    @commands.command(brief="removes send messages rights to specified role", pass_context=False)
    async def toggle_lockdown(self, targeted_role: discord.Role):
        "add command to removes send messages rights to specified role"

        perms = targeted_role.permissions

        if perms.send_messages():
            perms.update(send_messages=False)
        else:
            perms.update(send_messages=True)

        await targeted_role.edit(permissions=perms)
