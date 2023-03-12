import discord
import asyncio
import sqlite3
from discord import app_commands
from discord.ext import tasks, commands
from utils.functions import findItems


class marketalert(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='alert', description='Brings up my alert menu') # Create a slash command
    async def alertmenu(self, interaction: discord.Interaction):
        embed=discord.Embed(title=f"Welcome back {interaction.user.name}!", 
                        description="`My active alerts`: **0**", 
                        color=0xfe9a9a).set_author(name=interaction.user.name, icon_url=interaction.user.avatar)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/629036668531507222/1079318649325756498/78796e7f-eaa1-4f7e-abb6-099499a807ea.png')
        view=AlertMenu(interaction.user)
        await interaction.response.send_message(embed=embed, view=view) # Send a message with our View class that contains the button
        view.message = await interaction.original_response() # Sets the current message as view.message


async def setup(bot):
    await bot.add_cog(marketalert(bot), guild=discord.Object(id=561610616360534044))


class UserDB():
    async def get_user_from_db(self, userid):
        connection = sqlite3.connect("resources/alerts.db")
        cursor = connection.cursor()
        rows = cursor.execute(f"SELECT AlertList.item_id, AlertList.enhancement_level, AlertList.price, items.item_name, AlertTypes.alert_type\
                              FROM AlertList\
                              INNER JOIN items ON items.item_id = AlertList.item_id\
                              INNER JOIN AlertTypes ON AlertTypes.alert_id = AlertList.alert_id\
                              WHERE user_id = {userid}").fetchall()
        cursor.close()
        connection.close()
        return rows

    async def save_user_to_db(self, statement):
        connection = sqlite3.connect("resources/alerts.db")
        cursor = connection.cursor()
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        connection.close()


class User():
    def __init__(self, userid):
        self.userid = userid
        self._db = UserDB() 

    async def get_user(self):
        await self._db.get_user_from_db(self.userid)
    
    async def save_user(self, itemid, elevel, price, alert_id):
        await self._db.save_user_to_db(f"INSERT INTO AlertList VALUES ({self.userid}, {itemid}, {elevel}, {price}, {alert_id})")


"""Below are the Buttons necessary for UI"""
# Made thse global variables because it is used by all classes below
_alertMenuID = None
_alertMenuButton = None
_alertMenuView = None

# Main Alert Menu
class AlertMenu(discord.ui.View): 
    def __init__(self, author):
        super().__init__(timeout=5) # Timeout after this long
        self.author = author
        
    async def on_timeout(self):
        self.clear_items()
        await self.message.edit(content='Timedout', view=self)
        
    async def interaction_check(self, interaction):
        # Only allow the author that invoke the command to be able to use the interaction
        return interaction.user == self.author

    @discord.ui.button(label="Create a queue alert", style=discord.ButtonStyle.primary, emoji="🔔") 
    async def creat_alert_button_callback(self, interaction: discord.Interaction, button):
        global _alertMenuID, _alertMenuButton, _alertMenuView
        _alertMenuID = interaction.message
        _alertMenuButton = button
        _alertMenuView = self
        await interaction.response.send_modal(itemModal()) # Send a message when the button is clicked
        
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red) # Create a button with the label "Close" with color red
    async def exit_button_callback(self, interaction: discord.Interaction, button):
        self.stop()
        await interaction.message.delete() # Deletes current message


# Modal that sends after you click Create queue alert from above
class itemModal(discord.ui.Modal, title="Test test test test"):
    itemGrade = discord.ui.TextInput(label='Enter the level of the item (e.g. Base, Pen)')
    itemName = discord.ui.TextInput(label= 'Enter the name of the Item')
    
    # Creating the select menu (Might move to another Class later just for more organization)
    async def create_select_menu(self, list):
        menuoptions = Select()
        string = ''
        # Adding matching fields to Select menu
        for i in list:
            menuoptions.add_option(label=f'{i[0]}', value=f'{i[0]}-{i[1]}')
            string = string + f'[{list.index(i)}] {i[0]}\n'
        return menuoptions, string
    
    async def on_submit(self, interaction: discord.Interaction):
        # Disables the 'Create a Queue Alert' Button on Modal submit
        _alertMenuButton.disabled = True
        await _alertMenuID.edit(view=_alertMenuView)

        # Match input itemName from model to a BDO Item Name
        list = findItems(str(self.itemName))
        
        # Making sure list stays within Discord limits
        if len(list) > 1 and len(list) < 25:
            menuoptions, string = await self.create_select_menu(list)
            await interaction.response.send_message(embed=discord.Embed(title=f'Found a list of possible items related to `{self.itemName}`',
                                                                  description = f'{string}',
                                                                  color=0xfe9a9a).add_field(name='Please select the corret item below:', value=''), 
                                                                  view=SelectView(menuoptions))
        # If returned items only has one match
        elif len(list) == 1:
            await interaction.response.send_message(embed = discord.Embed(title='Creating queue alert for:',
                                description=f'`{str(self.itemGrade).upper()}:{list[0][0]}`',
                                color=0xfe9a9a).set_thumbnail(url=f'https://cdn.arsha.io/icons/{list[0][1]}.png'), view=Confirmation(interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title=f'No item or the list of possible items found with the name `{self.itemName}` is too long. Try to be more specific or check for typo', 
                                                                        color=0xfe9a9a))
            await asyncio.sleep(5)
            await interaction.delete_original_response()
            
            # For re-enabling Create a Queue Button
            _alertMenuButton.disabled = False
            await _alertMenuID.edit(view=_alertMenuView)


# Creates the Select Menu after modal above if there are more than 1 matched
class Select(discord.ui.Select):
    def __init__(self):
        options=[]
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title='Creating queue alert for:',
                                description=f"`{self.values[0].split('-')[0]}`",
                                color=0xfe9a9a).set_thumbnail(url=f"https://cdn.arsha.io/icons/{self.values[0].split('-')[1]}.png")
        await interaction.response.edit_message(embed=embed, view=ConfirmationMulti(interaction.user, self))

class SelectView(discord.ui.View):
    def __init__(self, menuoptions):
        super().__init__(timeout=60)
        self.add_item(menuoptions)
    

# Confirmation page if only 1 item is matched
class Confirmation(discord.ui.View):
    def __init__(self, author):
        super().__init__(timeout=30)
        self.author = author

    async def interaction_check(self, interaction):
        # Only allow the author that invoke the command to be able to use the interaction
        return interaction.user == self.author
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green) 
    async def confirm_button_callback(self, interaction: discord.Interaction, button):
        await interaction.response.defer() # Send a message when the button is clicked
    
    @discord.ui.button(label="Go back", style=discord.ButtonStyle.red) # Create a button with the label "Close" with color red
    async def before_button_callback(self, interaction: discord.Interaction, button):
        self.stop()
        await interaction.message.delete()
        
        # Re Enables 'Create queue alert' Button when 'Go Back' is pressed incase user exits Modal without submitting
        _alertMenuButton.disabled = False
        await _alertMenuID.edit(view=_alertMenuView)
        await interaction.response.send_modal(itemModal())


# Confirmation Menu for if multiple items are matched
class ConfirmationMulti(discord.ui.View):
    def __init__(self, author, options):
        super().__init__(timeout=30)
        self.author = author
        self.options = options

    async def interaction_check(self, interaction):
        # Only allow the author that invoke the command to be able to use the interaction
        return interaction.user == self.author
    
    @discord.ui.button(label="Confirm", row=0, style=discord.ButtonStyle.green) 
    async def confirm_button_callback(self, interaction: discord.Interaction, button):
        await interaction.response.defer() # Send a message when the button is clicked
    
    @discord.ui.button(label="Go Back", row=0, style=discord.ButtonStyle.red) # Create a button with the label "Close" with color red
    async def before_button_callback(self, interaction: discord.Interaction, button):
        self.stop()
        # Going back to Select View
        await interaction.response.edit_message(view=SelectView(self.options))
        
    @discord.ui.button(label="Re-Enter Item Name", row=1, style=discord.ButtonStyle.blurple) # Create a button with the label "Close" with color red
    async def modal_button_callback(self, interaction: discord.Interaction, button):
        self.stop()
        await interaction.message.delete()
        
        # Re Enables 'Create queue alert' Button 
        _alertMenuButton.disabled = False
        await _alertMenuID.edit(view=_alertMenuView)
        await interaction.response.send_modal(itemModal())
    
    
    @discord.ui.button(label='Exit', row = 1, style=discord.ButtonStyle.gray) # Exit button
    async def exit_callback(self, interaction: discord.Interaction, button):
        self.stop()
        await interaction.message.delete()
        
        # Re Enables 'Create queue alert' Button 
        _alertMenuButton.disabled = False
        await _alertMenuID.edit(view=_alertMenuView)