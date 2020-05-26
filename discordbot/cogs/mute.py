import discord
from discord.ext import commands
from discordbot.utils import Module

class Mute(Module):
	'''Mutes and unmutes user.'''

	@commands.command(usage='<member>')
	@commands.has_permissions(administrator = True)
	async def mute(self, ctx: commands.Context, member: discord.Member = None, reason: str = None) -> None:
		'''Mutes user.'''
		if reason is not None and member is not None:
			mute_role = discord.utils.get(ctx.message.guild.roles, name = 'mute')
			await member.add_roles(mute_role)
	
	@commands.command(usage='<member>')
	@commands.has_permissions(administrator = True)
	async def unmute(self, ctx: commands.Context, member: discord.Member = None, reason: str = None) -> None:
		'''Unmutes user.'''
		if reason is not None and member is not None:
			mute_role = discord.utils.get(ctx.message.guild.roles, name = 'mute')
			await member.remove_roles(mute_role)


def setup(bot: commands.Bot) -> None:
	bot.add_cog(Mute(bot))
