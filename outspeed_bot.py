"""Outspeed people and sends a message every time someone starts to type in a channel"""
import asyncio
import datetime
import logging
import os
import time

import discord
from dotenv import load_dotenv

load_dotenv()


class CustomClient(discord.Client):
    async def on_ready(self):
        print("bot ready")
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name="with the API")
        )

    @staticmethod
    async def on_typing(channel: discord.TextChannel, user: discord.Member, _: datetime.datetime):
        print(f"{user} is typing")
        await channel.send(f"<@{user.id}> \U0001F440", delete_after=1.5)


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename=time.strftime(os.path.join("logs", "outspeeder_%Y-%m-%d_%H-%M-%S.log")),
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = CustomClient(max_messages=None, intents=discord.Intents.default())


async def main():
    await client.start(os.environ.get("Outspeeder"))

asyncio.run(main())
