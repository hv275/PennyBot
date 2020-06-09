import os
import datetime
import random

import discord
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


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
#reacts to a join request to add player to a session and adds them
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == 'join the fun':
        await pennyjoin(message.channel)
    elif message.content.lower() == 'sink':
        await pennyleave(message.channel)


async def pennyjoin(channel):
    message = await channel.fetch_message(channel.last_message_id)
    newplayer=message.author
    await channel.send(sesh.add_player(newplayer))
    print(sesh.players)





async def pennyleave(channel):
    message = await channel.fetch_message(channel.last_message_id)
    goneplayer=message.author
    await channel.send(sesh.remove_player(goneplayer))
    print(sesh.players)

client.run(TOKEN)