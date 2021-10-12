import nextcord
from nextcord.ext import commands
from global_functions import ban_msg, kick_msg, BOT_USER_ID
import random
import asyncio
from difflib import get_close_matches


class BanConfirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(
        label="Confirm", style=nextcord.ButtonStyle.green, custom_id="yes"
    )
    async def confirm(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        self.value = True
        self.stop()

    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.red, custom_id="no")
    async def cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        self.value = False
        self.stop()


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author.id) != str(BOT_USER_ID):
            send = message.channel.send

    @commands.command(name="ban", description="Bans the member from your server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: nextcord.Member = None, *, reason=None):
        if member == None:
            embed1 = nextcord.Embed(
                title="Ban Error", description="Member to ban - Not Found"
            )
            return await ctx.send(embed=embed1)
        if member.id == ctx.author.id:
            embed69 = nextcord.Embed(
                title="Ban Error",
                description="Can not ban yourself, trust me I woulda ages ago <:hehe:796743161208504320>",
            )
            return await ctx.send(embed=embed69)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Ban Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em3 = nextcord.Embed(
                title="Ban Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        guild = ctx.guild
        banMsg = random.choice(ban_msg)
        banEmbed = nextcord.Embed(
            title="Ban Success", description=f"{member.mention} {banMsg}"
        )
        banEmbed.add_field(name="Reason", value=reason)
        await ctx.send(embed=banEmbed)
        await member.send(f"You got banned in **{guild}** | Reason: **{reason}**")
        await member.ban(reason=reason)

    @commands.command(description="Unbans a member from your server by ID")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):
        user = await self.client.fetch_user(id)
        await ctx.guild.unban(user)
        em = nextcord.Embed(title="Unban Success", description="Unbanned user :D")
        await ctx.send(embed=em)

    @commands.command(name="kick", description="Kicks the member from your server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: nextcord.Member = None, *, reason=None):
        if member == None:
            embed1 = nextcord.Embed(
                title="Kick Error", description="Member to kick - Not Found"
            )
            return await ctx.send(embed=embed1)
        if not (ctx.guild.me.guild_permissions.kick_members):
            embed2 = nextcord.Embed(
                title="Kick Error",
                description="I require the ``Kick Members`` permisson to run this command - Missing Permission",
            )
            return await ctx.send(embed=embed2)
        if member.id == ctx.author.id:
            embed69 = nextcord.Embed(
                title="Kick Error",
                description="You sadly can not kick your self <a:sadboi:795385450978213938>",
            )
            return await ctx.send(embed=embed69)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Kick Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em3 = nextcord.Embed(
                title="Kick Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        guild = ctx.guild
        kickMsg = random.choice(kick_msg)
        kickEmbed = nextcord.Embed(
            title="Kick Success", description=f"{member.mention} {kickMsg}"
        )
        kickEmbed.add_field(name="Reason", value=reason)
        await ctx.send(embed=kickEmbed)
        await member.send(f"You got kicked in **{guild}** | Reason: **{reason}**")
        await member.kick(reason=reason)

    @commands.command(name="tempmute", description="Mutes a member indefinitely.")
    @commands.has_permissions(manage_messages=True)
    async def tempmute(
        self, ctx, member: nextcord.Member = None, time=None, *, reason=None
    ):
        guild = ctx.guild
        if member == None:
            em1 = nextcord.Embed(
                title="Tempmute Error", description="Member to mute - Not Found"
            )
            return await ctx.send(embed=em1)
        elif member.id == ctx.author.id:
            em5 = nextcord.Embed(
                title="Tempmute Error", description="Don't bother, ive tried"
            )
            return await ctx.send(embed=em5)
        if time == None:
            em2 = nextcord.Embed(
                title="Tempmute Error", description="Time to mute - Not Found"
            )
            return await ctx.send(embed=em2)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Tempmute Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        if not (ctx.guild.me.guild_permissions.manage_roles):
            embed2 = nextcord.Embed(
                title="Tempmute Error",
                description="I require the ``Manage Roles`` permisson to run this command - Missing Permission",
            )
            return await ctx.send(embed=embed2)
        elif ctx.author.top_role.position == member.top_role.position:
            em4 = nextcord.Embed(
                title="Tempmute Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em4)
        mutedRole = nextcord.utils.get(guild.roles, name="Muted")
        if ctx.guild.me.top_role.position < mutedRole.position:
            em3 = nextcord.Embed(
                title="Tempmute Error",
                description="Muted role too high to give to a member",
            )
            return await ctx.send(embed=em3)
        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            await ctx.send("No mute role found. Creating mute role...")
            for channel in guild.channels:
                await channel.set_permissions(
                    mutedRole,
                    speak=False,
                    send_messages=False,
                    read_message_history=True,
                )

        if not time == None:
            time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
            tempmute = int(time[0]) * time_convert[time[-1]]
            embed = nextcord.Embed(
                title="Tempmute Success",
                description=f"{member.mention} was muted ",
                colour=nextcord.Colour.blue(),
            )
            embed.add_field(name="Reason:", value=reason, inline=False)
            embed.add_field(name="Duration", value=time)
            await ctx.send(embed=embed)
            await member.add_roles(mutedRole, reason=reason)
            await member.send(
                f"You have been muted from: **{guild.name}** | Reason: **{reason}** | Time: **{time}**"
            )
            if not time == None:
                await asyncio.sleep(tempmute)
                await member.remove_roles(mutedRole)
                await member.send(f"You have been unmuted from **{guild}**")
            return

    @commands.command(
        name="mute", description="Mutes a member for a specific amount of time."
    )
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: nextcord.Member = None, *, reason=None):
        guild = ctx.guild
        if member == None:
            em1 = nextcord.Embed(
                title="Mute Error", description="Member to mute - Not Found"
            )
            return await ctx.send(embed=em1)
        elif member.id == ctx.author.id:
            em5 = nextcord.Embed(
                title="Mute Error", description="Don't bother, ive tried"
            )
            return await ctx.send(embed=em5)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Mute Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em4 = nextcord.Embed(
                title="Mute Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em4)
        if not (ctx.guild.me.guild_permissions.manage_roles):
            embed2 = nextcord.Embed(
                title="Mute Error",
                description="I require the ``Manage Roles`` permisson to run this command - Missing Permission",
            )
            return await ctx.send(embed=embed2)
        mutedRole = nextcord.utils.get(guild.roles, name="Muted")
        if ctx.guild.me.top_role.position < mutedRole.position:
            em3 = nextcord.Embed(
                title="Mute Error",
                description="Muted role too high to give to a member",
            )
            return await ctx.send(embed=em3)
        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            await ctx.send("No mute role found. Creating mute role...")
            for channel in guild.channels:
                await channel.set_permissions(
                    mutedRole,
                    speak=False,
                    send_messages=False,
                    read_message_history=True,
                )

        embed = nextcord.Embed(
            title="Mute Success",
            description=f"{member.mention} was muted ",
            colour=nextcord.Colour.blue(),
        )
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(
            f"You have been muted from: **{guild.name}** | Reason: **{reason}**"
        )
        return

    @commands.command(name="unmute", description="Unmutes a muted member.")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: nextcord.Member = None, *, reason=None):
        guild = ctx.guild
        if member == None:
            em1 = nextcord.Embed(
                title="Unmute Error", description="Member to unmute - Not Found"
            )
            return await ctx.send(embed=em1)
        elif member.id == ctx.author.id:
            em5 = nextcord.Embed(
                title="Unmute Error", description="wHat? <:WHA:815331017854025790>"
            )
            return await ctx.send(embed=em5)
        elif ctx.author.top_role.position < member.top_role.position:
            em3 = nextcord.Embed(
                title="Unmute Error",
                description="Member **higher** than you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em3)
        elif ctx.author.top_role.position == member.top_role.position:
            em4 = nextcord.Embed(
                title="Unmute Error",
                description="Member has same role as you in the role heirarchy - Invalid Permission",
            )
            return await ctx.send(embed=em4)
        if not (ctx.guild.me.guild_permissions.manage_roles):
            embed2 = nextcord.Embed(
                title="Unmute Error",
                description="I require the ``Manage Roles`` permisson to run this command - Missing Permission",
            )
            return await ctx.send(embed=embed2)
        mutedRole = nextcord.utils.get(guild.roles, name="Muted")
        if ctx.guild.me.top_role.position < mutedRole.position:
            em3 = nextcord.Embed(
                title="Unmute Error",
                description="Muted role too high to remove from a member",
            )
            return await ctx.send(embed=em3)
        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            await ctx.send("No mute role found. Creating mute role...")
            for channel in guild.channels:
                await channel.set_permissions(
                    mutedRole,
                    speak=False,
                    send_messages=False,
                    read_message_history=True,
                )

        embed = nextcord.Embed(
            title="Unmute Success",
            description=f"{member.mention} was unmuted ",
            colour=nextcord.Colour.blue(),
        )
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.remove_roles(mutedRole, reason=reason)
        await member.send(
            f"You have been unmuted from: **{guild.name}** | Reason: **{reason}**"
        )
        return

    @commands.command(description="Clears a bundle of messages.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        amount = amount + 1
        if amount > 101:
            em1 = nextcord.Embed(
                title="Clear Error",
                description="Purge limit exedeed - Greater than 100",
            )
            return await ctx.send(embed=em1)
        else:
            await ctx.channel.purge(limit=amount)
            msg = await ctx.send("Cleared Messages")
            asyncio.sleep(10)
            await msg.delete()

    @commands.command(description="Change the channels slowmode.")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, time: int):
        try:
            if time == 0:
                em1 = nextcord.Embed(
                    title="Slowmode Success", description="Slowmode turned off"
                )
                await ctx.send(embed=em1)
                await ctx.channel.edit(slowmode_delay=0)
            elif time > 21600:
                em2 = nextcord.Embed(
                    title="Slowmode Error", description="Slowmode over 6 hours"
                )
                await ctx.send(embed=em2)
            else:
                await ctx.channel.edit(slowmode_delay=time)
                em3 = nextcord.Embed(
                    title="Slowmode Success",
                    description=f"Slowmode set to {time} seconds",
                )
                await ctx.send(embed=em3)
        except Exception:
            await ctx.send("Error has occoured, notifying dev team")
            print(Exception)

    @commands.command(
        aliases=["giverole", "addr"], description="Gives a member a certain role."
    )
    @commands.has_permissions(manage_roles=True)
    async def addrole(
        self, ctx, member: nextcord.Member = None, *, role: nextcord.Role = None
    ):
        if member is None:
            embed = nextcord.Embed(
                title="Add Role Error",
                description="Please ping a user to give them a role!",
            )
            await ctx.send(embed=embed)
            return
        if role is None:
            embed = nextcord.Embed(
                title="Add Role Error",
                description="Please ping a role to give {} that role!".format(
                    member.mention
                ),
            )
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < role.position:
            em = nextcord.Embed(
                title="Add Role Error",
                description="You do not have enough permissions to give this role",
            )
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position < role.position:
            embed = nextcord.Embed(
                title="Add Role Error",
                description="That role is too high for me to perform this action",
            )
            return await ctx.send(embed=embed)
        try:
            addRole = True
            for role_ in member.roles:
                if role_ == role:
                    addRole = False
                    break
            if not addRole:
                embed = nextcord.Embed(
                    title="Add Role Error",
                    description=f"{member.mention} already has the role you are trying to give",
                )
                await ctx.send(embed=embed)
                return
            else:
                em = nextcord.Embed(
                    title="Add Role Success",
                    description=f"{role.mention} has been assigned to {member.mention}",
                )
                await ctx.send(embed=em)
                await member.add_roles(role)
                return
        except Exception:
            print(Exception)

    @commands.command(
        aliases=["takerole", "remover"],
        description="Removes a certain role from a member.",
    )
    @commands.has_permissions(manage_roles=True)
    async def removerole(
        self,
        ctx,
        member: nextcord.Member = None,
        role: nextcord.Role = None,
        *,
        reason=None,
    ):
        if member is None:
            embed = nextcord.Embed(
                title="Remove Role Error",
                description="Please ping a user to remove a role from them!",
            )
            await ctx.send(embed=embed)
            return
        if role is None:
            embed = nextcord.Embed(
                title="Remove Role Error",
                description="Please ping a role to remove the role from {}!".format(
                    member.mention
                ),
            )
            await ctx.send(embed=embed)
            return
        if ctx.author.top_role.position < role.position:
            em = nextcord.Embed(
                title="Remove Role Error",
                description="You do not have enough permissions to remove this role",
            )
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position < role.position:
            embed = nextcord.Embed(
                title="Remove Role Error",
                description="That role is too high for me to perform this action",
            )
            return await ctx.send(embed=embed)
        try:
            roleRemoved = False
            for role_ in member.roles:
                if role_ == role:
                    await member.remove_roles(role)
                    roleRemoved = True
                    break
            if not roleRemoved:
                embed = nextcord.Embed(
                    title="Remove Role Error",
                    description=f"{member.mention} already has the role you are trying to give",
                )
                await ctx.send(embed=embed)
                return
            else:
                em = nextcord.Embed(
                    title="Remove Role Success!",
                    description=f"{role.mention} has been removed from {member.mention}",
                )
                await ctx.send(embed=em)
                return
        except Exception:
            print(Exception)

    @commands.command(description="Locks the channel.")
    @commands.has_permissions(kick_members=True)
    async def lock(self, ctx, channel: nextcord.TextChannel = None):
        if channel is None:
            channel = ctx.message.channel
        await channel.set_permissions(
            ctx.guild.default_role,
            reason=f"{ctx.author.name} locked {channel.name}",
            send_messages=False,
        )
        embed = nextcord.Embed(
            title="Lockdown Success",
            description=f"Locked {channel.mention} <:saluteboi:897263732948885574>",
        )
        await ctx.send(embed=embed)

    @commands.command(description="Unlocks the channel.")
    @commands.has_permissions(kick_members=True)
    async def unlock(self, ctx, channel: nextcord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(
            ctx.guild.default_role,
            reason=f"{ctx.author.name} unlocked {channel.name}",
            send_messages=True,
        )
        embed = nextcord.Embed(
            title="Unlock Success",
            description=f"Unlocked {channel.mention} <:happyboi:804920510508433428>",
        )
        await ctx.send(embed=embed)

    @commands.command(description="Modbans the member.")
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 21600, commands.BucketType.user)
    async def modban(self, ctx, member, *, reason=None):
        if reason is None:
            reason = f"{ctx.author.name} modbanned {member.name}"
        else:
            reason = (
                f"{ctx.author.name} modbanned {member.name} for the reason of {reason}"
            )
        if member == None:
            embed1 = nextcord.Embed(
                title="Ban Error", description="Member to ban - Not Found"
            )
            return await ctx.send(embed=embed1)
        if member.id == ctx.author.id:
            embed69 = nextcord.Embed(
                title="Ban Error",
                description="Can not ban yourself, trust me I woulda ages ago <:hehe:796743161208504320>",
            )
            return await ctx.send(embed=embed69)
        em = nextcord.Embed(
            title="Are you sure?",
            description="This is a very risky command only to be used in important situations such as, `NSFW or NSFLPosting` or `Raid on the Server`. Only use this command if no admin is online or responding. **If this command is used for the wrong purpose you may risk getting demoted if not banned from the staff team.**",
        )
        view = BanConfirm()
        await ctx.author.send(embed=em, view=view)
        await view.wait()
        if view.value is None:
            await ctx.author.send("Command has been Timed Out, please try again.")
        elif view.value:
            guild = ctx.guild
            banMsg = random.choice(ban_msg)
            banEmbed = nextcord.Embed(
                title="Ban Success", description=f"{member.mention} {banMsg}"
            )
            banEmbed.add_field(name="Reason", value=reason)
            await ctx.author.send(embed=banEmbed)
            await member.ban(reason=reason)
            await member.send(f"You got banned in **{guild}** | Reason: **{reason}**")
        else:
            banEmbed = nextcord.Embed(
                title="Ban Cancelled",
                description="Lets pretend like this never happened them :I",
            )
            await ctx.author.send(embed=banEmbed)


def setup(client):
    client.add_cog(Moderation(client))
