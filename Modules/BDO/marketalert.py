from discord import app_commands
from discord.ext import tasks, commands
from functions import *

class marketalert(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    '''def cog_unload(self):
        self.queuewatch.cancel()'''
    
    @commands.command(name='alert')
    async def alert(self, ctx):
        await ctx.reply(ctx.author)


    
async def setup(bot):
    await bot.add_cog(marketalert(bot))