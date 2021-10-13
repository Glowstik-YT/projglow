import nextcord
import random
from nextcord.ext import commands 

class Fun(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  
  @commands.command(name="Howgay", description="How gay are you?")
  async def howgay(self,ctx):
    gae = random.randint(1,100)
    e = nextcord.Embed(title=f"How Gay Is {ctx.author.mention}?",description=f"{ctx.author} is {gae}% gay!")
    await ctx.send(embed=e)
    
  @commands.command(name="Howsimp", description="How much of a simp are you?")
  async def simprate(self, ctx):
    simp = random.randint(1,100)
    e = nextcord.Embed(title="How much of simp is {ctx.author.mention}?",description=f"{ctx.author} is {simp}% simp!")
    
  @commands.command(name="russian roulette", description="Try not to push ur luck.")
  async def russian_roulette(self, ctx):
    oofed = [
      'Looks like the gun went off, *deletes system32 cutely*',
      'Oof you suck at this, the gun killed u',
      'You died Lmao, **told you not to push ur luck**'
      'ur save, for now...',
      'Save again? if i were you i wont do it again ;-;',
      'The gun was broken so i guess you were lucky?',
    ]
    
    response = random.choice(oofed)
    await ctx.reply(response)
    
