# utils/backup.py
import discord
from discord.ext import commands

async def backup_database(bot: commands.Bot, db_instance) -> None:
    """
    Backs up the local database by sending the .db file to the bot owner's DM.
    
    :param bot: The running bot instance.
    :param db_instance: Your LocalDatabase instance.
    """
    """
    
    DISABLING FOR TESTING
    
    """
    return
    # Get the database file (this will commit & close the connection)
    db_file = db_instance.shutdown()
    
    # Retrieve the bot owner's DM channel (assuming single guild or bot.owner_id is set)
    owner = None
    if bot.owner_id:
        owner = bot.get_user(bot.owner_id)
    else:
        # Fallback: use the owner of the first guild
        if bot.guilds:
            owner = bot.guilds[0].owner

    if owner is None:
        print("Bot owner not found; cannot send backup file.")
        return

    try:
        dm_channel = owner.dm_channel or await owner.create_dm()
        await dm_channel.send("Here is the latest backup of the database:", file=discord.File(db_file))
        print("Backup file sent successfully.")
    except Exception as e:
        print(f"Error sending backup file: {e}")
