import discord
from discord.ext import commands

class Osu:
	def __init__(self, bot):
		self.bot = bot


	@commands.command()
	async def hello(self, ctx):
		# await self.bot.send_message(ctx.message.channel, "Hello, World!")
		await ctx.send("Hello, world!")

def setup(bot):
	bot.add_cog(Osu(bot))