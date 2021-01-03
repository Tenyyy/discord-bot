import discord
import random as r
from discord.ext import commands


class example(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['credit'])
    async def credits(self, ctx):
        await ctx.send("This bot is made by `Tenyyy`!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'User {member.mention} has been kicked!\nReason: {reason}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'User {member.mention} has been banned!\nReason: {reason}')

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name="tenyyy's heart"))
        print('Bot is still online.')

    @commands.command(aliases=['hi'])
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.mention}! {round(self.client.latency * 1000)} ms")

    @commands.command()
    async def gaydar(self, ctx, *, member):
        meter = r.randint(1, 100)
        await ctx.send(f'{member} is {meter}% gay')

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        response = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely",
                    "You may rely on it", "As I see it, yes", "Most Likely", "Outlook Good",
                    "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later",
                    "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
                    "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very Doubtful"]
        await ctx.send(f'Question: {question}\nAnswer: {r.choice(response)}')

    @commands.command(aliases=['delete'])
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify the amount of messages to delete.\nFor example, !clear 5')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command!")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please mention the user you want to kick.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command!")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please mention the user you want to ban.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command!")


def setup(client):
    client.add_cog(example(client))
