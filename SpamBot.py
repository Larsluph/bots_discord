import os

import discord
from discord.ext import commands

from cogs.basic_cog import Misc
from cogs.spam_cog import Spam

bot = commands.Bot(
    command_prefix="s$",
    case_insensitive=True,
    description="Bot to help you spam some sh****t"
)

# cogs setup
bot.add_cog(Misc(bot))
bot.add_cog(Spam(bot))

bot.run(os.environ.get('SpamBot'))
