"instanciate Super Mod Discord bot"

import logging
import os
import time

from discord.ext import commands

from cogs.basic_cog import Misc
from cogs.mod_cog import Mod

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename=time.strftime("logs\\mod_bot_%Y-%m-%d_%H-%M-%S.log"),
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(
    command_prefix="^^",
    case_insensitive=True,
    description="Help you moderate server with mod cmds"
)

bot.add_cog(Misc(bot))
bot.add_cog(Mod(bot))

bot.run(os.environ.get("SuperMod"))
