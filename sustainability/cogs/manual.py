import discord
from discord import app_commands
from discord.ext import commands
import config
from main import local_db  # shared LocalDatabase instance
from utils.ismod import is_mod
from utils.logger import Logger

class ManualAdminCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = local_db

    @app_commands.command(name="remuser", description="Remove a user from the local database manually. (Format: user_id)")
    @is_mod()
    async def remuser(self, interaction: discord.Interaction, key: str):
        logs_channel = discord.utils.get(interaction.guild.channels, name=config.LOG_CHANNEL_NAME)
        try:
            user_id = int(key.strip())
        except Exception as e:
            await interaction.response.send_message("Error parsing user ID. Please provide a valid integer.", ephemeral=True)
            return

        result = self.db.remove_user(user_id)
        if result:
            error_embed = Logger.database_failure(
                interaction.user.mention,
                f"Failed to remove user {user_id} from the database."
            )
            if logs_channel:
                await logs_channel.send(embed=error_embed)
            await interaction.response.send_message("Failed to remove user.", ephemeral=True)
        else:
            success_embed = Logger.command_success(
                interaction.user.mention,
                f"Successfully removed user {user_id} from the database."
            )
            if logs_channel:
                await logs_channel.send(embed=success_embed)
            await interaction.response.send_message(f"Successfully removed user {user_id}.", ephemeral=True)



    @app_commands.command(name="delpoints", description="Subtract points from a user. (Format: user_id:points)")
    @is_mod()
    async def delpoints(self, interaction: discord.Interaction, key: str):
        """
        Manually subtract points from a user's current points.
        """
        logs_channel = discord.utils.get(interaction.guild.channels, name=config.LOG_CHANNEL_NAME)
        try:
            parts = key.split(":")
            if len(parts) < 2:
                await interaction.response.send_message("Invalid format. Use user_id:points", ephemeral=True)
                return
            user_id = int(parts[0])
            points_to_subtract = int(parts[1])
        except Exception as e:
            await interaction.response.send_message("Error parsing input. Format should be user_id:points", ephemeral=True)
            return

        # Subtract points by adding a negative value.
        result = self.db.add_points(user_id, -abs(points_to_subtract))
        if result:
            error_embed = Logger.database_failure(
                interaction.user.mention,
                f"Failed to subtract {points_to_subtract} points from user {user_id}."
            )
            if logs_channel:
                await logs_channel.send(embed=error_embed)
            await interaction.response.send_message("Database error while subtracting points.", ephemeral=True)
            return

        success_embed = Logger.command_success(
            interaction.user.mention,
            f"Successfully subtracted {points_to_subtract} points from user {user_id}."
        )
        if logs_channel:
            await logs_channel.send(embed=success_embed)
        await interaction.response.send_message(
            f"Successfully subtracted {points_to_subtract} points from user {user_id}.", ephemeral=True
        )

    @app_commands.command(name="addpoints", description="Add points to a user (current and total). (Format: user_id:points)")
    @is_mod()
    async def addpoints(self, interaction: discord.Interaction, key: str):
        """
        Manually add points to a user. Positive points will update both current and total points.
        """
        logs_channel = discord.utils.get(interaction.guild.channels, name=config.LOG_CHANNEL_NAME)
        try:
            parts = key.split(":")
            if len(parts) < 2:
                await interaction.response.send_message("Invalid format. Use user_id:points", ephemeral=True)
                return
            user_id = int(parts[0])
            points_to_add = int(parts[1])
        except Exception as e:
            await interaction.response.send_message("Error parsing input. Format should be user_id:points", ephemeral=True)
            return

        result = self.db.add_points(user_id, points_to_add)
        if result:
            error_embed = Logger.database_failure(
                interaction.user.mention,
                f"Failed to add {points_to_add} points to user {user_id}."
            )
            if logs_channel:
                await logs_channel.send(embed=error_embed)
            await interaction.response.send_message("Database error while adding points.", ephemeral=True)
            return

        success_embed = Logger.command_success(
            interaction.user.mention,
            f"Successfully added {points_to_add} points to user {user_id}. (Both current and total points updated)"
        )
        if logs_channel:
            await logs_channel.send(embed=success_embed)
        await interaction.response.send_message(
            f"Successfully added {points_to_add} points to user {user_id}.", ephemeral=True
        )

    @app_commands.command(name="addtotalpoints", description="Manually add points to a user's total only. (Format: user_id:points)")
    @is_mod()
    async def addtotalpoints(self, interaction: discord.Interaction, key: str):
        """
        Manually update a user's total points without changing their current points.
        """
        logs_channel = discord.utils.get(interaction.guild.channels, name=config.LOG_CHANNEL_NAME)
        try:
            parts = key.split(":")
            if len(parts) < 2:
                await interaction.response.send_message("Invalid format. Use user_id:points", ephemeral=True)
                return
            user_id = int(parts[0])
            points_to_add = int(parts[1])
        except Exception as e:
            await interaction.response.send_message("Error parsing input. Format should be user_id:points", ephemeral=True)
            return

        try:
            cur = self.db.conn.cursor()
            # Check if user exists.
            cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cur.fetchone()
            if row:
                new_total = row["points_total"] + points_to_add
                cur.execute("UPDATE users SET points_total = ? WHERE user_id = ?", (new_total, user_id))
            else:
                # If the user doesn't exist, insert a record with 0 current points.
                total = points_to_add if points_to_add > 0 else 0
                cur.execute("INSERT INTO users (user_id, points_cur, points_total) VALUES (?, ?, ?)", (user_id, 0, total))
            self.db.conn.commit()
        except Exception as e:
            error_embed = Logger.database_failure(
                interaction.user.mention,
                f"Error updating total points for user {user_id}: {e}"
            )
            if logs_channel:
                await logs_channel.send(embed=error_embed)
            await interaction.response.send_message("Database error while updating total points.", ephemeral=True)
            return

        success_embed = Logger.command_success(
            interaction.user.mention,
            f"Successfully added {points_to_add} total points to user {user_id}."
        )
        if logs_channel:
            await logs_channel.send(embed=success_embed)
        await interaction.response.send_message(
            f"Successfully added {points_to_add} total points to user {user_id}.", ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(ManualAdminCommands(bot))
