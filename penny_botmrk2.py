import os
import datetime
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
from penny import Session
from penny import Player

#normal bot code, nicked your past one
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_CHANNEL')
sesh = Session()
#working with bot class now
bot = commands.Bot(command_prefix='penny ')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='join', help = "Joining the game.")
async def join(ctx):
    await ctx.send(sesh.add_player(ctx.author.display_name))
    


@bot.command(name='leave', help = "Leave the game.")
async def leave(ctx):
    await ctx.send(sesh.remove_player(ctx.author.display_name))

@bot.command(name = 'players', help = "Show all the players currently in game")
async def players(ctx):
    await ctx.send(sesh.playershow())

@bot.command(name = 'attack', help = "Attempt to penny a player. Format: 'penny attack <name of victim>'")
async def attack(ctx, victim):
    #this is a highly retarded way to go about sending messages to channels but it will have to do
    guild = discord.utils.get(bot.guilds, name=GUILD)
    vchannels =  guild.voice_channels
    print(vchannels)
    response = sesh.penny(ctx.author.display_name, victim, vchannels)
    #change id to the appropriate channel
    channel = bot.get_channel(719657679601270905)
    await ctx.send(response)
    await channel.send(response)

@bot.command(name = 'balance', help = "See your balance")
async def getbalance(ctx):
    await ctx.send(sesh.get_balance(ctx.author.display_name))

#cash injection that checks that the user has an admin role
@bot.command(name = 'cashinjection', help = "dev only")
@commands.has_role('dev')
async def  cashinjection(ctx,name,num):
    await ctx.send(sesh.cashinjection(name,num))

#output in case of a check failure
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')












bot.run(TOKEN)
