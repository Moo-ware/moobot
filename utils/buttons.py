import discord
import json
from utils.functions import findItems
from discord.ext import menus

# These are embeds needed for button menus
def alertMenuEmbed(user):
    embed=discord.Embed(title=f"Welcome back {user.name}!", 
                        description="`My active alerts`: **0**", 
                        color=0xfe9a9a)
    return embed


# Main Alert Menu
class AlertMenu(discord.ui.View): 
    def __init__(self):
        super().__init__(timeout=180) # Timeout after this long
    
    async def on_timeout(self):
        self.clear_items()
        await self.message.edit(content='Timedout', view=self)
        

    @discord.ui.button(label="Create a queue alert", style=discord.ButtonStyle.primary, emoji="🔔") 
    async def creat_alert_button_callback(self, interaction: discord.Interaction, button):
        await interaction.response.send_modal(itemModal(message=interaction.message, button=button, view=self)) # Send a message when the button is clicked
        
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red) # Create a button with the label "Close" with color red
    async def exit_button_callback(self, interaction: discord.Interaction, button):
        self.stop()
        await interaction.message.delete() # Deletes current message


# Modal that sends after you click Create queue alert from above
class itemModal(discord.ui.Modal, title="Test test test test"):
    itemGrade = discord.ui.TextInput(label='Enter the level of the item (e.g. Base, Pen)')
    itemName = discord.ui.TextInput(label= 'Enter the name of the Item')
    def __init__(self, message=None, button=None, view=None):
        super().__init__()
        self.message = message
        self.button = button
        self.view = view

    async def on_submit(self, interaction: discord.Interaction):
        # Disables the 'Create a Queue Alert' Button on Modal submit
        self.button.disabled = True
        await self.message.edit(view=self.view)

        # Match input itemName from model to a BDO Item Name
        list = findItems(str(self.itemName))
        if len(list) > 1 and len(list) < 25:
            menuoptions = Select()
            string = ''
            for i in list:
                menuoptions.add_option(label=f'{i[0]}')
                string = string + f'[{list.index(i)}]{i[0]}\n'
            
            await interaction.response.send_message(embed=discord.Embed(title=f'Found a list of possible items related to `{self.itemName}`',
                                                                  description = f'{string}',
                                                                  color=0xfe9a9a), view=SelectView(menuoptions))
        elif len(list) == 1:
            await interaction.response.send_message(f'{list[0][0]}', view=Confirmation(interaction.user, self.message, self.button, self.view))
        else:
            await interaction.response.send_message(f'No item or the list of possible items found with the name `{self.itemName}` is too long. Try to be more specific or check for typo')


# Creates the Select Menu after modal above if there are more than 1 matched
class Select(discord.ui.Select):
    def __init__(self):
        options=[]
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title='Creating queue alert for:',
                                description=f'`{self.values[0]}`',
                                color=0xfe9a9a)
        await interaction.response.edit_message(embed=embed, view=ConfirmationMulti(interaction.user, embed))

class SelectView(discord.ui.View):
    def __init__(self, menuoptions):
        super().__init__(timeout=60)
        self.add_item(menuoptions)

# Confirmation page if only 1 item is matched
class Confirmation(discord.ui.View):
    def __init__(self, author, message, button, view):
        super().__init__()
        self.author = author
        self.message = message
        self.button = button
        self.view = view

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
        self.button.disabled = False
        await self.message.edit(view=self.view)
        await interaction.response.send_modal(itemModal(self.message, self.button, self.view))


# Confirmation Menu for if multiple items are matched
class ConfirmationMulti(discord.ui.View):
    def __init__(self, author, embed):
        super().__init__()
        self.author = author
        self.embed = embed

    async def interaction_check(self, interaction):
        # Only allow the author that invoke the command to be able to use the interaction
        return interaction.user == self.author
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green) 
    async def confirm_button_callback(self, interaction: discord.Interaction, button):
        await interaction.response.defer() # Send a message when the button is clicked
    
    @discord.ui.button(label="Go back", style=discord.ButtonStyle.red) # Create a button with the label "Close" with color red
    async def before_button_callback(self, interaction: discord.Interaction, button):
        self.stop()

        # Going back to Select View
        await interaction.response.edit_message(embed=self.embed)
        
    @discord.ui.button(label='Exit', style=discord.ButtonStyle.blurple) # Exit button
    async def exit_callback(self, interaction: discord.Interaction, button):
        self.stop()
        await interaction.message.delete()



    
        
        