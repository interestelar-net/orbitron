from dotenv import load_dotenv
from discord import Intents
from discord.ext.commands import Bot
from logging import getLogger
from os import getenv

load_dotenv(".env")  # Load environment variables from .env file

bot = Bot(command_prefix="!", intents=Intents.default())

@bot.event
async def on_ready() -> None:
    """
    This function is called when the bot has successfully connected to Discord and is ready to operate.
    """
    _logger = getLogger(__name__)
    _logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")

if __name__ == "__main__":
    token = getenv("DISCORD_TOKEN")

    if token is None:
        raise ValueError("DISCORD_TOKEN environment variable is not set.")

    bot.run(token, root_logger=True)