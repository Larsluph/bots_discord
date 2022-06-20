"""
Cog to implement delay tracking features
"""

import sqlite3
from typing import Optional
from os.path import join, exists

from discord import Member, User
from discord.ext import commands

from maps.retard.parameter import MapParameter


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
