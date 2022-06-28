"""
Cog to implement delay tracking features
"""

import logging
import sqlite3
from datetime import timedelta
from os.path import join, exists

from discord import Message, Member
from discord.ext import commands


class Queries:
    NEW_DELAY = "INSERT INTO delays(user, seconds_late) VALUES (?, ?);"


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
        self.conn = sqlite3.connect(db_path)

        if is_db_init_needed:
            self.init_schema()

    @property
    def logger(self):
        return logging.getLogger()

    def init_schema(self):
        self.sql('CREATE TABLE delays('
                 '"id" INTEGER PRIMARY KEY AUTOINCREMENT,'
                 '"user" INTEGER NOT NULL,'
                 '"seconds_late" INTEGER NOT NULL);')

    def sql(self, stmt: str, *args):
        cursor = self.conn.cursor()

        self.logger.info(stmt)
        self.logger.info(f"Parameters: {args!r}")

        result = cursor.execute(stmt, args).fetchall()
        self.conn.commit()

        return result

    @commands.command()
    async def register(self, ctx: commands.Context, msg_base: Message, msg_late: Message):
        author: Member = msg_late.author
        delta: timedelta = msg_late.created_at - msg_base.created_at
        self.sql(Queries.NEW_DELAY, author.id, delta.total_seconds())
