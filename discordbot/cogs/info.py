import discord
from discord.ext import commands
from discordbot import Module

class Info(Module):
	'''Shows information about the user.'''

	@commands.command(usage='<member>')
	async def info(self, ctx: commands.Context, member: discord.Member = None) -> None:
		'''Prints how much time does user spent in voice chats.'''
		if member is not None:
			await ctx.send("@{}: {} seconds".format(member.display_name, self.bot.members[member.display_name].get_active_time()))

def setup(bot: commands.Bot) -> None:
	bot.add_cog(Info(bot))
