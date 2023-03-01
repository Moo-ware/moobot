import discord
from discord.ext import commands
from functions import *

class BDOInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'queue', aliases = ['q'])
    async def queue(self, ctx, region='na'):
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
    

    @commands.command(name = 'boss', aliases=['next'])
    async def boss(self, ctx, boss=None):
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

async def setup(bot):
    await bot.add_cog(BDOInfo(bot))
