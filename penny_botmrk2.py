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
client = discord.Client()
#working with bot class now
bot = commands.Bot(command_prefix='penny ')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='join', help = "Joining the game.")
async def join(ctx):
    await ctx.send(sesh.add_player(ctx.author.name))

@bot.command(name='leave', help = "Leave the game.")
async def leave(ctx):
    await ctx.send(sesh.remove_player(ctx.author.name))

@bot.command(name = 'players', help = "Show all the players currently in game")
async def players(ctx):
    await ctx.send(sesh.playershow())
#currently fucked due to issues with Player and Session classes
@bot.command(name = 'attack', help = "Attempt to penny a player. Format: 'penny attack <name of victim>'")
async def attack(ctx, victim):
    await ctx.send(sesh.penny(Player(ctx.author.name),Player(victim)))

@bot.command(name = 'balance'), help = "See your balance")
async def getbalance(ctx):
    await ctx.send(sesh.get_balance(ctx.author.name))









bot.run(TOKEN)
