import discord
from discord.ext import commands
from discord.opus import OpusNotLoaded
from functools import wraps
import asyncio
import websockets
import json

def exists_check(func):
	@wraps(func)
	async def wrapped(self, ctx, *args):
		if not self.players[ctx.message.server.id]:
			return await self.bot.say("Radio isn't running, start with ~radio start <voice channel>")
		return await func(self, ctx, *args)
	return wrapped

json_data = None

async def get_info():
	global json_data
	async with websockets.connect('wss://listen.moe/api/v2/socket') as ws:
		data = await ws.recv()
		json_data = json.loads(data)

class Radio:
	def __init__(self, bot):
		self.bot = bot
		self.players = {}
		#self.loop = asyncio.get_event_loop()

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
		self.players[ctx.message.server.id] = voice.create_ffmpeg_player("http://listen.moe/opus", headers={"User-Agent": 'Discord bot Akane'})
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
		""" Command to show the song currently playing on the listen.moe radio (doesn't work on first try sometimes)
		**Example**:
		~radio stop
		"""
		future = asyncio.run_coroutine_threadsafe(get_info(), self.bot.loop)

		anime_name = 'None' if json_data['anime_name'] is '' else json_data['anime_name']
		
		await self.bot.say(embed=discord.Embed(
			colour=discord.Colour.red(), 
		).add_field(
			name='Song',
			value=json_data['song_name']
		).add_field(
			name='Artist',
			value=json_data['artist_name']
		).add_field(
			name='Anime',
			value=anime_name
		).add_field(
			name='ID',
			value=json_data['song_id']
		))



def setup(bot):
	bot.add_cog(Radio(bot))