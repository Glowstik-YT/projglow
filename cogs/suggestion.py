import nextcord
from nextcord.ext import commands
from global_functions import BOT_USER_ID
from ..internal.cog import Cog


class Suggestion(Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author.id) != str(BOT_USER_ID):
            send = message.channel.send

    @commands.command(name="suggest", description="Creates a suggestion in #suggestion")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def suggest(self, Context, *, suggestion):
        await Context.channel.purge(limit=1)
        channel = nextcord.utils.get(Context.guild.text_channels, name="suggestion")
        suggest = nextcord.Embed(
            title=f"Suggestion",
            description=f"{Context.message.author} suggests: **{suggestion}**",
        )
        sugg = await channel.send(embed=suggest)
        await channel.send(f"^^ Suggestion ID: {sugg.id}")
        await suggest.add_reaction("✅")
        await suggest.add_reaction("❌")

    @commands.command(name="approve", description="Approves a user's suggestion")
    async def approve(self, Context, id: int = None):
        if id == None:
            em = nextcord.Embed(
                title="Approve Error", description="Please specify message id"
            )
            return await Context.send(embed=em)
        channel = nextcord.utils.get(Context.guild.text_channels, name="suggestion")
        if channel is None:
            embed = nextcord.Embed(
                title="Approve Error", description="Can not find suggestion channel"
            )
            return await Context.send(embed=embed)
        suggestionMsg = await channel.fetch_message(id)
        embed = nextcord.Embed(
            title=f"Suggestion Approved!",
            description=f"The suggestion id of `{suggestionMsg.id}` has been approved by {Context.author.mention}",
        )
        await channel.send(embed=embed)


def setup(Bot):
    Bot.add_cog(Suggestion(Bot))
