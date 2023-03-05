import discord

class AlertMenu(discord.ui.View): # Create a class called AlertMenu that subclasses discord.ui.View
    def __init__(self):
        super().__init__(timeout=60) # Timeout after this long
    
    async def on_timeout(self):
        self.clear_items()
        await self.message.edit(content='Timedout', view=self)
        

    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, emoji="😎") 
    async def button_callback2(self, interaction: discord.Interaction, button):
        await interaction.response.send_message("You clicked the other button!") # Send a message when the button is clicked
    
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red) # Create a button with the label "Close" with color red
    async def exit_button_callback(self, interaction: discord.Interaction, button):
        self.stop()
        await interaction.message.delete() # Deletes current message