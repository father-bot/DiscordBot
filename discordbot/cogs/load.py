import discord
from discord.ext import commands
from discordbot import Module

class Load(Module):
	'''Loads, unloads and reloads packages.'''

	@commands.command(usage='<package>')
	@commands.has_permissions(administrator = True)
	async def load(self, ctx: commands.Context, extension: str = None) -> None:
		'''Loads new package.'''
		if extension is not None and not extension == 'all':
			try:
				self.bot.load_extension("discordbot.cogs.{}".format(extension))
			except commands.ExtensionError as e:
				await ctx.send(str(e).replace('discordbot.cogs.', ''))
		else:
			self.bot.modules.load_modules()

	@commands.command(usage='<package>')
	@commands.has_permissions(administrator = True)
	async def reload(self, ctx, extension: str = None) -> None:
		'''Reloads package.'''
		if extension is not None and not extension == 'all':
			try:
				self.bot.unload_extension("discordbot.cogs.{}".format(extension))
				self.bot.load_extension("discordbot.cogs.{}".format(extension))
			except commands.ExtensionError as e:
				await ctx.send(str(e).replace('discordbot.cogs.', ''))
		else:
			self.bot.modules.reload_modules()

	@commands.command(usage='<package>')
	@commands.has_permissions(administrator = True)
	async def unload(self, ctx, extension: str = None):
		'''Remove package'''
		if extension is not None and not extension == 'all':
			try:
				self.bot.unload_extension("discordbot.cogs.{}".format(extension))
			except commands.ExtensionError as e:
				await ctx.send(str(e).replace('discordbot.cogs.', ''))
		else:
			self.bot.modules.unload_modules()

def setup(bot: commands.Bot) -> None:
	bot.add_cog(Load(bot))
