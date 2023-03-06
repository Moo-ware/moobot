import discord
import json
from utils.functions import findItems

# These are embeds needed for button menus
def alertMenuEmbed(user):
    embed=discord.Embed(title=f"Welcome back {user.name}!", 
                        description="`My active alerts`: **0**", 
                        color=0xfe9a9a)
    return embed


# Below are the buttons, modals and select menus
class itemModal(discord.ui.Modal, title="Test test test test"):
    itemGrade = discord.ui.TextInput(label='Enter the level of the item (e.g. Base, Pen)')
    itemName = discord.ui.TextInput(label= 'Enter the name of the Item')

    async def on_submit(self, interaction: discord.Interaction):
        list = findItems(str(self.itemName))
        if len(list) > 1 and len(list) < 25:
            menuoptions = Select()
            string = ''
            for i in list:
                menuoptions.add_option(label=f'{i[0]}')
                string = string + f'[{list.index(i)}]{i[0]}\n'
            
            await interaction.response.send_message(f'{string}', view=SelectView(menuoptions))
        elif len(list) == 1:
            await interaction.response.send_message(f'{list[0][0]}')
        else:
            await interaction.response.send_message(f'No item or the list of possible items found with the name `{self.itemName}` is too long. Try to be more specific or check for typo')


class AlertMenu(discord.ui.View): # Create a class called AlertMenu that subclasses discord.ui.View
    def __init__(self):
        super().__init__(timeout=180) # Timeout after this long
    
    async def on_timeout(self):
        self.clear_items()
        await self.message.edit(content='Timedout', view=self)
        

    @discord.ui.button(label="Create a queue alert", style=discord.ButtonStyle.primary, emoji="🔔") 
    async def creat_alert_button_callback(self, interaction: discord.Interaction, button):
        
        await interaction.response.send_modal(itemModal()) # Send a message when the button is clicked
    
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red) # Create a button with the label "Close" with color red
    async def exit_button_callback(self, interaction: discord.Interaction, button):
        self.stop()
        await interaction.message.delete() # Deletes current message


class alertmenuCreateAlert(discord.ui.View): # Alert menu after you clicked Create an Alert **(Not in use for now)**
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, emoji="😎") 
    async def creat_alert_button_callback(self, interaction: discord.Interaction, button):
        await interaction.response.send_message("You clicked the other button!") # Send a message when the button is clicked
    
    @discord.ui.button(label="Go Back", style=discord.ButtonStyle.red) # Create a button with the label "Close" with color red
    async def exit_button_callback(self, interaction: discord.Interaction, button):
        await interaction.response.edit_message(content='s', view=AlertMenu()) # Deletes current message

class Select(discord.ui.Select):
    def __init__(self):
        options=[]
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content=f'{self.values[0]}')

class SelectView(discord.ui.View):
    def __init__(self, menuoptions):
        super().__init__()
        self.add_item(menuoptions)


    
        
        