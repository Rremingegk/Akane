import discord
from discord.ext import commands
from random import randint

from config import client_id, client_secret, reddit_password, user_agent, reddit_username
import praw

reddit_icon = 'https://camo.githubusercontent.com/b13830f5a9baecd3d83ef5cae4d5107d25cdbfbe/68747470733a2f2f662e636c6f75642e6769746875622e636f6d2f6173736574732f3732313033382f313732383830352f35336532613364382d363262352d313165332d383964312d3934376632373062646430332e706e67'
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, password=reddit_password, user_agent=user_agent, username=reddit_username)

class Picture:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True)
	async def reddit(self, ctx):
		if ctx.invoked_subcommand is None:
			await self.bot.say('commands available to reddit: \n ~reddit pic &')

	@reddit.command(pass_context=True)
	async def pic(self, ctx, sub: str):
		""" Gets a random picture of the last 50 posts of the hot page from the subreddit provided 
		
		**Example**:
		~reddit pic awwnime
		
		"""
		# sub = ctx.message.content.split(" ")[1]
		try:
			submissions = list(reddit.subreddit(sub).hot(limit=50))
		except:
			return await self.bot.say('Subreddit not found')
		
		if len(submissions) == 0:
			return await self.bot.say('Not any images on this sub')
		
		rand = randint(0, 49) if len(submissions) >= 50 else randint(0, len(submissions))
		picture = submissions[rand].url
		while 'imgur.com/a/' in picture or 'reddit.com/r/' in picture:
			rand = randint(0, 49) if len(submissions) >= 50 else randint(0, len(submissions))
			picture = submissions[rand].url

		if 'jpg' not in picture and 'png' not in picture:
			picture += '.jpg'

		print(picture)
		await self.bot.say(embed=discord.Embed(
		).set_image(
			url=picture
		).set_footer(
			text=sub,
			icon_url=reddit_icon
		))


def setup(bot):
	bot.add_cog(Picture(bot))