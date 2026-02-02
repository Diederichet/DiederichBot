import discord
from discord.ext import commands
import random
import aiohttp

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def balls(self, ctx, member: discord.Member = None):
        gif_url = "https://tenor.com/view/casino-royale-bond-james-bond-ouch-hurt-gif-18410770"

        if member is None:
            await ctx.send(gif_url)
            return

        verbs = ["whacks", "smacks", "clobbers", "obliterates"]
        targets = ["nuts", "balls", "family jewels"]

        await ctx.send(
            f"💥 {ctx.author.display_name} "
            f"{random.choice(verbs)} "
            f"{member.display_name}'s "
            f"{random.choice(targets)} 💥\n{gif_url}"
        )

    @commands.command()
    async def eightball(self, ctx, *, question: str):
        responses = [
            "It is certain",
            "Reply hazy, try again",
            "Don’t count on it",
            "It is decidedly so",
            "Ask again later",
            "My reply is no",
            "Without a doubt",
            "Better not tell you now",
            "My sources say no",
            "Yes definitely",
            "Cannot predict now",
            "Outlook not so good",
            "You may rely on it",
            "Concentrate and ask again",
            "Very doubtful",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes"
        ]

        if not question.strip():
            await ctx.send("Please ask a question!")
            return

        await ctx.send(f"{random.choice(responses)}")

    @commands.command()
    async def fact(self, ctx):
        url = "https://api.popcat.xyz/v2/fact"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await ctx.send("Could not fetch a fact.")
                    return

                data = await resp.json()
                await ctx.send(f"{data.get('message').get('fact')}")

def setup(bot):
    bot.add_cog(Fun(bot))
