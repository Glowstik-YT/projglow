# Code Is Under MPL-2.0
from nextcord.ext.commands import Cog as _BaseCog


class Cog(_BaseCog):
    """A custom Cog for extra functionality."""

    enabled = True


def disabled(target: Cog):
    """A decorator to disable a cog from being loaded."""

    target.enabled = False

    return target
