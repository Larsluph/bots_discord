"""instanciate Retard Discord bot"""
import asyncio
import logging
import os
import time

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

from cogs.basic_cog import Misc
from cogs.retard_cog import Retard

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename=time.strftime(os.path.join("logs", "retard_bot_%Y-%m-%d_%H-%M-%S.log")),
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = Intents.all()

bot = commands.Bot(
    command_prefix="$delay ",
    case_insensitive=True,
    description="Bot that tracks users' response delay",
    intents=intents
)


async def main():
    # cogs setup
    await bot.add_cog(Misc(bot))
    await bot.add_cog(Retard(bot))

    await bot.start(os.environ.get('RetardBot'))

asyncio.run(main())
