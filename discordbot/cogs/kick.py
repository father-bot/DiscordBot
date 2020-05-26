import discord
from discord.ext import commands
from discordbot.utils import Module

class Kick(Module):
	'''Kicks users from the server.'''

	@commands.command(usage='<member> <reason>')
	async def kick(self, ctx: commands.Context, member: discord.Member = None, *, reason: str = None) -> None:
		'''Kicks user from the server.'''
		if reason is not None and member is not None:
			await member.kick(reason=reason)

def setup(bot: commands.Bot) -> None:
	bot.add_cog(Kick(bot))
