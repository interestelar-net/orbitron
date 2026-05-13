# External imports:
from discord.ext.commands import Cog, Bot
from logging import getLogger

# Internal imports:
from .components import BotCommandGroup

# Code:
class BotExtension(Cog):
    """
    This is the bot extension that can be used to functions related to the bot. It includes basic functionality, for example, a command
    to check if the bot is alive. The extension is designed to be modular and can be easily integrated into the bot's architecture.
    """
    # Internal methods:
    def __init__(self, bot: Bot) -> None:
        """
        Initializes the BotExtension.

        :param bot: The instance of the Bot that is loading the extension.
        :type bot: Bot
        """
        self.bot = bot
        self.bot.tree.add_command(BotCommandGroup(bot, self))
        self._logger = getLogger(__package__)
        self._logger.debug("BotExtension initialized.")

    # Private methods:

    # Public methods: