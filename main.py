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
for bot_command in os.listdir('cogs'):
    if bot_command[-3:] == '.py':
        name = "cogs." + bot_command[:-3]
        client.load_extension(name)


@client.command(aliases = ['p'])
async def ping(ctx):
    await ctx.send('Pong! That took **{}** ms.'.format(round(client.latency, 5) * 1000))


@client.command()
async def helptest(ctx):
    embed=discord.Embed(title="Commands:", color=0x04ff00)
    embed.set_author(name="Help Menu")
    embed.add_field(name="ping [p]", value="bots ping", inline=True)
    embed.add_field(name="queue [q]", value="Market Queue List", inline=True)
    embed.set_footer(text="Prefix:  [ . ] ")
    await ctx.send(embed=embed)


@client.command(aliases = ['q'])
async def queue(ctx, region='na'):
    if region.lower() == 'eu':        
        waitList = GetWaitlistEU()
        embed=discord.Embed(title="In Registrations Queue:", url="https://eu-trade.naeu.playblackdesert.com/Home/list/wait", color=0xfe9a9a)
        embed.set_author(name="Central Market [EU]")
        if len(waitList["_waitList"]) != 0:
            for i in waitList["_waitList"]:
                embed.add_field(name="{}: {}".format(matchEnhancement(i['chooseKey']), i['name']), 
                value="{:,}  ```ansi\n \u001b[0;47m\u001b[1;35m    In {} min    \u001b[0m```".format(i['_pricePerOne'], timeCalc(i['_waitEndTime'])), inline=True)
        else:
            embed.add_field(name="", value="```ansi\n \u001b[0;47m\u001b[1;35m    Nothing is in Queue    \u001b[0m```", inline=False)
        
        embed.set_footer(text=datetime.datetime.now())
        await ctx.send(embed=embed)
    else:
        waitList = GetWaitlist()
        embed=discord.Embed(title="In Registrations Queue:", url="https://na-trade.naeu.playblackdesert.com/Home/list/wait", color=0xfe9a9a)
        embed.set_author(name="Central Market [NA]")
        if len(waitList["_waitList"]) != 0:
            for i in waitList["_waitList"]:
                embed.add_field(name="{}: {}".format(matchEnhancement(i['chooseKey']), i['name']), 
                value="{:,}  ```ansi\n \u001b[0;47m\u001b[1;35m    In {} min    \u001b[0m```".format(i['_pricePerOne'], timeCalc(i['_waitEndTime'])), inline=True)
        else:
            embed.add_field(name="", value="```ansi\n \u001b[0;47m\u001b[1;35m    Nothing is in Queue    \u001b[0m```", inline=False)
        
        embed.set_footer(text=datetime.datetime.now())
        await ctx.send(embed=embed)


@client.command()
async def boss(ctx):
    spawn = spawnFromNow()
    del spawn[4:]

    description = ''
    for i in spawn:
        if len(i) == 2:
            if i[0] == 'SPAWNED':
                newstring = '{0:25}{1}\n'.format(i[1], i[0])
                description = description + newstring
    
            elif int(i[0][:-3]) == 1:
                timestr = 'In {} hour and {} minutes'.format(i[0][:-3], i[0][-2:])
                newstring = '{0:25}{1}\n'.format(i[1], timestr)
                description = description + newstring
            else:
                timestr = 'In {} hours and {} minutes'.format(i[0][:-3], i[0][-2:])
                newstring = '{0:25}{1}\n'.format(i[1], timestr)
                description = description + newstring
            
        elif len(i) == 3:
            if int(i[0][8:-3]) == 1:
                timestr = 'In {} hour and {} minutes'.format(i[0][8:-3], i[0][-2:])
                newstring = '{0:25}{1}\n'.format(i[1], timestr)
                description = description + newstring
            else:
                timestr = 'In {} hours and {} minutes'.format(i[0][8:-3], i[0][-2:])
                newstring = '{0:25}{1}\n'.format(i[1], timestr)
                description = description + newstring
            
        else:
            print('Error')
    
    embed=discord.Embed(title="BDO Boss Timer:", description='```diff\n-{}\n```'.format(description), color=0xfe9a9a)
    await ctx.send(embed=embed)


# Gets bot token from apikey.json file
f = open('apikey.json')
data = json.load(f)
bot_token = data.get('token')

client.run(bot_token)


