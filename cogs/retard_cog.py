"""
Cog to implement delay tracking features
"""

import logging
import sqlite3
from datetime import timedelta
from os.path import exists, join

from discord import Embed, Member, Message
from discord.ext import commands


class Queries:
    CREATE_DELAY = 'CREATE TABLE delays(' \
                   '"id" INTEGER PRIMARY KEY AUTOINCREMENT,' \
                   '"user" INTEGER NOT NULL,' \
                   '"seconds_late" INTEGER NOT NULL);'

    INSERT_DELAY = "INSERT INTO delays(user, seconds_late)" \
                   "VALUES (?, ?);"

    SELECT_DELAY_BY_USER = "SELECT AVG(seconds_late) average FROM delays" \
                           "WHERE user = ?" \
                           "GROUP BY user;"
                           
    SELECT_DELAYS = "SELECT AVG(seconds_late) average FROM delays" \
                    "GROUP BY user;"


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
        self.sql(Queries.CREATE_DELAY)

    def sql(self, stmt: str, *args):
        cursor = self.conn.cursor()

        self.logger.info(stmt)
        self.logger.info(f"Parameters: {args!r}")

        cursor.execute(stmt, args)
        self.conn.commit()

        return cursor.fetchall()

    @commands.command()
    async def register(self, ctx: commands.Context, msg_base: Message, msg_late: Message):
        author: Member = msg_late.author
        delta: timedelta = msg_late.created_at - msg_base.created_at

        # register delay
        self.sql(Queries.INSERT_DELAY, author.id, delta.total_seconds())

    @commands.command()
    async def stats(self, ctx: commands.Context, member: Member = None):
        raise NotImplementedError

        if member is None:
            # global stats
            stats = self.sql(Queries.SELECT_DELAYS)
        else:
            # user stats
            stats = self.sql(Queries.SELECT_DELAY_BY_USER, member.id)

    @staticmethod
    def gen_embed():
        # https://cog-creators.github.io/discord-embed-sandbox/
        embed = Embed(title="RetardBot",
                      description="Here's a recap of the delays registered for <@!user>")
        title_url: str
        
        color: str
        
        # top right icon
        thumbnail: str
        
        author_name: str
        author_link: str
        author_avatar: str
