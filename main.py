import discord
import os
import json
from functions import *
from discord.ext import commands
import openai

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
async def queue(ctx):
    waitList = GetWaitlist()
    embed=discord.Embed(title="In Registrations Queue:", url="https://na-trade.naeu.playblackdesert.com/Home/list/wait", color=0xfe9a9a)
    embed.set_author(name="Central Market")
    if len(waitList["_waitList"]) != 0:
        for i in waitList["_waitList"]:
            embed.add_field(name="{}: {}".format(matchEnhancement(i['chooseKey']), i['name']), 
            value="{:,}  ```ansi\n \u001b[0;47m\u001b[1;35m    In {} min    \u001b[0m```".format(i['_pricePerOne'], timeCalc(i['_waitEndTime'])), inline=True)
    else:
<<<<<<< Updated upstream
        embed.add_field(name="", value="```ansi\n \u001b[0;47m\u001b[1;35m    Nothing is in Queue    \u001b[0m```", inline=False)
    
    embed.set_footer(text=datetime.datetime.now())
    await ctx.send(embed=embed)
=======
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
async def boss(ctx, boss=None):
    if boss is None:
        spawn = spawnFromNow()
        del spawn[4:]

        description = ''
        for i in spawn:
            if len(i) == 2:
                if i[0] == 'SPAWNED':
                    newstring = '{0:25}{1}\n'.format(i[1], i[0])
                    description = description + newstring
        
                elif int(i[0][:-3]) == 1:
                    timestr = 'In {} hr and {} min'.format(i[0][:-3], i[0][-2:])
                    newstring = '{0:25}{1}\n'.format(i[1], timestr)
                    description = description + newstring
                else:
                    timestr = 'In {} hr and {} min'.format(i[0][:-3], i[0][-2:])
                    newstring = '{0:25}{1}\n'.format(i[1], timestr)
                    description = description + newstring
                
            # len(i) == 3 means the times are from the next day
            elif len(i) == 3:
                if int(i[0][8:-3]) == 1:
                    timestr = 'In {} hr and {} min'.format(i[0][8:-3], i[0][-2:])
                    newstring = '{0:25}{1}\n'.format(i[1], timestr)
                    description = description + newstring
                else:
                    timestr = 'In {} hr and {} min'.format(i[0][8:-3], i[0][-2:])
                    newstring = '{0:25}{1}\n'.format(i[1], timestr)
                    description = description + newstring
                
            else:
                print('Error')
        
        embed=discord.Embed(title="Upcoming Bosses:", description='```diff\n-{}\n```'.format(description), color=0xfe9a9a)
        embed.add_field(name="❗Important  Spawns :", 
                        value="```ansi\n\u001b[1;31mGarmoth      {}\u001b[0m```\n```yaml\nVell         {}```".format(timeFromNow(findNextBoss('Garmoth')),timeFromNow(findNextBoss('Vell'))), 
                        inline=False)
        embed.set_author(name="BDO Boss Timer", icon_url="https://cdn.discordapp.com/attachments/629036668531507222/1079318649325756498/78796e7f-eaa1-4f7e-abb6-099499a807ea.png")
        embed.set_thumbnail(url= getBossIcon(description[0:3]))

        await ctx.send(embed=embed)
    else:
        result = findNextBoss(boss.capitalize())
        if result is None:
            await ctx.send('Please enter a valid name')
        else:
            embed=discord.Embed(title="Next {} Spawn:".format(boss.capitalize()), description='**{}\n**'.format(timeFromNow(result)), color=0xfe9a9a)
            embed.set_image(url= getBossIcon(boss.capitalize()[0:3]))
            await ctx.send(embed=embed)
>>>>>>> Stashed changes

@client.command(aliases = ['ask'])
async def askgpt(ctx, temp, *, body = None):
    if body is not None:
        openai.api_key = "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"
        response = openai.Completion.create(
            model="text-davinci-003", 
            prompt="{}".format(body), 
            temperature= float(temp), 
            max_tokens=1000)

        responseFormat = response.choices[0].text
        
        await ctx.send('```\n{}```'.format(responseFormat))
    else:
        await ctx.send('Please provide information')
# Gets bot token from apikey.json file
f = open('apikey.json')
data = json.load(f)
bot_token = data.get('token')

client.run(bot_token)


