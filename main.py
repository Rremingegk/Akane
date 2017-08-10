import os, logging

import discord
from discord.ext import commands
from discord.ext.commands import Bot

import config

command_prefix = '~'
description = 'My own weeb bot'
cogs = ['cogs.osu', 'cogs.mal', 'cogs.reddit', 'cogs.radio', 'cogs.util', 'cogs.kitsu', 'cogs.akane']

#logging.basicConfig(level=logging.INFO, filename='discord.log')

disc_logger = logging.getLogger('discord')
disc_logger.setLevel(logging.DEBUG)
disc_handler = logging.FileHandler('discord.log', 'w', 'utf-8')
#disc_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
disc_logger.addHandler(disc_handler)

logger = logging.getLogger('commands')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('errors.log', 'w', 'utf-8')
logger.addHandler(handler)		

class Akane(Bot):

	def __init__(self, command_prefix, **options):
		super().__init__(command_prefix, **options)

	@staticmethod
	async def on_ready():
		print("Online!")

	async def on_command_error(self, exception, ctx):
		if isinstance(exception, commands.errors.CommandNotFound):
			logger = logging.getLogger('commands')
			logger.debug(f'{ctx.message.author} - {ctx.message.server.name} - {ctx.message.content} - {exception}')
			


if __name__ == '__main__':
	bot = Akane(command_prefix=command_prefix, description=description)

	for cog in cogs:
		bot.load_extension(cog)

	bot.run(config.bot_token)