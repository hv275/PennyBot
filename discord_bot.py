import os
import datetime
import random

import discord
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_CHANNEL')

client = discord.Client()


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == 'is it friday?':
        if datetime.datetime.today().weekday() == 4:
            response = "Yes, today is Friday!"
        else:
            response = "No, it is not Friday."
        await message.channel.send(response)

@client.event
async def on_member_update(before, after):
    if (after.status is discord.Status.online and
        before.status is discord.Status.offline):
        guild = discord.utils.get(client.guilds, name=GUILD)
        channel = discord.utils.get(guild.text_channels, name=CHANNEL)
        
        if datetime.datetime.today().weekday() == 4:
            response = ", today is Friday!"
        else:
            response = ", it is not Friday today."
        await channel.send(f"Hi {after.display_name}{response}")
        
client.run(TOKEN)
