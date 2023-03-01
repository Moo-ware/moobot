import discord
import os
import json
from functions import *
from discord.ext import commands


intents = discord.Intents.all()

client = commands.Bot(command_prefix = ".", intents=intents)

@client.event
async def on_ready():
    print('Logged on as {0.user}'.format(client))
    
    #Loads all commands in cogs folder
    for bot_command in os.listdir('Modules'):
        if bot_command[-3:] == '.py':
            name = "Modules." + bot_command[:-3]
            await client.load_extension(name)
        elif bot_command[-1] != '_':
            for command in os.listdir(f'Modules/{bot_command}'):
                if command[-3:] == '.py':
                    name = f'Modules.{bot_command}.' + command[:-3]
                    await client.load_extension(name)


# Gets bot token from apikey.json file
f = open('apikey.json')
data = json.load(f)
bot_token = data.get('token')

client.run(bot_token)


