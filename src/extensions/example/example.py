from discord.ext.commands import Cog, Bot
from logging import getLogger

class ExampleExtension(Cog):
    """
    This is an example extension that demonstrates how to create a simple extension for a Discord bot using the discord.py library. It includes basic setup and logging to show when the extension is loaded.
    """
    # Internal methods:
    def __init__(self, bot: Bot) -> None:
        """
        Initializes the ExampleExtension.

        :param bot: The instance of the Bot that is loading the extension.
        :type bot: Bot
        """
        self.bot = bot
        self._logger = getLogger(__package__)
        self._logger.debug("ExampleExtension initialized.")

    # Private methods:

    # Public methods: