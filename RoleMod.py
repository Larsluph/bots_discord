import os

import discord
from discord.ext import commands

from cogs.basic_cog import Misc
from cogs.role_cog import Role

bot = commands.Bot(
    command_prefix="!role ",
    case_insensitive=True,
    description="Bot to help users manage their own role"
)

# cogs setup
bot.add_cog(Misc(bot))
bot.add_cog(Role(bot))

bot.run(os.environ.get('RoleMod'))
