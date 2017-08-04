import discord
from discord.ext import commands
from discord.opus import OpusNotLoaded
from functools import wraps

def exists_check(func):
	@wraps(func)
	async def wrapped(self, ctx, *args):
		if not self.players[ctx.message.server.id]:
			return await self.bot.say("Radio isn't running, start with ~radio start <voice channel>")
		return await func(self, ctx, *args)
	return wrapped


class Radio:
	def __init__(self, bot):
		self.bot = bot
		self.players = {}

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
		voice.encoder_options(sample_rate=48000, channels=2)
		self.players[ctx.message.server.id] = voice.create_ffmpeg_player("http://listen.moe/stream", headers={"User-Agent": 'Discord bot Akane'})
		self.players[ctx.message.server.id].start()

	@radio.command(pass_context=True)
	@exists_check
	async def pause(self, ctx):
		""" Command to pause the listen.moe radio
		**Example**:
		~radio pause
		"""
		self.players[ctx.message.server.id].pause()

	@radio.command(pass_context=True)
	@exists_check
	async def resume(self, ctx):
		""" Command to resume the listen.moe radio
		**Example**:
		~radio resume
		"""
		self.players[ctx.message.server.id].resume()


	@radio.command(pass_context=True)
	@exists_check
	async def volume(self, ctx, vol: int):
		""" Command to change the volume of the listen.moe radio
		**Example**:
		~radio volume 50
		"""
		self.players[ctx.message.server.id].volume = vol/100

	@radio.command(pass_context=True)
	@exists_check
	async def stop(self, ctx):
		""" Command to stop the listen.moe radio
		**Example**:
		~radio stop
		"""
		voice = self.bot.voice_client_in(ctx.message.server)
		self.players[ctx.message.server.id] = None
		await voice.disconnect()

	@radio.command(pass_context=True)
	@exists_check
	async def song(self, ctx):
		await self.bot.say("Not added yet.")



def setup(bot):
	bot.add_cog(Radio(bot))