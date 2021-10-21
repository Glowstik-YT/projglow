#This Code Is Under The MPL-2.0 License

from logging import exception
import nextcord
import traceback
import datetime
from nextcord.colour import Color
from nextcord.embeds import Embed
from nextcord.ext import commands, tasks
from global_functions import (
    PREFIX,
    responses,
    TOKEN,
    ERROR_CHANNELS,
    UPDATE_CHANNEL,
    MEMBERCOUNT_CHANNEL,
    read_database,
    write_database
)
import random, json, os, sys
from difflib import get_close_matches
import asyncio
import aiohttp
from urllib.request import urlopen
import json

intents = nextcord.Intents().all()
client = commands.Bot(
    command_prefix=str(PREFIX), intents=intents, case_insensitive=True
)
client.remove_command("help")

for fn in os.listdir("./cogs"):
    if fn.endswith(".py") and fn != "global_functions.py":
        client.load_extension(f"cogs.{fn[:-3]}")


@tasks.loop(minutes=10)
async def member_count():
    try:
        member_count_channel = await client.fetch_channel(MEMBERCOUNT_CHANNEL)
    except:
        return print(f"Error!\nThe member count channel id is invalid!")
    if not isinstance(member_count_channel, nextcord.VoiceChannel):
        return print(
            f"Error!\nThe member count channel id that you gave is not a voice channel!"
        )
    glowstiks_git_repo = client.get_guild(794739329956053063)

    for x in (member_count_channel_name := member_count_channel.name.split(" ")):
        if x.isdigit():
            member_count_channel_name[member_count_channel_name.index(x)] = str(
                glowstiks_git_repo.member_count
            )
    try:
        await member_count_channel.edit(
            name=" ".join(member_count_channel_name),
            reason="Automated Member Count Rename",
        )
    except:
        return print("Error in renaming the member channel ;-;")


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
    member_count.start()
    print("Ready")
    try:
        update_channel = await client.fetch_channel(int(UPDATE_CHANNEL))
        embed = nextcord.Embed(
            title="I am online!",
            description=f"I got online at {nextcord.utils.format_dt(nextcord.utils.utcnow(), 'F')}",
        )
        await update_channel.send(embed=embed)
    except:
        print(
            f"Can't Fetch The Update Channel!\nMake Sure That You Kept The Right ID, If You Did Try And Contact ||Dank Lord||#9919"
        )
    error_channels = []
    error_in_loading_channel = []
    for ERROR_CHANNEL in ERROR_CHANNELS:
        try:
            channel = await client.fetch_channel(int(ERROR_CHANNEL))
            error_channels.append(
                f"https://discord.com/channels/{channel.guild.id}/{channel.id}"
            )
        except:
            error_in_loading_channel.append(str(ERROR_CHANNEL))
    error_channels = ", ".join(error_channels)
    print(f"My errors will be logged to {error_channels}")
    smthing = "\n".join(error_in_loading_channel)
    print(
        f"Can't fetch my error channel with id `{smthing}`, I can't log the errors ;-;"
    ) if len(error_in_loading_channel) > 0 else ...


@client.event
async def on_member_join(member):
    if member.guild.id != 794739329956053063:
        return
    channel = client.get_channel(794745011128369182)
    await channel.send(f"{member.name} has joined")



@client.event
async def on_raw_reaction_add(payload):
    if str(payload.emoji) != "⭐":
        return
    database = read_database()
    try:
        guild_starboard_settings = database[str(payload.guild_id)]['starboard']
        guild_starboard_settings['on or off']
        guild_starboard_settings['channel']
        guild_starboard_settings['minimum stars']
    except:
        return
    try:
        if not guild_starboard_settings["on or off"]:
            return
    except:
        return
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    for react in message.reactions:
        if str(react.emoji) == "⭐":
            react_count = react.count
            break
    if react_count >= 1:
        try:
            starboard_channel = client.get_channel(
                    guild_starboard_settings["channel"])
            try:
                sent_msg = await starboard_channel.fetch_message(
                        guild_starboard_settings[str(message.id)]
                    )
                await sent_msg.edit(
                        content=f":star2: {react_count} {channel.mention}"
                    )
            except:
                embed = nextcord.Embed(
                        description=f"{message.content}\n**Source**\n[Jump!]({message.jump_url})"
                    )
                embed.set_author(
                        name=message.author.display_name,
                        icon_url=message.author.display_avatar,
                    )
                embed.set_footer(text=str(message.id))
                sent_msg = await starboard_channel.send(
                        f":star2: {react_count} {channel.mention}", embed=embed
                    )
                guild_starboard_settings[str(message.id)] = sent_msg.id
                write_database(data=database)

        except:
            ...



@client.event
async def on_message(message):
    mention = f"<@!{client.user.id}>"
    if message.content == mention:
        await message.channel.send(
            "Eyoo Nerds my prefix is `>` for help use the command `>help`"
        )
    await client.process_commands(message)


class UrlButton(nextcord.ui.Button):
    def __init__(self, *, label, url, emoji=None):
        super().__init__(label=label, url=url, emoji=emoji)


class HelpDropdown(nextcord.ui.View):
    def __init__(self, user):
        self.user = user
        super().__init__()
        self.add_item(
            UrlButton(label="Support Server", url="https://discord.gg/xA3hBtujg7")
        )
        # Set the options that will be presented inside the dropdown

    @nextcord.ui.select(
        placeholder="Choose your help page",
        min_values=1,
        max_values=1,
        options=[
            nextcord.SelectOption(
                label="Moderation", description=f"`{PREFIX}help moderation`", emoji="⚒️"
            ),
            nextcord.SelectOption(
                label="Utility", description=f"`{PREFIX}help utility`", emoji="⚙️"
            ),
            nextcord.SelectOption(
                label="Music", description=f"`{PREFIX}help music`", emoji="🎵"
            ),
        ],
    )
    async def help_callback(self, select, interaction: nextcord.Interaction):
        if interaction.user.id != self.user.id:
            em = nextcord.Embed(
                title="No U",
                description="This is not for you!",
                color=nextcord.Color.red(),
            )
            return await interaction.response.send_message(embed=em, ephemeral=True)
        select.placeholder = f"{select.values[0]} Help Page"
        if select.values[0] == "Moderation":
            embed = nextcord.Embed(
                title=f"{client.user.name} Moderation Commands:",
                description=f"Support Server: [Click Here!](https://discord.gg/xA3hBtujg7) || `{PREFIX}help [category]` for other information.",
            )
            for index, command in enumerate(client.get_cog("Moderation").get_commands()):
                description = command.description
                if not description or description is None or description == "":
                    description = "No description"
                embed.add_field(
                    name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
                    value=description,
                )
            await interaction.response.edit_message(embed=embed, view=self)
        elif select.values[0] == "Utility":
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
            await interaction.response.edit_message(embed=embed, view=self)
        elif select.values[0] == "Music":
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
            await interaction.response.edit_message(embed=embed, view=self)


@client.group(invoke_without_command=True)
async def help(ctx):
    view = HelpDropdown(ctx.author)
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
    dank_lord = await client.fetch_user(758290177919156244)
    embed.set_footer(
        text=f"Requested by {ctx.author} | Created by: palp#9999 | Improved by: {dank_lord}",
        icon_url=f"{ctx.author.display_avatar}",
    )
    await ctx.send(embed=embed, view=view)


@help.command(aliases=['sb','starb'])
async def starboard(ctx):
    embed=Embed(title="Help with Starboard", description=f"""
`{PREFIX}starboard setup`
Setup the starboard!

`{PREFIX}starboard toggle [on/off]`
Toggle the starboard

`{PREFIX}starboard channel [channel]`
Get/Change the starboard channel settings

`{PREFIX}starboard minstars [number]`
Get/Change the starboard minimum star settings""")
    await ctx.send(embed=embed)


@help.command()
async def moderation(ctx):
    view = HelpDropdown(ctx.author)
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
    view = HelpDropdown(ctx.author)
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
    view = HelpDropdown(ctx.author)
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
async def on_error(error, *args, **kwargs):
    try:
        formatted_args = '\n'.join([f'{args.index(arg)+1}) {str(arg)} ({type(arg)})' for arg in args])
        formatted_args = f"```py\n{formatted_args}```"
        for ERROR_CHANNEL in ERROR_CHANNELS:
            try:
                error_channel = await client.fetch_channel(int(ERROR_CHANNEL))
            except:
                print(f"Can't log errors to the channel with id `{ERROR_CHANNEL}`")
                continue
            exception = sys.exc_info()
            exc = "\n".join(
                traceback.format_exception(exception[0], exception[1], exception[2])
            )
            error_em = nextcord.Embed(
                title=exception[0].__name__,
                color=nextcord.Color.red(),
                description=f"**Error in**: `{error}`\n```py\n{exc}```\n{f'Args: {formatted_args}' if len(args) > 0 else ''}\n{f'Kwargs: {kwargs}' if len(kwargs) > 0 else ''}",
            )
            try:
                await error_channel.send(embed=error_em)
            except:
                ...
        print(exc)
    except:
        exception = sys.exc_info()
        exc = "\n".join(
            traceback.format_exception(exception[0], exception[1], exception[2])
        )
        formatted_args = '\n'.join([f'{args.index(arg)+1}) {str(arg)} ({type(arg)})' for arg in args])
        print(exc, "Args: \n"+formatted_args)


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
    if isinstance(error, commands.MissingRequiredArgument):
        embed=Embed(title="Missing Required Arguments!", description=error, color=Color.red())
        await ctx.send(embed=embed)
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
    exception = "\n".join(
        traceback.format_exception(type(error), error, error.__traceback__)
    )
    for ERROR_CHANNEL in ERROR_CHANNELS:
        try:
            error_channel = await client.fetch_channel(int(ERROR_CHANNEL))
        except:
            print(f"Can't Fetch The Error Channel With ID: `{ERROR_CHANNEL}`")
            return print(exception)
        error_em = nextcord.Embed(
            title=error.__class__.__name__,
            description=f"""
Message: ```txt\n{ctx.message.content}```
Command: {ctx.command}
Error Treaceback: ```py\n{exception}```""",
            color=nextcord.Color.red(),
        )
        try:
            await error_channel.send(embed=error_em)
        except:
            print(
                f"Was Not Able To Send The Error In The Channel With ID: `{error_channel.id}`"
            )
    em = nextcord.Embed(
        title="Error ;-;",
        description=f"There was an error in the command `{ctx.command}`\nThe developers have been informed about the error, please refrain from using this command again!",
    )
    await ctx.channel.send(
        embed=em
    )  # Doing this so even when slash commands are implemented, the error handler still works just fine.
    print(exception)

    
@client.command()
async def emojiy(ctx,*,text):
  emojis = []
  for s in text.lower():
    if s.isdecimal():
      num2emo = {'0':'zero','1':'one','2':'two',
                 '3':'three','4':'four','5':'five',
                 '6':'six','7':'seven','8':'eight','9':'nine'}
      emojis.append(f':{num2emo.get(s)}:')
    elif s.isalpha():
      emojis.append(f':regional_indicator_{s}:')
    else:
      emojis.append(s)
  await ctx.send(' '.join(emojis))

client.run(TOKEN)
