import os
import datetime
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
from penny import Session
from Cogs.Events import Events
from Cogs.Dev import devcom
from Cogs.Penny import pennying
from penny import Player
# normal bot code, nicked your past one
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_CHANNEL')
sesh = Session(GUILD)
# working with bot class now, named client
bot = commands.Bot(command_prefix='p- ')


#adding the imported cogs - more clunky than using add_extension but it allows to keep sesh
bot.add_cog(Events(bot))
bot.add_cog(devcom(bot,sesh))
bot.add_cog(pennying(bot,sesh))

print(TOKEN)
bot.run(TOKEN)
