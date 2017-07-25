import os

import discord
from discord.ext import commands

import config

command_prefix = '~'
description = 'My own weeb bot'
cogs = ['cogs.osu', 'cogs.mal']

class Akane(commands.AutoShardedBot):

	def __init__(self, command_prefix, **options):
		super().__init__(command_prefix, **options)

	@staticmethod
	async def on_ready():
		print("Online!")


if __name__ == '__main__':
	bot = Akane(command_prefix=command_prefix, description=description)

	for cog in cogs:
		bot.load_extension(cog)

	bot.run(config.bot_token)