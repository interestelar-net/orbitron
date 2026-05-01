from discord.ext.commands import Bot
from logging import getLogger

from .example import ExampleExtension

async def setup(bot: Bot) -> None:
    """
    This function is called when the extension is loaded. It can be used to set up any necessary resources or state for the extension.

    :param bot: The instance of the Bot that is loading the extension.
    :type bot: Bot
    """
    _logger = getLogger(__name__)
    _logger.info("Example extension is being loaded...")

    await bot.add_cog(ExampleExtension(bot))

    _logger.info("Example extension loaded successfully.")