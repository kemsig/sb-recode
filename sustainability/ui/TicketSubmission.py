import discord
from datetime import datetime as dt
from discord import ui
from utils.logger import Logger
import config

class TicketSubmitButtons(ui.View):
    def __init__(self):
        super().__init__()
    
    @discord.ui.button(label='Submit', style=discord.ButtonStyle.green)
    async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        
        # Notify the user that their response has been logged.
        await interaction.response.send_message(f'Thank you {user.mention}. Your response has been logged!')
        
        # Get the logs channel.
        logs_channel = discord.utils.get(interaction.guild.channels, name=config.LOG_CHANNEL_NAME)
        
        # Log the ticket submission.
        if logs_channel:
            submission_log = Logger.command_success(
                user.mention,
                f"Ticket submitted by {user.name} (ID: {user.id}) at {dt.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC."
            )
            await logs_channel.send(embed=submission_log)
        
        # Remove the user from the channel.
        await interaction.channel.remove_user(user)
        # if logs_channel:
        #     removal_log = Logger.command_success(
        #         user.mention,
        #         f"User {user.name} (ID: {user.id}) was removed from the ticket channel."
        #     )
        #     await logs_channel.send(embed=removal_log)
        
        # Get role by name.
        roles = await interaction.guild.fetch_roles()
        role_mention = None
        role_name = config.ROLE_NAME
        for role in roles:
            if role.name == role_name:
                role_mention = role.mention
                break
        
        # Stop the view's buttons.
        self.stop()
        
        # Get the guild owner's mention.
        owner_mention = interaction.guild.owner.mention
        
        # If the role wasn't found, notify and log an error.
        if role_mention is None:
            message = (f'ATTENTION. {owner_mention}. {role_name} was not found! '
                       f'Please create this role (word for word) and allow them to see threads in this channel, '
                       f'or check the configuration for errors.')
            await interaction.channel.send(message)
            if logs_channel:
                role_error = Logger.database_failure(
                    user.mention,
                    f"Role '{role_name}' not found in guild '{interaction.guild.name}'."
                )
                await logs_channel.send(embed=role_error)
            return
        
        # Check if no members are assigned the role.
        if len([member for member in interaction.guild.members if any(r.name == role_name for r in member.roles)]) == 0:
            message = (f'ATTENTION. {owner_mention}. No members are assigned "{role_name}". '
                       f'You will continue to be pinged unless you assign this role to at least 1 moderator.')
            await interaction.channel.send(message)
            if logs_channel:
                no_member_warning = Logger.warning(
                    user.mention,
                    f"No members found with role '{role_name}' in guild '{interaction.guild.name}'."
                )
                await logs_channel.send(embed=no_member_warning)
            return
        
        # Notify moderators that a new ticket is pending.
        new_ticket_message = f'ATTENTION! {role_mention}. New ticket pending. Use the command /confirm <num_points> to address. Or /deny <reason> (NOTE: the user can see the reason).'
        await interaction.channel.send(new_ticket_message)
        if logs_channel:
            ticket_log = Logger.command_success(
                user.mention,
                f"New ticket submitted in channel '{interaction.channel.name}' by {user.name} (ID: {user.id})."
            )
            await logs_channel.send(embed=ticket_log)
    
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        thread = interaction.channel
        user = interaction.user
        
        # Get the logs channel.
        logs_channel = discord.utils.get(interaction.guild.channels, name=config.LOG_CHANNEL_NAME)
        
        # Log the ticket cancellation.
        if logs_channel:
            cancel_log = Logger.warning(
                user.mention,
                f"Ticket in channel '{thread.name}' was cancelled by {user.name} (ID: {user.id}) at {dt.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC."
            )
            await logs_channel.send(embed=cancel_log)
        
        # Delete the thread if it's a thread.
        if isinstance(thread, discord.Thread):
            await interaction.channel.delete()
        
        # Stop the view.
        self.stop()
