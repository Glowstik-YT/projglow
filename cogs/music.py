# This Code Is Under The MPL-2.0 License

import nextcord
from nextcord.ext import commands
import random
import asyncio
import DiscordUtils
from difflib import get_close_matches
from global_functions import *

music = DiscordUtils.Music()


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author.id) != str(BOT_USER_ID):
            send = message.channel.send

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is not None:
            return
        elif (
            self.client.user in before.channel.members
            and len(before.channel.members) == 1
        ):
            voice_client = before.channel.guild.voice_client
            await voice_client.disconnect(force=True)

    @commands.command(description="Bot joins your voice channel.")
    async def join(self, ctx):
        voice_state = ctx.author.voice
        if voice_state is None:
            em1 = nextcord.Embed(
                title="Join Error",
                description="You must be in a voice channel to use this command",
            )
            return await ctx.send(embed=em1)
        await ctx.author.voice.channel.connect()
        em1 = nextcord.Embed(
            title="Joined Voice!", description="Successfully joined your voice channel"
        )
        return await ctx.send(embed=em1)

    @commands.command(description="Bot leaves your voice channel.")
    async def leave(self, ctx):
        voice_state = ctx.author.voice
        me_voice_state = ctx.guild.me.voice
        if voice_state is None:
            em1 = nextcord.Embed(
                title="Leave Error",
                description="You must be in a voice channel to use this command",
            )
            return await ctx.send(embed=em1)
        if me_voice_state is None:
            em1 = nextcord.Embed(
                title="Leave Error", description="I am not currently in a voice channel"
            )
            return await ctx.send(embed=em1)
        await ctx.voice_client.disconnect()
        player = music.get_player(guild_id=ctx.guild.id)
        try:
            await player.delete()
        except:
            ...
        em1 = nextcord.Embed(
            title="Left Voice!", description="Successfully left your voice channel"
        )
        return await ctx.send(embed=em1)

    @commands.command(description="Plays or queues music to the player.")
    async def play(self, ctx, *, url):
        voice_state = ctx.guild.me.voice
        if voice_state is None:
            await ctx.author.voice.channel.connect()
            em1 = nextcord.Embed(
                title="Joined Voice!",
                description="Successfully joined your voice channel",
            )
            await ctx.send(embed=em1)
        player = music.get_player(guild_id=ctx.guild.id)
        if not player:
            player = music.create_player(ctx, ffmpeg_error_betterfix=True)
        if not ctx.voice_client.is_playing():
            await player.queue(url, search=True)
            song = await player.play()
            em1 = nextcord.Embed(title=f"Playing {song.name}")
            em1.add_field(
                name="Channel", value=f"[**{song.channel}**]({song.channel_url})"
            )
            em1.add_field(name="Views", value=f"{song.views}")
            em1.set_thumbnail(url=song.thumbnail)
            em1.set_footer(text=f"Requested by: {ctx.author.name}")
            await ctx.send(embed=em1)
        else:
            song = await player.queue(url, search=True)
            em1 = nextcord.Embed(title=f"Queued {song.name}")
            em1.add_field(
                name="Channel", value=f"[**{song.channel}**]({song.channel_url})"
            )
            em1.add_field(name="Views", value=f"{song.views}")
            em1.set_thumbnail(url=song.thumbnail)
            em1.set_footer(text=f"Requested by: {ctx.author.name}")
            await ctx.send(embed=em1)

    @commands.command(description="Pauses the music.")
    async def pause(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.pause()
        e = nextcord.Embed(title=f"Paused {song.name}")
        await ctx.send(embed=e)

    @commands.command(description="Resumes the music.")
    async def resume(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.resume()
        e = nextcord.Embed(title=f"Resumed {song.name}")
        await ctx.send(embed=e)

    @commands.command(description="Stops the music.")
    async def stop(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        await player.stop()
        e = nextcord.Embed(title="Stopped the player.")
        await ctx.send(embed=e)

    @commands.command(description="Loops the music.")
    async def loop(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.toggle_song_loop()
        if song.is_looping:
            e = nextcord.Embed(title=f"Enabled loop for {song.name}")
            await ctx.send(embed=e)
        else:
            await ctx.send(f"Disabled loop for {song.name}")

    @commands.command(description="Sends the current music queue.")
    async def queue(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        e = nextcord.Embed(
            title=f"`{', '.join([song.name for song in player.current_queue()])}`"
        )
        await ctx.send(embed=e)

    @commands.command(description="Shows the song now playing.")
    async def np(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        song = player.now_playing()
        e = nextcord.Embed(title=f"Now Playing : {song.name}")
        await ctx.send(embed=e)

    @commands.command(description="Skips the song")
    async def skip(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        data = await player.skip(force=True)
        if len(data) == 2:
            await ctx.send(f"Skipped from {data[0].name} to {data[1].name}")
        else:
            await ctx.send(f"Skipped {data[0].name}")

    @commands.command(description="Sets the volume Limit[1-100]")
    async def volume(self, ctx, vol: int):
        if vol > 100:
            em1 = nextcord.Embed(
                title="Volume Error",
                description="Stop trying to go deaf, the volume limit is 100",
            )
            return await ctx.send(embed=em1)
        if vol < 1:
            em1 = nextcord.Embed(
                title="Volume Error", description="<:wtfboi:839156996221567027> wh- why"
            )
            return await ctx.send(embed=em1)
        player = music.get_player(guild_id=ctx.guild.id)
        song, volume = await player.change_volume(vol)
        em1 = nextcord.Embed(
            title="Volume Success",
            description=f"Changed volume for **{song.name}** to **{volume}%**",
        )
        await ctx.send(embed=em1)

    @commands.command(description="Removes a song from the queue")
    async def remove(self, ctx, index):
        player = music.get_player(guild_id=ctx.guild.id)
        song = await player.remove_from_queue(int(index))
        e = nextcord.Embed(title="Removed {song.name} from queue")
        await ctx.reply(embed=e)


def setup(client):
    client.add_cog(Music(client))
