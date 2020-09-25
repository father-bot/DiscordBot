from discord.ext import commands
from discordbot import Module

class Clear(Module):
	'''Clears chat.'''

	@commands.command(usage='<number of messages>')
	async def clear(self, ctx, limit: int = 1) -> None:
		'''Deletes last N messages.'''
		await ctx.channel.purge(limit=limit)

def setup(bot: commands.Bot) -> None:
	bot.add_cog(Clear(bot))
