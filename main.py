# ------------------------- imports ------------------------- #

import discord
from discord.ext import commands
import os

# ------------------------- preamble ------------------------- #

# get info from the env file
BOT_KEY = os.getenv("BOT_KEY")

# specify what the bot will access
intents = discord.Intents.default()
intents.message_content = True

# create the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# setup event
@bot.event
async def on_ready():
    print(f'{bot.user} connected to Discord!')

# ------------------------- begin commands ------------------------- #

@bot.command()
async def ping(ctx):
    await ctx.send("test message")

bot.run(BOT_KEY)