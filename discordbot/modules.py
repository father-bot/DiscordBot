import discord
from discord.ext import commands
import os

class Module(commands.Cog):
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot

def modules_load(bot: commands.Bot) -> bool:
	for filename in os.listdir('./discordbot/cogs/'):
		if filename.endswith('.py') and not '__init__' in filename:
			try:
				bot.load_extension('discordbot.cogs.{}'.format(filename[:-3]))
			except:
				return False
	return True

def modules_remove(bot: commands.Bot) -> bool:
	for filename in os.listdir('./discordbot/cogs/'):
		if filename.endswith('.py') and not '__init__' in filename:
			try:
				bot.unload_extension('discordbot.cogs.{}'.format(filename[:-3]))
			except:
				return False
	return True
