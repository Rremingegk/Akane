import requests

import discord
from discord.ext import commands

import config

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
		data = {}

		with requests.get(url, params=params) as resp:

			if not resp.json():
				return await ctx.send("Username not found")

			resp = resp.json()[0]
			
			data['pp'] = resp['pp_raw']
			data['name'] = resp['username']
			data['id'] = resp['user_id']
			data['rank'] = resp['pp_rank']
			data['country'] = resp['country']
			data['country_rank'] = resp['pp_country_rank']
		
		await ctx.send(embed=discord.Embed(
			colour=discord.Colour.red(), 
			title=f'{data["name"]}\'s profile',
			description='  '
		 ).set_thumbnail(
		 	url=f'https://a.ppy.sh/{data["id"]}'
		 )
		.add_field(
			name='PP',
			value=f'{data["pp"]}'
		).add_field(
			name='Rank',
			value=f'{data["rank"]}'
		).add_field(
			name='Country',
			value=f'{data["country"]}'
		).add_field(
			name='Country rank',
			value=f'{data["country_rank"]}'
		))

def setup(bot):
	bot.add_cog(Osu(bot))