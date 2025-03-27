import discord
from discord import app_commands
from discord.ext import commands
from main import local_db  # Assumes you have a shared LocalDatabase instance

class LeaderboardView(discord.ui.View):
    def __init__(self, db, author: discord.User, per_page: int = 10):
        super().__init__(timeout=120)
        self.db = db
        self.author = author  # Restrict control to the command invoker
        self.per_page = per_page
        self.current_page = 0
        self.total_entries = self.get_total_entries()
        self.max_page = (self.total_entries - 1) // self.per_page if self.total_entries > 0 else 0
        self.prev_button.disabled = True  # Disable previous button on first page

    def get_total_entries(self) -> int:
        try:
            cur = self.db.conn.cursor()
            cur.execute("SELECT COUNT(*) FROM users")
            result = cur.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error getting total entries: {e}")
            return 0

    def build_embed(self) -> discord.Embed:
        embed = discord.Embed(title="Leaderboard", color=discord.Color.blue())
        offset = self.current_page * self.per_page
        leaderboard_data = self.db.get_leaderboard(limit=self.per_page, offset=offset)
        if not leaderboard_data:
            embed.description = "No data available."
        else:
            description = ""
            rank = offset + 1
            for user in leaderboard_data:
                description += f"**#{rank}** - User ID: {user['user_id']} | Total Points: {user['points_total']}\n"
                rank += 1
            embed.description = description
            embed.set_footer(text=f"Page {self.current_page + 1} of {self.max_page + 1}")
        return embed

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.blurple)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.author:
            await interaction.response.send_message("You cannot control this leaderboard.", ephemeral=True)
            return
        if self.current_page > 0:
            self.current_page -= 1
            self.next_button.disabled = False  # Re-enable next button if disabled
            if self.current_page == 0:
                button.disabled = True
            await interaction.response.edit_message(embed=self.build_embed(), view=self)
        else:
            button.disabled = True
            await interaction.response.defer()

    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.author:
            await interaction.response.send_message("You cannot control this leaderboard.", ephemeral=True)
            return
        if self.current_page < self.max_page:
            self.current_page += 1
            self.prev_button.disabled = False  # Re-enable previous button if disabled
            if self.current_page == self.max_page:
                button.disabled = True
            await interaction.response.edit_message(embed=self.build_embed(), view=self)
        else:
            button.disabled = True
            await interaction.response.defer()