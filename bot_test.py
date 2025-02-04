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
    channel = ctx.author.voice.channel
    if ctx.author.voice is not None:
        await ctx.author.voice.channel.connect()
        await asyncio.sleep(5)
        await ctx.voice_client.disconnect()
        await ctx.send('bye lmao')

@bot.command()
async def balls(ctx):
    await ctx.send('https://tenor.com/view/casino-royale-bond-james-bond-ouch-hurt-gif-18410770')








with open('creds.txt') as file:
    firstline = file.readline()

bot.run(firstline)

