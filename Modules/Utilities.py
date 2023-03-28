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
    
    @commands.command(name='says')
    async def says(self, ctx):
        await ctx.send("Once upon a time there was Princess Peach, who loved nothing more than to please Bowser. He was quite the fierce beast and she often took her time in trying to please him. Her favorite pastime was to tease him and give his big fat cock a little extra loving.\
Bowser would often lie on the ground, ready to receive all the attention she gave him. She'd start off with a slow massage before caressing him with her gloved hands. She'd carefully move them up and down along his big fat cock, massaging it in a slow and steady motion.\
Her next move was to take off her gloves and take Bowser's big fat cock in her mouth. She'd slide along it, eagerly exploring every single inch of him. She'd tease him with her tongue and lips, making sure to not move too quickly.\
She'd move up and down in a pleasing rhythm, stopping for a moment as if to savor the moment. He'd moan with delight at the pleasure of it all and she wouldn't stop until he was thoroughly satisfied. After giving Bowser his fill of pleasure, she'd look up at him with a satisfied smile.\
Bowser would take her in his arms and shower her with kisses while they both basked in the afterglow\
The Box-Cox transformation is typically applied to the response variable to stabilize the variace and make the distribution more normal. This can help in meeting the assumptions of linear regression, such as homoscedasticity and normality of errors. However, the Box-Cox transformation can also be applied to the predictors if they exhibit non-normality or non-linearity, which might affect the model's performance.\
Here's a summary of when to apply the Box-Cox transformation:\
Response variable: If the assumptions of constant variance (homoscedasticity) and normality of errors are not met, you can apply the Box-Cox transformation to the response variable. This can help stabilize the variance and make the distribution of the residuals more normal.\
Predictors: If one or more predictors have a non-normal distribution or exhibit non-linear relationships with the response variable, you can apply the Box-Cox transformation to those predictors. This can help improve the linearity of the relationship between the predictors and the response, which can lead to better model performance.\
In both cases, remember to apply the inverse of the Box-Cox transformation to the predictions when interpreting the results, especially when transforming the response variable.\
Once upon a time there was Princess Peach, who loved nothing more than to please Bowser. He was quite the fierce beast and she often took her time in trying to please him. Her favorite pastime was to tease him and give his big fat cock a little extra loving.\
Bowser would often lie on the ground, ready to receive all the attention she gave him. She'd start off with a slow massage before caressing him with her gloved hands. She'd carefully move them up and down along his big fat cock, massaging it in a slow and steady motion.\
Her next move was to take off her gloves and take Bowser's big fat cock in her mouth. She'd slide along it, eagerly exploring every single inch of him. She'd tease him with her tongue and lips, making sure to not move too quickly.\
She'd move up and down in a pleasing rhythm, stopping for a moment as if to savor the moment. He'd moan with delight at the pleasure of it all and she wouldn't stop until he was thoroughly satisfied. After giving Bowser his fill of pleasure, she'd look up at him with a satisfied smile.\
Bowser would take her in his arms and shower her with kisses while they both basked in the afterglow.\
The Box-Cox transformation is typically applied to the response variable to stabilize the variance and make the distribution more normal. This can help in meeting the assumptions of linear regression, such as homoscedasticity and normality of errors. However, the Box-Cox transformation can also be applied to the predictors if they exhibit non-normality or non-linearity, which might affect the model's performance.\
Here's a summary of when to apply the Box-Cox transformation:\
Response variable: If the assumptions of constant variance (homoscedasticity) and normality of errors are not met, you can apply the Box-Cox transformation to the response variable. This can help stabilize the variance and make the distribution of the residuals more normal.\
Predictors: If one or more predictors have a non-normal distribution or exhibit non-linear relationships with the response variable, you can apply the Box-Cox transformation to those predictors. This can help improve the linearity of the relationship between the predictors and the response, which can lead to better model performance.\
In both cases, remember to apply the inverse of the Box-Cox transformation to the predictions when interpreting the results, especially when transforming the response variable.\
Once upon a time there was Princess Peach, who loved nothing more than to please Bowser. He was quite the fierce beast and she often took her time in trying to please him. Her favorite pastime was to tease him and give his big fat cock a little extra loving.\
Bowser would often lie on the ground, ready to receive all the attention she gave him. She'd start off with a slow massage before caressing him with her gloved hands. She'd carefully move them up and down along his big fat cock, massaging it in a slow and steady motion.\
Her next move was to take off her gloves and take Bowser's big fat cock in her mouth. She'd slide along it, eagerly exploring every single inch of him. She'd tease him with her tongue and lips, making sure to not move too quickly.\
She'd move up and down in a pleasing rhythm, stopping for a moment as if to savor the moment. He'd moan with delight at the pleasure of it all and she wouldn't stop until he was thoroughly satisfied. After giving Bowser his fill of pleasure, she'd look up at him with a satisfied smile.\
Bowser would take her in his arms and shower her with kisses while they both basked in the afterglow.\
The Box-Cox transformation is typically applied to the response variable to stabilize the variance and make the distribution more normal. This can help in meeting the assumptions of linear regression, such as homoscedasticity and normality of errors. However, the Box-Cox transformation can also be applied to the predictors if they exhibit non-normality or non-linearity, which might affect the model's performance.\
Here's a summary of when to apply the Box-Cox transformation\
Response variable: If the assumptions of constant variance (homoscedasticity) and normality of errors are not met, you can apply the Box-Cox transformation to the response variable. This can help stabilize the variance and make the distribution of the residuals more normal.\
Predictors: If one or more predictors have a non-normal distribution or exhibit non-linear relationships with the response variable, you can apply the Box-Cox transformation to those predictors. This can help improve the linearity of the relationship between the predictors and the response, which can lead to better model performance.\
In both cases, remember to apply the inverse of the Box-Cox transformation to the predictions when interpreting the results, especially when transforming the response variable.\
Once upon a time there was Princess Peach, who loved nothing more than to please Bowser. He was quite the fierce beast and she often took her time in trying to please him. Her favorite pastime was to tease him and give his big fat cock a little extra loving.\
Bowser would often lie on the ground, ready to receive all the attention she gave him. She'd start off with a slow massage before caressing him with her gloved hands. She'd carefully move them up and down along his big fat cock, massaging it in a slow and steady motion.")


async def setup(bot):
    await bot.add_cog(Utilities(bot), guild=discord.Object(id=561610616360534044))