# Code Is Under MPL-2.0
from traceback import format_exc
import nextcord
from nextcord import AllowedMentions, Intents, Message
from nextcord.ext import commands
from loguru import logger


class Bot(commands.Bot):
    """A subclass of commands.Bot with additional functionality."""

    def __init__(self, *args, **kwargs):
        logger.info("Starting up...")

        intents = Intents.all()

        super().__init__(
            command_prefix=self.get_prefix,
            intents=nextcord.Intents().all(),
            allowed_mentions=AllowedMentions(roles=False, everyone=False),
            *args,
            **kwargs,
        )

    def add_cog(self, cog) -> None:
        """Add a cog to the bot. Does not add disabled cogs."""

        if not hasattr(cog, "enabled") or cog.enabled:
            logger.info(f"Loading cog {cog.qualified_name}")
            return super().add_cog(cog)
        logger.info(f"Not loading cog {cog.qualified_name}")

    def load_extensions(self, *exts) -> None:
        """Load a given set of extensions."""

        logger.info(f"Starting loading {len(exts)} extensions...")

        success = 0

        for ext in exts:
            try:
                self.load_extension(ext)
            except Exception as e:
                logger.error(f"Error while loading {ext}: {e}:\n{format_exc()}")
            else:
                logger.info(f"Successfully loaded extension {ext}.")
                success += 1

        logger.info(
            f"Extension loading finished. Success: {success}. Failed: {len(exts) - success}."
        )

    async def get_prefix(self, message: Message):
        """Get a dynamic prefix."""

        return "!"

    async def on_connect(self):
        """Log the connect event."""

        logger.info("Connected to Discord.")


Bot.remove_command("help")
