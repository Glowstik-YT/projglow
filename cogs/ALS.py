##THE ADVANCED ECONOMY SYSTEM AND LEVEL SYSTEM.PY
##A GLOBAL LEVELING 
## The Advanced Leveling System By VincentRPS
from nextcord.ext import commands
from nextcord.ext.commands.core import command
import json

class level(commands.Cog):
    def __init__(self, client):
        self.client = client

@commands.command(name="level")



def setup(client):
    client.add_cog(level(client))