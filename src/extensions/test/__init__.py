# External imports:
from discord.ext.commands import Bot
from logging import getLogger

# Internal imports:
from .test import TestExtension

# Code:
async def setup(bot: Bot) -> None:
    """
    This function is called when the extension is loaded. It can be used to set up any necessary resources or state for the extension.

    :param bot: The instance of the Bot that is loading the extension.
    :type bot: Bot
    """
    _logger = getLogger(__package__)
    _logger.info("Test extension is being loaded...")

    await bot.add_cog(TestExtension(bot))

    _logger.info("Test extension loaded successfully.")