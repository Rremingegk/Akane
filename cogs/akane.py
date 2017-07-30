import discord
from discord.ext import commands
from functools import wraps
import urllib.request
import os

def is_creator(func):
	@wraps(func)
	async def wrapped(self, ctx, *args):
		if not int(ctx.message.author.id) == 98469757308633088:
			return await self.bot.say('You are not authorized to execute this command')
		return await func(self, ctx, *args)
	return wrapped

class Akane:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(pass_context=True)
	async def akane(self, ctx):
		""" Commands to retrieve and change Akane's info """
		if ctx.invoked_subcommand is None:
			await self.bot.say('That command does not exist in this group')

	@akane.command(pass_context=True)
	@is_creator
	async def servers(self, ctx):
		await self.bot.say(f'This bot is in {len(self.bot.servers)} servers')

	@akane.command(pass_context=True)
	@is_creator
	async def avatar(self, ctx, link: str):
		try:
			with urllib.request.urlopen(link) as response:
				img = response.read()
				await self.bot.edit_profile(avatar=img)
		except Exception as e:
			await self.bot.say(f"Failed to change avatar or edit_profile is on cooldown \n{e}")
		
	@akane.command(pass_context=True)
	@is_creator
	async def name(self, ctx, name: str):
		try:
			await self.bot.edit_profile(username=name)
		except Exception as e:
			await self.bot.say(f"Failed to change name or edit_profile is on cooldown \n{e}")

	@akane.command(pass_context=True)
	@is_creator
	async def status(self, ctx):
		status = " ".join(ctx.message.content.split(" ")[2:])
		print(status)
		try:
			await self.bot.change_presence(game=discord.Game(name=status))
		except Exception as e:
			await self.bot.say(f"Failed to change status or change_status is on cooldown \n{e}")

	@akane.command(pass_context=True)
	@is_creator
	async def exit(self, ctx):
		await self.bot.say("Logging out..")
		await self.bot.logout()

def setup(bot):
	bot.add_cog(Akane(bot))