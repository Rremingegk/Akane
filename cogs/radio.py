import discord
from discord.ext import commands
from functools import wraps

def exists_check(func):
	@wraps(func)
	async def wrapped(self, *args, **kwargs):
		if not self.player:
			return await self.bot.say("Radio isn't running, start with ~radio start <voice channel>")
		return await func(self, *args, **kwargs)
	return wrapped


class Radio:
	def __init__(self, bot):
		self.bot = bot
		self.player = None

	@commands.group(pass_context=True)
	async def radio(self, ctx):
		""" Commands to start, stop, resume and change volume of the listen.moe radio """
		if ctx.invoked_subcommand is None:
			await self.bot.say('That command does not exist in this group')

	@radio.command(pass_context=True)
	async def start(self, ctx, channel: discord.Channel):
		""" Command to start the listen.moe radio
		**Example**:
		~radio start <channel>
		"""
		voice = await self.bot.join_voice_channel(channel)
		# opus stream http://listen.moe:9999/opus use for better bitrate maybe?
		self.player = voice.create_ffmpeg_player("http://listen.moe:9999/stream", headers={"User-Agent": 'Discord bot Akane'})
		self.player.start()

	@radio.command(pass_context=True)
	@exists_check
	async def pause(self, ctx):
		""" Command to pause the listen.moe radio
		**Example**:
		~radio pause
		"""
		self.player.pause()

	@radio.command(pass_context=True)
	@exists_check
	async def resume(self, ctx):
		""" Command to resume the listen.moe radio
		**Example**:
		~radio resume
		"""
		self.player.resume()


	@radio.command(pass_context=True)
	@exists_check
	async def volume(self, ctx, vol: int):
		""" Command to change the volume of the listen.moe radio
		**Example**:
		~radio volume 50
		"""
		self.player.volume = vol/100

	@radio.command(pass_context=True)
	@exists_check
	async def stop(self, ctx):
		""" Command to stop the listen.moe radio
		**Example**:
		~radio stop
		"""
		voice = self.bot.voice_client_in(ctx.message.server)
		self.player = None
		await voice.disconnect()

	@radio.command(pass_context=True)
	@exists_check
	async def song(self, ctx):
		await self.bot.say("Not added yet.")



def setup(bot):
	bot.add_cog(Radio(bot))