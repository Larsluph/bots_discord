"""
Cog to implement delay tracking features
"""

import logging
import sqlite3
from os.path import exists, join

from discord import Embed, Member, Message
from discord.ext import commands


class Queries:
    CREATE_DELAY = 'CREATE TABLE delays(' \
                   '"id" INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                   '"user" INTEGER NOT NULL, ' \
                   '"seconds_late" INTEGER NOT NULL);'

    INSERT_DELAY = "INSERT INTO delays(user, seconds_late)" \
                   "VALUES (?, ?);"

    SELECT_DELAY_BY_USER = "SELECT SUM(seconds_late) delay_sum, AVG(seconds_late) delay_avg FROM delays " \
                           "WHERE user = ? " \
                           "GROUP BY user;"

    SELECT_TOP5 = "SELECT user user_id, SUM(seconds_late) total_delay FROM delays " \
                  "GROUP BY user " \
                  "ORDER BY total_delay DESC " \
                  "LIMIT 5;"


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
        delta = (msg_late.created_at - msg_base.created_at).total_seconds()

        # register delay
        self.sql(Queries.INSERT_DELAY, author.id, delta)

        await ctx.send(f"Delay registered ! ({delta} second{'s' if delta > 1 else ''})")

    @commands.command()
    async def stats(self, ctx: commands.Context, member: Member = None):
        if member is None:
            # global stats
            embed = self.gen_leaderboard()
        else:
            # user stats
            embed = self.gen_user_stats(member)

        await ctx.send(embed=embed)

    def gen_leaderboard(self) -> Embed:
        leaderboard = list(map(lambda x: (self.bot.get_user(x[0]), x[1]),
                               self.sql(Queries.SELECT_TOP5)))

        top_user = leaderboard[0][0]
        thumbnail = top_user.avatar_url

        # https://cog-creators.github.io/discord-embed-sandbox/
        embed = Embed(title="Les plus GROS retardataires",
                      description="pour ceux qui touchent trop d'herbe",
                      color=0xc27c0e)
        if thumbnail is not None:
            embed.set_thumbnail(url=thumbnail)
        for rank, (user, total_delay) in enumerate(leaderboard, start=1):
            embed.add_field(name=f"{rank}. {user}", value=f"{total_delay}", inline=False)
        embed.set_footer(text="ici régis les plus gros nonolife")
        return embed

    def gen_user_stats(self, member: Member) -> Embed:
        query = self.sql(Queries.SELECT_DELAY_BY_USER, member.id)

        if len(query) != 1:
            print("Invalid DB response:", query, sep="\n")

        embed = Embed(title=f"User stats for {member.display_name}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Somme des retards", value=f"{query[0]}", inline=False)
        embed.add_field(name="Moyenne des retards", value=f"{query[1]}", inline=False)

        return embed
