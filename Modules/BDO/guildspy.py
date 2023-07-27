import discord
import sqlite3
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from discord import app_commands
from discord.ext import commands


class GuildSpy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def listGuildMembers(self, guild_name: str):
        url = f"https://www.naeu.playblackdesert.com/en-US/Adventure/Guild/GuildProfile?guildName={guild_name}&region=na"
        guild_page = requests.get(url)
        soup = BeautifulSoup(guild_page.content, "html.parser")
        res = soup.find(class_="container guild_profile")

        if res is None:
            return None, None

        members = res.find_all("a")
        guild_member_list = []
        for i in members[1:]:
            guild_member_list.append(i.text)

        date = res.find('span', class_='desc').text
        return guild_member_list, date
    
    async def databaseWrite(self, guild_name: str, members: str, date: str):
        conn = sqlite3.connect('resources/guilds.db')
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO guilds VALUES (?, ?, ?)", (guild_name.lower(), members, date))
        conn.commit()
        conn.close()

    async def databaseRetrieve(self, guild_name: str):
        conn = sqlite3.connect('resources/guilds.db')
        c = conn.cursor()
        c.execute("SELECT members, index_date FROM guilds WHERE guild_name=?", (guild_name.lower(),))
        result = c.fetchone()
        conn.close()
        return result
    

    @app_commands.command(name='guild', description='View members of a guild')
    @app_commands.describe(guild='Guild name')
    async def guild(self, interaction: discord.Interaction, guild: str):
        members, date = await self.listGuildMembers(guild)
        time_now = datetime.now()
        date_now = time_now.strftime("%m-%d-%Y")
        # Check if guild is on website
        if members is None:
            await interaction.response.send_message("Guild not found")
            return
        
        # Sorting members
        member_string = ""
        members.sort()
        for i in members:
            member_string += f"{i}, "

        # Database stuff
        result = await self.databaseRetrieve(guild)
        if result is not None:
            set_old = set(result[0].split(', '))
            set_new = set(members)
            index_date= result[1]
            # Find the difference between the two sets
            people_left = set_old - set_new
            people_joined = set_new - set_old

            member_left = ""
            member_joined = ""

            for i in people_left:
                if i != ' ' or "":
                    member_left += f"{i}, "
            
            for j in people_joined:
                if j != ' ' or "":
                    member_joined += f"{j}, "

        else:
            index_date = "First time Indexing"
            member_left = None
            member_joined = None
        
        await self.databaseWrite(guild, member_string[:-2], date_now)

        embed = discord.Embed(title=f"{guild}",
                        url=f"https://www.naeu.playblackdesert.com/en-US/Adventure/Guild/GuildProfile?guildName={guild}&region=na",
                        description=f"**{len(members)}** Members\nCreated on **{date}**",
                        colour=0xfe7162)

        embed.add_field(name="Current Members:", value=f"```{member_string[:-2]}```", inline=False)
        embed.add_field(name=f"Changes from [**{index_date}**]:", value="", inline=False)
        embed.add_field(name="Members Joined:", value=f"{member_joined[:-2]}", inline=True)
        embed.add_field(name="Members Left:", value=f"{member_left[:-2]}", inline=True)
        embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(GuildSpy(bot), guild=discord.Object(id=561610616360534044))
        
        

