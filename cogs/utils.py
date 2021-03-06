"""\
Module that compiles misc functions to user with d.py bots\
"""

import discord
from discord.ext import commands

from typing import Union


async def auto_convert_obj(
        bot: commands.Bot,
        ctx: commands.Context,
        data: str) -> Union[discord.User, discord.TextChannel, int, str]:
    """\
    convert `data` to DiscordType object:
        - User
        - TextChannel
        - int
        - str\
    """

    if data.startswith("<@!"):
        return await commands.UserConverter().convert(ctx, data)

    elif data.startswith("@"):
        return ctx.guild.get_member(int(data[1:].strip()))

    elif data.startswith("<#"):
        return await commands.TextChannelConverter().convert(ctx, data)

    elif data.startswith("#"):
        return bot.get_channel(int(data[1:].strip()))

    elif data.isdigit():
        return int(data)

    else:
        return data
