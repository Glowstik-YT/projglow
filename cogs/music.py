# This Code Is Under The MPL-2.0 License
import nextcord
from nextcord.ext import commands
import random
import asyncio
import DiscordUtils
from difflib import get_close_matches
from global_functions import *
from ..internal.cog import Cog

music = DiscordUtils.Music()


class Music(Cog):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author.id) != str(BOT_USER_ID):
            send = message.channel.send

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is not None:
            return
        elif (
            self.Bot.user in before.channel.members and len(before.channel.members) == 1
        ):
            voice_Bot = before.channel.guild.voice_Bot
            await voice_Bot.disconnect(force=True)

    @commands.command(description="Bot joins your voice channel.")
    async def join(self, Context):
        voice_state = Context.author.voice
        if voice_state is None:
            em1 = nextcord.Embed(
                title="Join Error",
                description="You must be in a voice channel to use this command",
            )
            return await Context.send(embed=em1)
        await Context.author.voice.channel.connect()
        em1 = nextcord.Embed(
            title="Joined Voice!", description="Successfully joined your voice channel"
        )
        return await Context.send(embed=em1)

    @commands.command(description="Bot leaves your voice channel.")
    async def leave(self, Context):
        voice_state = Context.author.voice
        me_voice_state = Context.guild.me.voice
        if voice_state is None:
            em1 = nextcord.Embed(
                title="Leave Error",
                description="You must be in a voice channel to use this command",
            )
            return await Context.send(embed=em1)
        if me_voice_state is None:
            em1 = nextcord.Embed(
                title="Leave Error", description="I am not currently in a voice channel"
            )
            return await Context.send(embed=em1)
        await Context.voice_Bot.disconnect()
        player = music.get_player(guild_id=Context.guild.id)
        try:
            await player.delete()
        except:
            ...
        em1 = nextcord.Embed(
            title="Left Voice!", description="Successfully left your voice channel"
        )
        return await Context.send(embed=em1)

    @commands.command(description="Plays or queues music to the player.")
    async def play(self, Context, *, url):
        voice_state = Context.guild.me.voice
        if voice_state is None:
            await Context.author.voice.channel.connect()
            em1 = nextcord.Embed(
                title="Joined Voice!",
                description="Successfully joined your voice channel",
            )
            await Context.send(embed=em1)
        player = music.get_player(guild_id=Context.guild.id)
        if not player:
            player = music.create_player(Context, ffmpeg_error_betterfix=True)
        if not Context.voice_Bot.is_playing():
            await player.queue(url, search=True)
            song = await player.play()
            em1 = nextcord.Embed(title=f"Playing {song.name}")
            em1.add_field(
                name="Channel", value=f"[**{song.channel}**]({song.channel_url})"
            )
            em1.add_field(name="Views", value=f"{song.views}")
            em1.set_thumbnail(url=song.thumbnail)
            em1.set_footer(text=f"Requested by: {Context.author.name}")
            await Context.send(embed=em1)
        else:
            song = await player.queue(url, search=True)
            em1 = nextcord.Embed(title=f"Queued {song.name}")
            em1.add_field(
                name="Channel", value=f"[**{song.channel}**]({song.channel_url})"
            )
            em1.add_field(name="Views", value=f"{song.views}")
            em1.set_thumbnail(url=song.thumbnail)
            em1.set_footer(text=f"Requested by: {Context.author.name}")
            await Context.send(embed=em1)

    @commands.command(description="Pauses the music.")
    async def pause(self, Context):
        player = music.get_player(guild_id=Context.guild.id)
        song = await player.pause()
        e = nextcord.Embed(title=f"Paused {song.name}")
        await Context.send(embed=e)

    @commands.command(description="Resumes the music.")
    async def resume(self, Context):
        player = music.get_player(guild_id=Context.guild.id)
        song = await player.resume()
        e = nextcord.Embed(title=f"Resumed {song.name}")
        await Context.send(embed=e)

    @commands.command(description="Stops the music.")
    async def stop(self, Context):
        player = music.get_player(guild_id=Context.guild.id)
        await player.stop()
        e = nextcord.Embed(title="Stopped the player.")
        await Context.send(embed=e)

    @commands.command(description="Loops the music.")
    async def loop(self, Context):
        player = music.get_player(guild_id=Context.guild.id)
        song = await player.toggle_song_loop()
        if song.is_looping:
            e = nextcord.Embed(title=f"Enabled loop for {song.name}")
            await Context.send(embed=e)
        else:
            await Context.send(f"Disabled loop for {song.name}")

    @commands.command(description="Sends the current music queue.")
    async def queue(self, Context):
        player = music.get_player(guild_id=Context.guild.id)
        e = nextcord.Embed(
            title=f"`{', '.join([song.name for song in player.current_queue()])}`"
        )
        await Context.send(embed=e)

    @commands.command(description="Shows the song now playing.")
    async def np(self, Context):
        player = music.get_player(guild_id=Context.guild.id)
        song = player.now_playing()
        e = nextcord.Embed(title=f"Now Playing : {song.name}")
        await Context.send(embed=e)

    @commands.command(description="Skips the song")
    async def skip(self, Context):
        player = music.get_player(guild_id=Context.guild.id)
        data = await player.skip(force=True)
        if len(data) == 2:
            await Context.send(f"Skipped from {data[0].name} to {data[1].name}")
        else:
            await Context.send(f"Skipped {data[0].name}")

    @commands.command(description="Sets the volume Limit[1-100]")
    async def volume(self, Context, vol: int):
        if vol > 100:
            em1 = nextcord.Embed(
                title="Volume Error",
                description="Stop trying to go deaf, the volume limit is 100",
            )
            return await Context.send(embed=em1)
        if vol < 1:
            em1 = nextcord.Embed(
                title="Volume Error", description="<:wtfboi:839156996221567027> wh- why"
            )
            return await Context.send(embed=em1)
        player = music.get_player(guild_id=Context.guild.id)
        song, volume = await player.change_volume(vol)
        em1 = nextcord.Embed(
            title="Volume Success",
            description=f"Changed volume for **{song.name}** to **{volume}%**",
        )
        await Context.send(embed=em1)

    @commands.command(description="Removes a song from the queue")
    async def remove(self, Context, index):
        player = music.get_player(guild_id=Context.guild.id)
        song = await player.remove_from_queue(int(index))
        e = nextcord.Embed(title="Removed {song.name} from queue")
        await Context.reply(embed=e)


def setup(Bot):
    Bot.add_cog(Music(Bot))
