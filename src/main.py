from dotenv import load_dotenv
from discord import Intents
from discord.ext.commands import Bot
from logging import getLogger
from os import getenv

from services import DatabaseService

load_dotenv(".env")  # Load environment variables from .env file

intents = Intents.default()
intents.message_content = True

bot = Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready() -> None:
    """
    This function is called when the bot has successfully connected to Discord and is ready to operate.
    """
    _logger = getLogger(__name__)
    _logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")

    if DatabaseService().check_connection_name("default"):
        if await DatabaseService().check_connection_health("default"):
            _logger.info("Successfully connected to the database.")

        else:
            _logger.error("Failed to connect to the database. Please check your DATABASE_URL and ensure the database server is running.")

    else:
        _logger.warning("No database connection found with the name 'default'.")

    await DatabaseService().setup_connection("default")
    _logger.info("Database connection setup complete.")

    await bot.tree.sync()
    _logger.info("Command tree synchronized with Discord.")

if __name__ == "__main__":
    token = getenv("DISCORD_TOKEN")
    database_url = getenv("DATABASE_URL")

    if token is None:
        raise ValueError("DISCORD_TOKEN environment variable is not set.")

    if database_url is None:
        raise ValueError("DATABASE_URL environment variable is not set.")

    DatabaseService().create_connection("default", database_url)

    bot.run(token, root_logger=True)