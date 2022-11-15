"""instanciate Spam Discord bot"""
import asyncio
import logging
import os
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs.basic_cog import Misc
from cogs.spam_cog import Spam

load_dotenv()

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


async def main():
    # cogs setup
    await bot.add_cog(Misc(bot))
    await bot.add_cog(Spam(bot))

    await bot.start(os.environ.get('SpamBot'))

asyncio.run(main())
