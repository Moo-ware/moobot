import discord
from discord.ext import commands
from discord import app_commands

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
    
    @commands.command(name = 'send')
    async def send(self, ctx, channel, *, content):
        if channel != None:
            channel2 = self.bot.get_channel(int(channel))
            await channel2.send(content)
        else:
            await ctx.send('Please mention a channel.')

    
    @commands.command(name='sync')
    async def sync(self, ctx):
        guild = ctx.guild.id
        count = await ctx.bot.tree.sync(guild=discord.Object(id=guild))
        await ctx.send(f'{len(count)} commands synced to {ctx.guild.name}')

    # Slash commands
    @app_commands.command(name='avatar', description='Gets a users avatar')
    @app_commands.describe(user='Gets this users avatar')
    @app_commands.describe(scope='View server avatar or main avatar')
    @app_commands.choices(scope=[
        app_commands.Choice(name='Main avatar', value=0),
        app_commands.Choice(name='Server avatar', value=1)
    ])
    async def avatar(self, interaction: discord.Interaction, user: discord.Member = None, scope: app_commands.Choice[int] = None): 
        if user is None and scope is None: # If no params are given, return command user's server avatar
            title = "Server Avatar"
            image = (interaction.user.guild_avatar if interaction.user.guild_avatar is not None else interaction.user.avatar)
            footer = f'{interaction.user.name}#{interaction.user.discriminator}'
        elif user is None and scope is not None: # If no user is given, then return avatar based on scope param
            title = ("Server Avatar" if scope.value == 1 else "Main Avatar")
            image = (interaction.user.guild_avatar if scope.value == 1 else interaction.user.avatar)
            if image is None: # If user has no server avatar return default avatar
                image = interaction.user.avatar
            footer = f'{interaction.user.name}#{interaction.user.discriminator}'
        elif scope is None or scope.value == 1: # If user is give but no param is given or param is Server Avatar, return server avatar of user
            title = "Server Avatar"
            image = (user.guild_avatar if user.guild_avatar is not None else user.avatar)
            footer = f'{user.name}#{user.discriminator}'
        else: # If user is given and param is Main avatar, return main avatar of user
            title = "Main Avatar"
            image = user.avatar
            footer = f'{user.name}#{user.discriminator}'
        
        embed=discord.Embed(title=title, url=image, color=0xfe9a9a)
        embed.set_footer(text=footer)
        embed.set_image(url=image)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Utilities(bot), guild=discord.Object(id=561610616360534044))