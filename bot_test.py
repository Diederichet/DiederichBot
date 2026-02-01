import discord
from discord.ext import commands
import asyncio
import random
import json

with open("tarot.json", "r", encoding="utf-8") as f:
    tarot_deck = json.load(f)

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

@bot.command()
async def balls(ctx):
    await ctx.send('https://tenor.com/view/casino-royale-bond-james-bond-ouch-hurt-gif-18410770')

@bot.command()
async def eight_ball(ctx, *, question: str):
    responses = [
        "It is certain.",
        "Without a doubt.",
        "You may rely on it.",
        "Yes — definitely.",
        "Most likely.",
        "Outlook is good.",
        "Signs point to yes.",
        "Reply hazy — try again.",
        "Better not tell you now.",
        "Ask again later.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don’t count on it.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    answer = random.choice(responses)
    await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {answer}")

@bot.command()
async def tarot(ctx, *, question: str):
	card = random.choice(tarot_deck)
	# orientation = random.choice(["upright", "reversed"])
	orientation = "upright"
	meaning = card[orientation]
	await ctx.send(
        f"🔮 **Tarot Reading** 🔮\n\n"
        f"**Question:** {question}\n\n"
        f"🃏 **Card Drawn:** **{card['name']}** ({orientation.title()})\n"
        f"📖 **Meaning:** {meaning}"
    )

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

        await message.channel.send("Not Allowed")
        await message.channel.send(
            "https://spaces-cdn.clipsafari.com/pappp143jfsqozzyz6hobl6itaoe"
        )
    await bot.process_commands(message)

with open('creds.txt') as file:
    firstline = file.readline()

bot.run(firstline)

