import discord
from discord.ext import commands

class Misc(commands.Cog, name="Misc"):
    def __init__(self, bot):
        self.bot = bot
        self.cog_name = "Misc"

        @bot.check
        async def is_owner(ctx):
            return ctx.author.id == 292714635394809876

        @bot.event
        async def on_command_error(ctx: commands.Context, error: commands.CommandError):
            print("error handled:")
            print(*error.args, sep="\n", end="\n\n")
            if "error code: 50007" in error.args[0]:
                await ctx.send("can't message user")
            else:
                await ctx.send("Unhandled error")

    @commands.Cog.listener()
    async def on_connect(self):
        print('[LOGS] Connecting to discord')
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[LOGS] Bot is ready!")
        print(
            f"[LOGS] Logged in: {self.bot.user.name}\n"
            f"[LOGS] ID: {self.bot.user.id}\n"
            f"[LOGS] Number of users: {len(set(self.bot.get_all_members()))}"
        )
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name="with the API"))
    @commands.Cog.listener()
    async def on_resumed(self):
        print("\n[LOGS] Bot has resumed session!")


    @commands.command(brief="disconnects the bot from Discord")
    async def logout(self, ctx: commands.Context):
        await self.bot.change_presence(status=discord.Status.offline, activity=None)
        await ctx.send("Disconnected!")
        await self.bot.logout()
        print("[LOGS] Connection terminated")
        exit(0)
