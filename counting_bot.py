"""instanciate Counting Game Discord bot"""
import asyncio
import logging
import os
import time

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

from cogs.basic_cog import Misc
from cogs.counting_cog import Counting

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
    command_prefix="c!",
    description="Lets you play the counting game on Discord!",
    intents=Intents.all()
)


async def main():
    # cogs setup
    await bot.add_cog(Misc(bot))
    await bot.add_cog(Counting(bot))

    await bot.start(os.environ.get('CountingBot'))

asyncio.run(main())
