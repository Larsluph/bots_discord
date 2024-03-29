"""AudioGuard Discord bot"""
import asyncio
import logging
import os
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs.basic_cog import Misc
from cogs.audio_guard_cog import AudioGuardCog

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename=time.strftime(os.path.join("logs", "audioguard_bot_%Y-%m-%d_%H-%M-%S.log")),
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(
    command_prefix="!guard ",
    description="Voice Channel Guardian",
    intents=intents
)


async def main():
    # cogs setup
    await bot.add_cog(Misc(bot))
    await bot.add_cog(AudioGuardCog(bot))

    await bot.start(os.environ.get('AudioGuard'))

asyncio.run(main())
