import discord
from discord import app_commands
from discord.ext import tasks, commands
from utils.functions import *
from utils.buttons import *

class marketalert(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='alert', description='Brings up my alert menu') # Create a slash command
    async def alertmenu(self, interaction: discord.Interaction):
        view=AlertMenu()
        await interaction.response.send_message("This is a button!", view=view) # Send a message with our View class that contains the button
        view.message = await interaction.original_response() # Sets the current message as view.message


async def setup(bot):
    await bot.add_cog(marketalert(bot), guild=discord.Object(id=561610616360534044))