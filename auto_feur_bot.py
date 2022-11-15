"""Outspeed people and sends "feur" every time someone ends a message with "quoi" """
import asyncio
import datetime
import logging
import os
import time

import discord
from dotenv import load_dotenv

load_dotenv()


class CustomClient(discord.Client):
    PATTERNS = {
        'quoi': 'feur'
    }

    async def on_ready(self):
        print("bot ready")
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name="with the API")
        )

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        print("on_message")
        for k, v in self.PATTERNS.items():
            if message.content.endswith(k):
                await message.channel.send(v)


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename=time.strftime(os.path.join('logs', "auto_feur_%Y-%m-%d_%H-%M-%S.log")),
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = CustomClient(max_messages=None, intents=discord.Intents.all())


async def main():
    await client.start(os.environ.get("AutoFeur"))

asyncio.run(main())
