import discord
from datetime import datetime as dt
from discord import ui



class TicketSubmitButtons(ui.View):
    def __init__(self):
        super().__init__()
    
    # submit ticket button
    @discord.ui.button(label='Submit', style=discord.ButtonStyle.green)
    async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
        # get user info
        user = interaction.user

        # tell them that response has been logged
        await interaction.response.send_message(f'Thank you {user.mention}. Your response has been logged!')
        
        # kick the user out

        await interaction.channel.remove_user(user)

        # get role by id
        roles = await interaction.guild.fetch_roles()
        role_mention = None
        role_name = 'Sustain Mod'

        # assign role mention
        for role in roles:
            if role.name == role_name:
                role_mention = role.mention
                break

        # stop buttons functionality
        self.stop()

        # get owner mention
        owner_mention = interaction.guild.owner.mention

        # if not found @ the owner instead
        if role_mention is None:
            await interaction.channel.send(f'ATTENTION. {owner_mention}. {role_name} was not found! Please create this role (word for word) and allow them to see threads in this channel! or check the configuration for errors.')
            return
        
        # check if no one has this role
        if len(role.members) == 0:
            await interaction.channel.send(f'ATTENTION. {owner_mention}. No members are assigned "{role_name}". You will continue to be pinged unless you assign this role to at least 1 moderator.')
            return

        await interaction.channel.send(f'ATTENTION! {role_mention}. New ticket pending. Use the command /confirm <num_points> to address.')
        
    # cancel ticket button
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        thread = interaction.channel
        if isinstance(thread, discord.Thread):
            await interaction.channel.delete()

        # stop buttons functionality
        self.stop()