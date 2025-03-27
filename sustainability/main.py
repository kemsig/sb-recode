import discord
from discord.ext import commands
import config
from ui.TicketCreation import TicketCreateButton
from database.LocalDB import LocalDatabase
from utils.backup import backup_database

# create local db
if config.NO_MONGO:
    local_db = LocalDatabase(config.LOCAL_DB_NAME)
else:
    # mongo implementation
    print('sike there is no mongo implementation (cause i dont really need it right now)')

class SustainBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())
    
    async def setup_hook(self):
        # Load our cog extensions
        await self.load_extension("cogs.default")
        await self.load_extension("cogs.admin")
        await self.load_extension("cogs.events")
        await self.load_extension("cogs.manual")
        await self.load_extension("cogs.leaderboard")
    
    async def on_ready(self):
        print(f'Bot: "{self.user}" successfully logged in.')
        # Sync commands
        synced = await self.tree.sync()
        print("Synced " + str(len(synced)) + " commands.")

        # Add persistent view (for buttons, etc.)
        view = TicketCreateButton()
        self.add_view(view)


    async def close(self):
        print("safe closing")
        # Call the backup logic before shutting down
        await backup_database(self, local_db)
        # Then close the bot as usual
        await super().close()
        

if __name__ == "__main__":  
    bot = SustainBot()
    bot.run(config.DISCORD_BOT_SECRET)