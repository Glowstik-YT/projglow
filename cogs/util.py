# Code Is Under MPL-2.0
import time
import nextcord
import os
import psutil
import random
from datetime import datetime
from nextcord.ext import commands, tasks
from global_functions import (
    ban_msg,
    kick_msg,
    BOT_USER_ID,
    EMOJIS_TO_USE_FOR_CALCULATOR as etufc,
)
import aiohttp
from io import BytesIO
import requests
from nextcord import ButtonStyle
from nextcord.ui import button, View, Button
from ..internal.cog import Cog

green_button_style = ButtonStyle.success
grey_button_style = ButtonStyle.secondary
blue_button_style = ButtonStyle.primary
red_button_style = ButtonStyle.danger


class CalculatorButtons(View):
    def __init__(self, owner, embed, message):
        self.embed = embed
        self.owner = owner
        self.message = message
        self.expression = ""
        super().__init__(timeout=300.0)

    @button(emoji=etufc["1"], style=grey_button_style, row=1)
    async def one_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "1"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc["2"], style=grey_button_style, row=1)
    async def two_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "2"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc["3"], style=grey_button_style, row=1)
    async def three_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "3"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc["4"], style=grey_button_style, row=2)
    async def four_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "4"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc["5"], style=grey_button_style, row=2)
    async def five_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "5"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc["6"], style=grey_button_style, row=2)
    async def six_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "6"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc["7"], style=grey_button_style, row=3)
    async def seven_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "7"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc["8"], style=grey_button_style, row=3)
    async def eight_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "8"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc["9"], style=grey_button_style, row=3)
    async def nine_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "9"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc["0"], style=grey_button_style, row=4)
    async def zero_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "0"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(label="00 ", style=grey_button_style, row=4)
    async def double_zero_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "00"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc["."], style=grey_button_style, row=4)
    async def dot_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "."
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc["x"], style=blue_button_style, row=1, custom_id="*")
    async def multiplication_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "x"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc["÷"], style=blue_button_style, row=2, custom_id="/")
    async def division_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "÷"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc["+"], style=blue_button_style, row=3)
    async def addition_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "+"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc["-"], style=blue_button_style, row=4)
    async def subtraction_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "-"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(label="←", style=red_button_style, row=1)
    async def back_space_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression = self.expression[:-1]
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(label="Clear", style=red_button_style, row=2)
    async def clear_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression = ""
        self.embed.description = "Cleared Calculator"
        await interaction.response.edit_message(embed=self.embed)

    @button(label="Exit", style=red_button_style, row=3)
    async def exit_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        for child in self.children:
            child.disabled = True
        embed = nextcord.Embed(title="Abandoned Calculator", color=nextcord.Color.red())
        await interaction.response.edit_message(embed=embed, view=self)

    @button(label="=", style=green_button_style, row=4)
    async def equal_to_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        expression = self.expression
        expression = expression.replace("÷", "/").replace("x", "*")
        try:
            result = str(eval(expression))
            self.expression = result
        except:
            result = "An Error Occured ;-;"
        self.embed.description = result
        await interaction.response.edit_message(embed=self.embed)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        embed = nextcord.Embed(title="Time Up", color=nextcord.Color.red())
        await self.message.edit(embed=embed, view=self)


us = 0
um = 0
uh = 0
ud = 0


class util(Cog):
    def __init__(self, Bot):
        self.Bot = Bot
        self.Botuptime.start()

    @commands.command(description="A handy Calculator!", aliases=["calc"])
    async def calculator(self, Context):
        message = await Context.send("Loading Calculator....")
        embed = nextcord.Embed(
            title=f"{Context.author}'s Calculator",
            color=nextcord.Color.green(),
            description="This is the start of the calculator!",
        )
        view = CalculatorButtons(Context.author, embed, message)
        await message.edit(content=None, embed=embed, view=view)

    @commands.command(description="Shows the user's info.")
    async def userinfo(self, Context, *, user: nextcord.Member = None):  # b'\xfc'
        if user is None:
            user = Context.author
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = nextcord.Embed(color=0xDFA3FF, description=user.mention)
        embed.set_author(name=str(user.name), icon_url=user.display_avatar)
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(Context.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user) + 1))
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = " ".join([r.mention for r in user.roles][1:])
            embed.add_field(
                name="Roles [{}]".format(len(user.roles) - 1),
                value=role_string,
                inline=False,
            )
        perm_paginator = commands.Paginator(prefix="```diff", max_size=1000)
        for p in user.guild_permissions:
            perm_paginator.add_line(
                f"{'+' if p[1] else '-'} {str(p[0]).replace('_', ' ').title()}"
            )
        embed.add_field(
            name="Guild permissions", value=f"{perm_paginator.pages[0]}", inline=False
        )
        embed.set_footer(text=self.Bot.user.name, icon_url=self.Bot.user.display_avatar)
        return await Context.send(embed=embed)

    @commands.command(description="Shows the server's description.")
    async def serverinfo(self, Context):
        role_count = len(Context.guild.roles)
        list_of_bots = [bot.mention for bot in Context.guild.members if bot.bot]

        embed2 = nextcord.Embed(
            timestamp=Context.message.created_at, color=Context.author.color
        )
        embed2.add_field(name="Name", value=f"{Context.guild.name}", inline=False)
        embed2.add_field(
            name="Verification Level",
            value=str(Context.guild.verification_level),
            inline=True,
        )
        embed2.add_field(
            name="Highest role", value=Context.guild.roles[-1], inline=True
        )
        embed2.add_field(name="Number of roles", value=str(role_count), inline=True)
        embed2.add_field(
            name="Number Of Members", value=Context.guild.member_count, inline=True
        )
        embed2.add_field(
            name="Created At",
            value=Context.guild.created_at.__format__("%A, %d. %B %Y @ %H:%M:%S"),
            inline=True,
        )
        embed2.add_field(name="Bots:", value=(", ".join(list_of_bots)), inline=False)
        embed2.set_thumbnail(url=Context.guild.icon.url)
        embed2.set_author(
            name=Context.author.name, icon_url=Context.author.display_avatar
        )
        embed2.set_footer(
            text=self.Bot.user.name, icon_url=self.Bot.user.display_avatar
        )
        await Context.send(embed=embed2)

    @commands.command(
        aliases=["cs", "ci", "channelinfo"], description="Shows the channel's stats."
    )
    async def channelstats(self, Context, channel: nextcord.TextChannel = None):
        if channel == None:
            channel = Context.channel

        embed = nextcord.Embed(
            title=f"{channel.name}",
            description=f"{'Category - `{}`'.format(channel.category.name) if channel.category else '`This channel is not in a category`'}",
        )
        embed.add_field(name="Guild", value=Context.guild.name, inline=True)
        embed.add_field(name="Channel Id", value=channel.id, inline=True)
        embed.add_field(
            name="Channel Topic",
            value=f"{channel.topic if channel.topic else 'No topic'}",
            inline=False,
        )
        embed.add_field(name="Channel Position", value=channel.position, inline=True)
        embed.add_field(name="Slowmode", value=channel.slowmode_delay, inline=True)
        embed.add_field(name="NSFW", value=channel.is_nsfw(), inline=True)
        embed.add_field(name="Annoucement", value=channel.is_news(), inline=True)
        embed.add_field(
            name="Channel Permissions", value=channel.permissions_synced, inline=True
        )
        embed.add_field(name="Channel Hash", value=hash(channel), inline=False)
        embed.set_thumbnail(url=Context.guild.icon.url)
        embed.set_author(
            name=Context.author.name, icon_url=Context.author.display_avatar
        )
        embed.set_footer(text=self.Bot.user.name, icon_url=self.Bot.user.display_avatar)
        await Context.send(embed=embed)

    @commands.command(alisas=["adde"], description="Adds an emoji to the server.")
    async def emojiadd(self, Context, url: str, *, name):
        guild = Context.guild
        if Context.author.guild_permissions.manage_emojis:
            async with aiohttp.BotSession() as ses:
                async with ses.get(url) as r:

                    try:
                        img_or_gif = BytesIO(await r.read())
                        b_value = img_or_gif.getvalue()
                        if r.status in range(200, 299):
                            emoji = await guild.create_custom_emoji(
                                image=b_value, name=name
                            )
                            em = nextcord.Embed(
                                title="Emoji Success",
                                description=f"Successfully created emoji: <:{name}:{emoji.id}>",
                            )
                            await Context.send(embed=em)
                            await ses.close()
                        else:
                            em = nextcord.Embed(
                                title="Emoji Error",
                                description=f"Error when making request | {r.status} response.",
                            )
                            await Context.send(embed=em)
                            await ses.close()

                    except nextcord.HTTPException:
                        em = nextcord.Embed(
                            title="Emoji Error", description="File size is too big!"
                        )
                        await Context.send(embed=em)

    @commands.command(
        alisas=["removee"], description="Removes the specified emoji from the server."
    )
    async def emojiremove(self, Context, emoji: nextcord.Emoji):
        guild = Context.guild
        if Context.author.guild_permissions.manage_emojis:
            em = nextcord.Embed(
                title="Emoji Success",
                description=f"Successfully deleted (or not :P) {emoji}",
            )
            await Context.send(embed=em)
            await emoji.delete()

    @commands.command(name="toggle", description="Enable or disable a command!")
    @commands.is_owner()
    async def toggle(self, Context, *, command):
        command = self.Bot.get_command(command)

        if command is None:
            embed = nextcord.Embed(
                title="ERROR", description="I can't find a command with that name"
            )
            await Context.send(embed=embed)

        elif Context.command == command:
            embed = nextcord.Embed(
                title="ERROR", description="You cannot disable this command "
            )
            await Context.send(embed=embed)

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            embed = nextcord.Embed(title="Toggle", description=ternary)
            await Context.send(embed=embed)

    @commands.command(name="steal", description="Steals an emoji form a server")
    async def steal(self, Context, emoji: nextcord.PartialEmoji, *, text=None):

        if Context.author.guild_permissions.manage_emojis:

            if text == None:
                text = emoji.name
            else:
                text = text.replace(" ", "_")

            r = requests.get(emoji.url, allow_redirects=True)

            if emoji.animated == True:
                open("emoji.gif", "wb").write(r.content)
                with open("emoji.gif", "rb") as f:
                    z = await Context.guild.create_custom_emoji(
                        name=text, image=f.read()
                    )
                os.remove("emoji.gif")

            else:
                open("emoji.png", "wb").write(r.content)
                with open("emoji.png", "rb") as f:
                    z = await Context.guild.create_custom_emoji(
                        name=text, image=f.read()
                    )
                os.remove("emoji.png")

            embed = nextcord.Embed(
                title="Success",
                description=f"Succesfully Cloned {z}",
                color=nextcord.Color.green(),
            )
            await Context.send(embed=embed)

    @commands.command(description="Shows the ping of the bot")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def ping(self, Context):
        em = nextcord.Embed(title="Pong!🏓", colour=nextcord.Colour.random())
        em.add_field(
            name="My API Latency is:", value=f"{round(self.Bot.latency*1000)} ms!"
        )
        em.set_footer(
            text=f"Ping requested by {Context.author}",
            icon_url=Context.author.display_avatar,
        )
        await Context.send(embed=em)

    @tasks.loop(seconds=2.0)
    async def Botuptime(self):
        global uh, us, um, ud
        us += 2
        if us == 60:
            us = 0
            um += 1
            if um == 60:
                um = 0
                uh += 1
                if uh == 24:
                    uh = 0
                    ud += 1

    @Botuptime.before_loop
    async def before_Botuptime(self):
        print("waiting...")
        await self.Bot.wait_until_ready()

    @commands.command(
        aliases=["statistics", "stat", "statistic"],
        description="Shows the bot's statistics",
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def stats(self, Context):
        global ud, um, uh, us
        em = nextcord.Embed(title="How long have I been up?")
        em.add_field(name="Days:", value=ud, inline=False)
        em.add_field(name="Hours:", value=uh, inline=False)
        em.add_field(name="Minutes:", value=um, inline=False)
        em.add_field(name="Seconds:", value=us, inline=False)
        em.add_field(name="CPU usage:", value=f"{psutil.cpu_percent()}%", inline=False)
        em.add_field(
            name="RAM usage:", value=f"{psutil.virtual_memory()[2]}%", inline=False
        )
        em.set_footer(
            text=f"Stats requested by: {Context.author}",
            icon_url=Context.author.display_avatar,
        )
        await Context.send(embed=em)


def setup(Bot):
    Bot.add_cog(util(Bot))
