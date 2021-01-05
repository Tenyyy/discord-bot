import discord
import random as r
from discord.ext import commands
from datetime import datetime
from typing import Optional
from discord import Embed, Member


class example(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['credit'])
    async def credits(self, ctx):
        await ctx.send("This bot is made by `Tenyyy`!")

    @commands.command(name="userinfo", aliases=["memberinfo", "ui", "mi"])
    @commands.has_permissions(manage_emojis=True)
    async def user_info(self, ctx, target: Optional[Member]):
        target = target or ctx.author

        embed = Embed(title="User information",
                      colour=target.colour,
                      timestamp=datetime.utcnow())

        embed.set_thumbnail(url=target.avatar_url)

        fields = [("Name", str(target), True),
                  ("ID", target.id, True),
                  ("Bot?", target.bot, True),
                  ("Top rank", target.top_role.mention, True),
                  ("Status", str('Awesome!').title(), True),
                  ("Activity",
                   f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}",
                   True),
                  ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Boosted", bool(target.premium_since), True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command(aliases=['sr'])
    @commands.has_permissions(administrator=True)
    async def shadowrealm(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        shadowRealm = discord.utils.get(guild.roles, name='Shadow Realm')

        await member.add_roles(shadowRealm, reason=reason)
        await ctx.send(f'{member.mention} has been sent to Shadow Realm!\nReason: {reason}')
        await member.send(f'You were sent to the Shadow Realm in the server {guild.name} for {reason}')


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name='Muted')

        await member.add_roles(mutedRole, reason=reason)
        await ctx.send(f'{member.mention} has been muted!\nReason: {reason}')
        await member.send(f'You were muted in the server {guild.name} for {reason}')


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
        shadowRealm = discord.utils.get(ctx.guild.roles, name='Shadow Realm')

        await member.remove_roles(mutedRole)
        await member.remove_roles(shadowRealm)
        await ctx.send(f"{member.mention} has been unmuted!")
        await member.send(f"You are now unmuted in the server {ctx.guild.name}")


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
            activity=discord.Activity(type=discord.ActivityType.listening, name="your wishes"))
        print('Bot is still online.')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"This message took the bot {round(self.client.latency * 1000)}ms to respond!")

    @commands.command(aliases=["hl"])
    async def helplist(self, ctx):
        await ctx.send("Here is the commands list!\n`ping` = check bot response time\n`mute` = give the user muted role (mods only)\n`shadowrealm` or `sr` = sends the user to shadow realm (mods only)\n`ban` = ban the targer user from the server\n`unmute` = remove the shadow realm and muted role on targeted user (mods only)\n`asklune` = answers the question based on Lune's emotions\n`say` = make Lune says your message (staff+)\n`clear` = delete messages in channel (mods only)\n`userinfo` or `ui` = brings up the mentioned user's info or yourself (without mention, for staff+)")

    @commands.command(aliases=['asklune'])
    async def _8ball(self, ctx, *, question):
        response = ["Lune thinks it is certain! <:ACLune1:796009123602497598>", "It is decidedly so", "Without a doubt", "Yes, definitely",
                    "As Lune sees it, yes", "Most Likely", "Outlook Good",
                    "Yes", "Lune points to yes", "Reply hazy, try again", "Ask Lune again later",
                    "Better not tell you now", "Lune cannot predict now", "Concentrate and ask again",
                    "Don't count on it", "Lune doesn't think so", "My sources say no", "Outlook not so good", "Very Doubtful"]
        await ctx.send(f'Question: {question}\nAnswer: {r.choice(response)}')

    @commands.command()
    @commands.has_permissions(manage_emojis=True)
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(aliases=['delete'])
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=1+amount)

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

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please mention the user you want to mute.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command!")

    @shadowrealm.error
    async def shadowRealm_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please mention the user you want to send to the Shadow Realm.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command!")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please mention the user you want to unmute.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command!")

    @user_info.error
    async def user_info_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the permission to use this command!")

    @say.error
    async def say_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the permission to use this command!")

def setup(client):
    client.add_cog(example(client))
