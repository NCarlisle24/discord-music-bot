# ---------------------------------------------- imports ---------------------------------------------- #

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# ---------------------------------------------- preamble ---------------------------------------------- #

# constants
COMMAND_PREFIX = "!"
"""Defines the character/s used to call commands in Discord."""

TRACKED_CHANNEL_IDS = [1400122378222174382]
"""The list of channel IDs for the bot to get commands from."""

# get info from the env file
load_dotenv()
BOT_KEY = os.getenv("BOT_KEY")
"""The Discord bot's key (keep private)"""

# specify what the bot will access
intents = discord.Intents.default()
intents.message_content = True

# create the bot
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# ---------------------------------------------- begin events ---------------------------------------------- #

@bot.event
async def on_ready():
    print(f'{bot.user} connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user or message.channel.id not in TRACKED_CHANNEL_IDS:
        return
    
    print(f"Received message from user {message.author}: {message.content}")

    await bot.process_commands(message)

# ---------------------------------------------- begin helper functions ---------------------------------------------- #

# TODO: Make the function name/functionality more intuitive
def user_in_voice_channel(ctx):
    """Returns true if the user is in a voice channel, false otherwise."""

    if ctx.author.voice:
        return True
    else:
        return False

def bot_in_voice_channel(ctx):
    """Returns true if the bot is in a voice channel, false otherwise."""
    if ctx.voice_client:
        return True
    else:
        return False

def bot_in_user_voice_channel(ctx):
    """Returns true if the bot and user are in the same voice channel, false otherwise."""
    if not user_in_voice_channel(ctx) or not bot_in_voice_channel(ctx):
        return False

    USER_VOICE_CHANNEL = ctx.author.voice.channel
    BOT_VOICE_CHANNEL = ctx.guild.voice_client

    return (BOT_VOICE_CHANNEL == USER_VOICE_CHANNEL)

# ---------------------------------------------- begin commands ---------------------------------------------- #

@bot.command()
async def join(ctx):
    """Gets the bot to join the caller's voice channel."""

    if not user_in_voice_channel(ctx):
        await ctx.send("Error: Need to be in a voice channel.")
        return
    
    voice_channel = ctx.author.voice.channel

    # if already in a voice channel, disconnect first
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

    await voice_channel.connect()

@bot.command()
async def leave(ctx):
    """Gets the bot to leave its current voice channel."""

    if not ctx.voice_client:
        await ctx.send("Error: Bot is not in a voice channel.")
        return
    
    if not bot_in_user_voice_channel(ctx):
        await ctx.send("Error: Cannot disconnect bot without being in the same voice channel")
        return
    
    await ctx.voice_client.disconnect()

# ---------------------------------------------- run the bot ---------------------------------------------- #

bot.run(BOT_KEY)