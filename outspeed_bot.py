"Outspeed people and sends a message every time someone starts to type in a channel"

import datetime
import logging
import os
import time

import discord
from discord.ext import commands


class CustomClient(discord.Client):

    async def on_ready(self):
        print("bot ready")
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name="with the API")
        )

    async def on_typing(self, channel: discord.TextChannel, user: discord.Member, when: datetime.datetime):
        print(f"{user} is typing")
        await channel.send(f"<@{user.id}> \U0001F440", delete_after=1.5)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename=time.strftime("logs\\outspeeder_%Y-%m-%d_%H-%M-%S.log"),
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = CustomClient(max_messages=None, intents=discord.Intents.default())

client.run(os.environ.get("Outspeeder"))
