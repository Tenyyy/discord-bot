import discord
import os
import random as r
from discord.ext import commands

client = commands.Bot(command_prefix="!")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command doesn't exist!")

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')




client.run('Nzk0OTI4NzM4NTgzMTgzMzcx.X_B9FA.WtLXXs9XOU-rivutK0BdZ7Mu0Fg')
