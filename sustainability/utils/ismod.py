import discord
from discord import app_commands
from discord.ext import commands
import config

def is_mod():
    async def predicate(interaction: discord.Interaction):
        # Allow guild owner
        if interaction.user.id == interaction.guild.owner.id:
            return True
        # Allow if user has Administrator permission
        if interaction.user.guild_permissions.administrator:
            return True
        role = discord.utils.get(interaction.guild.roles, name=config.ROLE_NAME)
        return role in interaction.user.roles
    return app_commands.check(predicate)
