"instanciate Super Mod Discord bot"

import os

from discord.ext import commands

from cogs.basic_cog import Misc
from cogs.mod_cog import Mod

bot = commands.Bot(
    command_prefix="^^",
    case_insensitive=True,
    description="Help you moderate server with mod cmds"
)

bot.add_cog(Misc(bot))
bot.add_cog(Mod(bot))

bot.run(os.environ.get("SuperMod"))
