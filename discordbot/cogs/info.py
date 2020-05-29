import discord
from discord.ext import commands
from discordbot.utils import Module

class Info(Module):
	'''Shows information about the user.'''

	@commands.command(usage='<member>')
	async def info(self, ctx: commands.Context, member: discord.Member = None) -> None:
		'''Prints how much time does user spent in voice chats.'''
		if member == None:
			member = ctx.author
		await ctx.send(str(self.bot.members[member.guild.name][member.display_name]))

def setup(bot: commands.Bot) -> None:
	bot.add_cog(Info(bot))
