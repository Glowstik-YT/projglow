import nextcord
from nextcord.ext import commands
import re
from pistonapi import PistonAPI#do pip install pistonapi before running

pistonapi = PistonAPI()

class CodeCompiler(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.language_alias = {
            "bh": "bash",
            "java": "java",
            "py": "python",
            "lua": "lua",
            "php": "php",
            "ts": "typescript",
        }

        self.supported_langs = {
            "java": "15.0.2",
            "bash": "5.1.0",
            "python": "3.10.0",
            "lua": "5.4.2",
            "php": "8.0.2",
            "typescript": "4.2.3",
        }

    @commands.command()
    async def run(self, ctx, language=None, *, code=None):
        if language is None:
            return await ctx.send("Please provide a programming language!")

        if code is None:
            return await ctx.send(f"{ctx.author.mention} I dont see ur code block :|")

        blocks = re.findall(r"```(.*)\n(.*)\n?```\n?", code)[:2]

        if not blocks:
            return await ctx.send(
                f"{ctx.author.mention} I dont see ur code block :eyes:"
            )

        print(code)
        print(blocks)
        if len(blocks) == 1:
            code_input = None
            code_source = blocks[0][1]
        else:
            code_input = blocks[0][1]
            code_source = blocks[1][1]

        language = discord.utils.escape_mentions(language.lower())

        if language in self.language_alias:
            language = self.language_alias[language]

        if language in self.supported_langs:
            result = piston.execute(
                language=language,
                version=self.supported_langs[language],
                code=code_source,
                stdin=code_input or "",
            )
            return await ctx.reply(
                embed=nextcord.Embed(
                    title=f"{language.title()} Code Run",
                    description=f"```{language}\n{str(result)}```",
                    color=nextcord.Color.blurple(),
                )
            )
        else:
            return await ctx.send(
                f"{ctx.author.mention} I currently don't support **{language}**, Please give the devs a suggestion on what language to add next using >suggest <ur suggesttion>"
            )
          
          
def setup(client):
  client.add_cog(CodeCompiler(client))
