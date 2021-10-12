import nextcord
from nextcord.ext import commands
from global_functions import BOT_USER_ID


class Starboard(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author.id) != str(BOT_USER_ID):
            send = message.channel.send

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = str(payload.emoji)
        if message.author.bot:
            return
        else:
            if reaction == "⭐":
                await channel.send(f"{reaction}")
                print(reaction)


def setup(client):
    client.add_cog(Starboard(client))
