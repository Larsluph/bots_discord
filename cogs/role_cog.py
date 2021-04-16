import time

import discord
from discord.ext import commands

class Role(commands.Cog, name="RoleCog"):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = "RoleCog"

    @commands.command(brief="create personal role")
    async def claim(self, ctx: commands.Context):
        for role in ctx.author.roles:
            if role.name == ctx.author.name:
                break
        else:
            # no role found
            new_role = await ctx.guild.create_role(name=ctx.author.name, colour=discord.Color.random())
            await ctx.author.add_roles(new_role, reason="Claimed by bot")
            await ctx.send("Role claimed!")
            return

        # role already claimed
        await ctx.send("Role already claimed")
        return

    @commands.command(brief="change personal role name")
    async def name(self, ctx: commands.Context, name):
        if name == None:
            await ctx.send("put a name to rename your role")
            return

        for role in ctx.author.roles:
            if role.name == ctx.author.name:
                await role.edit(name=name)
                return
        else:
            await ctx.send("Claim personal role first: `!role claim`")
            return

    @commands.command(brief="change personal role color")
    async def color(self, ctx: commands.Context, *color):
        if len(color) != 3:
            await ctx.send("color not recognized. Syntax: !role color *r* *g* *b*")
            return
        else:
            r, g, b = map(int, color)

        for role in ctx.author.roles:
            if role.name == ctx.author.name:
                await role.edit(color=discord.Color.from_rgb(r, g, b))
                return
        else:
            await ctx.send("Claim personal role first: `!role claim`")
            return
