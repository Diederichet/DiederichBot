import discord
from discord.ext import commands
import asyncio
import aiohttp
import random
import json

# Check for PyNaCl (required for voice)
try:
    import nacl  # PyNaCl package provides the 'nacl' module
    VOICE_AVAILABLE = True
except Exception:
    VOICE_AVAILABLE = False
    print("Warning: PyNaCl is not installed. Voice features will be disabled. Install with: pip install PyNaCl")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)
denied_links = ["https://tenor.com/view/stop-sign-red-gif-25972505", 
				"https://tenor.com/view/no-babyjake-nope-not-allowed-cant-do-that-gif-21337058", 
				"https://tenor.com/view/you-can-not-say-that-youre-cancelled-you-are-cancelled-censored-not-allowed-gif-27665358",
				"https://tenor.com/view/woah-bro-you-cant-say-that-skeleton-pepsi-gif-23570205",
				"https://tenor.com/view/1984-george-orwell-george-orwell-1984-1984-chips-1984-ruffles-gif-7144052804264359069",
				"https://tenor.com/view/youre-fired-donald-trump-the-apprentice-point-gif-8557097",
				"https://tenor.com/view/disgust-disgusting-puke-vomit-eww-gif-19262390",
				"https://tenor.com/view/lmfao-dead-stan-twitter-emoji-gif-23492742"]

async def load_extensions():
    for filename in os.listdir("./Functions"):
        if filename.endswith(".py"):
            await bot.load_extension(f"Functions.{filename[:-3]}")

@bot.command()
async def ping(ctx):
	await ctx.send('pong')


@bot.command()
async def join(ctx):
    # Ensure PyNaCl is available for voice usage
    if not VOICE_AVAILABLE:
        await ctx.send("Voice support is unavailable. Please install PyNaCl: `pip install PyNaCl`")
        return

    # Ensure the author is in a voice channel before accessing it
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("You must be connected to a voice channel to use this command.")
        return

    channel = ctx.author.voice.channel
    try:
        if ctx.voice_client is None:
            await channel.connect()
        else:
            await ctx.voice_client.move_to(channel)

        await asyncio.sleep(5)

        vc = ctx.voice_client
        if vc is not None:
            await vc.disconnect()

        await ctx.send('bye lmao')
    except Exception as e:
        await ctx.send(f"Voice action failed: {e}")
	
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.upper()

    if "GOON" in content:
        try:
            await message.delete()
        except Exception as e:
            print("Delete failed:", e)

        await message.channel.send("Rule 5: Abosultely no G**NING Allowed!1!")
        await message.channel.send(
            random.choice(denied_links)
        )
    await bot.process_commands(message)

with open('creds.txt') as file:
    firstline = file.readline()

bot.run(firstline)

