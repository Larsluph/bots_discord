"instanciate Counting Game Discord bot"

import logging
import os

from discord.ext import commands

from cogs.basic_cog import Misc
from cogs.counting_cog import Counting

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="logs\\counting_bot.log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(
    command_prefix="c!",
    description="Lets you play the counting game on Discord!"
)

# cogs setup
bot.add_cog(Misc(bot))
bot.add_cog(Counting(bot))

bot.run(os.environ.get('CountingBot'))
