# External imports:
from discord.app_commands import Group, command
from discord.ext.commands import Cog, Bot
from logging import getLogger
from discord import Interaction, Embed, Color

# Internal imports:

# Code:
class BotCommandGroup(Group):
    """
    This is a command group for bot-related commands. It can be used to organize commands that are related to the bot's
    functionality, such as checking if the bot is alive or getting information about the bot. The command group is designed to be
    modular and can be easily integrated into the bot's architecture.
    """
    # Internal methods:
    def __init__(self, bot: Bot, cog: Cog) -> None:
        """
        Initializes the BotCommandGroup.

        :param bot: The instance of the Bot that is loading the command group.
        :type bot: Bot
        :param cog: The Cog that the command group belongs to.
        :type cog: Cog
        """
        super().__init__(name="bot", description="Commands related to the bot.")
        self.bot = bot
        self.cog = cog
        self._logger = getLogger(__package__)
        self._logger.debug("BotCommandGroup initialized.")

    # Private methods:

    # Public methods:
    @command(name="status", description="Check the status of the bot.")
    async def status(self, interaction: Interaction) -> None:
        """
        This command checks the status of the bot and responds with an embedded message containing the bot's latency and a status message.

        :param interaction: The interaction that triggered the command.
        :type interaction: Interaction
        """
        embed = Embed(
            title="Bot Status:",
            description="The bot is alive and functioning properly!",
            color=Color.blurple()
        )
        embed.add_field(
            name="Ping:",
            value=f"`{self.bot.latency * 1000:.0f} ms`",
            inline=True
        )
        embed.set_footer(
            text=f"{self.bot.user.name} is here to assist you!",
            icon_url=self.bot.user.avatar.url if self.bot.user.avatar else None
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)