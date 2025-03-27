# cogs/default.py
import discord
from discord import app_commands
from discord.ext import commands

import config


from main import local_db  # Import the shared instance created in main.py

class DefaultCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = local_db

    @app_commands.command(name="points", description='Shows how many points you have!')
    async def points(self, interaction: discord.Interaction):
        logs_channel = discord.utils.get(interaction.guild.channels, name=config.LOG_CHANNEL_NAME)
        mod_mention = interaction.user.mention
        guild_owner = interaction.guild.owner.mention

        user_id = interaction.user.id
    

        print(logs_channel, mod_mention, guild_owner, user_id)
        # add logging TODO

        # query for user info 
        user_info_dict = self.db.get_user_info(user_id=user_id)
        cur_points = user_info_dict['points_cur']
        total_points = user_info_dict['points_total']

        # send user info
        await interaction.response.send_message(f'Your current points is now **{cur_points} points** with a lifetime score of **{total_points} points**!', ephemeral=True)

        

async def setup(bot):
    await bot.add_cog(DefaultCommands(bot))
