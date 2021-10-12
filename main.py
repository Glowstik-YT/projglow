import nextcord
from nextcord.ext import commands
from global_functions import PREFIX, responses, TOKEN
import random, json, os
from difflib import get_close_matches
import asyncio
import aiohttp
from urllib.request import urlopen
import json

intents = nextcord.Intents().all()
client = commands.Bot(command_prefix=str(PREFIX), intents=intents, case_insensitive=True)
client.remove_command("help")

for fn in os.listdir("./cogs"):
    if fn.endswith(".py") and fn != "global_functions.py":
        client.load_extension(f"cogs.{fn[:-3]}")


async def startup():
    client.session = aiohttp.ClientSession()


client.loop.create_task(startup())


def apiReq(id, responseMSG):
    responseMSG = responseMSG.replace(" ", "-")

    url = f"http://api.brainshop.ai/get?bid=160228&key=nop&uid={id}&msg={responseMSG}"

    response = urlopen(url)
    data = json.loads(response.read())

    return data


@client.command()
async def chat(ctx, *, responseMSG):
    data = apiReq(ctx.author.id, responseMSG)
    await ctx.send(data)


@client.command()
async def load(ctx, extension):
    if ctx.author.id == 744715959817994371:
        client.load_extension(f"cogs.{extension}")
        await ctx.send("Cog loaded")
    else:
        await ctx.send("Only bot devs can run this command")


@client.command()
async def reload(ctx, extension):
    if ctx.author.id == 744715959817994371:
        client.unload_extension(f"cogs.{extension}")
        await asyncio.sleep(1)
        client.load_extension(f"cogs.{extension}")
        await ctx.send("Cog reloaded")
    else:
        await ctx.send("Only bot devs can run this command")


@client.command()
async def unload(ctx, extension):
    if ctx.author.id == 744715959817994371:
        client.unload_extension(f"cogs.{extension}")
        await ctx.send("Cog unloaded")
    else:
        await ctx.send("Only bot devs can run this command")


@client.command()
async def check(ctx, cog_name):
    if ctx.author.id == 744715959817994371:
        try:
            client.load_extension(f"cogs.{cog_name}")
        except commands.ExtensionAlreadyLoaded:
            await ctx.send("Cog is loaded")
        except commands.ExtensionNotFound:
            await ctx.send("Cog not found")
        else:
            await ctx.send("Cog is unloaded")
            client.unload_extension(f"cogs.{cog_name}")
    else:
        await ctx.send("Only bot devs can run this command")


@client.event
async def on_ready():
    print("Ready")


@client.event
async def on_member_join(member):
    channel = await client.get_channel(794745011128369182)
    await channel.send(f"{member.name} has joined")


class HelpDropdown(nextcord.ui.Select):
    def __init__(self):

        # Set the options that will be presented inside the dropdown
        options = [
            nextcord.SelectOption(
                label="Moderation", description=f"`{PREFIX}help moderation`", emoji="⚒️"
            ),
            nextcord.SelectOption(
                label="Utility", description=f"`{PREFIX}help utility`", emoji="⚙️"
            ),
            nextcord.SelectOption(
                label="Music", description=f"`{PREFIX}help music`", emoji="🎵"
            ),
        ]

        super().__init__(
            placeholder="Choose your help page",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == "Moderation":
            embed = nextcord.Embed(
                title=f"{client.user.name} Moderation Commands:",
                description=f"Support Server: [Click Here!](https://discord.gg/xA3hBtujg7) || `{PREFIX}help [category]` for other information.",
            )
            for command in client.get_cog("Moderation").walk_commands():
                description = command.description
                if not description or description is None or description == "":
                    description = "No description"
                embed.add_field(
                    name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
                    value=description,
                )
            await interaction.response.send_message(embed=embed)
        elif self.values[0] == "Utility":
            embed = nextcord.Embed(
                title=f"{client.user.name} Utility Commands:",
                description=f"Support Server: [Click Here!](https://discord.gg/xA3hBtujg7) || `{PREFIX}help [category]` for other information.",
            )
            for command in client.get_cog("util").walk_commands():
                description = command.description
                if not description or description is None or description == "":
                    description = "No description"
                embed.add_field(
                    name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
                    value=description,
                )
            await interaction.response.send_message(embed=embed)
        elif self.values[0] == "Music":
            embed = nextcord.Embed(
                title=f"{client.user.name} Music Commands:",
                description=f"Support Server: [Click Here!](https://discord.gg/xA3hBtujg7) || `{PREFIX}help [category]` for other information.",
            )
            for command in client.get_cog("Music").walk_commands():
                description = command.description
                if not description or description is None or description == "":
                    description = "No description"
                embed.add_field(
                    name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
                    value=description,
                )
            await interaction.response.send_message(embed=embed)


class HelpDropdownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(HelpDropdown())


@client.group(invoke_without_command=True)
async def help(ctx):
    view = HelpDropdownView()
    embed = nextcord.Embed(
        title=f"{client.user.name} Help",
        description=f"Support Server: [Click Here!](https://discord.gg/xA3hBtujg7) || `{PREFIX}help [category]` for more information.",
    )
    embed.set_thumbnail(url=f"{client.user.display_avatar}")
    embed.add_field(
        name="Moderation:", value=f"`{PREFIX}help moderation`", inline=False
    )
    embed.add_field(name="Utility:", value=f"`{PREFIX}help utility`", inline=False)
    embed.add_field(name="Music:", value=f"`{PREFIX}help music`", inline=False)
    embed.set_footer(
        text=f"Requested by {ctx.author} | Created by: palp#9999",
        icon_url=f"{ctx.author.display_avatar}",
    )
    await ctx.send(embed=embed, view=view)


@help.command()
async def moderation(ctx):
    view = HelpDropdownView()
    embed = nextcord.Embed(
        title=f"{client.user.name} Moderation Commands:",
        description=f"Support Server: [Click Here!](https://discord.gg/xA3hBtujg7) || `{PREFIX}help [category]` for other information.",
    )
    embed = nextcord.Embed(
        title=f"{client.user.name} Moderation Commands:",
        description=f"Support Server: [Click Here!](https://discord.gg/xA3hBtujg7) || `{PREFIX}help [category]` for other information.",
    )
    for command in client.get_cog("Moderation").walk_commands():
        description = command.description
        if not description or description is None or description == "":
            description = "No description"
        embed.add_field(
            name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
            value=description,
        )
    await ctx.send(embed=embed, view=view)


@help.command()
async def utility(ctx):
    view = HelpDropdownView()
    embed = nextcord.Embed(
        title=f"{client.user.name} Utility Commands:",
        description=f"Support Server: [Click Here!](https://discord.gg/xA3hBtujg7) || `{PREFIX}help [category]` for other information.",
    )
    for command in client.get_cog("util").walk_commands():
        description = command.description
        if not description or description is None or description == "":
            description = "No description"
        embed.add_field(
            name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
            value=description,
        )
    await ctx.send(embed=embed, view=view)


@help.command()
async def music(ctx):
    view = HelpDropdownView()
    embed = nextcord.Embed(
        title=f"{client.user.name} Music Commands:",
        description=f"Support Server: [Click Here!](https://discord.gg/xA3hBtujg7) || `{PREFIX}help [category]` for other information.",
    )
    for command in client.get_cog("Music").walk_commands():
        description = command.description
        if not description or description is None or description == "":
            description = "No description"
        embed.add_field(
            name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
            value=description,
        )
    await ctx.send(embed=embed, view=view)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        cmd = ctx.invoked_with
        cmds = [cmd.name for cmd in client.commands]
        matches = get_close_matches(cmd, cmds)
        if len(matches) > 0:
            embed = nextcord.Embed(
                title="Invalid Command!",
                description=f"Command `{str(PREFIX)}{cmd}` not found, maybe you meant `{str(PREFIX)}{matches[0]}`?",
            )
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
                title="Invalid Command!",
                description=f"Please type `{str(PREFIX)}help` to see all commands",
            )
            await ctx.send(embed=embed)
        return
    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            em = nextcord.Embed(
                title="**Command on cooldown**",
                description=f"You must wait `{int(s)}` seconds to use this command!",
            )
            await ctx.send(embed=em)
        elif int(h) == 0 and int(m) != 0:
            em = nextcord.Embed(
                title="**Command on cooldown**",
                description=f" You must wait `{int(m)}` minutes and `{int(s)}` seconds to use this command!",
            )
            await ctx.send(embed=em)
        else:
            em = nextcord.Embed(
                title="**Command on cooldown**",
                description=f" You must wait `{int(h)}` hours, `{int(m)}` minutes and `{int(s)}` seconds to use this command!",
            )
            await ctx.send(embed=em)
        return
    if isinstance(error, commands.DisabledCommand):
        em = nextcord.Embed(
            title="Command Disabled",
            description="It seems the command you are trying to use has been disabled",
        )
        await ctx.send(embed=em)
        return
    if isinstance(error, commands.MissingPermissions):
        missing = [
            perm.replace("_", " ").replace("guild", "server").title()
            for perm in error.missing_perms
        ]
        if len(missing) > 2:
            fmt = "{}, and {}".format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = " and ".join(missing)
        _message = "You require the `{}` permission to use this command.".format(fmt)
        em = nextcord.Embed(title="Invalid Permissions", description=_message)
        await ctx.send(embed=em)
        return
    if isinstance(error, commands.BotMissingPermissions):
        missing = [
            perm.replace("_", " ").replace("guild", "server").title()
            for perm in error.missing_perms
        ]
        if len(missing) > 2:
            fmt = "{}, and {}".format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = " and ".join(missing)
        _message = "I require the `{}` permission to use this command.".format(fmt)
        em = nextcord.Embed(title="Invalid Permissions", description=_message)
        await ctx.send(embed=em)
        return
    if isinstance(error, commands.BadArgument):
        em = nextcord.Embed(
            title="Bad Argument",
            description="The library ran into an error attempting to parse your argument.",
        )
        await ctx.send(embed=em)
        return
    if isinstance(error, nextcord.NotFound) and "Unknown interaction" in str(error):
        return
    print(error)


client.run(TOKEN)
