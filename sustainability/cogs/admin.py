# cogs/admin.py
import discord
from discord import app_commands
from discord.ext import commands
import config
from main import local_db
from ui.TicketCreation import TicketCreateButton
from utils.ismod import is_mod
from utils.logger import Logger

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = local_db

    @app_commands.command(name="setup")
    @is_mod()
    async def setup(self, interaction: discord.Interaction):
        logs_channel = discord.utils.get(interaction.guild.channels, name=config.LOG_CHANNEL_NAME)
        mod_mention = interaction.user.mention

        # Log that the setup command was initiated.
        setup_log = Logger.command_success(
            mod_mention,
            "Setup command initiated by moderator."
        )
        if logs_channel:
            await logs_channel.send(embed=setup_log)

        print("Setup in progress..")
        # Create the persistent ticket button.
        view = TicketCreateButton()
        await interaction.channel.send("hello", view=view)
        await view.wait()   

    @app_commands.command(name='confirm')
    @is_mod()
    async def confirm(self, interaction: discord.Interaction, num_points: int):
        # Get thread.
        thread = interaction.channel
        
        # Check if channel is a thread.
        if not isinstance(thread, discord.Thread):
            await interaction.response.send_message("This channel is not a thread.", ephemeral=True)
            return

        thread_name = thread.name
        logs_channel = discord.utils.get(interaction.guild.channels, name=config.LOG_CHANNEL_NAME)
        mod_mention = interaction.user.mention
        guild_owner = interaction.guild.owner.mention  # For critical failures.

        # Extract user ID from the thread name.
        try:
            user_id = thread_name.split('_')[1]
        except IndexError:
            error_embed = Logger.database_failure(
                mod_mention,
                f"Thread name '{thread_name}' is not formatted correctly for /confirm."
            )
            if logs_channel:
                await logs_channel.send(embed=error_embed)
            await interaction.response.send_message("Thread naming format is incorrect.", ephemeral=True)
            return

        user = await interaction.guild.fetch_member(user_id)
        user_dm = await user.create_dm()

        # Award points in the database.
        result = self.db.add_points(user_id, num_points)
        if result:
            error_embed = Logger.database_failure(
                mod_mention,
                f"Critical failure: Database could not add {num_points} points for user {user_id}. Manual intervention required."
            )
            if logs_channel:
                await logs_channel.send(embed=error_embed)
            await interaction.response.send_message("An error occurred while updating points. Please notify a moderator.", ephemeral=True)
            return

        # Retrieve the user's updated info.
        user_info = self.db.get_user_info(user_id)
        if user_info is None:
            error_embed = Logger.database_failure(
                mod_mention,
                f"Failed to fetch user data for user {user_id} after awarding points."
            )
            if logs_channel:
                await logs_channel.send(embed=error_embed)
            await user_dm.send(f"Your request for **{num_points} points** has been granted. However, an error occurred retrieving your stats. Please try with /points.")
        else:
            await user_dm.send(
                f"Your request for **{num_points} points** has been granted. "
                f"Your current points are **{user_info['points_cur']}** with a lifetime score of **{user_info['points_total']}**!"
            )
            success_embed = Logger.command_success(
                mod_mention,
                f"Point request confirmed: {num_points} points awarded to user {user_id}."
            )
            if logs_channel:
                await logs_channel.send(embed=success_embed)
        
        # Remove thread.
        await thread.delete()  

    @app_commands.command(name="deny")
    @is_mod()
    async def deny(self, interaction: discord.Interaction, reason: str):    
        thread = interaction.channel

        # Check if channel is a thread.
        if not isinstance(thread, discord.Thread):
            await interaction.response.send_message("This channel is not a thread.", ephemeral=True)
            return

        # Extract user ID from thread name.
        try:
            user_id = thread.name.split('_')[1]
        except IndexError:
            logs_channel = discord.utils.get(interaction.guild.channels, name=config.LOG_CHANNEL_NAME)
            mod_mention = interaction.user.mention
            error_embed = Logger.database_failure(
                mod_mention,
                f"Thread name '{thread.name}' is not formatted correctly for /deny."
            )
            if logs_channel:
                await logs_channel.send(embed=error_embed)
            await interaction.response.send_message("Thread naming format is incorrect.", ephemeral=True)
            return

        user = await interaction.guild.fetch_member(user_id)
        if user is not None:
            user_dm = await user.create_dm()
            await user_dm.send(f"Your point request has been denied. Reason: {reason}")

        # Log the denial.
        logs_channel = discord.utils.get(interaction.guild.channels, name=config.LOG_CHANNEL_NAME)
        mod_mention = interaction.user.mention
        deny_embed = Logger.warning(
            mod_mention,
            f"Point request denied for user {user_id}. Reason: {reason}"
        )
        if logs_channel:
            await logs_channel.send(embed=deny_embed)

        # Remove thread.
        await thread.delete()

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))
