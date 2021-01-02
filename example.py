import discord
import random as r
from discord.ext import commands

class example(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is still online.')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello! {round(self.client.latency * 1000)} ms')

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        response = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely",
                    "You may rely on it", "As I see it, yes", "Most Likely", "Outlook Good",
                    "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later",
                    "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
                    "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very Doubtful"]
        await ctx.send(f'Question: {question}\nAnswer: {r.choice(response)}')

    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
    

def setup(client):
    client.add_cog(example(client))