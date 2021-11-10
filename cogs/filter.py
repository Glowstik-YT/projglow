import nextcord, re, json, aiosqlite, asyncio
from nextcord.ext import commands,tasks


class FilterCog(commands.Cog, name = "Filter"):
    """Commands for filtering things"""

    def __init__(self, client):
        self.client = client
        self.channel = 794739330835808261 #id of general as i dont have perms to get the id of the log channel
        #self.sync_filter.start()
        
    async def filter_message(self,message):
        async with aiosqlite.connect('filter.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute('SELECT words, ignored, enabled FROM guilds WHERE id = ?',(message.guild.id,))
                data = await cursor.fetchone()
                if data:
                    enabled = data[2]
                    words = None
                    try:
                        words = json.loads(data[0])
                        ignored = json.loads(data[1])
                    except:
                        words = words or []
                        ignored = []
                else:
                    return
        new_message = message.content
        caught = False
        for_roles = False
        for role in message.author.roles:
            if role.id in ignored:
                for_roles = True
                break
        ignore_it = message.channel.id in ignored or message.author.id in ignored or message.channel.category_id in ignored or for_roles
        if enabled and not ignore_it and not message.author.bot:
            for word in words:
                pattern = r'(?i)(\b' + r'+\W*'.join(word) + f'|{word})' if word.isalnum() else word
                if re.search(pattern,message.content):
                    caught = True
                    try:
                        await message.delete()
                    except:
                        pass
                    new_message = re.sub(pattern,r'\*'*(len(word) if not len(word) > 5 else 5),new_message)
            if caught:
                webhooks = await message.channel.webhooks()
                try:
                    webhook = webhooks[0]
                except:
                    try:
                        webhook = await message.channel.create_webhook(name='BobDotBot filter')
                    except:
                        pass
                if webhook:
                    await webhook.send(
                        content=new_message,
                        username=message.author.nick or message.author.name,
                        display_avatar=message.author.display_avatar,
                        allowed_mentions=nextcord.AllowedMentions.none()
                    )
                await asyncio.sleep(1)
                channel = message.channel.id
                guild = message.guild.id
                try:
                    self.client.sniper[guild][channel] = {"author": f"{message.author}", "content": new_message, "avatar": message.author.display_avatar}
                except:
                    self.client.sniper[guild] = {}
                    self.client.sniper[guild][channel] = {"author": f"{message.author}", "content": new_message, "avatar": message.author.display_avatar}


    # LISTENERS #

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect('filter.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute('CREATE TABLE IF NOT EXISTS guilds (id INTEGER, ignored TEXT, words TEXT, enabled BOOL);')
                await connection.commit()

    @commands.Cog.listener()
    async def on_message(self,message):
        await self.filter_message(message)
        
    @commands.Cog.listener()
    async def on_message_edit(self,before,after):
        await self.filter_message(after)

    # COMMANDS #

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def filter(self,ctx):
        """Toggle the word filter. When the filter is on, messages are automatically deleted, and replaced with a filtered webhook message, with the avatar and name set. The bot needs manage message and create webhook permissions for this to work."""
        async with aiosqlite.connect('filter.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute('SELECT enabled FROM guilds WHERE id = ?',(ctx.guild.id,))
                previous = await cursor.fetchone()
                if not previous:
                    await cursor.execute('INSERT INTO guilds (id, ignored, words, enabled) VALUES (?,?,?,?)',(ctx.guild.id,'','',True,))
                    previous = False
                else:
                    previous = previous[0]
                    await cursor.execute('UPDATE guilds SET enabled = ? WHERE id = ?',(not previous,ctx.guild.id,))
                await connection.commit()
        await ctx.send(f'filter status: {not previous}')

    @filter.command()
    @commands.has_permissions(manage_channels=True)
    async def add(self,ctx,word):
        """Add a word to the filter"""
        try:
            await ctx.message.delete()
        except:
            pass
        async with aiosqlite.connect('filter.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute('SELECT words FROM guilds WHERE id = ?',(ctx.guild.id,))
                data = await cursor.fetchone()
                if data:
                    try:
                        words = json.loads(data[0])
                    except:
                        words = []
                    if not word in words:
                        words.append(word)
                        await cursor.execute('UPDATE guilds SET words = ? WHERE id = ?',(json.dumps(words),ctx.guild.id,))
                        await ctx.send("added to filter")
                    else:
                        await ctx.send('That is already in the filter')
                else:
                    await cursor.execute('INSERT INTO guilds (id, ignored, words, enabled) VALUES (?,?,?,?)',(ctx.guild.id,'',json.dumps([word]),False,))
                await connection.commit()

    @filter.command()
    @commands.has_permissions(manage_channels=True)
    async def remove(self,ctx,word):
        """Remove a word from the filter"""
        try:
            await ctx.message.delete()
        except:
            pass
        async with aiosqlite.connect('filter.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute('SELECT words FROM guilds WHERE id = ?',(ctx.guild.id,))
                data = await cursor.fetchone()
                if data:
                    if data[0]:
                        words = json.loads(data[0])
                    else:
                        words = []
                    if word in words:
                        words.remove(word)
                        await cursor.execute('UPDATE guilds SET words = ? WHERE id = ?',(json.dumps(words),ctx.guild.id,))
                        await ctx.send("removed from filter")
                    else:
                        await ctx.send("That isn't in the filter")
                else:
                    await cursor.execute('INSERT INTO guilds (id, ignored, words, enabled) VALUES (?,?,?,?)',(ctx.guild.id,'',json.dumps([word]),False,))
                await connection.commit()
    
    @filter.command(aliases=['list'])
    @commands.has_permissions(manage_channels=True)
    async def words(self,ctx):
        """Get a list of currently filtered words"""
        async with aiosqlite.connect('filter.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute('SELECT words FROM guilds WHERE id = ?',(ctx.guild.id,))
                data = await cursor.fetchone()
        try:
            try:
                data = json.loads(data[0])
            except:
                return await ctx.send("No word filter set")
            if len(data) > 0:
                await ctx.author.send(f"Current word list: `{', '.join(data)}`")
            else:
                await ctx.author.send(f"No words")
            await ctx.send("Check your DMs")
        except:
            await ctx.send("Please open your DMs")

    @filter.command()
    @commands.has_permissions(manage_channels=True)
    async def ignore(self,ctx,object):
        """Ignore a channel, channel category, member, or role. If it is already ignored the bot will stop ignoring it."""
        channel = object
        try:
            channel = await nextcord.ext.commands.MemberConverter().convert(ctx,channel)
        except nextcord.ext.commands.errors.MemberNotFound:
            try:
                channel = await nextcord.ext.commands.TextChannelConverter().convert(ctx,channel)
            except nextcord.ext.commands.errors.ChannelNotFound:
                try:
                    channel = await nextcord.ext.commands.CategoryChannelConverter().convert(ctx,channel)
                except nextcord.ext.commands.errors.ChannelNotFound:
                    try:
                        channel = await nextcord.ext.commands.RoleConverter().convert(ctx,channel)
                    except nextcord.ext.commands.errors.RoleNotFound:
                        return await ctx.send(f'I couldnt find `{text}`')
        
        async with aiosqlite.connect('filter.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute('SELECT ignored FROM guilds WHERE id = ?',(ctx.guild.id,))
                data = await cursor.fetchone()
                if data:
                    if data[0]:
                        channels = json.loads(data[0])
                    else:
                        channels = []
                    embed = nextcord.Embed(title='Filter Ignore')
                    if not channel.id in channels:
                        channels.append(channel.id)
                        embed.description=f"Ok, I will start ignoring {channel.mention}"
                        await ctx.send(embed=embed)
                    else:
                        channels.remove(channel.id)
                        embed.description=f"Ok, I will stop ignoring {channel.mention}"
                        await ctx.send(embed=embed)
                    await cursor.execute('UPDATE guilds SET ignored = ? WHERE id = ?',(json.dumps(channels),ctx.guild.id,))
                    await connection.commit()
                else:
                    await ctx.send("Please enable the filter first!")
                                      
    @filter.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def ignored(self, ctx):
        """List the ignored places in your server"""
        async with aiosqlite.connect('filter.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute('SELECT ignored FROM guilds WHERE id = ?',(ctx.guild.id,))
                data = await cursor.fetchone()
                if data:
                    try:
                        ignored = json.loads(data[0])
                    except:
                        ignored = ['None']
                else:
                    return
                all_ids = ctx.guild.text_channels + ctx.guild.members + ctx.guild.roles + ctx.guild.categories
                embed = nextcord.Embed(title="Ignored",description=' '.join([nextcord.utils.get(all_ids,id=id).mention for id in ignored]) if ignored != 'None' else ignored)
                await ctx.send(embed=embed)

    # LOOPS #

    @tasks.loop(seconds=60)
    async def sync_filter(self):
        with open('filter.json','r') as f:
            data = json.load(f)
        self.filtered_words = data['words']

    # CHECKS #

    async def cog_check(self,ctx):
        return True 

def setup(client):
    client.add_cog(FilterCog(client))
