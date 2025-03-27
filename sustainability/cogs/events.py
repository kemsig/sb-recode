# cogs/events.py
import discord
from discord.ext import commands
import config

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        # Create admin role if it doesn't exist
        role = discord.utils.get(guild.roles, name=config.ROLE_NAME)
        if not role:
            role = await guild.create_role(name=config.ROLE_NAME)
            print(f"Created role '{config.ROLE_NAME}' in guild: {guild.name}")
        else:
            print(f"Role '{config.ROLE_NAME}' already exists in guild: {guild.name}")

        # Create log channel if it doesn't exist
        channel = discord.utils.get(guild.channels, name=config.LOG_CHANNEL_NAME)
        if not channel:
            # Configure channel overwrites: by default, deny access to everyone except those with mod role.
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                role: discord.PermissionOverwrite(read_messages=True)
            }
            channel = await guild.create_text_channel(config.LOG_CHANNEL_NAME, overwrites=overwrites)
            print(f"Created channel '{config.LOG_CHANNEL_NAME}' in guild: {guild.name}")
        else:
            print(f"Channel '{config.LOG_CHANNEL_NAME}' already exists in guild: {guild.name}")

    @commands.Cog.listener()
    async def on_ready(self):
        # Iterate over all guilds on startup and ensure settings are in place
        for guild in self.bot.guilds:
            await self.on_guild_join(guild)

async def setup(bot):
    await bot.add_cog(Events(bot))
