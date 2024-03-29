"""Logger Discord bot"""
import asyncio
import logging
import os
import time

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

from cogs.basic_cog import Misc
from cogs.logging_cog import LoggingCog

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename=time.strftime(os.path.join("logs", "counting_bot_%Y-%m-%d_%H-%M-%S.log")),
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(
    command_prefix="log ",
    description="Logger Bot",
    intents=Intents.all()
)


async def main():
    # cogs setup
    await bot.add_cog(Misc(bot))
    await bot.add_cog(LoggingCog(bot))

    await bot.start(os.environ.get('LoggerBot'))

asyncio.run(main())
