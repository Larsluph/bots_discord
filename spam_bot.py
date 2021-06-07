"""instanciate Spam Discord bot"""

import logging
import os
import time

import discord
from discord.ext import commands

from cogs.basic_cog import Misc
from cogs.spam_cog import Spam

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename=time.strftime(os.path.join("logs", "spam_bot_%Y-%m-%d_%H-%M-%S.log")),
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="s$",
    case_insensitive=True,
    description="Bot to help you spam some sh****t",
    intents=intents
)

# cogs setup
bot.add_cog(Misc(bot))
bot.add_cog(Spam(bot))

bot.run(os.environ.get('SpamBot'))
