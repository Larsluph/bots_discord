import discord
from discord.ext import commands

async def auto_convert_obj(bot: commands.Bot, ctx: commands.Context, data: str):
    if data.startswith("<@!"):
        return await commands.UserConverter().convert(ctx, data)
    elif data.startswith("@"):
        return bot.get_user(int(data[1:].strip()))
    elif data.startswith("<#"):
        return await commands.TextChannelConverter().convert(ctx, data)
    elif data.isdigit():
        return int(data)
    else:
        return data
