import time
import nextcord
import os
import psutil
import random
from datetime import datetime
from nextcord.ext import commands, tasks
from global_functions import ban_msg, kick_msg, BOT_USER_ID
import aiohttp
from io import BytesIO

us = 0
um = 0
uh = 0
ud = 0


class util(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.clientuptime.start()

    @commands.command()
    async def userinfo(self, ctx, *, user: nextcord.Member = None):  # b'\xfc'
        if user is None:
            user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = nextcord.Embed(color=0xDFA3FF, description=user.mention)
        embed.set_author(name=str(user.name), icon_url=user.display_avatar)
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user) + 1))
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = " ".join([r.mention for r in user.roles][1:])
            embed.add_field(
                name="Roles [{}]".format(len(user.roles) - 1),
                value=role_string,
                inline=False,
            )
        perm_string = ", ".join(
            [
                str(p[0]).replace("_", " ").title()
                for p in user.guild_permissions
                if p[1]
            ]
        )
        embed.add_field(
            name="Guild permissions", value=f"`{perm_string}`", inline=False
        )
        embed.set_footer(
            text=self.client.user.name, icon_url=self.client.user.display_avatar
        )
        return await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        role_count = len(ctx.guild.roles)
        list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]

        embed2 = nextcord.Embed(
            timestamp=ctx.message.created_at, color=ctx.author.color
        )
        embed2.add_field(name="Name", value=f"{ctx.guild.name}", inline=False)
        embed2.add_field(
            name="Verification Level",
            value=str(ctx.guild.verification_level),
            inline=True,
        )
        embed2.add_field(name="Highest role", value=ctx.guild.roles[-1], inline=True)
        embed2.add_field(name="Number of roles", value=str(role_count), inline=True)
        embed2.add_field(
            name="Number Of Members", value=ctx.guild.member_count, inline=True
        )
        embed2.add_field(
            name="Created At",
            value=ctx.guild.created_at.__format__("%A, %d. %B %Y @ %H:%M:%S"),
            inline=True,
        )
        embed2.add_field(name="Bots:", value=(", ".join(list_of_bots)), inline=False)
        embed2.set_thumbnail(url=ctx.guild.icon.url)
        embed2.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
        embed2.set_footer(
            text=self.client.user.name, icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=embed2)

    @commands.command(aliases=["cs", "ci", "channelinfo"])
    async def channelstats(self, ctx, channel: nextcord.TextChannel = None):
        if channel == None:
            channel = ctx.channel

        embed = nextcord.Embed(
            title=f"{channel.name}",
            description=f"{'Category - `{}`'.format(channel.category.name) if channel.category else '`This channel is not in a category`'}",
        )
        embed.add_field(name="Guild", value=ctx.guild.name, inline=True)
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
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
        embed.set_footer(
            text=self.client.user.name, icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=embed)

    @commands.command(alisas=["adde"])
    async def emojiadd(self, ctx, url: str, *, name):
        guild = ctx.guild
        if ctx.author.guild_permissions.manage_emojis:
            async with aiohttp.ClientSession() as ses:
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
                            await ctx.send(embed=em)
                            await ses.close()
                        else:
                            em = nextcord.Embed(
                                title="Emoji Error",
                                description=f"Error when making request | {r.status} response.",
                            )
                            await ctx.send(embed=em)
                            await ses.close()

                    except nextcord.HTTPException:
                        em = nextcord.Embed(
                            title="Emoji Error", description="File size is too big!"
                        )
                        await ctx.send(embed=em)

    @commands.command(alisas=["removee"])
    async def emojiremove(self, ctx, emoji: nextcord.Emoji):
        guild = ctx.guild
        if ctx.author.guild_permissions.manage_emojis:
            em = nextcord.Embed(
                title="Emoji Success",
                description=f"Successfully deleted (or not :P) {emoji}",
            )
            await ctx.send(embed=em)
            await emoji.delete()

    @commands.command(name="toggle", description="Enable or disable a command!")
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        command = self.client.get_command(command)

        if command is None:
            embed = nextcord.Embed(
                title="ERROR", description="I can't find a command with that name"
            )
            await ctx.send(embed=embed)

        elif ctx.command == command:
            embed = nextcord.Embed(
                title="ERROR", description="You cannot disable this command "
            )
            await ctx.send(embed=embed)

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            embed = nextcord.Embed(title="Toggle", description=ternary)
            await ctx.send(embed=embed)

    @commands.command(aliases=["pong"])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def ping(self, ctx):
        em = nextcord.Embed(title="Pong!🏓", colour=nextcord.Colour.random())
        em.add_field(
            name="My API Latency is:", value=f"{round(self.client.latency*1000)} ms!"
        )
        em.set_footer(
            text=f"Ping requested by {ctx.author}", icon_url=ctx.author.display_avatar
        )
        await ctx.send(embed=em)

    @tasks.loop(seconds=2.0)
    async def clientuptime(self):
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

    @clientuptime.before_loop
    async def before_clientuptime(self):
        print("waiting...")
        await self.client.wait_until_ready()

    @commands.command(aliases=["statistics", "stat", "statistic"])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def stats(self, ctx):
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
            text=f"Stats requested by: {ctx.author}", icon_url=ctx.author.display_avatar
        )
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(util(client))
