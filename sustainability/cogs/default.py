# cogs/default.py
import discord
from discord import app_commands
from discord.ext import commands
from utils.logger import Logger
import config
from main import local_db  

class DefaultCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = local_db

    @app_commands.command(name="points", description='Shows how many points you have!')
    async def points(self, interaction: discord.Interaction):
        logs_channel = discord.utils.get(interaction.guild.channels, name=config.LOG_CHANNEL_NAME)
        mod_mention = interaction.user.mention
        user_id = interaction.user.id

        # Log that the user requested their points.
        # success_embed = Logger.command_success(
        #     mod_mention,
        #     f"User {user_id} requested their points."
        # )
        # await logs_channel.send(embed=success_embed)

        # Query for user info 
        user_info_dict = self.db.get_user_info(user_id=user_id)
        if user_info_dict is None:
            error_embed = Logger.database_failure(
                mod_mention,
                f"Failed to retrieve data for user {user_id} on /points command."
            )
            await logs_channel.send(embed=error_embed)
            await interaction.response.send_message(
                "An error occurred while fetching your data. Please notify a moderator.", 
                ephemeral=True
            )
            return

        cur_points = user_info_dict['points_cur']
        total_points = user_info_dict['points_total']

        # Send user info as a response.
        await interaction.response.send_message(
            f'Your current points are **{cur_points}** with a lifetime score of **{total_points}**!',
            ephemeral=True
        )

    @app_commands.command(name="gacha", description=f"Test your luck and win cool prizes! Uses {config.GACHA_MIN_BALANCE} points on use.")
    async def gacha(self, interaction: discord.Interaction):
        # Get user info and prepare DM channel
        user_id = interaction.user.id
        user_dm = await interaction.user.create_dm()

        # Open stats from the database
        user_info = self.db.get_user_info(user_id)
        logs_channel = discord.utils.get(interaction.guild.channels, name=config.LOG_CHANNEL_NAME)
        user_identifier = interaction.user.name  # using username as identifier in logs

        if user_info is None:
            error_embed = Logger.database_failure(
                user_identifier, 
                f"Failed to fetch data for user {user_id} during /gacha command."
            )
            await logs_channel.send(embed=error_embed)
            await interaction.response.send_message(
                "An error occurred. Please try again later or notify a moderator.", 
                ephemeral=True
            )
            return

        points = user_info['points_cur']
        if points < config.GACHA_MIN_BALANCE:
            warning_embed = Logger.warning(
                user_identifier,
                f"User {user_id} attempted /gacha with insufficient points: {points} (requires {config.GACHA_MIN_BALANCE})."
            )
            await logs_channel.send(embed=warning_embed)
            await interaction.response.send_message(
                f"Insufficient funds! You need at least {config.GACHA_MIN_BALANCE} points to roll.",
                ephemeral=True
            )
            return

        # Deduct points for gacha roll
        result = self.db.add_points(user_id, -config.GACHA_MIN_BALANCE)
        if result:
            error_embed = Logger.database_failure(
                user_identifier,
                f"Database failed to remove points from user {user_id} during /gacha."
            )
            await logs_channel.send(embed=error_embed)
            await interaction.response.send_message(
                "An error occurred while processing your roll. Please try again later.",
                ephemeral=True
            )
            return

        # Log successful deduction and gacha roll execution.
        # After a successful gacha roll:
        success_embed = Logger.successful_gacha_roll(
            moderator_string=user_identifier,  
            user_id=user_id,
            prize="TBD"  
        )
        # This ping notifies everyone in the log channel.
        await logs_channel.send(content="@everyone", embed=success_embed)


        # Send a response to the user (you might want to add further logic to deliver the prize)
        await interaction.response.send_message(
            "Gacha roll processed! 🎉 Please keep your DMs open so a moderator can reach out to deliver your prize. "
            "If no one contacts you within a reasonable time, feel free to message a moderator directly!",
            ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(DefaultCommands(bot))
