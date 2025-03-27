import discord
from discord import app_commands
from discord.ext import commands
from main import local_db
from ui.LeaderBoard import LeaderboardView
from utils.ismod import is_mod

class LeaderboardCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = local_db  # Use the shared local database instance

    @app_commands.command(
        name="leaderboard",
        description="Posts an interactive leaderboard showing the top users by total points."
    )
    @is_mod()
    async def leaderboard(self, interaction: discord.Interaction):
        # Create the leaderboard embed using the interactive view
        view = LeaderboardView(self.db, author=interaction.user, per_page=10)
        embed = view.build_embed()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=False)

async def setup(bot: commands.Bot):
    await bot.add_cog(LeaderboardCommands(bot))