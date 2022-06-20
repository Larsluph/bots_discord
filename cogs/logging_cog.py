"""\
Cog to implement guild logging
"""

import discord

from discord.ext import commands

from datetime import datetime as dt


class LoggingCog(commands.Cog, name="LoggingCog"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, msg: discord.Message):
        pass

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        pass

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        pass

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        pass

    @commands.command(brief="Debug embed integration")
    async def ebd(self, ctx: commands.Context):
        # embed = discord.Embed(title="Custom Embed",
        #                       description="Description Sample",
        #                       timestamp=dt.utcnow(),
        #                       colour=discord.Colour.gold())
        #
        # embed.set_thumbnail(url=ctx.author.avatar_url)
        # embed.set_footer(text="footer text")
        # embed.set_author(name="Larsluph", url="https://github.com/Larsluph")
        #
        # embed.add_field(name="Field Title 1", value=":x:line 1\nline 2\nline 3", inline=True)
        # embed.add_field(name="Field Title 2", value=":x:line 1\nline 2\nline 3", inline=True)
        # embed.add_field(name="Field Title 3", value=":x:line 1\nline 2\nline 3", inline=False)
        embed = discord.Embed(description="Larsluph's embed",
                              colour=discord.Colour.dark_purple())

        embed.set_footer(text='Check the long version of this command with "rpg cd"')

        embed.add_field(name="Experience",
                        value=""
                              ":white_check_mark: ~-~ `Hunt`\n"
                              ":white_check_mark: ~-~ `Training`\n"
                              ":white_check_mark: ~-~ `Duel`",
                        inline=False)
        embed.add_field(name=":sparkles:Progress",
                        value=""
                              ":white_check_mark: ~-~ `Chop | Fish | Pickup | Mine`\n"
                              ":white_check_mark: ~-~ `Farm`",
                        inline=False)

        await ctx.send(embed=embed)
