"""instanciate Super Mod Discord bot"""
import asyncio
import logging
import os
import time

from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

from cogs.basic_cog import Misc
from cogs.mod_cog import Mod

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename=time.strftime(os.path.join("logs", "mod_bot_%Y-%m-%d_%H-%M-%S.log")),
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="^^",
    case_insensitive=True,
    intents=intents,
    description="Help you moderate server with mod cmds"
)


async def main(b: commands.Bot):
    await b.add_cog(Misc(b))
    await b.add_cog(Mod(b))
    await b.start(os.environ.get("SuperMod"))

asyncio.run(main(bot))
