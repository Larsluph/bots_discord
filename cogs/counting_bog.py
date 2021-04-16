import discord
from discord.ext import commands

class Counting(commands.Cog, name="CountingCog"):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = "CountingCog"
