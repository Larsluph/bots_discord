"""
Cog to implement delay tracking features
"""

import sqlite3
from os.path import join, exists

from discord import Message
from discord.ext import commands

from retardabot.maps.parameter import MapParameter


class Retard(commands.Cog, name="RetardCog"):
    """Retard d.py cog (see module docstring for info)"""

    cog_name: str = "RetardCog"
    bot: commands.Bot
    conn: sqlite3.Connection

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        db_path = join("data", "retard.db")
        is_db_init_needed = not exists(db_path)

        # Init connection to DB using sqlite3
        self.conn = sqlite3.connect()

        if is_db_init_needed:
            self.init_schema(self.conn)

    @staticmethod
    def init_schema(conn: sqlite3.Connection):
        conn.execute(MapParameter.create_table())
        conn.executemany(MapParameter.fill_table(), MapParameter.DEFAULT_VALUES)

    @commands.command
    async def register(self, msg_base: Message, msg_late: Message):
        author = msg_late.author
        delta = msg_late.created_at - msg_base.created_at
        delay_amount = delta.total_seconds()
        # TODO: insert into db (author, delay_amount)
