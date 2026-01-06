import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def ping(ctx):
	await ctx.send('pong')


@bot.command()
async def join(ctx):
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

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "GOON" in message.content.upper():
        try:
            await message.delete()
        except Exception:
            pass
        await message.channel.send("Not Allowed")
        await message.channel.send('https://spaces-cdn.clipsafari.com/pappp143jfsqozzyz6hobl6itaoe')

    await bot.process_commands(message)

with open('creds.txt') as file:
    firstline = file.readline()

bot.run(firstline)

