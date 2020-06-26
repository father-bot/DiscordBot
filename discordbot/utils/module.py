import os
import discord
from discord.ext import commands

class Module(commands.Cog):
	"""Simple module class"""
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

class Modules:
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot
		self.modules = [filename[:-3] for filename in os.listdir('./discordbot/cogs/') if filename.endswith('.py') and not '__init__' in filename]

	def _base(self, func) -> bool:
		for module in self.modules:
			try:
				func('discordbot.cogs.{}'.format(module))
			except commands.ExtensionAlreadyLoaded:
				pass
			except Exception as e:
				print(e)
				return False
		return True

	def load(self) -> bool:
		return self._base(self.bot.load_extension)

	def reload(self) -> bool:
		self._base(self.bot.unload_extension)
		return self._base(self.bot.load_extension)

	def unload(self) -> bool:
		return self._base(self.bot.unload_extension)
