import os

import discord
from discord.ext import commands

from cogs.basic_cog import Misc

bot = commands.Bot(
    command_prefix="^^",
    case_insensitive=True,
    description="Help you moderate server with misc cmds"
)

bot.add_cog(Misc(bot))

bot.run(os.environ.get("SuperMod", None))
