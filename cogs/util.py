import discord
from discord.ext import commands

import random

class Util:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def about(self):
		await self.bot.say("This bot has been made by StandB out of boredom. You can check out the source on github https://github.com/StandB/Akane")

	@commands.command(pass_context=True)
	async def choose(self, ctx):
		options = ctx.message.content.split(" ")[1:]
		decision = random.choice(options)
		await self.bot.say(f"Decision: {decision}")



def setup(bot):
	bot.add_cog(Util(bot))