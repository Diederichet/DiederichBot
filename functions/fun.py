import discord
from discord.ext import commands
import random
import aiohttp
import asyncio


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
            "It is certain", "Reply hazy, try again", "Don’t count on it",
            "It is decidedly so", "Ask again later", "My reply is no",
            "Without a doubt", "Better not tell you now", "My sources say no",
            "Yes definitely", "Cannot predict now", "Outlook not so good",
            "You may rely on it", "Concentrate and ask again", "Very doubtful",
            "As I see it, yes", "Most likely", "Outlook good", "Yes",
            "Signs point to yes"
        ]

        if not question.strip():
            await ctx.send("Please ask a question!")
            return

        await ctx.send(random.choice(responses))


    @commands.command()
    async def fact(self, ctx):
        url = "https://api.popcat.xyz/v2/fact"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await ctx.send("Could not fetch a fact.")
                    return

                data = await resp.json()
                fact = data.get("message", {}).get("fact")

                await ctx.send(fact or "Fact format error.")


    @commands.command()
    async def age(self, ctx, *, name: str):
        url = f"https://api.agify.io?name={name}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await ctx.send("Response error.")
                    return

                data = await resp.json()
                guess = data.get("age")

                if guess:
                    await ctx.send(
                        f"The estimated age of {name} is: {guess}"
                    )
                else:
                    await ctx.send("Age response format error.")


    # -------------------------
    # Quote system
    # -------------------------

    async def get_quote(self):
        url = "https://api.breakingbadquotes.xyz/v1/quotes"
        # Adding a User-Agent makes the request look like it's coming from a browser
        headers = {"User-Agent": "Mozilla/5.0"}
        
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        # Verify data is a list and not empty
                        if isinstance(data, list) and len(data) > 0:
                            quote = data[0].get("quote", "No quote found")
                            author = data[0].get("author", "Unknown")
                            return quote, author
                        return "API returned empty data.", "System"
                    else:
                        # This will tell you exactly what status code you're getting
                        return f"API Error: Status {resp.status}", "System"
        except Exception as e:
            print(f"DEBUG: Quote error -> {e}")
            return f"Connection Error: {e}", "System"


    async def run_quote_quiz(self, ctx, quote, author):

        await ctx.send(
            f"**Who said this?**\n\n"
            f"\"{quote}\"\n\n"
            f"You have 2 minutes."
        )

        def check(message):
            return (
                message.author == ctx.author
                and message.channel == ctx.channel
            )

        try:
            msg = await self.bot.wait_for(
                "message",
                timeout=120.0,
                check=check
            )

            guess = msg.content.lower()
            correct = author.lower()

            if any(part in guess for part in correct.split()):
                await ctx.send(f"Correct! It was **{author}**.")
            else:
                await ctx.send(f"WRONG. It was **{author}**.")

        except asyncio.TimeoutError:
            await ctx.send(f"Time's up! It was **{author}**.")


    @commands.command()
    async def bbquote(self, ctx, mode: str = None):
        print("BBQUOTE CALLED")
        quote, author = await self.get_quote()

        if mode == "quiz":
            await self.run_quote_quiz(ctx, quote, author)
            return

        await ctx.send(
            f"\"{quote}\"\n"
            f"-**{author}**"
        )


async def setup(bot):
    await bot.add_cog(Fun(bot))
