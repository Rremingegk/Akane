import requests

import discord
from discord.ext import commands

import config

genres = ['any', 'unspecified', 'video game', 'anime', 'rock', 'pop', 'other', 'novelty', '', 'hip hop', 'electronic']

class Osu:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def hello(self, ctx):
		await ctx.send("Hello, world!")

	@commands.command(pass_context=True)
	async def player(self, ctx):
		name = ctx.message.content.split(" ")[1]
		url = 'https://osu.ppy.sh/api/get_user'
		params = {'k': config.osu_key, 'u': name}
		
		with requests.get(url, params=params) as resp:
			if not resp.json():
				return await ctx.send("Username not found")
			resp = resp.json()[0]

		title = f'{resp["username"]}\'s profile'
		url = f'https://osu.ppy.sh/u/{resp["user_id"]}'
		thumb = f'https://a.ppy.sh/{resp["user_id"]}'
		
		await ctx.send(embed=discord.Embed(
			colour=discord.Colour.red(), 
			title=title,
			url=url
		 ).set_thumbnail(
		 	url=thumb
		 )
		.add_field(
			name='PP',
			value=resp["pp_raw"]
		).add_field(
			name='Rank',
			value=resp["pp_rank"]
		).add_field(
			name='Country',
			value=resp["country"]
		).add_field(
			name='Country rank',
			value=resp["pp_country_rank"]
		))


	@commands.command(pass_context=True)
	async def beatmap(self, ctx):
		name = ctx.message.content.split(" ")[1]
		url = 'https://osu.ppy.sh/api/get_beatmaps'
		params = {'k': config.osu_key, 'b': name}

		with requests.get(url, params=params) as resp:
			if not resp.json():
				return await ctx.send("Beatmap not found")
			resp = resp.json()[0]

		url = f'https://osu.ppy.sh/b/{resp["beatmap_id"]}'
		difficulty = round(float(resp['difficultyrating']), 2)
		status = 'ranked' if int(resp['approved']) == 1 else 'not ranked'
		length = str(int(resp['total_length']) / 60)
		genre = genres[int(resp['genre_id'])]

		await ctx.send(embed=discord.Embed(
			url=url,
			colour=discord.Colour.red(), 
			title=resp["title"]
		 ).add_field(
			name='Difficulty',
			value=difficulty
		).add_field(
			name='BPM',
			value=resp["bpm"]
		).add_field(
			name='Length',
			value=f'{length} minutes'
		).add_field(
			name='Status',
			value=status
		).add_field(
			name='Genre',
			value=genre
		).add_field(
			name='Creator',
			value=resp["creator"]
		))

def setup(bot):
	bot.add_cog(Osu(bot))