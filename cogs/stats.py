import discord
from discord.ext import commands
from functools import wraps

def is_creator(func):
	@wraps(func)
	async def wrapped(self, ctx):
		if not int(ctx.message.author.id) == 98469757308633088:
			return await self.bot.say('You are not authorized to execute this command')
		return await func(self, ctx)
	return wrapped

class Stats:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	@is_creator
	async def server(self, ctx):
		await self.bot.say(f'This bot is in {len(self.bot.servers)} servers')



def setup(bot):
	bot.add_cog(Stats(bot))