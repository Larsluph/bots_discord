"""\
Cog to implement counting game\
"""

import json
import os

import discord
from discord.ext import commands


class Counting(commands.Cog, name="CountingCog"):
    "Counting game d.py cog (see module docstring for more info)"

    name = "CountingCog"
    save_location = "data\\counting_data.json"

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channels = self.load_save()

    def load_save(self) -> dict:
        "loads previous instances' data"
        result = dict()

        if os.path.exists(self.save_location):
            with open(self.save_location, 'r') as file:
                result = json.load(file)

        return result

    def save_count(self):
        "saves channel count"
        with open(self.save_location, 'w') as file:
            json.dump(self.channels, file)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        "validates game progression"
        if message.author == self.bot:
            return

        msg = message.content.strip()
        # channel = message.channel
        chan_id = message.channel.id
        # if channel is configured and contains only digits
        if chan_id in self.channels and msg.isdigit():
            if int(msg) == self.channels[chan_id]+1:
                if int(msg) % 10:
                    await message.add_reaction("\u2705")
                    # await channel.send("Keep up the good work!", delete_after=.3)
                else:
                    await message.add_reaction("\u2611")
                    # await channel.send("Good job!", delete_after=.3)
                self.channels[chan_id] += 1
            else:
                # await channel.send("Noob", delete_after=.3)
                await message.add_reaction("\u274c")
                self.channels[chan_id] = 0
            self.save_count()

    @commands.command(brief="setup TextChannel to listen to")
    async def setup(self, ctx: commands.Context, channel: discord.TextChannel):
        "setup TextChannel to listen to for the Counting Game"
        channel_id = channel.id
        self.channels[channel_id] = 0
        print(f"setup success: {channel}, #{channel_id}")
        await ctx.send("setup success!", delete_after=2)
        self.save_count()

    @commands.command(brief="reload data from the save file")
    async def reload(self, ctx: commands.Context):
        "add a command to reload data from the save file"
        self.channels = self.load_save()
        await ctx.send("reload finished!")
