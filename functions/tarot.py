import discord
from discord.ext import commands
import json
import random
import os


class Tarot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # Safe path loading
        base_dir = os.path.dirname(__file__)
        json_path = os.path.join(base_dir, "..", "data", "tarot.json")

        with open(json_path, "r", encoding="utf-8") as f:
            self.deck = json.load(f)


    @commands.group(invoke_without_command=True)
    async def tarot(self, ctx):
        await ctx.send(
            "Use `>tarot random` or `>tarot question <your question>`"
        )


    @tarot.command()
    async def random(self, ctx):

        card = random.choice(self.deck)

        await ctx.send(
            f"🔮 Random Tarot Draw 🔮\n"
            f"🃏 **Card:** {card['name']}\n"
            f"📖 **Meaning:** {card['upright']}"
        )


    @tarot.command()
    async def question(self, ctx, *, question: str):

        card = random.choice(self.deck)

        await ctx.send(
            f"🔮 Question: {question} 🔮\n"
            f"🃏 {card['name']}\n"
            f"{card['upright']}"
        )


async def setup(bot):
    await bot.add_cog(Tarot(bot))
