"""Outspeed people and sends a message every time someone starts to type in a channel"""
import asyncio
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

    async def on_message(self, message: discord.Message):
        if message.author == self.user or not message.content.startswith("c! "):
            return

        data = ""
        try:
            data = str(eval(message.content[3:]))
        except Exception as err:
            data = str(err)
            await message.add_reaction("\u274c")
        finally:
            await message.channel.send(data)


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename=time.strftime(os.path.join("logs", "mathcalc_%Y-%m-%d_%H-%M-%S.log")),
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = CustomClient(max_messages=None, intents=discord.Intents.all())


async def main():
    await client.start(os.environ.get("MathCalc"))

asyncio.run(main())
