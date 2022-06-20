import logging
import os
import time
from collections import deque
from typing import Iterable

import discord
from dotenv import load_dotenv

load_dotenv()


class CustomClient(discord.Client):
    to_clean_queue: Iterable[discord.Message] = deque()

    async def on_ready(self):
        print("bot ready")
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name="with the API")
        )

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        # TODO: auto clean config (timeout)
        # TODO: task to clean queue if timeout expired


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename=time.strftime(os.path.join("logs", "auto_cleaner_%Y-%m-%d_%H-%M-%S.log")),
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intent = discord.Intents.default()
intent.messages = True

client = CustomClient(max_messages=None, intents=intent)

client.run(os.environ.get("AutoCleaner"))
