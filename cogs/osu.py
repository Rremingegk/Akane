import requests

import discord
from discord.ext import commands

import config

genres = ['any', 'unspecified', 'video game', 'anime', 'rock', 'pop', 'other', 'novelty', '', 'hip hop', 'electronic']

class Osu:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True)
	async def osu(self, ctx):
		""" Osu related commands """
		if ctx.invoked_subcommand is None:
			await self.bot.say('commands available to osu!: \n ~osu player & ~osu beatmap')

	@osu.command(pass_context=True)
	async def player(self, ctx, name: str):
		""" Find osu! player by given name
		
		**Example**:
		~osu player Cookiezi
		
		"""
		url = 'https://osu.ppy.sh/api/get_user'
		params = {'k': config.osu_key, 'u': name}
		
		with requests.get(url, params=params) as resp:
			if not resp.json():
				return await self.bot.say("Username not found")
			resp = resp.json()[0]

		title = f'{resp["username"]}\'s profile'
		url = f'https://osu.ppy.sh/u/{resp["user_id"]}'
		thumb = f'https://a.ppy.sh/{resp["user_id"]}'
		
		await self.bot.say(embed=discord.Embed(
			colour=discord.Colour.red(), 
			url=url
		 ).set_thumbnail(
		 	url=thumb
		 ).set_author(
		 	name=title,
		 	icon_url='https://i.ppy.sh/528affadbdddcabaa861973fc5aa6ecdd9beb7ee/687474703a2f2f692e696d6775722e636f6d2f50553876382e706e67'
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


	@osu.command(pass_context=True)
	async def beatmap(self, ctx, name: str):
		""" Find osu! beatmap by given id
		
		**Example**:
		~osu beatmap 1266886
		
		"""
		url = 'https://osu.ppy.sh/api/get_beatmaps'
		params = {'k': config.osu_key, 'b': name}

		with requests.get(url, params=params) as resp:
			if not resp.json():
				return await self.bot.say("Beatmap not found")
			resp = resp.json()[0]

		url = f'https://osu.ppy.sh/b/{resp["beatmap_id"]}'
		difficulty = round(float(resp['difficultyrating']), 2)
		status = 'ranked' if int(resp['approved']) == 1 else 'not ranked'
		length = str(round(int(resp['total_length']) / 60, 2))
		genre = genres[int(resp['genre_id'])]

		await self.bot.say(embed=discord.Embed(
			url=url,
			colour=discord.Colour.red(), 
		 ).set_author(
		 	name=resp["title"],
		 	icon_url='https://i.ppy.sh/528affadbdddcabaa861973fc5aa6ecdd9beb7ee/687474703a2f2f692e696d6775722e636f6d2f50553876382e706e67'
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

	@osu.command(pass_context=True)
	async def beatmapset(self, ctx, name: str):
		""" Find osu! beatmapset by given id
		
		**Example**:
		~osu beatmapset 599457
		
		"""
		url = 'https://osu.ppy.sh/api/get_beatmaps'
		params = {'k': config.osu_key, 's': name}

		with requests.get(url, params=params) as resp:
			if not resp.json():
				return await self.bot.say("Beatmap not found")
			resp = resp.json()

		url = f'https://osu.ppy.sh/s/{resp[0]["beatmapset_id"]}'

		embed = discord.Embed(
			colour=discord.Colour.red(),
			url=url,
		).set_author(
			name=resp[0]['title'],
			icon_url='https://i.ppy.sh/528affadbdddcabaa861973fc5aa6ecdd9beb7ee/687474703a2f2f692e696d6775722e636f6d2f50553876382e706e67'
		).set_footer(
			text='acces these beatmaps individually with ~osu beatmap <id>'
		)

		resp = sorted(resp, key=lambda x: x['difficultyrating'])

		for item in resp:
			beatmap_id = f'[{item["beatmap_id"]}](https://osu.ppy.sh/b/{item["beatmap_id"]})'
			difficulty = round(float(item['difficultyrating']), 2)
			version = item['version']
			embed.add_field(
				name='ID',
				value=beatmap_id
			).add_field(
				name='Difficulty',
				value=difficulty
			).add_field(
				name='Version',
				value=version
			)

		embed.add_field(
			name='\u200b',
			value=f'[Download](https://osu.ppy.sh/d/{resp[0]["beatmapset_id"]})'
		)

		await self.bot.say(embed=embed)

def setup(bot):
	bot.add_cog(Osu(bot))