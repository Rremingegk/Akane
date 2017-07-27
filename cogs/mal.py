import requests

import discord
from discord.ext import commands

from lxml import objectify
import html
import re

import config

class Mal:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def anime(self, ctx):
		""" Find anime on MyAnimeList by given name
		
		**Example**:
		~anime Toradora!
		
		"""
		name = ctx.message.content.split(" ")[1:]
		if not name:
			return await ctx.send("No anime specified")
		name = "+".join(name)
		url = f'https://myanimelist.net/api/anime/search.xml?q={name}'
		
		r = requests.get(url, auth=(config.mal_username, config.mal_password))
		if not r.content:
			return await ctx.send("Anime not found")
		xml_obj = objectify.fromstring(r.content)
		anime = xml_obj.entry[0] 

		synopsis = html.unescape(anime.synopsis.pyval)
		synopsis = re.sub(r'<.*?>', '', synopsis)
		synopsis = synopsis.replace('[Written by MAL Rewrite]', '')
		synopsis = synopsis[0:425] + '...'
		url = f'https://myanimelist.net/anime/{anime.id.pyval}'
		
		await ctx.send(embed=discord.Embed(
			colour=discord.Colour.red(), 
			url=url
		).set_thumbnail(
		 	url=anime.image.pyval
		).set_author(
			name=anime.title.pyval,
			icon_url=anime.image.pyval
		).add_field(
			name='Score',
			value=anime.score.pyval
		).add_field(
			name='Episodes',
			value=anime.episodes.pyval
		).add_field(
			name='Status',
			value=anime.status.pyval
		).add_field(
			name='Type',
			value=anime.type.pyval
		).add_field(
			name="Description",
			value=synopsis
		))

	@commands.command(pass_context=True)
	async def manga(self, ctx):
		""" Find manga on MyAnimeList by given name
		
		**Example**:
		~manga Sakurasou no pet na Kanojo
		
		"""
		name = ctx.message.content.split(" ")[1:]
		if not name:
			return await ctx.send("No manga specified")
		name = "+".join(name)
		url = f'https://myanimelist.net/api/manga/search.xml?q={name}'
		
		r = requests.get(url, auth=(config.mal_username, config.mal_password))
		if not r.content:
			return await ctx.send("Manga not found")
		xml_obj = objectify.fromstring(r.content)
		manga = xml_obj.entry[0] 

		synopsis = html.unescape(manga.synopsis.pyval)
		synopsis = re.sub(r'<.*?>', '', synopsis)
		synopsis = synopsis.replace('[Written by MAL Rewrite]', '')
		synopsis = synopsis[0:425] + '...'
		url = f'https://myanimelist.net/anime/{manga.id.pyval}'
		
		await ctx.send(embed=discord.Embed(
			colour=discord.Colour.red(), 
			url=url
		).set_thumbnail(
		 	url=manga.image.pyval
		).set_author(
			name=manga.title.pyval,
			icon_url=manga.image.pyval
		).add_field(
			name='Score',
			value=manga.score.pyval
		).add_field(
			name='Chapters',
			value=manga.chapters.pyval
		).add_field(
			name='Status',
			value=manga.status.pyval
		).add_field(
			name='Type',
			value=manga.type.pyval
		).add_field(
			name="Description",
			value=synopsis
		))

	

def setup(bot):
	bot.add_cog(Mal(bot))