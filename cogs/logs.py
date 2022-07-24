import nextcord
from nextcord.ext import commands
import aiosqlite
import asyncio
from datetime import datetime

class Logs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Online!")
        setattr(self.client, "db", await aiosqlite.connect("main.db"))
        await asyncio.sleep(1)
        async with self.client.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS logging (channel INTEGER, guild INTEGER)")
        await self.client.db.commit()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild = message.guild
        async with self.client.db.cursor() as cursor:
            await cursor.execute("SELECT channel FROM logging WHERE guild = ?", (guild.id,))
            channel = await cursor.fetchone()
            msgDelete = self.client.get_channel(channel[0])
            embed = nextcord.Embed(title = f"{message.author}'s Message was Deleted", description = f"Deleted Message: {message.content}\nAuthor: {message.author.mention}", timestamp = datetime.now(), color = nextcord.Colour.red())
            embed.set_author(name = message.author.name, icon_url = message.author.display_avatar)
            embed.set_footer(text=str(message.author.id))
            await msgDelete.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        guild = before.guild
        async with self.client.db.cursor() as cursor:
            await cursor.execute("SELECT channel FROM logging WHERE guild = ?", (guild.id,))
            channel = await cursor.fetchone()
            msgEdit = self.client.get_channel(channel[0])
            embed = nextcord.Embed(title = f"{before.author} Edited Their Message", description = f"Before: {before.content}\nAfter: {after.content}\nAuthor: {before.author.mention}\n", timestamp = datetime.now(), color = nextcord.Colour.blue())
            embed.set_author(name = after.author.name, icon_url = after.author.display_avatar)
            embed.set_footer(text=str(before.author.id))
            await msgEdit.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        guild = before.guild
        async with self.client.db.cursor() as cursor:
            await cursor.execute("SELECT channel FROM logging WHERE guild = ?", (guild.id,))
            channel = await cursor.fetchone()
            memUpdate = self.client.get_channel(channel[0])
            if len(before.roles) > len(after.roles):
                role = next(role for role in before.roles if role not in after.roles)
                embed = nextcord.Embed(title = f"{before}'s Role has Been Removed", description = f"{role.mention} was removed from {before.mention}.",  timestamp = datetime.now(), color = nextcord.Colour.red())
            elif len(after.roles) > len(before.roles):
                role = next(role for role in after.roles if role not in before.roles)
                embed = nextcord.Embed(title = f"{before} Got a New Role", description = f"{role.mention} was added to {before.mention}.",  timestamp = datetime.now(), color = nextcord.Colour.green())
            elif before.nick != after.nick:
                embed = nextcord.Embed(title = f"{before}'s Nickname Changed", description = f"Before: {before.nick}\nAfter: {after.nick}",  timestamp = datetime.now(), color = nextcord.Colour.blue())
            else:
                return
            embed.set_author(name = after.name, icon_url = after.display_avatar)
            await memUpdate.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        async with self.client.db.cursor() as cursor:
            await cursor.execute("SELECT channel FROM logging WHERE guild = ?", (guild.id,))
            channelID = await cursor.fetchone()
            chanCreate = self.client.get_channel(channelID[0])
            embed = nextcord.Embed(title = f"{channel.name} was Created", description = channel.mention, timestamp = datetime.now(), color = nextcord.Colour.green())
            await chanCreate.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild = channel.guild
        async with self.client.db.cursor() as cursor:
            await cursor.execute("SELECT channel FROM logging WHERE guild = ?", (guild.id,))
            channelID = await cursor.fetchone()
            chanDelete = self.client.get_channel(channelID[0])
            embed = nextcord.Embed(title = f"{channel.name} was Deleted", timestamp = datetime.now(), color = nextcord.Colour.red())
            await chanDelete.send(embed=embed)

    @commands.group()
    async def logs(ctx):
        return

    @logs.command()
    @commands.has_permissions(manage_guild=True)
    async def channel(self, ctx, channel: nextcord.TextChannel):
        async with self.client.db.cursor() as cursor:
            await cursor.execute("SELECT channel FROM logging WHERE guild = ?", (ctx.guild.id,))
            channelData = await cursor.fetchone()
            if channelData:
                channelData = channelData[0]
                if channelData == channel.id:
                    return await ctx.send("That's the same channel bro.")
                await cursor.execute("UPDATE logging SET channel = ? WHERE guild = ?", (channel.id, ctx.guild.id,))
                await ctx.send(f"{channel.mention} is now the logging channel.")
            else:
                await cursor.execute("INSERT INTO logging VALUES (?, ?)", (channel.id, ctx.guild.id,))
                await ctx.send(f"{channel.mention} is now the logging channel.")
        await self.client.db.commit()

def setup(client):
    client.add_cog(Logs(client))