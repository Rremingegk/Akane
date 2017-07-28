import discord
from discord.ext import commands

class Radio:
	def __init__(self, bot):
		self.bot = bot
		self.player = None
		#self.volume = 100

	@commands.group(pass_context=True)
	async def radio(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send('commands available to radio: \n ~reddit pic &')

	@radio.command(pass_context=True)
	async def start(self, ctx, channel: discord.Channel):
		""" Command to start the listen.moe radio
		**Example**:
		~radio start <channel>
		"""
		voice = await self.bot.join_voice_channel(channel)
		self.player = voice.create_ffmpeg_player("http://listen.moe:9999/stream", headers={"User-Agent": 'No user-agent yet.'})
		self.player.start()

	@radio.command(pass_context=True)
	async def pause(self, ctx):
		self.player.pause()


	@radio.command(pass_context=True)
	async def resume(self, ctx):
		self.player.resume()


	@radio.command(pass_context=True)
	async def volume(self, ctx, vol: int = 100):
		self.player.volume = vol/100

	@radio.command(pass_context=True)
	async def stop(self, ctx):
		voice = self.bot.voice_client_in(ctx.message.server)
		await voice.disconnect()


def setup(bot):
	bot.add_cog(Radio(bot))