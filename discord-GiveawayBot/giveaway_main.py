import os

import discord
from discord.ext import commands

from cogs.basic_cog import Misc
from cogs.giveaway_cog import Giveaway

bot = commands.Bot(
    command_prefix="g!",
    case_insensitive=True,
    description="Bot to generate some giveaways"
)

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    print("error handled")
    if len(error.args) > 0:
        await ctx.send(error.args[0])
    else:
        await ctx.send("**Unknown error.** Check spelling and try again")

# cogs setup
bot.add_cog(Misc(bot))
bot.add_cog(Giveaway(bot))

bot.run(os.environ.get('GiveawayBot'))
