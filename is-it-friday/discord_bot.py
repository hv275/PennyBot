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
        await is_it_friday_request(message.channel)

@client.event
async def on_member_update(before, after):
    guild = discord.utils.get(client.guilds, name=GUILD)
    channel = discord.utils.get(guild.text_channels, name=CHANNEL)
    
    if (after.status is discord.Status.online and
        before.status is discord.Status.offline):
        print(f"\n{after.display_name} has come online")
        await is_it_friday_greeting(after.display_name, channel)


async def is_it_friday_request(channel):
    print("\nis_it_friday_request() called")
    if datetime.datetime.today().weekday() == 4:
            response = "Yes, today is Friday!"
    else:
        response = "No, it is not Friday."
    await channel.send(response)

async def is_it_friday_greeting(member_name, channel):
    print("is_it_friday_greeting() called:")

    message = await channel.fetch_message(channel.last_message_id)
    print(f"  Last message was from: {message.author}")
    if datetime.datetime.today().weekday() == 4:
        response = "today is Friday!"
    else:
        response = "it is not Friday today."

    if message.author.display_name != "IsItFriday":
        print("  Last message not sent by me; sending message.")
        await channel.send(f"Hi {member_name}, {response}")
            
    elif response not in message.content:
        print(f"  {message.content}")
        print("  Response changed; sending message")
        await channel.send(f"Hi {member_name}, {response}")
    else:
        print(f"{message.content}")
        print("  No change in response, message not sent")
client.run(TOKEN)
