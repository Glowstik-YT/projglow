## Advanced Economy System By VincentRPS
from nextcord.ext import commands
import json
from settings.rankcard import settings

class economy(commands.Cog):
    def __init__(self, client):
        self.client = client

def setup(client):
    client.add_cog(economy(client))