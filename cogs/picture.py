import discord
from discord.ext import commands
from random import randint

from config import client_id, client_secret, reddit_password, user_agent, reddit_username
import praw

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, password=reddit_password, user_agent=user_agent, username=reddit_username)

class Picture:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def pic(self, ctx):
		""" Gets a random picture of the subreddit provided 
		
		**Example**:
		!pic awwnime
		
		"""
		sub = ctx.message.content.split(" ")[1]
		submissions = list(reddit.subreddit(sub).hot(limit=50))
		if not submissions:
			return await ctx.send('Subreddit not found')
		picture = submissions[randint(0, 50)].url
		await ctx.send(embed=discord.Embed(
		).set_image(
			url=picture
		).set_footer(
			text=sub,
			icon_url='https://camo.githubusercontent.com/b13830f5a9baecd3d83ef5cae4d5107d25cdbfbe/68747470733a2f2f662e636c6f75642e6769746875622e636f6d2f6173736574732f3732313033382f313732383830352f35336532613364382d363262352d313165332d383964312d3934376632373062646430332e706e67'
		))


def setup(bot):
	bot.add_cog(Picture(bot))