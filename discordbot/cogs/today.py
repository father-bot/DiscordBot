import discord
from discord.ext import commands
from discordbot import Module
import datetime

class Today(Module):
	'''Shows today's date.'''

	@commands.command(usage='')
	async def today(self, ctx: commands.Context) -> None:
		'''Shows today's date.'''
		await ctx.send('Today is {}'.format(['Monday', 'Tuesaday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][datetime.datetime.today().weekday()]))

def setup(bot: commands.Bot) -> None:
	bot.add_cog(Today(bot))
