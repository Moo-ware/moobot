import discord
from discord.ext import commands

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'ping', aliases = ['p'])
    async def ping(self, ctx):
        await ctx.send('Pong! That took **{}** ms.'.format(round(self.bot.latency, 5) * 1000))

    @commands.command(name = 'say')
    @commands.has_guild_permissions(administrator = True) 
    async def say(self, ctx, *content):
        try:
            await ctx.send(' '.join(content))
        except:
            await ctx.send('Please provide something for me to say.')
    
    @commands.command(name = 'slap')
    async def slap(self, ctx, member: discord.Member = None):
        if member != None:
            try:
                await ctx.send('{} has been slapped by {}'.format(member, ctx.author))
            except:
                await ctx.send('User not found.')
        else:
            await ctx.send('Please mention a user.')
    


def setup(bot):
    bot.add_cog(Utilities(bot))