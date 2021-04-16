import os

import discord
from discord.ext import commands

from cogs.basic_cog import Misc
from cogs.clear_cog import Clear

bot = commands.Bot(
    command_prefix="^^",
    case_insensitive=True,
    description="Help you moderate server with misc cmds"
)

bot.add_cog(Misc(bot))
bot.add_cog(Clear(bot))

bot.run(os.environ.get("SuperMod"))
