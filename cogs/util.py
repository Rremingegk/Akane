import discord
from discord.ext import commands

import random

class Util:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def choose(self, ctx):
		options = ctx.message.content.split(" ")[1:]
		decision = random.choice(options)
		await self.bot.say(f"Decision: {decision}")

def setup(bot):
	bot.add_cog(Util(bot))