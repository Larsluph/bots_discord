"""\
Cog for discord bot including basic stuff for every instance:
    - error handling
    - global check
    - logging when bot is (dis)connecting to the API
    - logout command to shutdown bot instance\
"""

import sys

import discord
from discord.ext import commands

from cogs import utils


class Misc(commands.Cog, name="MiscCog"):
    """Misc d.py cog (see module docstring for more info)"""

    name = "MiscCog"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        @bot.check
        async def is_owner(ctx: commands.Context):
            return ctx.author.id == 292714635394809876

        @bot.event
        async def on_command_error(ctx: commands.Context, error: commands.CommandError):
            await ctx.message.add_reaction("\u274c")
            if isinstance(error, commands.CommandInvokeError):
                error = error.original

            # print debug
            print("=====")
            print("Error detected:", type(error))
            print("- " + "\n- ".join(error.args))

            msg = str()

            # send error msg in chat
            if isinstance(error, commands.CheckFailure):
                if isinstance(error, commands.MissingPermissions):
                    msg = "You don't have enough permissions!"
                elif isinstance(error, commands.BotMissingPermissions):
                    msg = "I don't have enough permissions!"
                elif isinstance(error, commands.MissingRole):
                    msg = "You're missing roles!"
                elif isinstance(error, commands.BotMissingRole):
                    msg = "I'm missing roles!"
                else:
                    msg = "The command requires a check that didn't pass."

                if hasattr(error, "missing_perms"):
                    msg += " Missing permissions:\n- " + "\n- ".join(*error.missing_perms)
                if hasattr(error, "missing_role"):
                    msg += " Missing roles:\n- " + "\n- ".join(*error.missing_role)

            elif isinstance(error, commands.CommandNotFound):
                msg = "Unknown command. Try calling help command"

            elif isinstance(error, commands.UserInputError):
                if isinstance(error, commands.MissingRequiredArgument):
                    msg = "You forgot some arguments."
                elif isinstance(error, commands.TooManyArguments):
                    msg = "You passed too many arguments."
                elif isinstance(error, commands.BadArgument):
                    msg = "Some arguments are invalid."
                elif isinstance(error, commands.BadUnionArgument):
                    msg = f"Invalid argument type: {error.errors}."
                elif isinstance(error, commands.ArgumentParsingError):
                    msg = "Error while parsing argument(s)."
                msg += " Check command syntax and try again."

            elif isinstance(error, discord.HTTPException):
                if "10013" in error.args[0]:
                    msg = "Unknown User"
                elif "10014" in error.args[0]:
                    msg = "Unknown Emoji"

                elif "50007" in error.args[0]:
                    msg = "Can't message user ATM."
                elif "50013" in error.args[0]:
                    msg = "You either don't have enough permissions or\
the targeted user has higher privileges than you."

            else:
                print("Unhandled")
                msg = f"Unhandled error: {error}"
            # END

            print("=====")
            await ctx.reply(msg)

    @commands.Cog.listener()
    async def on_connect(self):
        """logging func when connecting to Discord API Gateway"""

        print('[LOGS] Connecting to discord')

    @commands.Cog.listener()
    async def on_ready(self):
        """logging func when connection is ready"""

        print("[LOGS] Bot is ready!")
        print(
            f"[LOGS] Logged in: {self.bot.user.name}\n"
            f"[LOGS] ID: {self.bot.user.id}\n"
            f"[LOGS] Number of users: {len(set(self.bot.get_all_members()))}"
        )
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name="with the API")
        )

    @commands.Cog.listener()
    async def on_resumed(self):
        """logging func when connection resumed after being interrupted"""

        print("\n[LOGS] Bot has resumed session!")

    @commands.command(brief="disconnects the bot from Discord")
    async def logout(self, ctx: commands.Context):
        """disconnect bot instance from Discord"""

        await self.bot.change_presence(status=discord.Status.offline, activity=None)
        await ctx.send("Disconnected!")
        await self.bot.close()
        print("[LOGS] Connection terminated")
        sys.exit(0)

    @commands.command(brief="test parsing data")
    async def parse(self, ctx: commands.Context, *args):
        """debug msg parsing"""

        for data in args:
            await ctx.send(f"`{data}`: {type(data)}")

            converted = await utils.auto_convert_obj(self.bot, ctx, data)
            await ctx.send(f"{converted}: {type(converted)}")
