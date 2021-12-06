# Code Is Under MPL-2.0
import nextcord
import sys
import os
from time import time
from nextcord.ext import commands
from inspect import getsource
from ..internal.cog import Cog


class Eval(Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    def resolve_variable(self, variable):
        if hasattr(variable, "__iter__"):
            var_length = len(list(variable))
            if (var_length > 100) and (not isinstance(variable, str)):
                return f"<a {type(variable).__name__} iterable with more than 100 values ({var_length})>"
            elif not var_length:
                return f"<an empty {type(variable).__name__} iterable>"

        if (not variable) and (not isinstance(variable, bool)):
            return f"<an empty {type(variable).__name__} object>"
        return (
            variable
            if (len(f"{variable}") <= 1000)
            else f"<a long {type(variable).__name__} object with the length of {len(f'{variable}'):,}>"
        )

    def prepare(self, string):
        arr = (
            string.strip("```").replace("py\n", "").replace("python\n", "").split("\n")
        )
        if not arr[::-1][0].replace(" ", "").startswith("return"):
            arr[len(arr) - 1] = "return " + arr[::-1][0]
        return "".join(f"\n\t{i}" for i in arr)

    @commands.command(
        pass_context=True,
        aliases=["eval", "exec", "evaluate"],
        description="Evaluates given code",
    )
    async def _eval(self, Context, *, code: str):
        if not Context.author.id == 744715959817994371:
            return
        silent = "-s" in code

        code = self.prepare(code.replace("-s", ""))
        args = {
            "nextcord": nextcord,
            "sauce": getsource,
            "sys": sys,
            "os": os,
            "imp": __import__,
            "this": self,
            "Context": Context,
            "member": Context.author,
            "Bot": self.Bot,
        }

        try:
            exec(f"async def func():{code}", args)
            a = time()
            response = await eval("func()", args)
            if silent or (response is None) or isinstance(response, nextcord.Message):
                em = nextcord.Embed(
                    title="Eval Success :D",
                    description="```Code ran without any errors```",
                )
                await Context.send(embed=em)
                del args, code
                return
            em = nextcord.Embed(
                title="Eval Success :o",
                description=f"```py\n{self.resolve_variable(response)}```",
            )
            em.set_footer(
                text=f"`{type(response).__name__} | {(time() - a) / 1000} ms`"
            )
            await Context.send(embed=em)
        except Exception as e:
            em = nextcord.Embed(
                title="Eval Error ._.",
                description=f"```{type(e).__name__}: {str(e)}```",
            )
            await Context.send(embed=em)

        del args, code, silent


def setup(Bot):
    Bot.add_cog(Eval(Bot))
